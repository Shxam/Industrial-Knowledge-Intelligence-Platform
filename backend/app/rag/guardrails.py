"""
Guardrails for RAG responses
Includes groundedness checking, hallucination detection, confidence gating
"""
from typing import Dict, Any, List
from app.rag.llm_client import llm_client
from app.core.config import settings
from app.core.logging import logger


class RAGGuardrails:
    """
    Safety and quality checks for RAG responses
    
    Features:
    - Groundedness checking (answer supported by context)
    - Hallucination detection
    - Confidence scoring
    - Response quality assessment
    """
    
    def __init__(self):
        self.llm_client = llm_client
        self.hallucination_threshold = settings.HALLUCINATION_THRESHOLD
        self.groundedness_threshold = settings.GROUNDEDNESS_THRESHOLD
    
    def check_groundedness(
        self,
        answer: str,
        context: str
    ) -> Dict[str, Any]:
        """
        Check if answer is grounded in the provided context
        
        Returns dict with score and explanation
        """
        logger.info("Checking answer groundedness")
        
        system_prompt = """You are a fact-checking assistant.
Determine if the given answer is fully supported by the provided context.
Be strict: the answer should only contain information from the context."""
        
        prompt = f"""Context:
{context[:4000]}

Answer:
{answer}

Is this answer fully supported by the context above?
Respond with:
1. Score: 0.0 to 1.0 (0 = not grounded, 1 = fully grounded)
2. Explanation: Brief reasoning

Format:
Score: [0.0-1.0]
Explanation: [your explanation]"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=200
            )
            
            # Parse response
            score = 0.5  # Default
            explanation = "Could not parse response"
            
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('Score:'):
                    try:
                        score_str = line.split(':', 1)[1].strip()
                        score = float(score_str)
                    except:
                        pass
                elif line.startswith('Explanation:'):
                    explanation = line.split(':', 1)[1].strip()
            
            is_grounded = score >= self.groundedness_threshold
            
            logger.info(f"Groundedness check: {score:.2f} ({'PASS' if is_grounded else 'FAIL'})")
            
            return {
                'is_grounded': is_grounded,
                'score': score,
                'explanation': explanation,
                'threshold': self.groundedness_threshold
            }
            
        except Exception as e:
            logger.error(f"Error checking groundedness: {e}")
            return {
                'is_grounded': True,  # Fail-open for availability
                'score': 0.5,
                'explanation': f"Error: {str(e)}",
                'threshold': self.groundedness_threshold
            }
    
    def detect_hallucination(
        self,
        answer: str,
        context: str,
        query: str
    ) -> Dict[str, Any]:
        """
        Detect potential hallucinations in the answer
        
        Returns dict with hallucination indicators
        """
        logger.info("Detecting hallucinations")
        
        system_prompt = """You are a hallucination detection expert.
Identify any information in the answer that is NOT found in the context.
Look for:
- Made-up facts or numbers
- Unsupported claims
- Information not in the context"""
        
        prompt = f"""Query: {query}

Context:
{context[:4000]}

Answer:
{answer}

Are there any hallucinations (information not in the context)?
Respond with:
1. Has hallucination: yes or no
2. Confidence: 0.0 to 1.0 (how confident you are)
3. Details: What might be hallucinated (if any)

Format:
Has hallucination: [yes/no]
Confidence: [0.0-1.0]
Details: [details]"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=250
            )
            
            # Parse response
            has_hallucination = False
            confidence = 0.5
            details = ""
            
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('Has hallucination:'):
                    has_str = line.split(':', 1)[1].strip().lower()
                    has_hallucination = has_str == 'yes'
                elif line.startswith('Confidence:'):
                    try:
                        conf_str = line.split(':', 1)[1].strip()
                        confidence = float(conf_str)
                    except:
                        pass
                elif line.startswith('Details:'):
                    details = line.split(':', 1)[1].strip()
            
            is_safe = not (has_hallucination and confidence >= self.hallucination_threshold)
            
            logger.info(
                f"Hallucination check: "
                f"{'DETECTED' if has_hallucination else 'NONE'} "
                f"(confidence: {confidence:.2f})"
            )
            
            return {
                'has_hallucination': has_hallucination,
                'is_safe': is_safe,
                'confidence': confidence,
                'details': details,
                'threshold': self.hallucination_threshold
            }
            
        except Exception as e:
            logger.error(f"Error detecting hallucination: {e}")
            return {
                'has_hallucination': False,
                'is_safe': True,
                'confidence': 0.0,
                'details': f"Error: {str(e)}",
                'threshold': self.hallucination_threshold
            }
    
    def assess_answer_quality(
        self,
        answer: str,
        query: str
    ) -> Dict[str, Any]:
        """
        Assess overall answer quality
        
        Checks:
        - Completeness
        - Relevance
        - Clarity
        """
        logger.info("Assessing answer quality")
        
        # Simple heuristics
        quality_score = 1.0
        issues = []
        
        # Check length
        if len(answer) < 20:
            quality_score -= 0.3
            issues.append("Answer too short")
        elif len(answer) > 2000:
            quality_score -= 0.1
            issues.append("Answer very long")
        
        # Check for uncertainty phrases
        uncertainty_phrases = [
            "i don't know",
            "i'm not sure",
            "unclear",
            "insufficient information",
            "cannot determine"
        ]
        answer_lower = answer.lower()
        for phrase in uncertainty_phrases:
            if phrase in answer_lower:
                quality_score -= 0.2
                issues.append(f"Contains uncertainty: '{phrase}'")
                break
        
        # Check if answer addresses query keywords
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())
        keyword_overlap = len(query_words & answer_words) / len(query_words) if query_words else 0
        
        if keyword_overlap < 0.3:
            quality_score -= 0.2
            issues.append("Low keyword overlap with query")
        
        # Clamp score
        quality_score = max(0.0, min(1.0, quality_score))
        
        return {
            'quality_score': quality_score,
            'is_high_quality': quality_score >= 0.7,
            'issues': issues
        }
    
    def gate_response(
        self,
        answer: str,
        context: str,
        query: str,
        citations: List[Dict[str, Any]],
        enable_checks: bool = True
    ) -> Dict[str, Any]:
        """
        Main guardrail function - check all safety measures
        
        Returns dict with:
        - should_return: Whether response passes all checks
        - answer: Original or filtered answer
        - warnings: List of issues found
        - checks: Detailed check results
        """
        if not enable_checks or not settings.ENABLE_GUARDRAILS:
            return {
                'should_return': True,
                'answer': answer,
                'warnings': [],
                'checks': {}
            }
        
        logger.info("Running guardrails on response")
        
        warnings = []
        checks = {}
        
        # Check groundedness
        groundedness = self.check_groundedness(answer, context)
        checks['groundedness'] = groundedness
        if not groundedness['is_grounded']:
            warnings.append(f"Low groundedness: {groundedness['score']:.2f}")
        
        # Check for hallucinations
        hallucination = self.detect_hallucination(answer, context, query)
        checks['hallucination'] = hallucination
        if hallucination['has_hallucination'] and not hallucination['is_safe']:
            warnings.append(f"Potential hallucination detected")
        
        # Assess quality
        quality = self.assess_answer_quality(answer, query)
        checks['quality'] = quality
        if not quality['is_high_quality']:
            warnings.append(f"Quality issues: {', '.join(quality['issues'])}")
        
        # Check if we have citations
        if not citations:
            warnings.append("No citations provided")
        
        # Decide if response should be returned
        critical_issues = [
            not groundedness['is_grounded'],
            hallucination['has_hallucination'] and not hallucination['is_safe'],
            quality['quality_score'] < 0.3
        ]
        
        should_return = not any(critical_issues)
        
        # If blocked, provide explanation
        if not should_return:
            filtered_answer = (
                "I cannot provide a confident answer to this question based on the available information. "
                "Please try rephrasing your question or provide more context."
            )
        else:
            filtered_answer = answer
        
        logger.info(
            f"Guardrails result: {'PASS' if should_return else 'BLOCKED'} "
            f"({len(warnings)} warnings)"
        )
        
        return {
            'should_return': should_return,
            'answer': filtered_answer,
            'warnings': warnings,
            'checks': checks
        }
    
    def add_confidence_disclaimer(
        self,
        answer: str,
        confidence: float
    ) -> str:
        """
        Add confidence disclaimer to low-confidence answers
        """
        if confidence < 0.6:
            disclaimer = "\n\n⚠️ Note: This answer has lower confidence. Please verify the information."
            return answer + disclaimer
        return answer


# Global guardrails instance
guardrails = RAGGuardrails()
