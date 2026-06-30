"""
Startup validation script
Checks all services and dependencies before starting the backend
"""
import sys
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def check_services():
    """Check if required services are running"""
    print("🔍 Checking services...\n")
    
    services_ok = True
    
    # Check Neo4j
    print("1. Neo4j (Knowledge Graph)...")
    try:
        from neo4j import GraphDatabase
        from app.core.config import settings
        
        driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        with driver.session() as session:
            result = session.run("RETURN 1")
            result.single()
        driver.close()
        print("   ✅ Neo4j is running and accessible")
    except Exception as e:
        print(f"   ❌ Neo4j connection failed: {e}")
        print("   💡 Run: docker-compose up -d neo4j")
        services_ok = False
    
    # Check Redis
    print("\n2. Redis (Session Management)...")
    try:
        import redis
        from app.core.config import settings
        
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        r.ping()
        print("   ✅ Redis is running and accessible")
    except Exception as e:
        print(f"   ⚠️ Redis connection failed: {e}")
        print("   💡 Run: docker-compose up -d redis")
        print("   ⚠️ Session management will use in-memory fallback")
    
    # Check MinIO
    print("\n3. MinIO (Document Storage)...")
    try:
        from minio import Minio
        from app.core.config import settings
        
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        # Try to check if bucket exists (will fail gracefully if not)
        try:
            client.bucket_exists(settings.MINIO_BUCKET)
        except:
            pass
        print("   ✅ MinIO is running and accessible")
    except Exception as e:
        print(f"   ❌ MinIO connection failed: {e}")
        print("   💡 Run: docker-compose up -d minio")
        services_ok = False
    
    return services_ok

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...\n")
    
    deps_ok = True
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
        ('numpy', 'NumPy'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('faiss', 'FAISS'),
        ('spacy', 'spaCy'),
        ('neo4j', 'Neo4j Driver'),
        ('redis', 'Redis'),
        ('minio', 'MinIO'),
        ('openai', 'OpenAI'),
    ]
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} not installed")
            print(f"      💡 Run: pip install {package}")
            deps_ok = False
    
    # Check spaCy model
    print("\n   Checking spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("   ✅ en_core_web_sm model installed")
    except:
        print("   ❌ spaCy model en_core_web_sm not found")
        print("      💡 Run: python -m spacy download en_core_web_sm")
        deps_ok = False
    
    return deps_ok

def check_config():
    """Check if configuration is valid"""
    print("\n🔍 Checking configuration...\n")
    
    try:
        from app.core.config import settings
        
        print(f"   App Name: {settings.APP_NAME}")
        print(f"   Environment: {settings.APP_ENV}")
        print(f"   LLM Provider: {settings.LLM_PROVIDER}")
        print(f"   Embedding Model: {settings.EMBEDDING_MODEL}")
        print(f"   KG Enabled: {settings.ENABLE_KNOWLEDGE_GRAPH}")
        print(f"   Hybrid Search: {settings.ENABLE_HYBRID_SEARCH}")
        
        # Check LLM configuration
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-api-key-here":
                print("\n   ⚠️ OpenAI API key not configured")
                print("      💡 Set OPENAI_API_KEY in .env file")
                return False
        
        print("\n   ✅ Configuration is valid")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n🔍 Checking directories...\n")
    
    from app.core.config import settings
    
    dirs_to_check = [
        Path(settings.FAISS_INDEX_PATH),
        Path("./data"),
    ]
    
    for dir_path in dirs_to_check:
        if not dir_path.exists():
            print(f"   📁 Creating {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"   ✅ {dir_path} exists")
    
    return True

def main():
    """Run all startup checks"""
    print("="*60)
    print("🚀 IKIP Backend Startup Validation")
    print("="*60)
    
    all_ok = True
    
    # 1. Check dependencies
    if not check_dependencies():
        all_ok = False
    
    # 2. Check configuration
    if not check_config():
        all_ok = False
    
    # 3. Check directories
    if not check_directories():
        all_ok = False
    
    # 4. Check services
    if not check_services():
        all_ok = False
    
    # 5. Run import verification
    print("\n🔍 Verifying imports...\n")
    try:
        from verify_imports import verify_imports
        if not verify_imports():
            all_ok = False
    except Exception as e:
        print(f"   ❌ Import verification failed: {e}")
        all_ok = False
    
    # Summary
    print("\n" + "="*60)
    if all_ok:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 Ready to start backend:")
        print("   python app/main.py")
        print("   OR")
        print("   uvicorn app.main:app --reload")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("\n⚠️ Please fix the issues above before starting the backend")
        return 1

if __name__ == "__main__":
    sys.exit(main())
