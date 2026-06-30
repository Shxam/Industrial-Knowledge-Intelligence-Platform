"""
Import verification script
Checks that all modules can be imported successfully
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def verify_imports():
    """Verify all critical imports work"""
    errors = []
    
    print("🔍 Verifying backend imports...\n")
    
    # Core imports
    print("1. Core modules...")
    try:
        from app.core.config import settings
        print("   ✅ app.core.config")
    except Exception as e:
        errors.append(f"❌ app.core.config: {e}")
        print(f"   ❌ app.core.config: {e}")
    
    try:
        from app.core.logging import logger
        print("   ✅ app.core.logging")
    except Exception as e:
        errors.append(f"❌ app.core.logging: {e}")
        print(f"   ❌ app.core.logging: {e}")
    
    # Models
    print("\n2. Data models...")
    try:
        from app.models.schemas import (
            RCARequest, RCAResponse, QueryRequest, QueryResponse
        )
        print("   ✅ app.models.schemas")
    except Exception as e:
        errors.append(f"❌ app.models.schemas: {e}")
        print(f"   ❌ app.models.schemas: {e}")
    
    # RAG modules
    print("\n3. RAG engine...")
    try:
        from app.rag.embeddings import embedding_service
        print("   ✅ app.rag.embeddings")
    except Exception as e:
        errors.append(f"❌ app.rag.embeddings: {e}")
        print(f"   ❌ app.rag.embeddings: {e}")
    
    try:
        from app.rag.chunking import chunker
        print("   ✅ app.rag.chunking")
    except Exception as e:
        errors.append(f"❌ app.rag.chunking: {e}")
        print(f"   ❌ app.rag.chunking: {e}")
    
    try:
        from app.rag.vector_store import vector_store
        print("   ✅ app.rag.vector_store")
    except Exception as e:
        errors.append(f"❌ app.rag.vector_store: {e}")
        print(f"   ❌ app.rag.vector_store: {e}")
    
    try:
        from app.rag.bm25_search import bm25_search
        print("   ✅ app.rag.bm25_search")
    except Exception as e:
        errors.append(f"❌ app.rag.bm25_search: {e}")
        print(f"   ❌ app.rag.bm25_search: {e}")
    
    try:
        from app.rag.llm_client import llm_client
        print("   ✅ app.rag.llm_client")
    except Exception as e:
        errors.append(f"❌ app.rag.llm_client: {e}")
        print(f"   ❌ app.rag.llm_client: {e}")
    
    try:
        from app.rag.pipeline import rag_pipeline
        print("   ✅ app.rag.pipeline")
    except Exception as e:
        errors.append(f"❌ app.rag.pipeline: {e}")
        print(f"   ❌ app.rag.pipeline: {e}")
    
    # Knowledge Graph modules
    print("\n4. Knowledge graph...")
    try:
        from app.kg.ner import ner
        print("   ✅ app.kg.ner")
    except Exception as e:
        errors.append(f"❌ app.kg.ner: {e}")
        print(f"   ❌ app.kg.ner: {e}")
    
    try:
        from app.kg.relations import relationship_extractor
        print("   ✅ app.kg.relations")
    except Exception as e:
        errors.append(f"❌ app.kg.relations: {e}")
        print(f"   ❌ app.kg.relations: {e}")
    
    try:
        from app.kg.neo4j_client import neo4j_client
        print("   ✅ app.kg.neo4j_client")
    except Exception as e:
        errors.append(f"❌ app.kg.neo4j_client: {e}")
        print(f"   ❌ app.kg.neo4j_client: {e}")
    
    try:
        from app.kg.entity_resolution import entity_resolver
        print("   ✅ app.kg.entity_resolution")
    except Exception as e:
        errors.append(f"❌ app.kg.entity_resolution: {e}")
        print(f"   ❌ app.kg.entity_resolution: {e}")
    
    # AI Agents
    print("\n5. AI agents...")
    try:
        from app.agents.rca_agent import rca_agent
        print("   ✅ app.agents.rca_agent")
    except Exception as e:
        errors.append(f"❌ app.agents.rca_agent: {e}")
        print(f"   ❌ app.agents.rca_agent: {e}")
    
    # Document processing
    print("\n6. Document processing...")
    try:
        from app.ingestion.loader import document_loader
        print("   ✅ app.ingestion.loader")
    except Exception as e:
        errors.append(f"❌ app.ingestion.loader: {e}")
        print(f"   ❌ app.ingestion.loader: {e}")
    
    # Services
    print("\n7. Services...")
    try:
        from app.services.session import session_manager
        print("   ✅ app.services.session")
    except Exception as e:
        errors.append(f"❌ app.services.session: {e}")
        print(f"   ❌ app.services.session: {e}")
    
    # API routes
    print("\n8. API routes...")
    try:
        from app.api.routes import health, documents, query, graph, rca
        print("   ✅ app.api.routes (all)")
    except Exception as e:
        errors.append(f"❌ app.api.routes: {e}")
        print(f"   ❌ app.api.routes: {e}")
    
    # Main app
    print("\n9. Main application...")
    try:
        from app.main import app
        print("   ✅ app.main")
    except Exception as e:
        errors.append(f"❌ app.main: {e}")
        print(f"   ❌ app.main: {e}")
    
    # Summary
    print("\n" + "="*60)
    if errors:
        print(f"❌ FAILED: {len(errors)} import error(s)")
        print("\nErrors:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✅ SUCCESS: All imports verified!")
        return True

if __name__ == "__main__":
    success = verify_imports()
    sys.exit(0 if success else 1)
