# SKILLS.md — Skills & Knowledge Required

## 1. AI / ML
- **RAG architecture** — chunking, embeddings, retrieval, generation
- **Embeddings** — sentence-transformers, BGE models, vector math
- **Vector search** — FAISS (IVF, HNSW, flat), similarity metrics
- **Hybrid search** — BM25, Reciprocal Rank Fusion
- **Re-ranking** — cross-encoders, relevance scoring
- **Query transformation** — HyDE, query expansion, multi-query
- **Prompt engineering** — system prompts, few-shot, structured output
- **Agentic AI** — tool use, planning, routing, ReAct pattern
- **Guardrails** — groundedness, hallucination detection, confidence calibration
- **Evaluation** — RAGAS metrics (faithfulness, context precision/recall, answer relevance)

## 2. NLP / Document Intelligence
- **NER** — spaCy, custom entity models, LLM-based extraction
- **Relationship extraction** — triplet extraction
- **OCR** — Tesseract, PaddleOCR, layout analysis
- **Document parsing** — PyMuPDF, pdfplumber, unstructured.io
- **Entity resolution** — fuzzy matching, deduplication, ontology alignment

## 3. Computer Vision
- **Object detection** — YOLOv8 (P&ID symbols)
- **OpenCV** — image preprocessing, line/connection detection
- **Vision LLMs** — GPT-4V/Gemini for diagram understanding

## 4. Knowledge Graphs
- **Graph databases** — Neo4j, Cypher query language
- **Ontology engineering** — industrial domain modeling (ISA-95, equipment taxonomies)
- **Graph algorithms** — pathfinding, centrality, pattern matching

## 5. Backend Engineering
- **Python** — async/await, FastAPI
- **APIs** — REST, Server-Sent Events (streaming)
- **Task queues** — Celery / RQ
- **Databases** — PostgreSQL, Redis
- **Object storage** — MinIO / S3

## 6. Frontend Engineering
- **React** + state management
- **Tailwind CSS** — responsive, mobile-first
- **PWA** — service workers, offline, installable
- **SSE client** — streaming UI
- **Graph viz** — Cytoscape.js / D3.js
- **Web Speech API** — voice input

## 7. DevOps
- **Docker** + Docker Compose
- **Kubernetes** (scale path)
- **Local LLM serving** — Ollama, vLLM
- **CI/CD** — GitHub Actions

## 8. Domain Knowledge (Industrial)
- **P&IDs** — reading piping & instrumentation diagrams, tag conventions (ISA-5.1)
- **Maintenance** — CMMS, work orders, RCA (5-Why, Fishbone, FMEA)
- **Compliance** — Factory Act, OISD, PESO, environmental norms
- **Reliability** — predictive maintenance, failure modes, MTBF

## Team Role Mapping (suggested 4–5 people)
| Role | Owns |
|------|------|
| ML/RAG Engineer | EPIC 2, 4, 8 |
| Backend Engineer | EPIC 0, 1, 7 |
| Knowledge/Graph Engineer | EPIC 3, parts of 5 |
| Agent/AI Engineer | EPIC 5 |
| Frontend Engineer | EPIC 6 |