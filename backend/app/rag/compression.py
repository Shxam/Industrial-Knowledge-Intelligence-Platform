"""
Context compression for efficient LLM usage
Reduces context size while preserving relevance
"""
from typing import List, Dict, Any
from app.rag.llm_client import llm_client
from app.core.logging import logger


class ContextCompressor:
    """
    Compress retrieved context to reduce token usage
    
    Techniques:
    - LLM-based relevance extraction
    - Redundancy removal
    - Summary generation
    """
    
    def __init__(self):
        self.llm_client = llm_client
    
    def extract_relevant_spans(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        max_length: int = 2000
    ) -> str:
        """
        Extract only relevant spans from documents using LLM
        
        Args:
            query: User query
            documents: Retrieved documents
            max_length: Maximum context length in characters
        
        Returns:
            Compressed context string
        """
        logger.info(f"Extracting relevant spans for query: '{query[:50]}...'")
        
        # Build context from documents
        full_context = "\n\n".join([
            f"[Doc {i+1}] {doc.get('metadata', {}).get('text', doc.get('text', ''))}"
            for i, doc in enumerate(documents[:10])
        ])
        
        # If already short enough, return as-is
        if len(full_context) <= max_length:
            return full_context
        
        system_prompt = """You are a context extraction assistant.
Extract ONLY the sentences and phrases that are directly relevant to answering the user's query.
Remove any redundant or irrelevant information.
Preserve the exact wording from the original context."""
        
        prompt = f"""Query: {query}

Context:
{full_context[:8000]}  # Limit input size

Extract only the relevant parts that help answer the query.
Keep the document markers [Doc N] for citation tracking.
Maximum length: {max_length} characters."""
        
        try:
            compressed = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Lower temperature for precision
                max_tokens=max_length // 3  # Rough token estimate
            )
            
            logger.info(
                f"Compressed context: {len(full_context)} → {len(compressed)} chars "
                f"({len(compressed)/len(full_context)*100:.1f}%)"
            )
            
            return compressed.strip()
            
        except Exception as e:
            logger.error(f"Error compressing context: {e}")
            # Fallback: truncate
            return full_context[:max_length]
    
    def deduplicate_chunks(
        self,
        documents: List[Dict[str, Any]],
        similarity_threshold: float = 0.9
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate or highly similar chunks
        
        Args:
            documents: List of document chunks
            similarity_threshold: Threshold for considering chunks duplicate
        
        Returns:
            Deduplicated list
        """
        if len(documents) <= 1:
            return documents
        
        logger.info(f"Deduplicating {len(documents)} chunks")
        
        deduplicated = []
        seen_texts = set()
        
        for doc in documents:
            text = doc.get('metadata', {}).get('text', doc.get('text', ''))
            text_lower = text.lower().strip()
            
            # Simple deduplication by exact match
            if text_lower not in seen_texts:
                deduplicated.append(doc)
                seen_texts.add(text_lower)
        
        logger.info(f"Removed {len(documents) - len(deduplicated)} duplicates")
        
        return deduplicated
    
    def summarize_chunks(
        self,
        documents: List[Dict[str, Any]],
        max_summary_length: int = 1500
    ) -> str:
        """
        Generate a summary of multiple chunks
        
        Useful when you have many similar chunks
        """
        logger.info(f"Summarizing {len(documents)} chunks")
        
        # Combine texts
        combined_text = "\n\n".join([
            doc.get('metadata', {}).get('text', doc.get('text', ''))
            for doc in documents[:10]
        ])
        
        system_prompt = """You are a technical summarization assistant.
Create a concise summary that captures all key information from the provided text.
Preserve technical details, numbers, and specific procedures."""
        
        prompt = f"""Summarize the following technical documentation:

{combined_text[:6000]}

Create a comprehensive but concise summary (max {max_summary_length} characters).
Include all critical details."""
        
        try:
            summary = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.4,
                max_tokens=max_summary_length // 3
            )
            
            logger.info(f"Generated summary: {len(summary)} chars")
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return combined_text[:max_summary_length]
    
    def compress_context(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        method: str = "extract",
        max_length: int = 2000
    ) -> str:
        """
        Main compression method with strategy selection
        
        Args:
            query: User query
            documents: Retrieved documents
            method: "extract", "summarize", or "dedupe"
            max_length: Target max length
        
        Returns:
            Compressed context string
        """
        if not documents:
            return ""
        
        if method == "dedupe":
            # First deduplicate
            deduplicated = self.deduplicate_chunks(documents)
            # Then extract relevant spans
            return self.extract_relevant_spans(query, deduplicated, max_length)
        
        elif method == "summarize":
            return self.summarize_chunks(documents, max_length)
        
        else:  # extract
            return self.extract_relevant_spans(query, documents, max_length)
    
    def smart_truncate(
        self,
        text: str,
        max_length: int,
        preserve_sentences: bool = True
    ) -> str:
        """
        Intelligently truncate text
        
        Preserves sentence boundaries if requested
        """
        if len(text) <= max_length:
            return text
        
        if preserve_sentences:
            # Truncate at sentence boundary
            truncated = text[:max_length]
            last_period = truncated.rfind('.')
            if last_period > max_length * 0.8:  # If close to end
                return truncated[:last_period + 1]
        
        return text[:max_length] + "..."


# Global compressor instance
context_compressor = ContextCompressor()
