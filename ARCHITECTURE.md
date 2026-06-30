# Architecture — Industrial Knowledge Intelligence Platform

## High-Level Architecture (Layered)

┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER (Multi-device)                   │
│  Mobile PWA (Field Tech) │ Web Dashboard │ Voice Input │ API     │
└───────────────────────────────┬─────────────────────────────────┘
                                 │ HTTPS / SSE (streaming)
┌───────────────────────────────▼─────────────────────────────────┐
│                      API GATEWAY (FastAPI)                        │
│   Auth (JWT/RBAC) │ Rate Limit │ Routing │ SSE Stream Handler    │
└───────────────────────────────┬─────────────────────────────────┘
                                 │
┌───────────────────────────────▼─────────────────────────────────┐
│                    AGENTIC ORCHESTRATION LAYER                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Router Agent (Agentic RAG — picks strategy per query)      │ │
│  └────────────────────────────────────────────────────────────┘ │
│   ┌───────────┬───────────┬────────────┬─────────────┬────────┐ │
│   │ Copilot   │ RCA /     │ Compliance │ Lessons     │ Graph  │ │
│   │ Agent     │ Maint.    │ Agent      │ Learned     │ QA     │ │
│   │           │ Agent     │            │ Agent       │ Agent  │ │
│   └───────────┴───────────┴────────────┴─────────────┴────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                 │
┌───────────────────────────────▼─────────────────────────────────┐
│                  ADVANCED RAG ENGINE                              │
│  Query Rewriting + HyDE → Hybrid Retrieval (Vector+BM25+RRF)     │
│  → Multi-Vector (raw+summary) → Cross-Encoder Re-rank            │
│  → Context Compression → LLM Generation → Guardrails             │
│  → RAGAS Eval (offline) → Conversation Memory                    │
└──────────┬──────────────────────────────┬────────────────────────┘
           │                              │
┌──────────▼──────────┐        ┌──────────▼───────────────────────┐
│   RETRIEVAL STORES   │        │       KNOWLEDGE GRAPH            │
│  FAISS (vectors)     │◄──────►│  Neo4j (entities + relations    │
│  BM25 index          │        │  + provenance to source docs)   │
│  Doc/Chunk metadata  │        └──────────────────────────────────┘
└──────────┬───────────┘
           │
┌──────────▼───────────────────────────────────────────────────────┐
│                 INGESTION & PROCESSING PIPELINE                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │
│  │ Loader   │→│ OCR /    │→│ P&ID CV  │→│ Smart    │→│ Embed  │  │
│  │ (multi-  │ │ Doc      │ │ Parser   │ │ Chunking │ │ (BGE)  │  │
│  │ format)  │ │ Intel.   │ │          │ │          │ │        │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └────────┘  │
│       │                                                            │
│       ▼  NER + Relation Extraction → Entity Resolution → Graph    │
└───────────────────────────────────────────────────────────────────┘
           │
┌──────────▼───────────────────────────────────────────────────────┐
│                       STORAGE LAYER                                │
│  Object Store (MinIO/S3 - raw docs) │ PostgreSQL (metadata,       │
│  users, audit) │ FAISS files │ Neo4j │ Redis (cache, sessions)    │
└───────────────────────────────────────────────────────────────────┘


## Component Detail

### A. Ingestion Pipeline
| Stage | Tech | Output |
|-------|------|--------|
| Loader | unstructured.io, PyMuPDF, openpyxl, mail-parser | Raw text + layout |
| OCR | PaddleOCR / Tesseract | Text from scans |
| P&ID CV | YOLOv8 (symbol detect) + OpenCV + Vision LLM | Tags, symbols, connections |
| Table extraction | Camelot / pdfplumber | Structured tables |
| Smart Chunking | LangChain Recursive + Semantic + Context-aware | Chunks w/ metadata |
| Embedding | BAAI/bge-small-en-v1.5 (local, ~130MB) | 384-dim vectors |
| Multi-Vector | LLM summary per chunk → embed both | raw + summary vectors |

### B. Knowledge Graph Schema (Neo4j)

(:Equipment {tag, type, location, criticality})
(:Document {id, type, title, page, source_path})
(:FailureMode {name, description})
(:Regulation {code, body, clause})
(:Procedure {id, title, revision})
(:Person {name, role})
(:Parameter {name, value, unit})
(:Incident {id, date, severity})

Relationships:
(Equipment)-[:HAS_FAILURE]->(FailureMode)
(Equipment)-[:DOCUMENTED_IN]->(Document)
(Equipment)-[:GOVERNED_BY]->(Regulation)
(Procedure)-[:SATISFIES]->(Regulation)
(Incident)-[:INVOLVES]->(Equipment)
(Document)-[:MENTIONS]->(Person)
(FailureMode)-[:CAUSED_BY]->(Parameter)


### C. Advanced RAG Flow (Agentic)
1. **Query In** → Router Agent classifies intent (lookup / RCA / compliance / pattern)
2. **Query Rewriting** → expansion + HyDE hypothetical doc
3. **Hybrid Retrieval** → FAISS top-k ∪ BM25 top-k → RRF fusion
4. **Multi-Vector** → search raw + summary embeddings
5. **Graph Augmentation** → pull connected entities from Neo4j
6. **Cross-Encoder Re-rank** → ms-marco-MiniLM-L-6-v2
7. **Context Compression** → LLM extract relevant spans, dedupe
8. **Generation** → LLM with cited context (streamed via SSE)
9. **Guardrails** → groundedness check, hallucination detect, confidence
10. **Memory** → store turn in session history
11. **RAGAS** → offline eval (faithfulness, relevance, context precision)

### D. Tech Stack Summary
| Layer | Technology |
|-------|-----------|
| Frontend | React + Tailwind (PWA), SSE client, voice (Web Speech API) |
| Backend | FastAPI (Python), async, SSE |
| LLM | OpenAI / Llama-3 / Mistral (configurable; local option) |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Re-ranker | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Vector DB | FAISS |
| Keyword | rank-bm25 |
| Graph DB | Neo4j |
| OCR | PaddleOCR / Tesseract |
| CV | YOLOv8, OpenCV |
| Relational | PostgreSQL |
| Cache/Session | Redis |
| Object Store | MinIO / S3 |
| Eval | RAGAS |
| Orchestration | LangChain / LlamaIndex + custom agents |
| Deploy | Docker Compose / Kubernetes |

## Data Sovereignty Note
All embedding + retrieval + graph can run **fully on-prem** with local models
(BGE, FAISS, Neo4j, Llama-3 via Ollama) — critical for industrial clients who
cannot send data to cloud APIs.