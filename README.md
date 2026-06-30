# IKIP (Industrial Knowledge Intelligence Platform)

**AI-Powered Industrial Knowledge Management System**  
*Transform scattered industrial documents into unified, queryable intelligence*

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/Shxam/ET-hackathon)
[![Backend](https://img.shields.io/badge/Backend-Verified-green)](./BACKEND_VERIFICATION_REPORT.md)
[![License](https://img.shields.io/badge/License-MIT-blue)](./LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Our Solution](#our-solution)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

IKIP is an AI-powered platform that addresses critical knowledge management challenges in heavy industries. It combines advanced RAG (Retrieval-Augmented Generation), knowledge graphs, and agentic AI to transform how industrial workers access and utilize information.

### Key Capabilities

- 📚 **Multi-Format Document Ingestion** - PDF, Excel, Word, images, P&ID diagrams
- 🧠 **Knowledge Graph** - Understand relationships between equipment, failures, procedures
- 🤖 **Agentic AI** - Root cause analysis, compliance checking, proactive recommendations
- 📱 **Mobile-First** - PWA for field technicians with offline support
- 🔒 **Data Sovereignty** - Full on-premises deployment capability
- ⚡ **Real-Time Answers** - Sub-10-second response time with citations

---

## 🔥 The Problem

### Industrial Knowledge Fragmentation

- **35% of time wasted** searching for information across scattered documents
- **18-22% unplanned downtime** due to fragmented knowledge
- **Safety risks** from outdated or hard-to-find procedures
- **Knowledge loss** when experienced engineers retire
- **Compliance challenges** with regulations like OISD, API standards

### Current Pain Points

```
❌ Documents scattered across: SharePoint, email, file servers, paper
❌ No unified search across different formats
❌ Critical P&ID diagrams trapped in PDFs
❌ Tribal knowledge not documented
❌ Compliance gaps discovered only during audits
❌ Mobile access limited or non-existent
```

---

## ✨ Our Solution

### Unified Intelligent Interface


```
✅ Single search bar for all industrial knowledge
✅ Natural language queries: "What's the torque spec for P-101?"
✅ Automatic equipment relationship mapping
✅ Proactive failure prediction and recommendations
✅ Compliance gap detection with evidence packages
✅ Mobile-optimized for field use
```

### How It Works

1. **Ingest** - Upload any document type (PDF, Excel, Word, images, P&IDs)
2. **Process** - Extract text, recognize entities, build knowledge graph
3. **Index** - Create vector embeddings for semantic search
4. **Query** - Ask questions in natural language
5. **Answer** - Get cited responses with confidence scores in < 10 seconds
6. **Analyze** - Run root cause analysis or compliance checks on demand

---

## 🏗️ Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────┐
│          Client Layer (PWA / Mobile / API)           │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS / Server-Sent Events
┌──────────────────▼──────────────────────────────────┐
│               API Gateway (FastAPI)                  │
│    Authentication │ Rate Limiting │ Routing          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│          Agentic Orchestration Layer                 │
│  ┌──────────────────────────────────────────────┐   │
│  │  Router Agent (Strategy Selection)            │   │
│  └──────────────────────────────────────────────┘   │
│  ┌─────────┬─────────┬──────────┬──────────────┐   │
│  │ Copilot │   RCA   │Compliance│ Lessons Agent│   │
│  │  Agent  │  Agent  │  Agent   │              │   │
│  └─────────┴─────────┴──────────┴──────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              Advanced RAG Engine                     │
│  Query Enhancement → Hybrid Retrieval →             │
│  Re-ranking → Context Compression → LLM Generation  │
│  → Guardrails → Response Streaming                  │
└──────┬────────────────────────┬────────────────────┘
       │                        │
┌──────▼─────────┐     ┌────────▼───────────────────┐
│ Vector Store    │◄───►│   Knowledge Graph         │
│ (FAISS + BM25)  │     │   (Neo4j)                 │
└──────┬──────────┘     └───────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────┐
│         Ingestion & Processing Pipeline              │
│ Document Loader → OCR → P&ID Parser → Chunking →    │
│ Embeddings → NER → Entity Resolution → Graph Build  │
└──────┬──────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────┐
│              Storage Layer                           │
│  MinIO/S3 │ PostgreSQL │ Redis │ FAISS │ Neo4j     │
└─────────────────────────────────────────────────────┘
```

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Server** | FastAPI | REST API with async support |
| **LLM** | Groq (llama3-70b) / OpenAI | Text generation |
| **Embeddings** | BGE-small-en-v1.5 | Semantic vector search |
| **Vector DB** | FAISS | Fast similarity search |
| **Keyword Search** | BM25 | Traditional keyword retrieval |
| **Graph DB** | Neo4j | Entity relationships |
| **Object Storage** | MinIO | Document storage |
| **Cache** | Redis | Session & query cache |
| **Database** | PostgreSQL | Metadata & users |
| **OCR** | PaddleOCR | Text extraction from images |

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- Python 3.11 or higher
- 8GB+ RAM (16GB recommended)
- Groq API key (free at https://console.groq.com) OR OpenAI API key

### Installation (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/Shxam/ET-hackathon.git
cd ET-hackathon

# 2. Configure environment
copy .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. Start services
docker-compose up -d

# 4. Install Python dependencies
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# OR: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# 5. Start backend
python app/main.py
```

### Verify Installation

```bash
# Check health
curl http://localhost:8000/api/v1/health

# Access API docs
http://localhost:8000/docs

# Check services
docker-compose ps
```

### Quick Test

```bash
# Upload a document and query it
cd backend
python ../test_api.py path/to/your/document.pdf
```

---

## 🎯 Features

### ✅ Currently Available

- **Document Management**
  - Upload: PDF, DOCX, XLSX, TXT
  - Status tracking and metadata
  - Document deletion
  
- **Advanced RAG Pipeline**
  - Hybrid search (vector + keyword)
  - Smart chunking with context preservation
  - BM25 + FAISS with RRF fusion
  - Citation with confidence scores
  
- **Multi-Provider LLM Support**
  - Groq (fast & free)
  - OpenAI
  - Azure OpenAI
  - Ollama (local/on-prem)
  
- **Knowledge Graph (Basic)**
  - Entity extraction with spaCy
  - Neo4j integration
  - Graph visualization endpoints

- **Root Cause Analysis**
  - 5-Why analysis
  - Fishbone diagrams
  - Failure history correlation

### 🚧 In Development

- **Frontend UI** (React PWA)
- **Advanced Query Enhancement** (HyDE, multi-query)
- **Cross-Encoder Re-ranking**
- **P&ID Diagram Understanding** (Computer Vision)
- **Compliance Agent** (OISD, API standards)
- **Offline Mode** (Service Workers)
- **Voice Input** (Web Speech API)

---

## 💻 Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.14
- **LLM Orchestration**: LangChain 0.1+
- **Async Runtime**: Uvicorn with asyncio

### AI/ML
- **LLM**: Groq (llama3-70b-8192), OpenAI GPT-4
- **Embeddings**: BAAI/bge-small-en-v1.5 (384-dim)
- **Vector Search**: FAISS (IVFFlat, HNSW)
- **Keyword Search**: rank-bm25
- **Re-ranking**: sentence-transformers cross-encoder
- **NER**: spaCy (en_core_web_sm)
- **OCR**: PaddleOCR, Tesseract
- **CV**: YOLOv8 (planned), OpenCV

### Databases & Storage
- **Graph**: Neo4j 5.15+
- **Relational**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Object Store**: MinIO 7.2+ (S3-compatible)
- **Vector Index**: FAISS files

### Frontend (Planned)
- **Framework**: React 18+
- **Styling**: Tailwind CSS
- **State**: Context API
- **Build**: Vite
- **PWA**: Service Workers
- **Charts**: D3.js / Recharts for graph visualization

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (planned)
- **Monitoring**: Prometheus + Grafana (planned)
- **Logging**: Structured JSON logging

---

## 📁 Project Structure

```
ET-hackathon/
├── backend/                        # FastAPI backend
│   ├── app/
│   │   ├── main.py                # Application entry point
│   │   ├── core/
│   │   │   ├── config.py          # Configuration management
│   │   │   └── logging.py         # Logging setup
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py      # Health check endpoints
│   │   │       ├── documents.py   # Document management
│   │   │       ├── query.py       # RAG query endpoints
│   │   │       ├── graph.py       # Knowledge graph API
│   │   │       └── rca.py         # Root cause analysis
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic data models
│   │   ├── rag/
│   │   │   ├── embeddings.py      # BGE embedding service
│   │   │   ├── chunking.py        # Smart document chunking
│   │   │   ├── vector_store.py    # FAISS vector database
│   │   │   ├── bm25_search.py     # Keyword search
│   │   │   ├── llm_client.py      # Multi-provider LLM client
│   │   │   ├── pipeline.py        # RAG orchestration
│   │   │   ├── query_enhancement.py # Query rewriting
│   │   │   ├── reranking.py       # Cross-encoder reranking
│   │   │   ├── compression.py     # Context compression
│   │   │   └── guardrails.py      # Response validation
│   │   ├── kg/
│   │   │   ├── ner.py             # Named entity recognition
│   │   │   ├── relations.py       # Relationship extraction
│   │   │   ├── neo4j_client.py    # Neo4j operations
│   │   │   └── entity_resolution.py # Entity deduplication
│   │   ├── agents/
│   │   │   ├── rca_agent.py       # Root cause analysis agent
│   │   │   └── __init__.py
│   │   ├── ingestion/
│   │   │   └── loader.py          # Document ingestion
│   │   └── services/
│   │       └── session.py         # Session management
│   ├── tests/
│   │   └── test_api_comprehensive.py
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile
│   └── verify_and_start.ps1       # Setup verification script
│
├── frontend/                       # React PWA (in development)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── DocumentList.tsx
│   │   │   ├── GraphVisualization.tsx
│   │   │   └── RCADisplay.tsx
│   │   ├── api/
│   │   │   └── client.ts          # API client
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── data/                           # Data storage
│   ├── faiss_index/               # Vector store files
│   ├── uploads/                   # Raw documents
│   └── processed/                 # Processed chunks
│
├── test-documents/                 # Sample test documents
│   ├── equipment_maintenance_guide.txt
│   ├── incident_report.txt
│   └── safety_procedures.txt
│
├── docker-compose.yml              # Service orchestration
├── .env.example                    # Environment template
├── .gitignore
├── Makefile                        # Development commands
├── LICENSE
├── README.md                       # This file
├── BACKEND_VERIFICATION_REPORT.md  # Backend verification details
└── VERIFICATION_SUMMARY.md         # Quick verification summary
```

---

## 🛠️ Development

### Backend Development

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/

# Check code style
black app/
flake8 app/
```

### Frontend Development (When Ready)

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Key configuration in `.env`:

```bash
# LLM Provider
LLM_PROVIDER=groq  # groq | openai | azure | ollama
GROQ_API_KEY=your_key_here
LLM_MODEL=llama3-70b-8192

# Features
ENABLE_KNOWLEDGE_GRAPH=false  # Set to true after Neo4j setup
ENABLE_HYBRID_SEARCH=true
ENABLE_GUARDRAILS=true

# Service Endpoints
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password_change_me
```

### Docker Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart neo4j

# Stop all services
docker-compose down

# Clean volumes (removes all data!)
docker-compose down -v
```

---

## 📖 API Documentation

### Interactive Docs

Access Swagger UI: `http://localhost:8000/docs`  
Access ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Health Check
```http
GET /api/v1/health
```

#### Document Management
```http
POST   /api/v1/documents/upload      # Upload document
GET    /api/v1/documents              # List documents
GET    /api/v1/documents/{id}/status  # Get status
DELETE /api/v1/documents/{id}         # Delete document
```

#### Query (RAG)
```http
POST   /api/v1/query                  # Ask question
Body: {
  "question": "What is the torque specification for P-101?",
  "strategy": "hybrid",  # hybrid | vector | keyword
  "top_k": 5
}
```

#### Knowledge Graph
```http
GET    /api/v1/graph/stats            # Graph statistics
GET    /api/v1/graph/entities          # List entities
GET    /api/v1/graph/visualize         # Visualization data
```

#### Root Cause Analysis
```http
POST   /api/v1/rca/analyze            # Perform RCA
GET    /api/v1/rca/health             # RCA agent status
Body: {
  "failure_description": "P-101 pump seal leak at 100°C",
  "context": {...}
}
```

### Example Usage

```python
import requests

# Upload document
with open('manual.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/documents/upload',
        files={'file': f}
    )
doc_id = response.json()['document_id']

# Query
response = requests.post(
    'http://localhost:8000/api/v1/query',
    json={
        'question': 'What are the safety procedures for P-101?',
        'strategy': 'hybrid'
    }
)
answer = response.json()['answer']
citations = response.json()['citations']
```

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

### Manual API Testing

Use the provided test script:

```bash
python test_api.py path/to/document.pdf
```

Or use curl:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Upload document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.pdf"

# Query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is P-101?","strategy":"hybrid"}'
```

---

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up --scale backend=3
```

### Environment-Specific Configs

- `docker-compose.yml` - Development
- `docker-compose.prod.yml` - Production (to be created)

### Production Checklist

- [ ] Change all default passwords
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure HTTPS/TLS
- [ ] Enable rate limiting
- [ ] Set up monitoring (Prometheus)
- [ ] Configure log aggregation
- [ ] Set up automated backups
- [ ] Review security settings

---

## 🗺️ Roadmap

### Phase 1: MVP (Current) ✅
- [x] Core infrastructure setup
- [x] Document ingestion pipeline
- [x] RAG with hybrid search
- [x] Basic knowledge graph
- [x] API endpoints
- [x] Backend verification

### Phase 2: Advanced Features (In Progress)
- [ ] Frontend UI (React PWA)
- [ ] Advanced query enhancement
- [ ] Cross-encoder re-ranking
- [ ] Streaming responses (SSE)
- [ ] Session management
- [ ] Guardrails & validation

### Phase 3: Agentic AI (Upcoming)
- [ ] RCA agent refinement
- [ ] Compliance checking agent
- [ ] Router agent for strategy selection
- [ ] Lessons learned extraction
- [ ] Proactive recommendations

### Phase 4: Enterprise Features (Future)
- [ ] P&ID diagram understanding (CV)
- [ ] Multi-tenant support
- [ ] SSO integration
- [ ] Advanced RBAC
- [ ] Audit trail
- [ ] Custom model fine-tuning
- [ ] Offline mode (PWA)
- [ ] Voice input

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Python: Follow PEP 8, use Black formatter
- TypeScript/React: Follow Airbnb style guide
- Write tests for new features
- Update documentation

### Reporting Issues

Use GitHub Issues and include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs if applicable

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Resources

### Documentation
- **Backend Verification**: [BACKEND_VERIFICATION_REPORT.md](./BACKEND_VERIFICATION_REPORT.md)
- **Quick Summary**: [VERIFICATION_SUMMARY.md](./VERIFICATION_SUMMARY.md)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [LangChain Docs](https://python.langchain.com)
- [FAISS Guide](https://github.com/facebookresearch/faiss)
- [Neo4j Documentation](https://neo4j.com/docs)
- [Groq API](https://console.groq.com)

### Services Access (Local Development)
- **API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (neo4j/neo4j_password_change_me)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

---

## 🎯 Project Status

**Current Status**: Backend Complete & Verified ✅  
**Progress**: 40% of MVP Complete  
**Next Milestone**: Frontend UI Development

### What's Working
- ✅ Document upload and processing
- ✅ Hybrid retrieval (vector + keyword)
- ✅ RAG query with citations
- ✅ Knowledge graph extraction
- ✅ Root cause analysis
- ✅ Multi-provider LLM support

### In Progress
- 🚧 Frontend UI (React PWA)
- 🚧 Advanced query enhancement
- 🚧 Streaming responses

For detailed progress, see [BACKEND_VERIFICATION_REPORT.md](./BACKEND_VERIFICATION_REPORT.md)

---

## ⭐ Acknowledgments

- **FastAPI** team for the excellent framework
- **LangChain** community for RAG components
- **Facebook Research** for FAISS
- **Groq** for fast, free LLM inference
- **Neo4j** for graph database technology

---

## 📊 Metrics & Performance

### Target Performance
- Query response time: < 10 seconds
- Document processing: < 30 seconds per document
- Concurrent users: 100+
- Knowledge graph: 100,000+ entities

### Current Benchmarks
- Health check: < 100ms
- Simple query: ~3-5 seconds
- Document upload: ~5-10 seconds

---

**Built with ❤️ for the Industrial AI Hackathon**

*Making industrial knowledge accessible, intelligent, and actionable*

---

_Last Updated: June 30, 2026_
