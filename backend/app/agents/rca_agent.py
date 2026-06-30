"""
Root Cause Analysis (RCA) Agent

Performs intelligent failure analysis using:
- Knowledge graph (failure chains, relationships)
- RAG (documentation retrieval)
- LLM reasoning (5-Why, fishbone analysis)
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from app.kg.neo4j_client import neo4j_client
from app.kg.ner import ner
from app.rag.pipeline import rag_pipeline
from app.rag.llm_client import llm_client
from app.core.logging import logger


class RCAAgent:
    """
    Root Cause Analysis Agent
    
    Workflow:
    1. Parse failure description
    2. Extract equipment/failure entities
    3. Collect evidence from graph and documents
    4. Perform 5-Why analysis
    5. Generate fishbone diagram data
    6. Provide recommendations
    """
    
    def __init__(self):
        """Initialize RCA agent"""
        self.neo4j_client = neo4j_client
        self.ner = ner
        self.rag_pipeline = rag_pipeline
        self.llm_client = llm_client
        logger.info("RCA Agent initialized")
    
    def analyze(
        self,
        failure_description: str,
        equipment_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform root cause analysis
        
        Args:
            failure_description: Description of the failure
            equipment_id: Optional equipment ID (if known)
            context: Optional additional context
        
        Returns:
            RCA report with causes, evidence, recommendations
        """
        logger.info(f"Starting RCA for: {failure_description[:100]}...")
        
        start_time = datetime.now()
        
        # Step 1: Extract entities from failure description
        entities = self._extract_entities(failure_description)
        logger.info(f"Extracted {len(entities)} entities")
        
        # Step 2: Collect evidence from knowledge graph
        graph_evidence = self._collect_graph_evidence(entities, equipment_id)
        logger.info(f"Collected {len(graph_evidence.get('entities', []))} graph entities")
        
        # Step 3: Retrieve relevant documents
        doc_evidence = self._retrieve_documentation(failure_description, entities)
        logger.info(f"Retrieved {len(doc_evidence.get('chunks', []))} document chunks")
        
        # Step 4: Perform 5-Why analysis
        five_why = self._perform_five_why(
            failure_description,
            graph_evidence,
            doc_evidence
        )
        logger.info(f"Completed 5-Why analysis with {len(five_why)} levels")
        
        # Step 5: Generate fishbone categories
        fishbone = self._generate_fishbone(
            failure_description,
            graph_evidence,
            doc_evidence
        )
        logger.info("Generated fishbone diagram data")
        
        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(
            failure_description,
            five_why,
            fishbone,
            doc_evidence
        )
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        # Step 7: Calculate confidence
        confidence = self._calculate_confidence(
            graph_evidence,
            doc_evidence,
            five_why
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Build report
        report = {
            'failure_description': failure_description,
            'equipment_id': equipment_id,
            'entities': [
                {
                    'text': e.text,
                    'type': e.entity_type,
                    'confidence': e.confidence
                }
                for e in entities
            ],
            'five_why_analysis': five_why,
            'fishbone_diagram': fishbone,
            'recommendations': recommendations,
            'evidence': {
                'graph_entities': len(graph_evidence.get('entities', [])),
                'graph_relationships': len(graph_evidence.get('relationships', [])),
                'document_chunks': len(doc_evidence.get('chunks', [])),
                'citations': doc_evidence.get('citations', [])
            },
            'confidence': confidence,
            'processing_time_seconds': processing_time,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"RCA completed in {processing_time:.2f}s (confidence: {confidence:.2f})")
        
        return report
    
    def _extract_entities(self, text: str) -> List[Any]:
        """Extract entities from failure description"""
        try:
            entities = self.ner.extract_all(text)
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []
    
    def _collect_graph_evidence(
        self,
        entities: List[Any],
        equipment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect evidence from knowledge graph
        
        Finds:
        - Equipment entities
        - Related failures
        - Operating conditions
        - Regulatory requirements
        - Historical patterns
        """
        evidence = {
            'entities': [],
            'relationships': [],
            'paths': []
        }
        
        try:
            # If equipment_id provided, start there
            if equipment_id:
                entity = self.neo4j_client.get_entity(equipment_id)
                if entity:
                    evidence['entities'].append(entity)
                    
                    # Get all relationships
                    relationships = self.neo4j_client.get_related_entities(
                        equipment_id,
                        direction='both'
                    )
                    evidence['relationships'].extend(relationships)
            
            # Search for entities mentioned in description
            for entity in entities:
                if entity.entity_type == 'EQUIPMENT':
                    # Find in graph
                    found = self.neo4j_client.find_entities(
                        entity_type='EQUIPMENT',
                        text_pattern=entity.text,
                        limit=1
                    )
                    
                    if found:
                        equipment = found[0]
                        evidence['entities'].append(equipment)
                        
                        # Get failure relationships
                        failures = self.neo4j_client.get_related_entities(
                            equipment['id'],
                            relation_type='HAS_FAILURE'
                        )
                        evidence['relationships'].extend(failures)
                        
                        # Get CAUSED_BY chains for each failure
                        for failure_rel in failures:
                            failure_entity = failure_rel['target']
                            causes = self.neo4j_client.get_related_entities(
                                failure_entity['id'],
                                relation_type='CAUSED_BY'
                            )
                            evidence['relationships'].extend(causes)
                
                elif entity.entity_type == 'FAILURE_MODE':
                    # Find failure mode in graph
                    found = self.neo4j_client.find_entities(
                        entity_type='FAILURE_MODE',
                        text_pattern=entity.text,
                        limit=5
                    )
                    
                    for failure in found:
                        evidence['entities'].append(failure)
                        
                        # Get causes
                        causes = self.neo4j_client.get_related_entities(
                            failure['id'],
                            relation_type='CAUSED_BY'
                        )
                        evidence['relationships'].extend(causes)
            
            # Remove duplicates
            seen_ids = set()
            unique_entities = []
            for entity in evidence['entities']:
                if entity['id'] not in seen_ids:
                    seen_ids.add(entity['id'])
                    unique_entities.append(entity)
            evidence['entities'] = unique_entities
            
        except Exception as e:
            logger.error(f"Error collecting graph evidence: {e}")
        
        return evidence
    
    def _retrieve_documentation(
        self,
        failure_description: str,
        entities: List[Any]
    ) -> Dict[str, Any]:
        """Retrieve relevant documentation using RAG"""
        try:
            # Query for failure description
            result = self.rag_pipeline.query(
                question=f"What documentation exists about: {failure_description}",
                top_k=10,
                strategy="hybrid",
                use_kg_expansion=True
            )
            
            return {
                'chunks': result.get('num_sources', 0),
                'citations': result.get('citations', []),
                'answer': result.get('answer', '')
            }
            
        except Exception as e:
            logger.error(f"Error retrieving documentation: {e}")
            return {'chunks': 0, 'citations': [], 'answer': ''}
    
    def _perform_five_why(
        self,
        failure_description: str,
        graph_evidence: Dict[str, Any],
        doc_evidence: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Perform 5-Why analysis
        
        Iteratively asks "why" to find root cause
        """
        try:
            # Build context from evidence
            context = self._build_evidence_context(graph_evidence, doc_evidence)
            
            system_prompt = """You are an expert in industrial failure analysis.
Perform a 5-Why analysis to find the root cause of failures.
For each "why" level, provide:
1. The question asked
2. The answer based on evidence
3. Supporting evidence/citations

Be specific and cite sources. Stop when you reach a root cause."""
            
            prompt = f"""Failure Description: {failure_description}

Available Evidence:
{context}

Perform a 5-Why root cause analysis. For each level:
- Ask "Why did [previous answer] happen?"
- Answer based on evidence
- Cite sources

Format as JSON array:
[
  {{
    "level": 1,
    "question": "Why did [failure] occur?",
    "answer": "Because...",
    "evidence": ["source 1", "source 2"],
    "is_root_cause": false
  }},
  ...
]

Provide the analysis:"""
            
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=1500
            )
            
            # Parse JSON response
            try:
                # Extract JSON from response (handle markdown code blocks)
                json_str = response
                if '```json' in response:
                    json_str = response.split('```json')[1].split('```')[0]
                elif '```' in response:
                    json_str = response.split('```')[1].split('```')[0]
                
                five_why = json.loads(json_str.strip())
                
                # Validate structure
                if not isinstance(five_why, list):
                    raise ValueError("Response is not a list")
                
                return five_why[:5]  # Limit to 5 levels
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse 5-Why JSON: {e}")
                # Fallback: create structured response from text
                return self._parse_five_why_from_text(response)
        
        except Exception as e:
            logger.error(f"Error in 5-Why analysis: {e}")
            return []
    
    def _generate_fishbone(
        self,
        failure_description: str,
        graph_evidence: Dict[str, Any],
        doc_evidence: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate fishbone (Ishikawa) diagram data
        
        Categories:
        - People (personnel, training, experience)
        - Process (procedures, steps, workflow)
        - Equipment (machinery, tools, condition)
        - Materials (quality, specifications, supply)
        - Environment (conditions, temperature, pressure)
        - Management (supervision, resources, planning)
        """
        try:
            context = self._build_evidence_context(graph_evidence, doc_evidence)
            
            system_prompt = """You are an expert in industrial failure analysis.
Generate fishbone diagram data categorizing contributing factors.

Categories: People, Process, Equipment, Materials, Environment, Management"""
            
            prompt = f"""Failure: {failure_description}

Evidence:
{context}

Generate fishbone diagram data as JSON:
{{
  "People": [
    {{"factor": "...", "evidence": "...", "impact": "high/medium/low"}}
  ],
  "Process": [...],
  "Equipment": [...],
  "Materials": [...],
  "Environment": [...],
  "Management": [...]
}}

Only include categories with evidence. Provide the fishbone data:"""
            
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=1500
            )
            
            # Parse JSON
            try:
                json_str = response
                if '```json' in response:
                    json_str = response.split('```json')[1].split('```')[0]
                elif '```' in response:
                    json_str = response.split('```')[1].split('```')[0]
                
                fishbone = json.loads(json_str.strip())
                return fishbone
                
            except json.JSONDecodeError:
                logger.error("Failed to parse fishbone JSON")
                return self._default_fishbone(graph_evidence)
        
        except Exception as e:
            logger.error(f"Error generating fishbone: {e}")
            return {}
    
    def _generate_recommendations(
        self,
        failure_description: str,
        five_why: List[Dict[str, Any]],
        fishbone: Dict[str, List[Dict[str, Any]]],
        doc_evidence: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        try:
            # Build summary of analysis
            analysis_summary = f"""
Failure: {failure_description}

Root Causes Identified:
{self._summarize_five_why(five_why)}

Contributing Factors:
{self._summarize_fishbone(fishbone)}
"""
            
            system_prompt = """You are an expert in industrial safety and maintenance.
Provide actionable recommendations to prevent failure recurrence.

For each recommendation:
- Be specific and actionable
- Assign priority (Critical/High/Medium/Low)
- Estimate timeframe (Immediate/Short-term/Long-term)
- Identify responsible party
- Reference evidence"""
            
            prompt = f"""{analysis_summary}

Generate 5-7 specific recommendations as JSON:
[
  {{
    "title": "Short title",
    "description": "Detailed description",
    "priority": "Critical/High/Medium/Low",
    "timeframe": "Immediate/Short-term/Long-term",
    "responsible": "Role/Department",
    "rationale": "Why this helps",
    "evidence": "Supporting evidence"
  }}
]

Provide recommendations:"""
            
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.4,
                max_tokens=1500
            )
            
            # Parse JSON
            try:
                json_str = response
                if '```json' in response:
                    json_str = response.split('```json')[1].split('```')[0]
                elif '```' in response:
                    json_str = response.split('```')[1].split('```')[0]
                
                recommendations = json.loads(json_str.strip())
                return recommendations[:7]  # Limit to 7
                
            except json.JSONDecodeError:
                logger.error("Failed to parse recommendations JSON")
                return self._default_recommendations(five_why, fishbone)
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    def _build_evidence_context(
        self,
        graph_evidence: Dict[str, Any],
        doc_evidence: Dict[str, Any],
        max_length: int = 2000
    ) -> str:
        """Build context string from evidence"""
        context_parts = []
        
        # Graph evidence
        if graph_evidence.get('entities'):
            context_parts.append("Knowledge Graph Entities:")
            for entity in graph_evidence['entities'][:10]:
                context_parts.append(f"- {entity.get('text', '')} ({entity.get('type', '')})")
        
        if graph_evidence.get('relationships'):
            context_parts.append("\nRelationships:")
            for rel in graph_evidence['relationships'][:10]:
                target = rel.get('target', {})
                context_parts.append(
                    f"- {rel.get('relation_type', '')} → {target.get('text', '')}"
                )
        
        # Document evidence
        if doc_evidence.get('citations'):
            context_parts.append("\nDocument Evidence:")
            for citation in doc_evidence['citations'][:5]:
                text = citation.get('text', '')[:200]
                context_parts.append(f"- {text}")
        
        context = "\n".join(context_parts)
        
        # Truncate if too long
        if len(context) > max_length:
            context = context[:max_length] + "..."
        
        return context
    
    def _calculate_confidence(
        self,
        graph_evidence: Dict[str, Any],
        doc_evidence: Dict[str, Any],
        five_why: List[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score for RCA"""
        confidence = 0.5  # Base confidence
        
        # Boost for graph evidence
        if len(graph_evidence.get('entities', [])) > 0:
            confidence += 0.1
        if len(graph_evidence.get('relationships', [])) > 0:
            confidence += 0.1
        
        # Boost for document evidence
        if len(doc_evidence.get('citations', [])) > 0:
            confidence += 0.1
        if len(doc_evidence.get('citations', [])) >= 3:
            confidence += 0.1
        
        # Boost for complete 5-Why
        if len(five_why) >= 3:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _parse_five_why_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Fallback parser for 5-Why from text"""
        # Simple fallback
        return [
            {
                'level': 1,
                'question': 'Why did the failure occur?',
                'answer': text[:200],
                'evidence': [],
                'is_root_cause': False
            }
        ]
    
    def _default_fishbone(self, graph_evidence: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Default fishbone from graph evidence"""
        fishbone = {}
        
        # Extract equipment factors
        equipment_entities = [
            e for e in graph_evidence.get('entities', [])
            if e.get('type') == 'EQUIPMENT'
        ]
        if equipment_entities:
            fishbone['Equipment'] = [
                {
                    'factor': e.get('text', ''),
                    'evidence': 'From knowledge graph',
                    'impact': 'medium'
                }
                for e in equipment_entities[:3]
            ]
        
        return fishbone
    
    def _default_recommendations(
        self,
        five_why: List[Dict[str, Any]],
        fishbone: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Default recommendations"""
        return [
            {
                'title': 'Conduct detailed inspection',
                'description': 'Perform thorough inspection of affected equipment',
                'priority': 'High',
                'timeframe': 'Immediate',
                'responsible': 'Maintenance Team',
                'rationale': 'Verify current equipment condition',
                'evidence': 'Standard practice'
            }
        ]
    
    def _summarize_five_why(self, five_why: List[Dict[str, Any]]) -> str:
        """Summarize 5-Why analysis"""
        if not five_why:
            return "No analysis available"
        
        lines = []
        for item in five_why:
            level = item.get('level', 0)
            answer = item.get('answer', '')
            lines.append(f"Level {level}: {answer}")
        
        return "\n".join(lines)
    
    def _summarize_fishbone(self, fishbone: Dict[str, List[Dict[str, Any]]]) -> str:
        """Summarize fishbone diagram"""
        if not fishbone:
            return "No factors identified"
        
        lines = []
        for category, factors in fishbone.items():
            if factors:
                lines.append(f"{category}: {len(factors)} factors")
        
        return "\n".join(lines)


# Global RCA agent instance
rca_agent = RCAAgent()
