"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    
    services = {
        "api": "healthy",
        "postgres": "checking",
        "neo4j": "checking",
        "redis": "checking",
        "minio": "checking",
        "embedding_model": "checking",
        "llm": "checking"
    }
    
    # TODO: Add actual health checks for each service
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "services": services,
        "config": {
            "llm_provider": settings.LLM_PROVIDER,
            "embedding_model": settings.EMBEDDING_MODEL,
            "hybrid_search": settings.ENABLE_HYBRID_SEARCH,
            "graph_augmentation": settings.ENABLE_GRAPH_AUGMENTATION,
            "guardrails": settings.ENABLE_GUARDRAILS
        }
    }
