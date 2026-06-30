"""
Embedding service using BGE models
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
from app.core.config import settings
from app.core.logging import logger


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        self.model = None
        
    def load_model(self):
        """Load the embedding model"""
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded successfully")
        return self.model
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text"""
        if self.model is None:
            self.load_model()
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Embed multiple texts in batch"""
        if self.model is None:
            self.load_model()
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 100
        )
        return embeddings
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension


# Global embedding service instance
embedding_service = EmbeddingService()
