# TASK.md — Engineering Task Breakdown

## EPIC 0: Foundation & Setup
- [ ] T0.1 Repo + monorepo structure (backend/, frontend/, infra/, docs/)
- [ ] T0.2 Docker Compose (Postgres, Neo4j, Redis, MinIO, app)
- [ ] T0.3 Environment config (.env, model selection toggle local/cloud)
- [ ] T0.4 CI lint/test pipeline
- [ ] T0.5 Base FastAPI app + health checks + logging

## EPIC 1: Document Ingestion Pipeline
- [ ] T1.1 Multi-format loader (PDF, XLSX, EML, DOCX, images)
- [ ] T1.2 OCR module (PaddleOCR) with quality scoring
- [ ] T1.3 Table extraction (pdfplumber/Camelot)
- [ ] T1.4 Email parser (headers, body, attachments recursion)
- [ ] T1.5 P&ID CV parser (YOLOv8 symbol detect + Vision LLM tags)
- [ ] T1.6 Upload API + async job queue (Celery/RQ)
- [ ] T1.7 File storage to MinIO + metadata to Postgres
- [ ] T1.8 Auto re-index trigger on new doc

## EPIC 2: Chunking & Embeddings
- [ ] T2.1 Smart Chunking (recursive + semantic + context-aware)
- [ ] T2.2 BGE embedding service (bge-small-en-v1.5)
- [ ] T2.3 Multi-vector: generate chunk summaries + embed
- [ ] T2.4 FAISS index build + persistence
- [ ] T2.5 BM25 index build
- [ ] T2.6 Metadata store linking chunk→doc→page

## EPIC 3: Knowledge Extraction & Graph
- [ ] T3.1 NER pipeline (equipment tags, params, regs, persons, dates, failures)
- [ ] T3.2 Relationship extraction (LLM + rules)
- [ ] T3.3 Entity resolution / dedup (fuzzy + ontology)
- [ ] T3.4 Neo4j schema + ingestion
- [ ] T3.5 Provenance linking (entity → source doc/page)
- [ ] T3.6 Graph query API (Cypher templates)

## EPIC 4: Advanced RAG Engine
- [ ] T4.1 Query Rewriting (expansion + reformulation + HyDE)
- [ ] T4.2 Hybrid Retrieval (Vector + BM25 + RRF)
- [ ] T4.3 Multi-Vector retrieval (raw + summary)
- [ ] T4.4 Graph-augmented retrieval
- [ ] T4.5 Cross-Encoder re-ranking
- [ ] T4.6 Context Compression (LLM extract + dedupe)
- [ ] T4.7 LLM generation with citations
- [ ] T4.8 SSE streaming endpoint
- [ ] T4.9 Conversation memory (Redis session + window mgmt)
- [ ] T4.10 Guardrails (groundedness, hallucination, confidence)
- [ ] T4.11 RAGAS evaluation harness

## EPIC 5: Agentic Layer
- [ ] T5.1 Router Agent (intent classification + strategy selection)
- [ ] T5.2 Copilot Agent
- [ ] T5.3 Maintenance & RCA Agent (fuse WO + failures + OEM + inspections)
- [ ] T5.4 Compliance Agent (reg mapping + gap detection + evidence pack)
- [ ] T5.5 Lessons Learned Agent (pattern mining + proactive push)
- [ ] T5.6 Tool registry (graph query, vector search, doc fetch)

## EPIC 6: Frontend
- [ ] T6.1 PWA scaffold (React + Tailwind, installable, offline shell)
- [ ] T6.2 Chat UI with streaming + citations + confidence badges
- [ ] T6.3 Voice input (Web Speech API)
- [ ] T6.4 Document upload + ingestion status UI
- [ ] T6.5 Knowledge graph visualization (Cytoscape/D3)
- [ ] T6.6 RCA workspace UI
- [ ] T6.7 Compliance dashboard + evidence export
- [ ] T6.8 Lessons-learned alerts feed
- [ ] T6.9 Mobile-first responsive layouts

## EPIC 7: Security & Ops
- [ ] T7.1 JWT auth + RBAC (technician/engineer/compliance/manager)
- [ ] T7.2 Audit logging
- [ ] T7.3 Rate limiting
- [ ] T7.4 Local model path (Ollama) toggle

## EPIC 8: Evaluation & Demo
- [ ] T8.1 Domain-expert benchmark Q&A set
- [ ] T8.2 Entity extraction accuracy eval
- [ ] T8.3 Time-to-answer benchmark vs keyword search
- [ ] T8.4 Compliance gap detection eval
- [ ] T8.5 Seed synthetic + public industrial dataset
- [ ] T8.6 Architecture diagram, deck, demo video