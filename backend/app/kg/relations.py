"""
Relationship extraction for knowledge graph
Extracts relationships between entities
"""
import re
from typing import List, Dict, Any, Tuple, Optional
from app.kg.ner import Entity
from app.rag.llm_client import llm_client
from app.core.logging import logger


class Relationship:
    """Represents a relationship between two entities"""
    def __init__(
        self,
        source: str,
        relation_type: str,
        target: str,
        confidence: float = 1.0,
        metadata: Dict[str, Any] = None
    ):
        self.source = source
        self.relation_type = relation_type
        self.target = target
        self.confidence = confidence
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'relation_type': self.relation_type,
            'target': self.target,
            'confidence': self.confidence,
            'metadata': self.metadata
        }


class RelationshipExtractor:
    """
    Extract relationships between entities
    
    Relationship types:
    - HAS_FAILURE: Equipment → FailureMode
    - DOCUMENTED_IN: Entity → Document
    - GOVERNED_BY: Equipment/Procedure → Regulation
    - INVOLVES: Incident → Equipment
    - CAUSED_BY: FailureMode → Parameter
    - SATISFIES: Procedure → Regulation
    - MEASURED_BY: Equipment → Parameter
    - OPERATES_AT: Equipment → Measurement
    """
    
    def __init__(self):
        self.llm_client = llm_client
    
    def extract_has_failure(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Extract HAS_FAILURE relationships
        
        Pattern: Equipment + failure mode
        Example: "P-101 seal leak", "Tank 205 corrosion"
        """
        relationships = []
        
        equipment_entities = [e for e in entities if e.entity_type == 'EQUIPMENT']
        failure_entities = [e for e in entities if e.entity_type == 'FAILURE_MODE']
        
        for equip in equipment_entities:
            for failure in failure_entities:
                # Check if failure is near equipment (within 50 chars)
                distance = abs(equip.start - failure.start)
                if distance < 50:
                    # Check if there's connecting text
                    start = min(equip.start, failure.start)
                    end = max(equip.end, failure.end)
                    snippet = text[start:end]
                    
                    # Look for connecting words
                    connectors = ['has', 'experienced', 'suffered', 'with', 'due to']
                    if any(conn in snippet.lower() for conn in connectors) or distance < 20:
                        relationships.append(Relationship(
                            source=equip.text,
                            relation_type='HAS_FAILURE',
                            target=failure.text,
                            confidence=0.80,
                            metadata={'distance': distance}
                        ))
        
        return relationships
    
    def extract_governed_by(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Extract GOVERNED_BY relationships
        
        Pattern: Equipment/Procedure + regulation
        Example: "complies with OISD-STD-105", "per Factory Act"
        """
        relationships = []
        
        equipment_entities = [e for e in entities if e.entity_type == 'EQUIPMENT']
        regulation_entities = [e for e in entities if e.entity_type == 'REGULATION']
        
        for equip in equipment_entities:
            for reg in regulation_entities:
                distance = abs(equip.start - reg.start)
                if distance < 100:
                    start = min(equip.start, reg.start)
                    end = max(equip.end, reg.end)
                    snippet = text[start:end].lower()
                    
                    # Look for regulatory language
                    connectors = [
                        'complies with', 'per', 'according to', 'as per',
                        'governed by', 'regulated by', 'in accordance with'
                    ]
                    if any(conn in snippet for conn in connectors):
                        relationships.append(Relationship(
                            source=equip.text,
                            relation_type='GOVERNED_BY',
                            target=reg.text,
                            confidence=0.85,
                            metadata={'snippet': snippet[:50]}
                        ))
        
        return relationships
    
    def extract_measured_by(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Extract MEASURED_BY relationships
        
        Pattern: Equipment + parameter
        Example: "P-101 temperature", "flow rate of Pump 205"
        """
        relationships = []
        
        equipment_entities = [e for e in entities if e.entity_type == 'EQUIPMENT']
        parameter_entities = [e for e in entities if e.entity_type == 'PARAMETER']
        
        for equip in equipment_entities:
            for param in parameter_entities:
                distance = abs(equip.start - param.start)
                if distance < 30:
                    relationships.append(Relationship(
                        source=equip.text,
                        relation_type='MEASURED_BY',
                        target=param.text,
                        confidence=0.75,
                        metadata={'distance': distance}
                    ))
        
        return relationships
    
    def extract_operates_at(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Extract OPERATES_AT relationships
        
        Pattern: Equipment + measurement
        Example: "P-101 at 45 Nm", "operating at 100°C"
        """
        relationships = []
        
        equipment_entities = [e for e in entities if e.entity_type == 'EQUIPMENT']
        measurement_entities = [e for e in entities if e.entity_type == 'MEASUREMENT']
        
        for equip in equipment_entities:
            for measurement in measurement_entities:
                distance = abs(equip.start - measurement.start)
                if distance < 40:
                    start = min(equip.start, measurement.start)
                    end = max(equip.end, measurement.end)
                    snippet = text[start:end].lower()
                    
                    connectors = ['at', 'of', 'with', 'operating']
                    if any(conn in snippet for conn in connectors) or distance < 15:
                        relationships.append(Relationship(
                            source=equip.text,
                            relation_type='OPERATES_AT',
                            target=measurement.text,
                            confidence=0.80,
                            metadata={'measurement_value': measurement.metadata.get('value')}
                        ))
        
        return relationships
    
    def extract_caused_by(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Extract CAUSED_BY relationships
        
        Pattern: Failure mode + parameter/condition
        Example: "seal leak caused by high temperature"
        """
        relationships = []
        
        failure_entities = [e for e in entities if e.entity_type == 'FAILURE_MODE']
        parameter_entities = [e for e in entities if e.entity_type == 'PARAMETER']
        measurement_entities = [e for e in entities if e.entity_type == 'MEASUREMENT']
        
        for failure in failure_entities:
            for param in parameter_entities + measurement_entities:
                distance = abs(failure.start - param.start)
                if distance < 60:
                    start = min(failure.start, param.start)
                    end = max(failure.end, param.end)
                    snippet = text[start:end].lower()
                    
                    # Look for causal language
                    connectors = [
                        'caused by', 'due to', 'because of', 'resulted from',
                        'attributed to', 'from', 'by'
                    ]
                    if any(conn in snippet for conn in connectors):
                        relationships.append(Relationship(
                            source=failure.text,
                            relation_type='CAUSED_BY',
                            target=param.text,
                            confidence=0.75,
                            metadata={'snippet': snippet[:50]}
                        ))
        
        return relationships
    
    def extract_with_llm(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """
        Use LLM to extract complex relationships
        
        More accurate but slower - use for important relationships only
        """
        if len(entities) < 2:
            return []
        
        logger.info("Using LLM for relationship extraction")
        
        # Build entity list
        entity_list = "\n".join([
            f"- {e.text} ({e.entity_type})"
            for e in entities[:20]  # Limit to first 20
        ])
        
        system_prompt = """You are a relationship extraction expert.
Extract relationships between entities in technical documents.
Focus on: equipment failures, regulations, measurements, and causes."""
        
        prompt = f"""Text: {text[:1000]}

Entities:
{entity_list}

Extract relationships in format:
[Entity1] -[RELATIONSHIP]-> [Entity2]

Relationship types:
- HAS_FAILURE: equipment has failure mode
- GOVERNED_BY: equipment/procedure governed by regulation
- CAUSED_BY: failure caused by condition
- MEASURED_BY: equipment measured by parameter

List relationships (one per line):"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=300
            )
            
            # Parse response
            relationships = []
            for line in response.strip().split('\n'):
                line = line.strip()
                # Parse format: [Source] -[REL]-> [Target]
                match = re.match(r'\[(.+?)\]\s*-\[(.+?)\]->\s*\[(.+?)\]', line)
                if match:
                    source, rel_type, target = match.groups()
                    relationships.append(Relationship(
                        source=source.strip(),
                        relation_type=rel_type.strip(),
                        target=target.strip(),
                        confidence=0.70,
                        metadata={'source': 'llm'}
                    ))
            
            logger.info(f"Extracted {len(relationships)} relationships with LLM")
            return relationships
            
        except Exception as e:
            logger.error(f"Error in LLM relationship extraction: {e}")
            return []
    
    def extract_all(
        self,
        text: str,
        entities: List[Entity],
        use_llm: bool = False
    ) -> List[Relationship]:
        """
        Extract all relationships from text
        
        Args:
            text: Document text
            entities: Extracted entities
            use_llm: Whether to use LLM for complex relationships
        
        Returns:
            List of Relationship objects
        """
        logger.info(f"Extracting relationships from {len(entities)} entities")
        
        all_relationships = []
        
        # Pattern-based extraction
        all_relationships.extend(self.extract_has_failure(text, entities))
        all_relationships.extend(self.extract_governed_by(text, entities))
        all_relationships.extend(self.extract_measured_by(text, entities))
        all_relationships.extend(self.extract_operates_at(text, entities))
        all_relationships.extend(self.extract_caused_by(text, entities))
        
        # LLM-based extraction (optional, slower)
        if use_llm:
            all_relationships.extend(self.extract_with_llm(text, entities))
        
        # Remove duplicates
        unique_relationships = self._remove_duplicates(all_relationships)
        
        logger.info(f"Extracted {len(unique_relationships)} unique relationships")
        return unique_relationships
    
    def _remove_duplicates(
        self,
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """Remove duplicate relationships, keeping highest confidence"""
        if not relationships:
            return []
        
        # Group by (source, relation_type, target)
        seen = {}
        for rel in relationships:
            key = (
                rel.source.lower(),
                rel.relation_type,
                rel.target.lower()
            )
            if key not in seen or rel.confidence > seen[key].confidence:
                seen[key] = rel
        
        return list(seen.values())
    
    def extract_with_context(
        self,
        text: str,
        entities: List[Entity],
        document_id: str,
        chunk_id: str = None,
        use_llm: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Extract relationships with document context for knowledge graph
        
        Returns list of relationship dicts ready for graph ingestion
        """
        relationships = self.extract_all(text, entities, use_llm=use_llm)
        
        result = []
        for i, rel in enumerate(relationships):
            result.append({
                'relationship_id': f"{document_id}_rel_{i}",
                'source': rel.source,
                'relation_type': rel.relation_type,
                'target': rel.target,
                'confidence': rel.confidence,
                'metadata': rel.metadata,
                'provenance': {
                    'document_id': document_id,
                    'chunk_id': chunk_id
                }
            })
        
        return result


# Global relationship extractor
relationship_extractor = RelationshipExtractor()
