# TODOLIST.md — Phased Build Plan

## 🏁 PHASE 0 — Setup (Day 1)
- [ ] Initialize repo + folder structure
- [ ] docker-compose: Postgres, Neo4j, Redis, MinIO
- [ ] FastAPI skeleton + health endpoint
- [ ] Download models: bge-small-en-v1.5, ms-marco-MiniLM-L-6-v2
- [ ] Configure LLM (cloud key OR Ollama local)
- [ ] Collect sample dataset (synthetic P&IDs, work orders, SOPs, incidents)

## 🔧 PHASE 1 — Core Ingestion + Basic RAG (Day 2–3)
- [ ] Multi-format loader (start: PDF + XLSX)
- [ ] Smart chunking (recursive first, add semantic)
- [ ] BGE embeddings + FAISS index + persistence
- [ ] BM25 index
- [ ] Basic /query endpoint (vector only) — PROVE IT WORKS
- [ ] Simple chat UI to test

## 🚀 PHASE 2 — Advanced RAG (Day 4–5)
- [ ] Hybrid retrieval (Vector + BM25 + RRF)
- [ ] Query rewriting + HyDE
- [ ] Cross-encoder re-ranking
- [ ] Context compression
- [ ] Citations + confidence scoring
- [ ] SSE streaming
- [ ] Conversation memory
- [ ] Guardrails (groundedness + hallucination flag)

## 🧠 PHASE 3 — Knowledge Graph (Day 6–7)
- [ ] NER extraction (equipment tags, params, regs, dates, persons)
- [ ] Relationship extraction → Neo4j
- [ ] Entity resolution/dedup
- [ ] Provenance links to source docs
- [ ] Graph-augmented retrieval
- [ ] Graph visualization UI

## 🖼️ PHASE 4 — Document Intelligence Plus (Day 8)
- [ ] OCR for scanned docs (PaddleOCR)
- [ ] P&ID CV parsing (YOLOv8 + Vision LLM)
- [ ] Email ingestion
- [ ] Table extraction
- [ ] Auto re-index on new doc

## 🤖 PHASE 5 — Agentic Features (Day 9–10)
- [ ] Router Agent (Agentic RAG strategy selection)
- [ ] Maintenance & RCA Agent
- [ ] Compliance Agent + evidence pack export
- [ ] Lessons Learned pattern engine
- [ ] Multi-vector retrieval

## 📱 PHASE 6 — UX Polish + Mobile (Day 11)
- [ ] PWA (installable, offline shell)
- [ ] Voice input
- [ ] Mobile-first responsive
- [ ] Confidence badges, citation cards
- [ ] Dashboards (compliance, lessons learned)

## 🔐 PHASE 7 — Security + RBAC (Day 12)
- [ ] JWT auth + roles
- [ ] Audit logging
- [ ] Local-only data path demonstration

## 📊 PHASE 8 — Eval + Deliverables (Day 13–14)
- [ ] RAGAS evaluation report
- [ ] Entity extraction accuracy report
- [ ] Time-to-answer benchmark vs search
- [ ] Compliance gap detection accuracy
- [ ] Architecture diagram (visual)
- [ ] Presentation deck
- [ ] Demo video (3 personas: technician, engineer, compliance)

## 🎯 HACKATHON PRIORITY (if short on time — MVP core)
1. Ingestion (PDF + XLSX) ✅ MUST
2. Advanced RAG with citations + streaming ✅ MUST
3. Knowledge Graph (basic) ✅ MUST (differentiator)
4. RCA Agent OR Compliance Agent (pick 1) ✅ MUST (business impact)
5. Mobile PWA + voice ✅ MUST (UX score)
6. P&ID CV parsing ⭐ WOW factor (innovation score)
7. RAGAS eval numbers ⭐ (technical excellence score)