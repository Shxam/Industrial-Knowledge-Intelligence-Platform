"""
Main FastAPI application for IKIP (Pragya)
Industrial Knowledge Intelligence Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logger
from app.api.routes import health, documents, query, graph, rca
from app.kg.neo4j_client import neo4j_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    logger.info(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    
    # Initialize services
    if settings.ENABLE_KNOWLEDGE_GRAPH:
        try:
            logger.info("Initializing Neo4j knowledge graph schema...")
            neo4j_client.create_schema()
            logger.info("Neo4j schema initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j schema: {e}")
            logger.warning("Knowledge graph features may not work properly")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    if settings.ENABLE_KNOWLEDGE_GRAPH:
        try:
            neo4j_client.close()
        except Exception as e:
            logger.error(f"Error closing Neo4j connection: {e}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered industrial knowledge intelligence platform",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["Knowledge Graph"])
app.include_router(rca.router, prefix="/api/v1/rca", tags=["Root Cause Analysis"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG
    )
