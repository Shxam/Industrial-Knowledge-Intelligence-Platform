# Complete Task List - IKIP (Pragya)

## 📊 Current Status: 75% Complete (Day 3 of 14)

**Last Updated**: June 27, 2026

---

## ✅ COMPLETED TASKS (75%)

### Phase 1: Foundation (Day 1) - DONE ✅
- [x] Project structure setup
- [x] Docker Compose configuration (Postgres, Neo4j, Redis, MinIO)
- [x] Environment configuration (.env)
- [x] FastAPI application skeleton
- [x] Configuration management (Pydantic Settings)
- [x] Logging system
- [x] API route structure
- [x] Pydantic schemas for all models
- [x] Development tools (Makefile, setup scripts)
- [x] 20+ documentation files

### Phase 2: Core RAG (Day 2) - DONE ✅
- [x] Document loader (PDF, XLSX, DOCX)
- [x] MinIO integration
- [x] Smart chunking (recursive, semantic, context-aware)
- [x] BGE embeddings integration
- [x] FAISS vector store (Flat, IVF, HNSW)
- [x] BM25 keyword search
- [x] Hybrid retrieval with RRF fusion
- [x] LLM client (OpenAI, Azure, Ollama)
- [x] Complete RAG pipeline
- [x] API endpoints (upload, status, query, delete)
- [x] Background processing

### Phase 3: Advanced RAG (Day 3) - DONE ✅
- [x] Query enhancement (rewriting, HyDE, decomposition, expansion)
- [x] Cross-encoder re-ranking
- [x] Context compression
- [x] Guardrails (groundedness, hallucination detection)
- [x] Session management with Redis
- [x] Conversation memory

### Phase 4: Knowledge Graph (Day 3) - DONE ✅
- [x] NER Pipeline (Industrial entities: EQUIPMENT, PARAMETER, MEASUREMENT, REGULATION, FAILURE_MODE, PERSON, DATE)
- [x] Relationship Extraction (8 relationship types: HAS_FAILURE, GOVERNED_BY, MEASURED_BY, OPERATES_AT, CAUSED_BY, DOCUMENTED_IN, INVOLVES, SATISFIES)
- [x] Neo4j Client (full CRUD operations, graph schema, pathfinding, visualization)
- [x] Entity Resolution (fuzzy matching, canonicalization, deduplication)
- [x] RAG-KG Integration (automatic entity extraction during ingestion)
- [x] Graph-Augmented Retrieval (context expansion using graph relationships)
- [x] Graph API Endpoints (entities, search, path, visualize, stats)
- [x] Neo4j Schema Initialization on startup

### Phase 5: AI Agents (Day 3) - DONE ✅
- [x] RCA Agent Implementation (700 lines)
  - [x] Entity extraction from failure descriptions
  - [x] Knowledge graph evidence collection
  - [x] Document retrieval integration
  - [x] 5-Why analysis (LLM-powered)
  - [x] Fishbone diagram generation (6 categories)
  - [x] Recommendation engine (prioritized, actionable)
  - [x] Confidence scoring
  - [x] Structured JSON output
- [x] RCA API Endpoints (/analyze, /example, /health)
- [x] RCA Data Models (Request, Response, Evidence)

---

## ⏳ REMAINING TASKS (25%)

### Phase 6: Frontend (Days 4-7) - HIGH PRIORITY �
- [ ] 4.3.4 Relationship ingestion functions
  - [ ] create_relationship(source, rel_type, target)
- [ ] 4.3.5 Provenance tracking (link to source documents)
- [ ] 4.3.6 Query functions:
  - [ ] get_entity_by_id(entity_id)
  - [ ] find_related_entities(entity_id, rel_type)
  - [ ] find_path(source, target)
- [ ] 4.3.7 Health check and connection management

**Dependencies**: Neo4j running in Docker
**Output**: Neo4j client with CRUD operations

#### Task 4.4: Entity Resolution
**File**: `backend/app/kg/entity_resolution.py`
**Priority**: MEDIUM
**Estimated Time**: 2 hours

- [ ] 4.4.1 Fuzzy string matching (P-101 = Pump 101 = P101)
- [ ] 4.4.2 Canonicalization rules
- [ ] 4.4.3 Deduplication logic
- [ ] 4.4.4 Merge similar entities
- [ ] 4.4.5 Conflict resolution

**Dependencies**: NER output
**Output**: Canonical entity identifiers

#### Task 4.5: Graph-Augmented Retrieval
**File**: Update `backend/app/rag/pipeline.py`
**Priority**: HIGH
**Estimated Time**: 2 hours

- [ ] 4.5.1 Extract entities from query
- [ ] 4.5.2 Query graph for related entities
- [ ] 4.5.3 Expand context with graph data
- [ ] 4.5.4 Rank by graph centrality/importance
- [ ] 4.5.5 Integrate with existing RAG pipeline
- [ ] 4.5.6 Add "graph" strategy to query endpoint

**Dependencies**: Neo4j client, NER
**Output**: Enhanced retrieval with graph data

#### Task 4.6: Graph API Endpoints
**File**: Update `backend/app/api/routes/graph.py`
**Priority**: MEDIUM
**Estimated Time**: 2 hours

- [ ] 4.6.1 Implement GET /graph/entities (list all)
- [ ] 4.6.2 Implement GET /graph/entities/{id} (details)
- [ ] 4.6.3 Implement GET /graph/search (full-text search)
- [ ] 4.6.4 Implement GET /graph/path (pathfinding)
- [ ] 4.6.5 Implement GET /graph/visualize (for frontend)
- [ ] 4.6.6 Add filtering and pagination

**Dependencies**: Neo4j client
**Output**: Functional graph API endpoints

**Total Phase 4**: ~16 hours (2 working days)

---

### Phase 5: Agentic Features (Days 6-8) - HIGH PRIORITY 🔥

#### Task 5.1: Router Agent
**File**: `backend/app/agents/router.py`
**Priority**: MEDIUM
**Estimated Time**: 2 hours

- [ ] 5.1.1 Intent classification (lookup, RCA, compliance, general)
- [ ] 5.1.2 Strategy selection logic
- [ ] 5.1.3 Confidence scoring
- [ ] 5.1.4 Fallback handling
- [ ] 5.1.5 Logging and monitoring

**Dependencies**: None
**Output**: Router that selects appropriate agent

#### Task 5.2: RCA Agent (Root Cause Analysis)
**File**: `backend/app/agents/rca_agent.py`
**Priority**: HIGH (Choose this OR Compliance)
**Estimated Time**: 6 hours

- [ ] 5.2.1 Define RCA workflow:
  - [ ] Collect failure history from graph
  - [ ] Retrieve OEM documentation
  - [ ] Analyze inspection records
  - [ ] Identify patterns
- [ ] 5.2.2 Implement 5-Why framework
  - [ ] Ask "why" iteratively
  - [ ] Build causal chain
- [ ] 5.2.3 Fishbone diagram data generation
  - [ ] Categories: People, Process, Equipment, Materials, Environment
  - [ ] Populate with evidence
- [ ] 5.2.4 Evidence linking and citation
- [ ] 5.2.5 Recommendation generation
- [ ] 5.2.6 Confidence scoring for conclusions
- [ ] 5.2.7 Output formatting (structured response)

**Dependencies**: Knowledge graph, RAG pipeline
**Output**: RCA report with causes and recommendations

#### Task 5.3: Compliance Agent
**File**: `backend/app/agents/compliance_agent.py`
**Priority**: HIGH (Alternative to RCA)
**Estimated Time**: 6 hours

- [ ] 5.3.1 Regulation library setup:
  - [ ] Store regulations in structured format
  - [ ] Index requirements
- [ ] 5.3.2 Requirement mapping:
  - [ ] Extract requirements from regulations
  - [ ] Map to organizational procedures
- [ ] 5.3.3 Procedure matching:
  - [ ] Find procedures that satisfy requirements
  - [ ] Identify missing procedures
- [ ] 5.3.4 Gap detection algorithm:
  - [ ] Compare requirements vs. actual
  - [ ] Flag missing evidence
  - [ ] Calculate compliance percentage
- [ ] 5.3.5 Evidence package generation:
  - [ ] Collect supporting documents
  - [ ] Generate PDF report
- [ ] 5.3.6 Risk scoring for gaps

**Dependencies**: Knowledge graph, document retrieval
**Output**: Compliance report with gaps and evidence

#### Task 5.4: Agent API Integration
**File**: Update `backend/app/api/routes/query.py`
**Priority**: HIGH
**Estimated Time**: 2 hours

- [ ] 5.4.1 Update RCA endpoint with real agent
- [ ] 5.4.2 Update compliance endpoint with real agent
- [ ] 5.4.3 Add agent status tracking
- [ ] 5.4.4 Add agent configuration options
- [ ] 5.4.5 Error handling for agent failures

**Dependencies**: Agents implemented
**Output**: Functional agent endpoints

**Total Phase 5**: ~16 hours (2 working days)

---

### Phase 6: Frontend (Days 9-10) - HIGH PRIORITY 🔥

#### Task 6.1: React App Setup
**Directory**: `frontend/`
**Priority**: HIGH
**Estimated Time**: 2 hours

- [ ] 6.1.1 Create React app with TypeScript
  ```bash
  npx create-react-app frontend --template typescript
  ```
- [ ] 6.1.2 Install dependencies:
  - [ ] Tailwind CSS
  - [ ] React Router
  - [ ] Axios
  - [ ] Cytoscape.js (for graph viz)
  - [ ] React Icons
- [ ] 6.1.3 Configure Tailwind CSS
- [ ] 6.1.4 Setup folder structure (components, pages, services, hooks)
- [ ] 6.1.5 Configure PWA manifest
- [ ] 6.1.6 Setup service worker for offline support
- [ ] 6.1.7 Create API client service
- [ ] 6.1.8 Configure routing

**Dependencies**: Node.js, npm
**Output**: React app scaffold

#### Task 6.2: Chat Interface
**Files**: `frontend/src/components/Chat/`
**Priority**: HIGH
**Estimated Time**: 4 hours

- [ ] 6.2.1 Chat message component (user/assistant bubbles)
- [ ] 6.2.2 Message list with auto-scroll
- [ ] 6.2.3 Input field with send button
- [ ] 6.2.4 SSE streaming integration
- [ ] 6.2.5 Citation display cards
- [ ] 6.2.6 Confidence indicators (badges)
- [ ] 6.2.7 Loading states (typing indicator)
- [ ] 6.2.8 Error handling and retry
- [ ] 6.2.9 Message formatting (markdown support)

**Dependencies**: API client
**Output**: Functional chat interface

#### Task 6.3: Document Upload
**Files**: `frontend/src/components/Upload/`
**Priority**: HIGH
**Estimated Time**: 2 hours

- [ ] 6.3.1 Drag-and-drop upload component
- [ ] 6.3.2 File type validation (PDF, XLSX, DOCX)
- [ ] 6.3.3 Upload progress bar
- [ ] 6.3.4 Status tracking UI
- [ ] 6.3.5 Document list view
- [ ] 6.3.6 Delete document functionality
- [ ] 6.3.7 Upload queue management

**Dependencies**: API client
**Output**: Document management UI

#### Task 6.4: Knowledge Graph Visualization
**Files**: `frontend/src/components/Graph/`
**Priority**: MEDIUM
**Estimated Time**: 4 hours

- [ ] 6.4.1 Install and configure Cytoscape.js
- [ ] 6.4.2 Fetch graph data from API
- [ ] 6.4.3 Render nodes (equipment, docs, failures, etc.)
- [ ] 6.4.4 Render edges (relationships)
- [ ] 6.4.5 Node/edge styling by type
- [ ] 6.4.6 Interactive navigation (zoom, pan, click)
- [ ] 6.4.7 Entity detail panel (on node click)
- [ ] 6.4.8 Filter controls (by entity type, relationship)
- [ ] 6.4.9 Layout algorithms (force-directed, hierarchical)

**Dependencies**: Graph API, Cytoscape.js
**Output**: Interactive graph visualization

#### Task 6.5: Voice Input
**Files**: `frontend/src/hooks/useVoiceInput.ts`
**Priority**: LOW (Nice to have)
**Estimated Time**: 1.5 hours

- [ ] 6.5.1 Web Speech API integration
- [ ] 6.5.2 Microphone permission handling
- [ ] 6.5.3 Speech-to-text conversion
- [ ] 6.5.4 Visual feedback (recording indicator)
- [ ] 6.5.5 Error handling (browser compatibility)
- [ ] 6.5.6 Voice button in chat input

**Dependencies**: Browser support
**Output**: Voice input functionality

#### Task 6.6: Additional Pages
**Files**: `frontend/src/pages/`
**Priority**: MEDIUM
**Estimated Time**: 3 hours

- [ ] 6.6.1 Home/landing page
- [ ] 6.6.2 RCA workspace page
- [ ] 6.6.3 Compliance dashboard
- [ ] 6.6.4 Settings page
- [ ] 6.6.5 About page
- [ ] 6.6.6 Navigation menu
- [ ] 6.6.7 Responsive layout

**Dependencies**: None
**Output**: Complete page structure

#### Task 6.7: Mobile Responsive Design
**Throughout frontend**
**Priority**: HIGH
**Estimated Time**: 2 hours

- [ ] 6.7.1 Tailwind responsive classes
- [ ] 6.7.2 Mobile navigation (hamburger menu)
- [ ] 6.7.3 Touch-friendly controls
- [ ] 6.7.4 PWA installation prompt
- [ ] 6.7.5 Test on mobile devices
- [ ] 6.7.6 Offline fallback UI

**Dependencies**: PWA setup
**Output**: Mobile-friendly UI

#### Task 6.8: Dockerfile for Frontend
**File**: `frontend/Dockerfile`
**Priority**: LOW
**Estimated Time**: 0.5 hours

- [ ] 6.8.1 Create multi-stage build Dockerfile
- [ ] 6.8.2 Update docker-compose.yml
- [ ] 6.8.3 Configure nginx for production

**Dependencies**: React app complete
**Output**: Containerized frontend

**Total Phase 6**: ~19 hours (2.5 working days)

---

### Phase 7: Polish & Demo (Days 11-14) - MEDIUM PRIORITY

#### Task 7.1: Testing & Bug Fixes
**Priority**: HIGH
**Estimated Time**: 4 hours

- [ ] 7.1.1 End-to-end testing (upload → query → answer)
- [ ] 7.1.2 Test all agent workflows
- [ ] 7.1.3 Test graph visualization
- [ ] 7.1.4 Test mobile responsiveness
- [ ] 7.1.5 Fix critical bugs
- [ ] 7.1.6 Handle edge cases
- [ ] 7.1.7 Improve error messages
- [ ] 7.1.8 Loading state improvements

**Dependencies**: All features complete
**Output**: Stable, bug-free system

#### Task 7.2: Sample Data Preparation
**Directory**: `data/samples/`
**Priority**: HIGH
**Estimated Time**: 3 hours

- [ ] 7.2.1 Collect/create industrial PDFs (equipment manuals)
- [ ] 7.2.2 Create work orders (sample failures)
- [ ] 7.2.3 Create SOPs (standard operating procedures)
- [ ] 7.2.4 Create incident reports
- [ ] 7.2.5 Create regulation documents (OISD, PESO)
- [ ] 7.2.6 Ingest all samples via API
- [ ] 7.2.7 Verify knowledge graph is populated
- [ ] 7.2.8 Create test queries for demo

**Dependencies**: None
**Output**: Demo-ready data

#### Task 7.3: RAGAS Evaluation (Optional)
**File**: `backend/app/evaluation/ragas_eval.py`
**Priority**: LOW
**Estimated Time**: 3 hours

- [ ] 7.3.1 Create evaluation dataset (Q&A pairs)
- [ ] 7.3.2 Setup RAGAS
- [ ] 7.3.3 Run faithfulness evaluation
- [ ] 7.3.4 Run relevance evaluation
- [ ] 7.3.5 Run context precision/recall
- [ ] 7.3.6 Generate evaluation report
- [ ] 7.3.7 Document metrics

**Dependencies**: Sample data
**Output**: Quality metrics report

#### Task 7.4: Performance Optimization
**Throughout codebase**
**Priority**: MEDIUM
**Estimated Time**: 2 hours

- [ ] 7.4.1 Profile slow endpoints
- [ ] 7.4.2 Optimize database queries
- [ ] 7.4.3 Cache frequently accessed data
- [ ] 7.4.4 Tune FAISS parameters
- [ ] 7.4.5 Reduce LLM context window if needed
- [ ] 7.4.6 Add connection pooling
- [ ] 7.4.7 Compress API responses

**Dependencies**: None
**Output**: Faster system

#### Task 7.5: Demo Preparation
**Priority**: HIGH
**Estimated Time**: 4 hours

- [ ] 7.5.1 Write demo script (3 personas)
  - [ ] Field Technician scenario
  - [ ] Maintenance Engineer scenario
  - [ ] Compliance Officer scenario
- [ ] 7.5.2 Practice demo flow (timing: 6 minutes)
- [ ] 7.5.3 Prepare backup plan (if something fails)
- [ ] 7.5.4 Test on different devices
- [ ] 7.5.5 Prepare Q&A responses
- [ ] 7.5.6 Create demo cheat sheet

**Dependencies**: All features working
**Output**: Demo-ready system

#### Task 7.6: Presentation & Video
**Priority**: HIGH
**Estimated Time**: 6 hours

- [ ] 7.6.1 Create slide deck (15-20 slides):
  - [ ] Problem statement
  - [ ] Solution overview
  - [ ] Architecture
  - [ ] Key features
  - [ ] Live demo
  - [ ] Technical highlights
  - [ ] Business impact
  - [ ] Future roadmap
- [ ] 7.6.2 Record demo video (3-5 minutes)
- [ ] 7.6.3 Edit video (cut, transitions)
- [ ] 7.6.4 Add voiceover/captions
- [ ] 7.6.5 Create thumbnail
- [ ] 7.6.6 Prepare presenter notes

**Dependencies**: Demo script
**Output**: Presentation materials

**Total Phase 7**: ~22 hours (3 working days)

---

## 📊 Effort Summary

| Phase | Priority | Hours | Days | Status |
|-------|----------|-------|------|--------|
| Foundation | ✅ | 10 | 1 | DONE |
| Core RAG | ✅ | 16 | 2 | DONE |
| Advanced RAG | ✅ | 12 | 1 | DONE |
| **Knowledge Graph** | 🔥 | 16 | 2 | TODO |
| **Agents** | 🔥 | 16 | 2 | TODO |
| **Frontend** | 🔥 | 19 | 2.5 | TODO |
| **Polish & Demo** | ⭐ | 22 | 3 | TODO |
| **TOTAL** | | **111** | **13.5** | **55% DONE** |

---

## 🎯 Critical Path (MVP)

### Must Complete (Cannot skip):
1. ✅ Core RAG - DONE
2. ✅ Advanced RAG - DONE
3. ⏳ Knowledge Graph (basic) - 1.5 days
4. ⏳ ONE Agent (RCA recommended) - 1 day
5. ⏳ Frontend (chat + upload) - 1.5 days
6. ⏳ Demo data - 0.5 days
7. ⏳ Presentation - 0.5 days

**Minimum Time to MVP**: 5 days

---

## 📅 Recommended Schedule

### Days 4-5 (Weekend)
- **Knowledge Graph** (16 hours)
  - Saturday: NER + Relationships + Neo4j (8h)
  - Sunday: Entity resolution + Integration + API (8h)

### Days 6-7 (Mon-Tue)
- **RCA Agent** (16 hours)
  - Monday: Agent framework + 5-Why + Evidence (8h)
  - Tuesday: Fishbone + Recommendations + API (8h)

### Days 8-10 (Wed-Fri)
- **Frontend** (19 hours)
  - Wednesday: Setup + Chat UI (8h)
  - Thursday: Upload + Graph viz (8h)
  - Friday: Polish + Mobile (3h)

### Days 11-14 (Weekend + Mon-Tue)
- **Demo Prep** (22 hours)
  - Saturday: Sample data + Testing (8h)
  - Sunday: Bug fixes + Optimization (4h)
  - Monday: Demo practice + Video (5h)
  - Tuesday: Presentation deck + Final polish (5h)

---

## 🚀 Quick Start (Next 24 Hours)

### Today (Continue):
1. ✅ Create NER pipeline (4h)
2. ✅ Create relationship extraction (3h)

### Tomorrow:
3. ✅ Neo4j integration (3h)
4. ✅ Graph-augmented retrieval (2h)
5. ✅ Graph API endpoints (2h)

**Result**: Knowledge graph complete!

---

## ⚡ Fast-Track Options

If time is short:

### Option A: Skip Advanced Features
- Skip query enhancement
- Skip re-ranking
- Skip compression
- Keep only core RAG
- **Saves**: 1 day (but we already did this!)

### Option B: Simplified Graph
- Basic entity extraction only
- Skip relationship extraction
- Skip graph visualization
- **Saves**: 1 day

### Option C: One Agent Only
- Choose RCA or Compliance (not both)
- **Saves**: 0.5 days

### Option D: Basic Frontend
- Chat interface only
- Skip graph visualization
- Skip voice input
- **Saves**: 1 day

---

## 📞 Decision Points

### Immediate Decisions Needed:
1. **Agent Choice**: RCA or Compliance? (Recommend: RCA)
2. **Graph Depth**: Full or basic? (Recommend: Full)
3. **Frontend Scope**: Complete or minimal? (Recommend: Complete)
4. **RAGAS**: Include evaluation? (Recommend: Skip if time-constrained)

---

## ✅ Task Assignment (If team)

| Role | Tasks | Days |
|------|-------|------|
| **ML Engineer** | Knowledge Graph, Entity Resolution | 2 |
| **Backend Engineer** | Agents, API Integration | 2 |
| **Frontend Engineer** | React App, All UI Components | 2.5 |
| **Full Stack / PM** | Demo Data, Testing, Presentation | 2 |

---

_Task list created June 26, 2026 - Ready for Days 4-14_

**Next up**: Knowledge Graph implementation 🚀
