"""
FAISS vector store for document embeddings
"""
import faiss
import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app.core.config import settings
from app.core.logging import logger


class FaissVectorStore:
    """
    FAISS-based vector store for document chunks
    
    Supports both Flat and IVF indices for scalability
    """
    
    def __init__(self, index_path: str = None):
        """Initialize vector store"""
        self.index_path = index_path or settings.FAISS_INDEX_PATH
        self.dimension = settings.EMBEDDING_DIMENSION
        self.index = None
        self.metadata = []
        self.doc_count = 0
        
        # Create index directory if it doesn't exist
        Path(self.index_path).mkdir(parents=True, exist_ok=True)
    
    def create_index(self, index_type: str = None):
        """
        Create FAISS index
        
        Types:
        - Flat: Exact search, best for small datasets (< 1M vectors)
        - IVFFlat: Approximate search with clustering, faster for large datasets
        - HNSW: Hierarchical graph, best accuracy/speed tradeoff
        """
        index_type = index_type or settings.FAISS_INDEX_TYPE
        
        logger.info(f"Creating FAISS index: {index_type}, dimension: {self.dimension}")
        
        if index_type == "Flat":
            # Exact search using L2 distance
            self.index = faiss.IndexFlatL2(self.dimension)
            
        elif index_type == "IVFFlat":
            # Approximate search with inverted file index
            nlist = 100  # Number of clusters
            quantizer = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            # Note: IVF index needs training before adding vectors
            
        elif index_type == "HNSW":
            # Hierarchical Navigable Small World graph
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
            
        else:
            raise ValueError(f"Unknown index type: {index_type}")
        
        logger.info(f"Created {index_type} index successfully")
    
    def train_index(self, training_vectors: np.ndarray):
        """
        Train IVF index (required before adding vectors)
        
        Only needed for IVF-type indices
        """
        if isinstance(self.index, faiss.IndexIVFFlat):
            logger.info(f"Training IVF index with {len(training_vectors)} vectors")
            self.index.train(training_vectors.astype('float32'))
            logger.info("IVF index training complete")
    
    def add_documents(
        self,
        embeddings: np.ndarray,
        metadata: List[Dict[str, Any]]
    ) -> List[int]:
        """
        Add document embeddings to index
        
        Args:
            embeddings: numpy array of shape (n_docs, dimension)
            metadata: list of metadata dicts for each document
        
        Returns:
            List of assigned document IDs
        """
        if self.index is None:
            self.create_index()
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Validate dimensions
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension {embeddings.shape[1]} "
                f"doesn't match index dimension {self.dimension}"
            )
        
        # Train IVF index if needed and not yet trained
        if isinstance(self.index, faiss.IndexIVFFlat) and not self.index.is_trained:
            self.train_index(embeddings)
        
        # Add to index
        start_id = len(self.metadata)
        self.index.add(embeddings)
        
        # Store metadata with IDs
        for i, meta in enumerate(metadata):
            meta['_id'] = start_id + i
            meta['_indexed_at'] = datetime.utcnow().isoformat()
            self.metadata.append(meta)
        
        self.doc_count += len(embeddings)
        
        logger.info(f"Added {len(embeddings)} documents to index (total: {self.doc_count})")
        
        return list(range(start_id, start_id + len(embeddings)))
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 10,
        filter_func: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            filter_func: Optional function to filter results
        
        Returns:
            List of dicts with metadata, score, and distance
        """
        if self.index is None or self.index.ntotal == 0:
            logger.warning("Index is empty, returning no results")
            return []
        
        # Ensure query is right shape and type
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Format results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for missing results
                continue
            
            if idx >= len(self.metadata):
                logger.warning(f"Index {idx} out of range for metadata")
                continue
            
            result = {
                'metadata': self.metadata[idx],
                'distance': float(dist),
                'score': self._distance_to_score(float(dist)),
                'index': int(idx)
            }
            
            # Apply filter if provided
            if filter_func is None or filter_func(result):
                results.append(result)
        
        return results
    
    def _distance_to_score(self, distance: float) -> float:
        """
        Convert L2 distance to similarity score (0-1)
        
        Uses inverse distance: score = 1 / (1 + distance)
        """
        return 1.0 / (1.0 + distance)
    
    def batch_search(
        self,
        query_embeddings: np.ndarray,
        k: int = 10
    ) -> List[List[Dict[str, Any]]]:
        """
        Search for multiple queries at once
        
        More efficient than individual searches
        """
        if self.index is None or self.index.ntotal == 0:
            return [[] for _ in range(len(query_embeddings))]
        
        query_embeddings = query_embeddings.astype('float32')
        
        distances, indices = self.index.search(query_embeddings, k)
        
        all_results = []
        for query_distances, query_indices in zip(distances, indices):
            results = []
            for dist, idx in zip(query_distances, query_indices):
                if idx >= 0 and idx < len(self.metadata):
                    results.append({
                        'metadata': self.metadata[idx],
                        'distance': float(dist),
                        'score': self._distance_to_score(float(dist)),
                        'index': int(idx)
                    })
            all_results.append(results)
        
        return all_results
    
    def get_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Get document metadata by ID"""
        if 0 <= doc_id < len(self.metadata):
            return self.metadata[doc_id]
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        return {
            'total_documents': self.doc_count,
            'index_size': self.index.ntotal if self.index else 0,
            'dimension': self.dimension,
            'index_type': type(self.index).__name__ if self.index else None,
            'is_trained': self.index.is_trained if isinstance(self.index, faiss.IndexIVFFlat) else True
        }
    
    def save(self, path: str = None):
        """Save index and metadata to disk"""
        path = path or self.index_path
        Path(path).mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_file = Path(path) / "index.faiss"
        faiss.write_index(self.index, str(index_file))
        logger.info(f"Saved FAISS index to {index_file}")
        
        # Save metadata
        metadata_file = Path(path) / "metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved metadata to {metadata_file}")
        
        # Save stats
        stats_file = Path(path) / "stats.json"
        with open(stats_file, 'w') as f:
            json.dump({
                'doc_count': self.doc_count,
                'dimension': self.dimension,
                'saved_at': datetime.utcnow().isoformat()
            }, f, indent=2)
        
        logger.info(f"Vector store saved successfully to {path}")
    
    def load(self, path: str = None):
        """Load index and metadata from disk"""
        path = path or self.index_path
        
        index_file = Path(path) / "index.faiss"
        metadata_file = Path(path) / "metadata.pkl"
        
        if not index_file.exists():
            logger.warning(f"No index found at {index_file}, creating new index")
            self.create_index()
            return
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_file))
        logger.info(f"Loaded FAISS index from {index_file}")
        
        # Load metadata
        if metadata_file.exists():
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
            logger.info(f"Loaded metadata from {metadata_file}")
        
        self.doc_count = len(self.metadata)
        
        logger.info(f"Vector store loaded successfully from {path}")
        logger.info(f"Index stats: {self.get_stats()}")
    
    def clear(self):
        """Clear the index and metadata"""
        self.create_index()
        self.metadata = []
        self.doc_count = 0
        logger.info("Vector store cleared")
    
    def delete_by_document_id(self, document_id: str) -> int:
        """
        Delete all chunks belonging to a document
        
        Returns number of chunks deleted
        
        Note: FAISS doesn't support true deletion, so we mark as deleted
        and rebuild index if needed
        """
        deleted_count = 0
        new_metadata = []
        
        for meta in self.metadata:
            if meta.get('document_id') != document_id:
                new_metadata.append(meta)
            else:
                deleted_count += 1
        
        if deleted_count > 0:
            self.metadata = new_metadata
            self.doc_count = len(new_metadata)
            logger.info(f"Marked {deleted_count} chunks for deletion from document {document_id}")
            logger.warning("Index needs rebuild to remove deleted vectors")
        
        return deleted_count


# Global vector store instance
vector_store = FaissVectorStore()
