# Product Requirements Document (PRD)
## Industrial Knowledge Intelligence Platform (IKIP)
**Codename:** "Pragya" (Sanskrit: wisdom/intelligence)

**Version:** 1.0
**Status:** Draft for Hackathon Build

---

## 1. Problem Statement

Industrial professionals in asset-intensive industries waste **35% of working hours**
searching for, clarifying, or recreating information that already exists. Indian heavy
industry plants operate **7–12 disconnected document systems**, causing:

- **18–22% of unplanned downtime** due to fragmented equipment context
- **Safety & compliance risks** from outdated/scattered procedures
- **The knowledge cliff:** 25% of experienced engineers retire within a decade,
  taking undocumented tribal knowledge with them

This is NOT a file-management problem. It is a **safety, quality, and operational
efficiency problem** that compounds over time.

---

## 2. Vision

> Build an AI platform that turns scattered industrial documents into a single,
> living, queryable intelligence layer — preserving institutional knowledge and
> making it actionable at the point of need, on any device.

---

## 3. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| Reduce time-to-answer | vs. traditional search | < 10s (10x faster) |
| Entity extraction accuracy | F1 across doc types | > 90% |
| Answer quality | RAGAS faithfulness | > 0.85 |
| Knowledge graph linkage | relationship completeness | > 80% |
| Compliance gap detection | precision/recall | > 85% |
| Hallucination rate | guardrail flagged | < 3% |
| Field usability | mobile task completion | > 90% |

---

## 4. Target Users (Personas)

### P1 — Field Technician ("Ravi")
- On the plant floor with a phone/tablet
- Needs: "What's the torque spec for Pump P-101 seal? Any recent failures?"
- Pain: Can't carry binders; OEM manual is in an office cabinet
- Requirement: Mobile-first, voice query, offline-tolerant, instant citations

### P2 — Maintenance Engineer ("Priya")
- Plans schedules, does RCA after failures
- Needs: Failure history + OEM data + inspection trends fused together
- Requirement: RCA copilot, predictive recommendations, cross-doc linkage

### P3 — Compliance / Safety Officer ("Anand")
- Prepares for OISD/PESO/Factory Act audits
- Needs: Map regulations → current procedures → evidence
- Requirement: Auto compliance evidence packages, gap flags

### P4 — Plant Manager ("Meera")
- Wants operational visibility & risk reduction
- Needs: Dashboards, systemic failure patterns, knowledge-loss risk
- Requirement: Lessons-learned engine, trend dashboards

---

## 5. Scope

### In-Scope (MVP / Hackathon)
1. **Universal Document Ingestion** — PDF, P&ID images, scanned forms, XLSX, email
2. **Entity Extraction** — equipment tags, parameters, regulations, personnel, dates
3. **Knowledge Graph** — unified relationships across doc types
4. **Expert Copilot (RAG)** — conversational, cited, confidence-scored, mobile
5. **Maintenance Intelligence & RCA Agent**
6. **Compliance Intelligence** — gap detection + evidence packages
7. **Lessons Learned Engine** — pattern mining across incidents

### Advanced RAG Stack (from your component list — ALL integrated)
Smart Chunking, BGE Embeddings, FAISS, Hybrid Retrieval (Vector+BM25+RRF),
Query Rewriting/HyDE, Multi-Vector Retrieval, Cross-Encoder Re-ranking,
Context Compression, RAGAS Eval, Conversation Memory, Guardrails,
SSE Streaming, Agentic RAG (strategy selection).

### Out-of-Scope (Post-Hackathon)
- Real-time IoT/SCADA streaming integration (mock/simulated only for demo)
- Full ERP/CMMS write-back
- Multi-tenant billing
- Native mobile apps (responsive PWA instead)

---

## 6. Functional Requirements

### FR-1: Document Ingestion
- FR-1.1 Accept PDF, PNG/JPG (scanned/P&ID), XLSX/CSV, EML/MSG, DOCX
- FR-1.2 OCR scanned documents (Tesseract / PaddleOCR)
- FR-1.3 P&ID symbol & tag detection (CV pipeline)
- FR-1.4 Extract tables from spreadsheets & PDFs
- FR-1.5 Parse email headers, bodies, attachments
- FR-1.6 Auto-trigger re-indexing on new document arrival

### FR-2: Knowledge Extraction & Graph
- FR-2.1 NER for: EquipmentTag, ProcessParameter, Regulation, Person, Date, Document, FailureMode
- FR-2.2 Relationship extraction (e.g., Pump-101 → HAS_FAILURE → Seal Leak)
- FR-2.3 Store in graph DB (Neo4j) with provenance to source doc/page
- FR-2.4 Entity resolution / deduplication (P-101 = Pump 101 = P101)

### FR-3: Expert Copilot
- FR-3.1 Natural language Q&A with streaming responses (SSE)
- FR-3.2 Every answer cites source doc + page + confidence score
- FR-3.3 Conversation memory within session
- FR-3.4 Agentic strategy selection (vector vs hybrid vs graph vs RCA)
- FR-3.5 Guardrails: groundedness, hallucination flag, "I don't know" fallback

### FR-4: Maintenance & RCA Agent
- FR-4.1 Fuse work orders + failure records + OEM + inspections
- FR-4.2 Generate RCA (5-Why / Fishbone scaffolding) with evidence
- FR-4.3 Predictive maintenance recommendations
- FR-4.4 Optimized schedule suggestions

### FR-5: Compliance Intelligence
- FR-5.1 Regulation library (Factory Act, OISD, PESO, env norms)
- FR-5.2 Map requirements → procedures/records → gap detection
- FR-5.3 Auto-generate audit evidence package (PDF export)

### FR-6: Lessons Learned Engine
- FR-6.1 Mine incidents/near-miss/NCRs for systemic patterns
- FR-6.2 Proactive warning push to relevant teams/assets

---

## 7. Non-Functional Requirements
- **Performance:** < 10s P95 answer latency
- **Security:** Role-based access, audit logs, on-prem/local option (data sovereignty)
- **Cost:** Free/local models where possible (BGE, FAISS, open LLMs)
- **Availability:** 99.5% (post-hackathon)
- **Privacy:** No industrial data leaves premises (local embedding/inference path)

---

## 8. Assumptions & Risks
| Risk | Mitigation |
|------|------------|
| Poor OCR on old scans | Multi-engine OCR + human-in-loop verification |
| P&ID parsing accuracy | Hybrid CV + LLM vision; allow manual tag tagging |
| LLM hallucination | Guardrails + mandatory citations + confidence gating |
| Entity resolution errors | Fuzzy matching + ontology rules + review queue |
| Sparse real data | Use synthetic + public industrial datasets for demo |

---

## 9. Deliverables (Hackathon)
1. Working Prototype (web app + mobile-responsive PWA)
2. Architecture Diagram
3. Presentation Deck
4. Demo Video