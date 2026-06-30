"""
Query enhancement techniques for improved retrieval
Includes: Query rewriting, HyDE, Multi-query generation
"""
from typing import List, Dict, Any, Optional
from app.rag.llm_client import llm_client
from app.core.logging import logger


class QueryEnhancer:
    """
    Enhance queries for better retrieval
    
    Techniques:
    - Query rewriting (expansion, rephrasing)
    - HyDE (Hypothetical Document Embeddings)
    - Multi-query generation
    - Query decomposition
    """
    
    def __init__(self):
        self.llm_client = llm_client
    
    def rewrite_query(self, query: str, num_variations: int = 3) -> List[str]:
        """
        Generate query variations for better coverage
        
        Returns list of rewritten queries including original
        """
        logger.info(f"Rewriting query: '{query}'")
        
        system_prompt = """You are a query optimization assistant. 
Generate alternative phrasings of the user's query to improve search results.
Focus on:
- Different word choices (synonyms)
- Different perspectives
- More specific or general versions
- Technical vs layman terms"""
        
        prompt = f"""Original query: "{query}"

Generate {num_variations} alternative ways to ask this question.
Each should capture the same intent but use different words.

Format: One query per line, numbered.
1. [first alternative]
2. [second alternative]
3. [third alternative]"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            # Parse response
            variations = [query]  # Include original
            for line in response.strip().split('\n'):
                line = line.strip()
                if line and any(line.startswith(str(i)) for i in range(1, 10)):
                    # Remove number prefix
                    cleaned = line.split('.', 1)[1].strip() if '.' in line else line
                    # Remove quotes if present
                    cleaned = cleaned.strip('"\'')
                    if cleaned:
                        variations.append(cleaned)
            
            logger.info(f"Generated {len(variations)} query variations")
            return variations[:num_variations + 1]  # Include original + variations
            
        except Exception as e:
            logger.error(f"Error rewriting query: {e}")
            return [query]  # Fallback to original
    
    def generate_hyde(self, query: str) -> str:
        """
        HyDE: Generate a hypothetical document that would answer the query
        
        This document is then embedded and used for retrieval.
        Often retrieves better results than the query itself.
        """
        logger.info(f"Generating HyDE document for: '{query}'")
        
        system_prompt = """You are an expert technical writer.
Generate a detailed, hypothetical document passage that would perfectly answer the user's question.
Write as if you're writing the actual documentation or manual page.
Be specific and technical."""
        
        prompt = f"""Question: {query}

Write a detailed technical document passage (2-3 paragraphs) that would answer this question.
Include specific details, technical terms, and procedures as if this were from an actual manual or documentation."""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=400
            )
            
            logger.info("Generated HyDE document")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating HyDE: {e}")
            return query  # Fallback to original query
    
    def decompose_query(self, query: str) -> List[str]:
        """
        Decompose complex query into simpler sub-queries
        
        Useful for multi-part questions
        """
        logger.info(f"Decomposing query: '{query}'")
        
        system_prompt = """You are a query analysis expert.
Break down complex questions into simpler, atomic sub-questions.
Each sub-question should be answerable independently."""
        
        prompt = f"""Question: {query}

If this is a complex question with multiple parts, break it down into simpler sub-questions.
If it's already simple, just return the original question.

Format: One sub-question per line, numbered.
1. [first sub-question]
2. [second sub-question]
etc."""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=300
            )
            
            # Parse response
            sub_queries = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line and any(line.startswith(str(i)) for i in range(1, 10)):
                    # Remove number prefix
                    cleaned = line.split('.', 1)[1].strip() if '.' in line else line
                    cleaned = cleaned.strip('"\'')
                    if cleaned:
                        sub_queries.append(cleaned)
            
            # If no decomposition or only one, return original
            if len(sub_queries) <= 1:
                sub_queries = [query]
            
            logger.info(f"Decomposed into {len(sub_queries)} sub-queries")
            return sub_queries
            
        except Exception as e:
            logger.error(f"Error decomposing query: {e}")
            return [query]
    
    def expand_query(self, query: str) -> str:
        """
        Expand query with related terms and context
        
        Adds synonyms, related terms, and context
        """
        logger.info(f"Expanding query: '{query}'")
        
        system_prompt = """You are a query expansion assistant.
Add related terms, synonyms, and contextual keywords to improve search coverage."""
        
        prompt = f"""Original query: "{query}"

Expand this query by adding:
- Important synonyms
- Related technical terms
- Industry-specific terminology
- Common variations

Return the expanded query that includes the original plus additional relevant terms."""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.6,
                max_tokens=150
            )
            
            expanded = response.strip()
            logger.info("Expanded query successfully")
            return expanded
            
        except Exception as e:
            logger.error(f"Error expanding query: {e}")
            return query
    
    def enhance_query(
        self,
        query: str,
        strategy: str = "rewrite"
    ) -> Dict[str, Any]:
        """
        Main enhancement method with strategy selection
        
        Args:
            query: Original query
            strategy: "rewrite", "hyde", "decompose", "expand", or "all"
        
        Returns:
            Dict with enhanced queries and metadata
        """
        result = {
            "original": query,
            "variations": [],
            "hyde_document": None,
            "sub_queries": [],
            "expanded": None,
            "strategy_used": strategy
        }
        
        if strategy == "rewrite" or strategy == "all":
            result["variations"] = self.rewrite_query(query)
        
        if strategy == "hyde" or strategy == "all":
            result["hyde_document"] = self.generate_hyde(query)
        
        if strategy == "decompose" or strategy == "all":
            result["sub_queries"] = self.decompose_query(query)
        
        if strategy == "expand" or strategy == "all":
            result["expanded"] = self.expand_query(query)
        
        return result


# Global query enhancer instance
query_enhancer = QueryEnhancer()
