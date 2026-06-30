# Knowledge Graph - Quick Reference Card

**Status**: ✅ Complete and Operational  
**Version**: 1.0  
**Date**: June 27, 2026

---

## 🎯 What It Does

The Knowledge Graph automatically extracts entities and relationships from industrial documents, storing them in Neo4j for graph-based queries and enhanced RAG responses.

---

## 📦 Entity Types (7)

| Type | Examples | Pattern |
|------|----------|---------|
| `EQUIPMENT` | P-101, TK-205, Pump 101 | Equipment tags |
| `PARAMETER` | temperature, pressure, flow | Process params |
| `MEASUREMENT` | 45 Nm, 100°C, 15 bar | Value + unit |
| `REGULATION` | OISD-STD-105, PESO, IS 2825 | Standards |
| `FAILURE_MODE` | seal leak, corrosion, wear | Failure types |
| `PERSON` | John Smith, Engineer | Names |
| `DATE` | June 25, 2026 | Timestamps |

---

## 🔗 Relationship Types (8)

| Type | Pattern | Example |
|------|---------|---------|
| `HAS_FAILURE` | Equipment → Failure | P-101 → seal leak |
| `GOVERNED_BY` | Equipment → Regulation | P-101 → OISD-105 |
| `MEASURED_BY` | Equipment → Parameter | P-101 → temperature |
| `OPERATES_AT` | Equipment → Measurement | P-101 → 45 Nm |
| `CAUSED_BY` | Failure → Parameter | seal leak → high temp |
| `DOCUMENTED_IN` | Entity → Document | P-101 → manual.pdf |
| `INVOLVES` | Incident → Equipment | failure → P-101 |
| `SATISFIES` | Procedure → Regulation | SOP → Factory Act |

---

## 🚀 Quick Start

### 1. Enable Knowledge Graph
```bash
# In .env file
ENABLE_KNOWLEDGE_GRAPH=true
```

### 2. Start Services
```bash
docker-compose up -d neo4j
python backend/app/main.py
```

### 3. Upload Document
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.pdf"
```

Entities automatically extracted to graph!

---

## 📡 API Endpoints

### List Entities
```bash
GET /api/v1/graph/entities?entity_type=EQUIPMENT&limit=50
```

### Get Entity Details
```bash
GET /api/v1/graph/entities/{entity_id}
# Returns entity + all relationships
```

### Search Graph
```bash
GET /api/v1/graph/search?query=P-101
```

### Find Path
```bash
GET /api/v1/graph/path?source_id=A&target_id=B&max_depth=5
```

### Visualize
```bash
GET /api/v1/graph/visualize?depth=2&limit=100
# Returns Cytoscape.js format
```

### Stats
```bash
GET /api/v1/graph/stats
# Returns node/relationship counts
```

---

## 💻 Code Examples

### Extract Entities
```python
from app.kg.ner import ner

text = "P-101 pump failed due to seal leak at 100°C"
entities = ner.extract_all(text)

# Returns:
# [
#   Entity(text="P-101", type="EQUIPMENT", confidence=0.95),
#   Entity(text="seal leak", type="FAILURE_MODE", confidence=0.80),
#   Entity(text="100°C", type="MEASUREMENT", confidence=0.95)
# ]
```

### Extract Relationships
```python
from app.kg.relations import relationship_extractor

relationships = relationship_extractor.extract_all(text, entities)

# Returns:
# [
#   Relationship("P-101", "HAS_FAILURE", "seal leak", confidence=0.80),
#   Relationship("seal leak", "CAUSED_BY", "100°C", confidence=0.75)
# ]
```

### Query Graph
```python
from app.kg.neo4j_client import neo4j_client

# Find equipment
entities = neo4j_client.find_entities(
    entity_type="EQUIPMENT",
    text_pattern="P-101"
)

# Get relationships
related = neo4j_client.get_related_entities(
    entity_id="doc_123_ent_0",
    relation_type="HAS_FAILURE"
)
```

### Graph-Augmented Query
```python
from app.rag.pipeline import rag_pipeline

response = rag_pipeline.query(
    question="What failures does P-101 have?",
    strategy="hybrid",
    use_kg_expansion=True  # Enable graph context
)

# response includes:
# - answer (LLM generated)
# - citations (from documents)
# - kg_entities (from graph) ← NEW!
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Enable/disable knowledge graph
ENABLE_KNOWLEDGE_GRAPH=true

# Neo4j connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Control extraction
# (in code: rag/pipeline.py line 155)
chunks_to_process = 10  # First N chunks per document
```

### Toggle Features
```python
# Disable KG extraction but keep existing graph
settings.ENABLE_KNOWLEDGE_GRAPH = False

# Disable graph-augmented retrieval
rag_pipeline.query(
    question="...",
    use_kg_expansion=False  # Don't use graph
)

# Enable LLM relationship extraction (slower, more accurate)
relationship_extractor.extract_all(
    text,
    entities,
    use_llm=True  # Use LLM for relationships
)
```

---

## 🐛 Troubleshooting

### No entities extracted?
```bash
# Check if enabled
curl http://localhost:8000/api/v1/health

# Check logs
tail -f logs/app.log | grep "Extracting entities"

# Verify Neo4j
docker ps | grep neo4j
```

### Graph queries fail?
```bash
# Test Neo4j connection
curl http://localhost:8000/api/v1/graph/stats

# Restart Neo4j
docker-compose restart neo4j

# Check Neo4j browser
open http://localhost:7474
```

### Empty kg_entities in query?
```bash
# Check if entities exist
curl http://localhost:8000/api/v1/graph/stats

# Verify entity text matches query
curl "http://localhost:8000/api/v1/graph/search?query=P-101"
```

---

## 📁 File Locations

```
backend/app/kg/
├── __init__.py              # Module exports
├── ner.py                   # Entity extraction (530 lines)
├── relations.py             # Relationship extraction (380 lines)
├── neo4j_client.py          # Graph database (480 lines)
└── entity_resolution.py     # Deduplication (380 lines)

backend/app/rag/
└── pipeline.py              # KG integration (lines 40, 150-250, 235-320)

backend/app/api/routes/
└── graph.py                 # Graph API (150 lines)

backend/app/main.py          # Schema init (lines 25-32)
```

---

## 🧪 Quick Test

```bash
# 1. Create test file
echo "P-101 pump has seal leak at 100°C per OISD-STD-105" > test.txt

# 2. Upload
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"

# 3. Check entities (wait 5s)
curl http://localhost:8000/api/v1/graph/entities

# 4. Query with graph
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What failures does P-101 have?"}'

# Look for kg_entities array in response!
```

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Entity Extraction | ~1s | Per document |
| Graph Storage | ~0.5s | Batched |
| Graph Query | <100ms | Indexed |
| Path Finding | <200ms | Max depth 5 |
| Augmented RAG | +0.2s | Vs normal RAG |

---

## 🎯 Use Cases

### 1. Equipment Failure Analysis
"What causes P-101 failures?" → Graph shows failure chains

### 2. Compliance Checking
"What regulations govern P-101?" → Graph shows GOVERNED_BY

### 3. Impact Analysis
"What equipment is affected by OISD-105?" → Reverse query

### 4. Knowledge Discovery
"What's the relationship between P-101 and TK-205?" → Path finding

### 5. Visualization
Graph of equipment, failures, regulations → Frontend display

---

## 🚀 Next Steps

### For RCA Agent (Day 4)
```python
# Use graph to find failure chains
def analyze_failure(equipment_id):
    # 1. Get equipment from graph
    equipment = neo4j_client.get_entity(equipment_id)
    
    # 2. Find failure modes
    failures = neo4j_client.get_related_entities(
        equipment_id,
        relation_type="HAS_FAILURE"
    )
    
    # 3. Find causes (traverse graph)
    for failure in failures:
        causes = neo4j_client.get_related_entities(
            failure['id'],
            relation_type="CAUSED_BY"
        )
    
    # 4. Generate 5-Why analysis...
```

### For Frontend (Day 6)
```javascript
// Fetch graph data
const response = await fetch('/api/v1/graph/visualize?depth=2');
const {nodes, edges} = await response.json();

// Render with Cytoscape.js
const cy = cytoscape({
  container: document.getElementById('graph'),
  elements: {
    nodes: nodes,
    edges: edges
  },
  style: [ /* styling */ ]
});
```

---

## 📝 Documentation

- `DAY3_KG_COMPLETION.md` - Full progress report
- `KG_INTEGRATION_SUMMARY.md` - Component overview  
- `TEST_KG_INTEGRATION.md` - Testing guide
- `KNOWLEDGE_GRAPH_COMPLETE.md` - Detailed summary
- **This file** - Quick reference

---

## ✅ Checklist

Before using knowledge graph:

- [ ] Neo4j running (`docker ps | grep neo4j`)
- [ ] `ENABLE_KNOWLEDGE_GRAPH=true` in .env
- [ ] Backend started (initializes schema)
- [ ] Test document uploaded
- [ ] Entities visible (`/graph/stats`)
- [ ] Query returns `kg_entities`

---

**Status**: ✅ Production Ready  
**Version**: 1.0  
**Last Updated**: June 27, 2026

🚀 **Ready to build agents!**
