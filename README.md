# IKIP - Industrial Knowledge Intelligence Platform
## Codename: "Pragya" (Sanskrit: wisdom/intelligence)

> AI-powered industrial knowledge intelligence platform that turns scattered documents into actionable intelligence for asset-intensive industries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Problem We Solve

Industrial professionals waste **35% of working hours** searching for information across 7-12 disconnected systems, causing:
- 18-22% unplanned downtime due to fragmented equipment context
- Safety & compliance risks from outdated procedures
- Knowledge loss as experienced engineers retire

**IKIP** provides a single, intelligent query interface powered by advanced RAG, knowledge graphs, and agentic AI.

---

## 🚀 Key Features

### Core Capabilities
- **🔍 Universal Document Intelligence** — PDF, P&IDs, scanned forms, XLSX, emails
- **🧠 Advanced RAG Engine** — Hybrid retrieval (Vector+BM25), cross-encoder re-ranking, query rewriting, HyDE
- **🕸️ Knowledge Graph** — Unified entity relationships across all document types (Neo4j)
- **🤖 Agentic AI** — Maintenance RCA, compliance checking, lessons learned mining
- **📱 Mobile-First PWA** — Field technician ready with voice input, offline support
- **🔒 Data Sovereignty** — Runs 100% on-premises with local models

### Technical Highlights
- **Multi-Vector Retrieval** — Raw + summary embeddings for better context
- **Context Compression** — LLM-powered relevance extraction
- **Guardrails** — Groundedness checks, hallucination detection, confidence scoring
- **SSE Streaming** — Real-time response generation
- **RAGAS Evaluation** — Automated quality metrics (faithfulness, relevance, precision)

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────┐
│  Frontend (React PWA) + Voice Input + Mobile    │
└─────────────────┬───────────────────────────────┘
                  │ HTTPS / SSE
┌─────────────────▼───────────────────────────────┐
│  FastAPI Gateway (Auth, Rate Limit, Routing)    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Agentic Orchestration Layer                    │
│  ┌──────────────────────────────────────────┐   │
│  │ Router Agent (Strategy Selection)        │   │
│  └──────────────────────────────────────────┘   │
│  ┌─────┬──────┬────────┬──────────┬────────┐   │
│  │Copy │ RCA  │Compli  │Lessons   │Graph   │   │
│  │Pilot│Agent │ance    │Learned   │QA      │   │
│  └─────┴──────┴────────┴──────────┴────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Advanced RAG Engine                            │
│  Query Rewriting → Hybrid Retrieval (V+BM25)    │
│  → Multi-Vector → Re-rank → Compression →       │
│  Generation → Guardrails → RAGAS                │
└────┬─────────────────────────┬──────────────────┘
     │                         │
┌────▼────────┐      ┌─────────▼────────────────┐
│ FAISS       │◄────►│ Neo4j Knowledge Graph    │
│ BM25        │      │ (Entities + Relations)   │
└────┬────────┘      └──────────────────────────┘
     │
┌────▼─────────────────────────────────────────────┐
│ Ingestion Pipeline                               │
│ Loader → OCR → P&ID CV → Chunking → Embedding   │
│ → NER → Relation Extraction → Graph Ingestion   │
└──────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Python 3.11+ |
| **Frontend** | React 18 + TypeScript, Vite, Tailwind CSS |
| **LLM** | OpenAI GPT-4 / Llama-3 / Mistral (configurable) |
| **Embeddings** | BAAI/bge-small-en-v1.5 (local) |
| **Re-ranker** | ms-marco-MiniLM-L-6-v2 |
| **Vector DB** | FAISS |
| **Graph DB** | Neo4j |
| **Keyword Search** | BM25 |
| **OCR** | PaddleOCR / Tesseract |
| **CV** | YOLOv8, OpenCV |
| **Database** | PostgreSQL, Redis |
| **Storage** | MinIO / S3 |
| **Evaluation** | RAGAS |

---

## 🚦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- 8GB RAM minimum (16GB recommended)

### 1. Clone Repository
```bash
git clone <repository-url>
cd ET-hackathon
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Start Services
```bash
# Start all services (Postgres, Neo4j, Redis, MinIO)
docker-compose up -d

# Wait for services to be healthy
docker-compose ps
```

### 4. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run migrations (when available)
# alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### 5. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

### 6. Access Services
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (neo4j / neo4j_password_change_me)
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin)

---

## 📚 Documentation

- [Product Requirements Document](./PRD.md)
- [Architecture Details](./ARCHITECTURE.md)
- [Task Breakdown](./TASKS.md)
- [Skills Required](./SKILLS.md)
- [Development Roadmap](./todo.md)

---

## 🔧 Development

### Project Structure
```
ET-hackathon/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration, logging
│   │   ├── rag/         # RAG engine components
│   │   ├── ingestion/   # Document processing
│   │   ├── kg/          # Knowledge graph
│   │   ├── agents/      # Agentic AI modules
│   │   └── models/      # Data models
│   ├── tests/           # Backend tests
│   └── requirements.txt
├── frontend/            # React PWA
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── data/                # Local data storage
├── docs/                # Additional documentation
├── infra/               # Infrastructure as code
└── docker-compose.yml
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend
black backend/
flake8 backend/
mypy backend/

# Frontend
npm run lint
npm run format
```

---

## 📊 Evaluation Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Time-to-answer | < 10s | TBD |
| Entity extraction F1 | > 90% | TBD |
| RAGAS Faithfulness | > 0.85 | TBD |
| Knowledge graph completeness | > 80% | TBD |
| Hallucination rate | < 3% | TBD |

---

## 🎯 Hackathon Priorities

### MUST HAVE (MVP Core)
1. ✅ Document ingestion (PDF + XLSX)
2. ✅ Advanced RAG with citations + streaming
3. ✅ Knowledge Graph (basic)
4. ⏳ RCA Agent OR Compliance Agent
5. ⏳ Mobile PWA + voice input

### WOW FACTORS
6. ⏳ P&ID CV parsing
7. ⏳ RAGAS evaluation numbers
8. ⏳ Multi-vector retrieval
9. ⏳ Graph visualization

---

## 🤝 Contributing

This is a hackathon project. For contributions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👥 Team

Built with ❤️ for the ET Hackathon 2026

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- Beijing Academy of Artificial Intelligence for BGE embeddings
- Neo4j for graph database
- LangChain community
- All open-source contributors

---

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Contact the team

---

**Status**: 🚧 Active Development
**Last Updated**: June 26, 2026
#   E T - h a c k a t h o n  
 