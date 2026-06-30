"""
Configuration management for IKIP (Pragya)
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True
    APP_NAME: str = "IKIP - Pragya"
    APP_VERSION: str = "1.0.0"
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai | ollama | azure
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    
    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384
    
    # Re-ranker
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "ikip_db"
    POSTGRES_USER: str = "ikip_user"
    POSTGRES_PASSWORD: str = "ikip_password_change_me"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j_password_change_me"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # MinIO / S3
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "ikip-documents"
    MINIO_SECURE: bool = False
    
    # Vector Store
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    FAISS_INDEX_TYPE: str = "IVFFlat"
    
    # OCR
    OCR_ENGINE: str = "paddleocr"
    OCR_LANG: str = "en"
    
    # RAG Configuration
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 10
    RERANK_TOP_K: int = 5
    CONFIDENCE_THRESHOLD: float = 0.7
    ENABLE_HYBRID_SEARCH: bool = True
    ENABLE_GRAPH_AUGMENTATION: bool = True
    ENABLE_KNOWLEDGE_GRAPH: bool = True
    
    # Security
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Guardrails
    ENABLE_GUARDRAILS: bool = True
    HALLUCINATION_THRESHOLD: float = 0.6
    GROUNDEDNESS_THRESHOLD: float = 0.7
    
    # Monitoring & Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_AUDIT_LOG: bool = True
    
    # RAGAS Evaluation
    ENABLE_RAGAS_EVAL: bool = True
    RAGAS_TESTSET_SIZE: int = 50
    
    class Config:
        env_file = "../.env"  # .env is in project root, not backend folder
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "ignore"


# Global settings instance
settings = Settings()
