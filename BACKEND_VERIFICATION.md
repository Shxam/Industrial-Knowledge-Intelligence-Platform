# Backend Verification Checklist

**Purpose**: Verify all backend components are properly integrated before frontend development  
**Date**: June 27, 2026  
**Status**: Ready for verification

---

## 🎯 Pre-Frontend Checklist

### 1. Code Integration ✅

#### Files Created (37 total):
- [x] `backend/app/main.py` - Updated with RCA router
- [x] `backend/app/core/config.py` - Updated with ENABLE_KNOWLEDGE_GRAPH
- [x] `backend/app/core/logging.py` - Complete
- [x] `backend/app/models/schemas.py` - Updated with RCA models
- [x] `backend/app/api/routes/health.py` - Complete
- [x] `backend/app/api/routes/documents.py` - Complete
- [x] `backend/app/api/routes/query.py` - Complete
- [x] `backend/app/api/routes/graph.py` - Complete with real implementations
- [x] `backend/app/api/routes/rca.py` - NEW, complete
- [x] `backend/app/rag/embeddings.py` - Complete
- [x] `backend/app/rag/chunking.py` - Complete
- [x] `backend/app/rag/vector_store.py` - Complete
- [x] `backend/app/rag/bm25_search.py` - Complete
- [x] `backend/app/rag/llm_client.py` - Updated with additional_context
- [x] `backend/app/rag/pipeline.py` - Updated with KG integration
- [x] `backend/app/rag/query_enhancement.py` - Complete
- [x] `backend/app/rag/reranking.py` - Complete
- [x] `backend/app/rag/compression.py` - Complete
- [x] `backend/app/rag/guardrails.py` - Complete
- [x] `backend/app/kg/__init__.py` - NEW, complete
- [x] `backend/app/kg/ner.py` - NEW, complete
- [x] `backend/app/kg/relations.py` - NEW, complete
- [x] `backend/app/kg/neo4j_client.py` - NEW, complete
- [x] `backend/app/kg/entity_resolution.py` - NEW, complete
- [x] `backend/app/agents/__init__.py` - NEW, complete
- [x] `backend/app/agents/rca_agent.py` - NEW, complete
- [x] `backend/app/ingestion/loader.py` - Complete
- [x] `backend/app/services/session.py` - Complete
- [x] `.env.example` - Updated with ENABLE_KNOWLEDGE_GRAPH
- [x] `docker-compose.yml` - Complete
- [x] `backend/requirements.txt` - Complete

#### Documentation (20+ files):
- [x] All progress reports
- [x] All technical guides
- [x] All testing guides
- [x] Architecture diagrams
- [x] Executive summary

---

## 2. Import Dependencies ⚠️ CHECK NEEDED

### To Verify:

#### In `backend/app/main.py`:
```python
from app.api.routes import health, documents, query, graph, rca  # ← Check rca import
from app.kg.neo4j_client import neo4j_client  # ← Check import
```

#### In `backend/app/rag/pipeline.py`:
```python
from app.kg.ner import ner  # ← Check import
from app.kg.relations import relationship_extractor  # ← Check import
from app.kg.neo4j_client import neo4j_client  # ← Check import
from app.kg.entity_resolution import entity_resolver  # ← Check import
```

#### In `backend/app/agents/rca_agent.py`:
```python
from app.kg.neo4j_client import neo4j_client  # ← Check import
from app.kg.ner import ner  # ← Check import
from app.rag.pipeline import rag_pipeline  # ← Check import
from app.rag.llm_client import llm_client  # ← Check import
```

#### In `backend/app/api/routes/rca.py`:
```python
from app.agents.rca_agent import rca_agent  # ← Check import
```

#### In `backend/app/api/routes/graph.py`:
```python
from app.kg.neo4j_client import neo4j_client  # ← Check import
```

---

## 3. Configuration Verification ⚠️ CHECK NEEDED

### Environment Variables:
```bash
# Core
APP_NAME=IKIP
APP_ENV=development
APP_DEBUG=true

# LLM
LLM_PROVIDER=ollama  # or openai
OPENAI_API_KEY=sk-...  # if using OpenAI

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password_change_me

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Features
ENABLE_KNOWLEDGE_GRAPH=true  # ← NEW
ENABLE_HYBRID_SEARCH=true
```

---

## 4. Syntax Verification ⚠️ REQUIRED

### Run Syntax Checks:
```bash
# Navigate to backend
cd backend

# Check for Python syntax errors
python -m py_compile app/main.py
python -m py_compile app/agents/rca_agent.py
python -m py_compile app/kg/ner.py
python -m py_compile app/kg/relations.py
python -m py_compile app/kg/neo4j_client.py
python -m py_compile app/kg/entity_resolution.py
python -m py_compile app/api/routes/graph.py
python -m py_compile app/api/routes/rca.py

# Or check all at once
find app -name "*.py" -exec python -m py_compile {} \;

# Check imports
python -c "from app.kg import ner, relationship_extractor, neo4j_client, entity_resolver"
python -c "from app.agents import rca_agent"
```

---

## 5. Dependency Installation ⚠️ REQUIRED

### Install New Dependencies:
```bash
# Make sure spaCy is installed (for NER)
pip install spacy
python -m spacy download en_core_web_sm

# Make sure sentence-transformers is installed (for reranking)
pip install sentence-transformers

# Check all requirements
pip install -r requirements.txt
```

### Update requirements.txt if needed:
```txt
# Should include:
spacy>=3.7.0
neo4j>=5.14.0
sentence-transformers>=2.2.0
```

---

## 6. Service Verification ⚠️ REQUIRED

### Start Services:
```bash
# Start Docker services
docker-compose up -d

# Verify Neo4j is running
docker ps | grep neo4j

# Check Neo4j logs
docker logs et-hackathon-neo4j-1

# Verify Redis is running
docker ps | grep redis

# Verify MinIO is running
docker ps | grep minio
```

### Service Health:
```bash
# Neo4j browser
open http://localhost:7474
# Login: neo4j / neo4j_password_change_me

# MinIO console
open http://localhost:9001
# Login: minioadmin / minioadmin

# Redis ping
redis-cli ping
# Should return: PONG
```

---

## 7. Backend Startup ⚠️ CRITICAL

### Start Backend:
```bash
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Start app
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Expected Startup Logs:
```
INFO:     Starting IKIP (Pragya) v0.1.0
INFO:     Environment: development
INFO:     LLM Provider: ollama
INFO:     Embedding Model: BAAI/bge-small-en-v1.5
INFO:     Initializing Neo4j knowledge graph schema...
INFO:     Connecting to Neo4j at bolt://localhost:7687
INFO:     Connected to Neo4j successfully
INFO:     Neo4j schema initialized successfully
INFO:     RAG Pipeline initialized
INFO:     RCA Agent initialized
INFO:     Started server process [pid]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Watch for Errors:
- ❌ Neo4j connection failed → Check docker-compose
- ❌ Import errors → Check file paths
- ❌ spaCy model not found → Run: `python -m spacy download en_core_web_sm`

---

## 8. API Endpoint Verification ⚠️ CRITICAL

### Test All Endpoints:

#### Health Check:
```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status": "healthy", ...}
```

#### API Documentation:
```bash
open http://localhost:8000/docs
# Should show all 15 endpoints
```

#### Graph Stats (Neo4j):
```bash
curl http://localhost:8000/api/v1/graph/stats
# Expected: {"node_count": 0, "relationship_count": 0, ...}
```

#### RCA Health:
```bash
curl http://localhost:8000/api/v1/rca/health
# Expected: {"status": "healthy", "agent": "RCA Agent", ...}
```

#### Document Upload (Test):
```bash
echo "Test document for P-101 pump" > test.txt
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"
# Expected: {"document_id": "...", "status": "processing", ...}
```

---

## 9. Integration Tests ⚠️ RECOMMENDED

### Test Complete Flow:

#### Test 1: Document → KG
```bash
# 1. Create test document
echo "P-101 pump has seal leak at 100°C per OISD-STD-105" > failure.txt

# 2. Upload
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@failure.txt")
DOC_ID=$(echo $RESPONSE | jq -r .document_id)

# 3. Wait 5 seconds
sleep 5

# 4. Check graph stats
curl http://localhost:8000/api/v1/graph/stats
# Expected: node_count > 0

# 5. List entities
curl http://localhost:8000/api/v1/graph/entities
# Expected: entities array with P-101, seal leak, etc.
```

#### Test 2: Query with KG
```bash
# Query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is P-101?","strategy":"hybrid"}'
# Expected: answer with kg_entities array
```

#### Test 3: RCA Analysis
```bash
# RCA
curl -X POST http://localhost:8000/api/v1/rca/analyze \
  -H "Content-Type: application/json" \
  -d '{"failure_description":"P-101 seal leak at 100°C"}'
# Expected: five_why_analysis, fishbone_diagram, recommendations
```

---

## 10. Error Handling ⚠️ CHECK

### Test Error Scenarios:

#### Invalid Requests:
```bash
# Empty failure description
curl -X POST http://localhost:8000/api/v1/rca/analyze \
  -H "Content-Type: application/json" \
  -d '{"failure_description":""}'
# Expected: 422 Validation Error

# Non-existent document
curl http://localhost:8000/api/v1/documents/invalid-id/status
# Expected: 404 Not Found
```

#### Service Failures:
```bash
# Stop Neo4j
docker-compose stop neo4j

# Try graph query
curl http://localhost:8000/api/v1/graph/stats
# Expected: 500 error OR graceful degradation

# Restart Neo4j
docker-compose start neo4j
```

---

## 11. Performance Check ⚠️ OPTIONAL

### Measure Response Times:

```bash
# Document upload
time curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"
# Target: < 5s

# Query
time curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is P-101?"}'
# Target: < 3s

# RCA
time curl -X POST http://localhost:8000/api/v1/rca/analyze \
  -H "Content-Type: application/json" \
  -d '{"failure_description":"pump failure"}'
# Target: < 10s
```

---

## 12. Documentation Check ✅

### Verify Documentation:
- [x] All 20+ documents created
- [x] API documented in code
- [x] Testing guides complete
- [x] Architecture diagrams done
- [x] Quick references available

---

## ✅ Verification Summary

| Check | Status | Action Required |
|-------|--------|-----------------|
| 1. Code Integration | ✅ Done | None |
| 2. Import Dependencies | ⚠️ Verify | Run import tests |
| 3. Configuration | ⚠️ Verify | Check .env |
| 4. Syntax | ⚠️ Verify | Run py_compile |
| 5. Dependencies | ⚠️ Install | Run pip install |
| 6. Services | ⚠️ Start | docker-compose up |
| 7. Backend Startup | ⚠️ Test | python app/main.py |
| 8. API Endpoints | ⚠️ Test | curl tests |
| 9. Integration | ⚠️ Test | End-to-end flows |
| 10. Error Handling | ⚠️ Test | Error scenarios |
| 11. Performance | ℹ️ Optional | Time tests |
| 12. Documentation | ✅ Done | None |

---

## 🚨 Common Issues & Solutions

### Issue: Import Error - module not found
**Solution**:
```bash
# Make sure you're in the backend directory
cd backend

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run with module syntax
python -m app.main
```

### Issue: Neo4j connection failed
**Solution**:
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Check Neo4j logs
docker logs et-hackathon-neo4j-1

# Restart Neo4j
docker-compose restart neo4j

# Wait 10 seconds for startup
sleep 10
```

### Issue: spaCy model not found
**Solution**:
```bash
python -m spacy download en_core_web_sm
```

### Issue: Port 8000 already in use
**Solution**:
```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000

# Kill process or change port
uvicorn app.main:app --port 8001
```

---

## 🎯 Success Criteria

### Backend is Ready When:
- [ ] All services start without errors
- [ ] Backend starts and shows "Application startup complete"
- [ ] All 15 API endpoints return 200/201
- [ ] Can upload document and extract entities
- [ ] Can query with graph augmentation
- [ ] Can perform RCA analysis
- [ ] No import errors
- [ ] No syntax errors
- [ ] Neo4j schema initialized
- [ ] Documentation complete

---

## 📋 Next Steps After Verification

Once all checks pass:

1. ✅ Backend is verified and stable
2. 🎨 Start frontend development (Day 4)
3. 🧪 Write integration tests (Day 8-9)
4. 🎬 Prepare demo (Day 10-11)
5. 🚀 Polish and submit (Day 12-14)

---

## 🔧 Quick Verification Script

```bash
#!/bin/bash
# quick-verify.sh

echo "=== IKIP Backend Verification ==="

echo "1. Checking services..."
docker-compose ps

echo "2. Testing imports..."
cd backend
python -c "from app.kg import ner, neo4j_client; print('KG imports: OK')"
python -c "from app.agents import rca_agent; print('Agent imports: OK')"

echo "3. Starting backend..."
python app/main.py &
BACKEND_PID=$!
sleep 5

echo "4. Testing endpoints..."
curl -s http://localhost:8000/api/v1/health | grep healthy && echo "Health: OK"
curl -s http://localhost:8000/api/v1/graph/stats && echo "Graph: OK"
curl -s http://localhost:8000/api/v1/rca/health && echo "RCA: OK"

echo "5. Cleanup..."
kill $BACKEND_PID

echo "=== Verification Complete ==="
```

---

**Status**: Ready for verification  
**Estimated Time**: 30-45 minutes  
**Priority**: HIGH - Do this before frontend

---

**Last Updated**: June 27, 2026  
**Next**: Run verification, then start frontend
