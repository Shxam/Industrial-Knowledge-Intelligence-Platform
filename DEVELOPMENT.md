# Development Guide

## Getting Started

### 1. Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd ET-hackathon

# Run setup script
python setup.py

# OR use Make (if available)
make setup
```

### 2. Configuration

Edit `.env` file with your settings:

```bash
# Critical settings to configure:
OPENAI_API_KEY=your-key-here          # If using OpenAI
LLM_PROVIDER=openai                    # or ollama for local
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5 # Local model, no key needed
```

### 3. Start Development

#### Option A: Using Make (Recommended on Linux/Mac)
```bash
# Start all services
make start

# Start backend
make dev-backend

# Start frontend (in another terminal)
make dev-frontend
```

#### Option B: Manual (Works on Windows)
```bash
# Start Docker services
docker-compose up -d

# Activate virtual environment
cd backend
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Start backend
uvicorn app.main:app --reload

# In another terminal, start frontend
cd frontend
npm start
```

---

## Project Structure Explained

```
ET-hackathon/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── api/               # API endpoints
│   │   │   └── routes/
│   │   │       ├── health.py  # Health checks
│   │   │       ├── documents.py # Document upload/manage
│   │   │       ├── query.py   # RAG query endpoint
│   │   │       └── graph.py   # Knowledge graph API
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings management
│   │   │   └── logging.py     # Logging setup
│   │   ├── rag/               # RAG engine
│   │   │   ├── embeddings.py  # BGE embeddings
│   │   │   ├── chunking.py    # Smart chunking
│   │   │   ├── retrieval.py   # Hybrid retrieval (TODO)
│   │   │   ├── reranking.py   # Cross-encoder (TODO)
│   │   │   └── generation.py  # LLM generation (TODO)
│   │   ├── ingestion/         # Document processing
│   │   │   ├── loader.py      # Multi-format loader (TODO)
│   │   │   ├── ocr.py         # OCR processing (TODO)
│   │   │   └── pid_parser.py  # P&ID CV parser (TODO)
│   │   ├── kg/                # Knowledge Graph
│   │   │   ├── ner.py         # Entity extraction (TODO)
│   │   │   ├── relations.py   # Relationship extraction (TODO)
│   │   │   └── neo4j_client.py # Neo4j operations (TODO)
│   │   ├── agents/            # Agentic AI
│   │   │   ├── router.py      # Strategy router (TODO)
│   │   │   ├── rca_agent.py   # RCA agent (TODO)
│   │   │   └── compliance_agent.py # Compliance (TODO)
│   │   └── models/            # Data models
│   │       └── schemas.py     # Pydantic schemas
│   ├── tests/                 # Tests
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
├── frontend/                  # React PWA (TODO)
├── data/                      # Local data storage
│   ├── faiss_index/          # FAISS vector store
│   ├── uploads/              # Uploaded documents
│   └── processed/            # Processed documents
├── docs/                      # Additional documentation
├── infra/                     # Infrastructure configs
├── docker-compose.yml         # Docker orchestration
├── .env                       # Environment configuration
└── README.md
```

---

## Development Workflow

### Phase 1: Core RAG (Current Priority)

**Goal**: Get basic document upload and query working

#### Tasks:
1. **Document Loading** (`app/ingestion/loader.py`)
   - [ ] PDF text extraction (PyMuPDF)
   - [ ] Basic chunking integration
   - [ ] Store in MinIO

2. **Embeddings** (`app/rag/embeddings.py`) ✅ DONE
   - [x] BGE model loading
   - [x] Single text embedding
   - [x] Batch embedding

3. **Vector Store** (`app/rag/vector_store.py`)
   - [ ] FAISS index creation
   - [ ] Add documents to FAISS
   - [ ] Search/retrieval

4. **Basic RAG Pipeline** (`app/rag/pipeline.py`)
   - [ ] Query → Embed → Retrieve → Generate
   - [ ] Citation tracking
   - [ ] Streaming response

5. **Test It**
   ```bash
   # Upload a test PDF
   curl -F "file=@test.pdf" http://localhost:8000/api/v1/documents/upload
   
   # Query it
   curl -X POST http://localhost:8000/api/v1/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the torque spec?", "stream": false}'
   ```

### Phase 2: Advanced RAG

1. **Hybrid Retrieval**
   - [ ] BM25 index
   - [ ] Reciprocal Rank Fusion
   
2. **Re-ranking**
   - [ ] Cross-encoder integration
   
3. **Query Enhancement**
   - [ ] Query rewriting
   - [ ] HyDE

### Phase 3: Knowledge Graph

1. **Entity Extraction**
   - [ ] NER with spaCy
   - [ ] Custom entity types
   
2. **Neo4j Integration**
   - [ ] Graph schema creation
   - [ ] Entity + relationship ingestion

### Phase 4: Agents

1. **RCA Agent**
2. **Compliance Agent**
3. **Router Agent**

---

## Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test detailed health
curl http://localhost:8000/api/v1/health/detailed

# View API docs
open http://localhost:8000/docs
```

### Automated Testing

```bash
# Run backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_embeddings.py
```

---

## Common Commands

```bash
# View Docker logs
docker-compose logs -f

# Restart a service
docker-compose restart neo4j

# Reset everything
docker-compose down -v
docker-compose up -d

# Check service status
docker-compose ps

# Access Neo4j browser
open http://localhost:7474

# Access MinIO console
open http://localhost:9001
```

---

## Troubleshooting

### Issue: Backend won't start

**Check:**
1. Is virtual environment activated?
2. Are dependencies installed? `pip install -r requirements.txt`
3. Is .env file present?
4. Are Docker services running? `docker-compose ps`

### Issue: Docker services failing

**Try:**
```bash
docker-compose down -v
docker-compose up -d
docker-compose logs -f
```

### Issue: Out of memory

**Fix:**
1. Increase Docker memory limit (Docker Desktop settings)
2. Use smaller embedding models
3. Reduce batch sizes in config

### Issue: Model download fails

**Fix:**
```python
# Manually download in Python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
```

---

## Code Style

### Python (Backend)

```bash
# Format with black
black app/

# Lint with flake8
flake8 app/

# Type check with mypy
mypy app/
```

**Guidelines:**
- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions small and focused

### TypeScript/JavaScript (Frontend)

```bash
# Format with prettier
npm run format

# Lint with ESLint
npm run lint
```

---

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/document-loader

# Make changes and commit
git add .
git commit -m "feat: add PDF document loader"

# Push and create PR
git push origin feature/document-loader
```

**Commit Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

---

## Performance Optimization

### Embedding Generation
- Use batch embedding for multiple texts
- Cache embeddings when possible
- Consider quantization for production

### Vector Search
- Use IVFFlat or HNSW for large datasets
- Tune nprobe parameter for speed/accuracy tradeoff
- Implement pagination for search results

### LLM Generation
- Use streaming for better UX
- Implement caching for common queries
- Consider local models for cost reduction

---

## Deployment (Post-Hackathon)

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes (Future)

```bash
kubectl apply -f infra/k8s/
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangChain Docs**: https://python.langchain.com/
- **Neo4j Docs**: https://neo4j.com/docs/
- **FAISS Wiki**: https://github.com/facebookresearch/faiss/wiki
- **BGE Models**: https://huggingface.co/BAAI/bge-small-en-v1.5

---

## Getting Help

1. Check this guide first
2. Review relevant documentation
3. Check error logs: `docker-compose logs -f`
4. Ask the team
5. Create an issue with:
   - Error message
   - Steps to reproduce
   - Environment details

---

**Happy Coding! 🚀**
