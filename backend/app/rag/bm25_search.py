"""
BM25 keyword-based search for hybrid retrieval
"""
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any, Optional
import pickle
from pathlib import Path
from datetime import datetime

from app.core.logging import logger


class BM25Search:
    """
    BM25 keyword search for document retrieval
    
    Complements vector search with exact keyword matching
    """
    
    def __init__(self):
        """Initialize BM25 search"""
        self.bm25 = None
        self.documents = []
        self.metadata = []
        self.tokenized_corpus = []
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization
        
        For production, consider using spaCy or NLTK for better tokenization
        """
        # Lowercase and split on whitespace/punctuation
        text = text.lower()
        # Simple split - can be improved with proper tokenizer
        tokens = text.split()
        # Remove very short tokens
        tokens = [t for t in tokens if len(t) > 2]
        return tokens
    
    def index_documents(
        self,
        documents: List[str],
        metadata: List[Dict[str, Any]] = None
    ):
        """
        Index documents for BM25 search
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        logger.info(f"Indexing {len(documents)} documents for BM25 search")
        
        self.documents = documents
        self.metadata = metadata or [{} for _ in documents]
        
        # Tokenize all documents
        self.tokenized_corpus = [self._tokenize(doc) for doc in documents]
        
        # Create BM25 index
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        logger.info("BM25 indexing complete")
    
    def search(
        self,
        query: str,
        k: int = 10,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search documents using BM25
        
        Args:
            query: Search query
            k: Number of results to return
            min_score: Minimum BM25 score threshold
        
        Returns:
            List of dicts with metadata, text, and BM25 score
        """
        if self.bm25 is None:
            logger.warning("BM25 index not initialized")
            return []
        
        # Tokenize query
        tokenized_query = self._tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        top_indices = scores.argsort()[-k:][::-1]
        
        # Format results
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            
            if score < min_score:
                continue
            
            result = {
                'text': self.documents[idx],
                'metadata': self.metadata[idx],
                'score': score,
                'index': int(idx),
                'search_type': 'bm25'
            }
            results.append(result)
        
        logger.info(f"BM25 search returned {len(results)} results for query: '{query[:50]}...'")
        
        return results
    
    def batch_search(
        self,
        queries: List[str],
        k: int = 10
    ) -> List[List[Dict[str, Any]]]:
        """
        Search multiple queries at once
        """
        return [self.search(query, k) for query in queries]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get BM25 index statistics"""
        return {
            'total_documents': len(self.documents),
            'avg_document_length': sum(len(doc) for doc in self.tokenized_corpus) / len(self.tokenized_corpus) if self.tokenized_corpus else 0,
            'is_indexed': self.bm25 is not None
        }
    
    def save(self, path: str):
        """Save BM25 index to disk"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'documents': self.documents,
            'metadata': self.metadata,
            'tokenized_corpus': self.tokenized_corpus,
            'saved_at': datetime.utcnow().isoformat()
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved BM25 index to {path}")
    
    def load(self, path: str):
        """Load BM25 index from disk"""
        if not Path(path).exists():
            logger.warning(f"No BM25 index found at {path}")
            return
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.documents = data['documents']
        self.metadata = data['metadata']
        self.tokenized_corpus = data['tokenized_corpus']
        
        # Recreate BM25 index
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        logger.info(f"Loaded BM25 index from {path}")
        logger.info(f"BM25 stats: {self.get_stats()}")
    
    def clear(self):
        """Clear the BM25 index"""
        self.bm25 = None
        self.documents = []
        self.metadata = []
        self.tokenized_corpus = []
        logger.info("BM25 index cleared")


class HybridRetriever:
    """
    Combines vector search and BM25 search with Reciprocal Rank Fusion (RRF)
    """
    
    def __init__(self, vector_store, bm25_search, k: int = 60):
        """
        Initialize hybrid retriever
        
        Args:
            vector_store: FaissVectorStore instance
            bm25_search: BM25Search instance
            k: RRF parameter (default 60 as per paper)
        """
        self.vector_store = vector_store
        self.bm25_search = bm25_search
        self.rrf_k = k
    
    def search(
        self,
        query: str,
        query_embedding: Any,
        top_k: int = 10,
        vector_weight: float = 0.5,
        bm25_weight: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search using vector + BM25 with RRF
        
        Args:
            query: Text query
            query_embedding: Embedding vector for query
            top_k: Number of final results
            vector_weight: Weight for vector search (not used in RRF, kept for compatibility)
            bm25_weight: Weight for BM25 search (not used in RRF, kept for compatibility)
        
        Returns:
            Fused results ranked by RRF
        """
        # Get results from both retrievers
        vector_results = self.vector_store.search(query_embedding, k=top_k * 2)
        bm25_results = self.bm25_search.search(query, k=top_k * 2)
        
        # Apply Reciprocal Rank Fusion
        fused_results = self._reciprocal_rank_fusion(
            vector_results,
            bm25_results,
            top_k
        )
        
        logger.info(
            f"Hybrid search: {len(vector_results)} vector + "
            f"{len(bm25_results)} BM25 → {len(fused_results)} fused"
        )
        
        return fused_results
    
    def _reciprocal_rank_fusion(
        self,
        vector_results: List[Dict[str, Any]],
        bm25_results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """
        Reciprocal Rank Fusion (RRF)
        
        RRF score = sum(1 / (k + rank_i)) for all systems
        
        where:
        - k is a constant (typically 60)
        - rank_i is the rank in system i
        """
        # Build document id → score mapping
        doc_scores = {}
        doc_metadata = {}
        
        # Process vector results
        for rank, result in enumerate(vector_results, start=1):
            # Use chunk_id as unique identifier
            doc_id = result['metadata'].get('chunk_id', result.get('index'))
            rrf_score = 1.0 / (self.rrf_k + rank)
            
            if doc_id not in doc_scores:
                doc_scores[doc_id] = 0
                doc_metadata[doc_id] = result['metadata']
            
            doc_scores[doc_id] += rrf_score
        
        # Process BM25 results
        for rank, result in enumerate(bm25_results, start=1):
            doc_id = result['metadata'].get('chunk_id', result.get('index'))
            rrf_score = 1.0 / (self.rrf_k + rank)
            
            if doc_id not in doc_scores:
                doc_scores[doc_id] = 0
                doc_metadata[doc_id] = result['metadata']
            
            doc_scores[doc_id] += rrf_score
        
        # Sort by RRF score
        sorted_docs = sorted(
            doc_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        # Format results
        fused_results = []
        for doc_id, rrf_score in sorted_docs:
            fused_results.append({
                'metadata': doc_metadata[doc_id],
                'rrf_score': rrf_score,
                'search_type': 'hybrid_rrf'
            })
        
        return fused_results


# Global BM25 search instance
bm25_search = BM25Search()
