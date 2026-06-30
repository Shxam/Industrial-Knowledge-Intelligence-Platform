"""
Cross-encoder re-ranking for improved relevance
"""
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import CrossEncoder

from app.core.config import settings
from app.core.logging import logger


class CrossEncoderReranker:
    """
    Cross-encoder for re-ranking retrieved documents
    
    More accurate than bi-encoder (embeddings) but slower.
    Use after initial retrieval to re-rank top candidates.
    """
    
    def __init__(self, model_name: str = None):
        """Initialize cross-encoder model"""
        self.model_name = model_name or settings.RERANKER_MODEL
        self.model = None
    
    def load_model(self):
        """Load cross-encoder model"""
        if self.model is None:
            logger.info(f"Loading cross-encoder model: {self.model_name}")
            try:
                self.model = CrossEncoder(self.model_name)
                logger.info("Cross-encoder model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading cross-encoder: {e}")
                raise
    
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Re-rank documents using cross-encoder
        
        Args:
            query: Search query
            documents: List of retrieved documents with metadata
            top_k: Number of top results to return (None = return all)
        
        Returns:
            Re-ranked list of documents with new scores
        """
        if not documents:
            return []
        
        if self.model is None:
            self.load_model()
        
        logger.info(f"Re-ranking {len(documents)} documents")
        
        # Prepare query-document pairs
        pairs = []
        for doc in documents:
            text = doc.get('metadata', {}).get('text', '')
            if not text:
                text = doc.get('text', '')
            pairs.append([query, text])
        
        # Score all pairs
        try:
            scores = self.model.predict(pairs)
            
            # Add re-rank scores to documents
            reranked = []
            for doc, score in zip(documents, scores):
                doc_copy = doc.copy()
                doc_copy['rerank_score'] = float(score)
                doc_copy['original_score'] = doc.get('score', doc.get('rrf_score', 0.0))
                reranked.append(doc_copy)
            
            # Sort by re-rank score
            reranked.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            # Return top-k if specified
            if top_k:
                reranked = reranked[:top_k]
            
            logger.info(
                f"Re-ranking complete. Top score: {reranked[0]['rerank_score']:.4f}, "
                f"Bottom score: {reranked[-1]['rerank_score']:.4f}"
            )
            
            return reranked
            
        except Exception as e:
            logger.error(f"Error during re-ranking: {e}")
            # Fallback: return original documents
            return documents
    
    def rerank_with_threshold(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        threshold: float = 0.5,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Re-rank and filter by relevance threshold
        
        Args:
            query: Search query
            documents: List of documents
            threshold: Minimum relevance score
            top_k: Max number of results
        
        Returns:
            Filtered and re-ranked documents
        """
        reranked = self.rerank(query, documents, top_k=None)
        
        # Filter by threshold
        filtered = [doc for doc in reranked if doc['rerank_score'] >= threshold]
        
        logger.info(
            f"Filtered {len(reranked)} → {len(filtered)} documents "
            f"(threshold: {threshold})"
        )
        
        # Apply top-k if specified
        if top_k:
            filtered = filtered[:top_k]
        
        return filtered
    
    def batch_rerank(
        self,
        queries: List[str],
        document_lists: List[List[Dict[str, Any]]],
        top_k: int = None
    ) -> List[List[Dict[str, Any]]]:
        """
        Re-rank multiple query-document sets
        
        Args:
            queries: List of queries
            document_lists: List of document lists (one per query)
            top_k: Number of top results per query
        
        Returns:
            List of re-ranked document lists
        """
        results = []
        for query, documents in zip(queries, document_lists):
            reranked = self.rerank(query, documents, top_k=top_k)
            results.append(reranked)
        
        return results
    
    def get_relevance_score(self, query: str, text: str) -> float:
        """
        Get relevance score for a single query-text pair
        
        Returns:
            Relevance score (higher = more relevant)
        """
        if self.model is None:
            self.load_model()
        
        try:
            score = self.model.predict([[query, text]])[0]
            return float(score)
        except Exception as e:
            logger.error(f"Error scoring pair: {e}")
            return 0.0


# Global reranker instance
reranker = CrossEncoderReranker()
