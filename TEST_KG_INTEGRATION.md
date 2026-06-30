# Testing Knowledge Graph Integration

**Purpose**: Validate that the knowledge graph system works end-to-end  
**Prerequisites**: Docker running, backend started  
**Time**: 15-20 minutes

---

## 🎯 Test Scenarios

### Scenario 1: System Health Check
### Scenario 2: Document Upload with Entity Extraction
### Scenario 3: Graph Queries
### Scenario 4: Graph-Augmented RAG
### Scenario 5: Visualization Data

---

## Scenario 1: System Health Check ✅

### Goal
Verify all services are running and connected.

### Steps

#### 1.1 Check Backend Health
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-27T...",
  "services": {
    "neo4j": "connected",
    "redis": "connected",
    "minio": "connected"
  }
}
```

#### 1.2 Check Neo4j Connection
```bash
curl http://localhost:8000/api/v1/graph/stats
```

**Expected Response:**
```json
{
  "node_count": 0,
  "relationship_count": 0,
  "node_types": [],
  "relationship_types": []
}
```

✅ **Pass Criteria**: All services show "connected", graph starts empty

---

## Scenario 2: Document Upload with Entity Extraction ✅

### Goal
Upload a document and verify entities are extracted to the knowledge graph.

### Steps

#### 2.1 Create Test Document
Create a file `test_document.txt` with this content:

```
Equipment Maintenance Report

Equipment: P-101 (Primary Feed Pump)
Location: Unit A, Refinery
Date: June 25, 2026

Issue Description:
The pump P-101 experienced a seal leak at 45 Nm torque. 
Temperature reading was 100°C, exceeding the normal operating range.

Root Cause:
The seal failure was caused by high temperature operation.

Compliance:
This equipment must comply with OISD-STD-105 and Factory Act requirements.

Recommendation:
Replace seal and verify operating parameters per IS 2825 standards.
```

#### 2.2 Upload Document
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test_document.txt" \
  -F "metadata={\"category\":\"maintenance\",\"equipment\":\"P-101\"}"
```

**Expected Response:**
```json
{
  "document_id": "doc_...",
  "filename": "test_document.txt",
  "status": "processing",
  "message": "Document uploaded successfully"
}
```

#### 2.3 Wait for Processing
```bash
# Wait 5-10 seconds, then check status
curl http://localhost:8000/api/v1/documents/{document_id}/status
```

**Expected Response:**
```json
{
  "document_id": "doc_...",
  "status": "completed",
  "chunk_count": 1,
  "kg_entities": 8,      # NEW!
  "kg_relationships": 5   # NEW!
}
```

✅ **Pass Criteria**: 
- Status is "completed"
- `kg_entities` > 0
- `kg_relationships` > 0

---

## Scenario 3: Graph Queries ✅

### Goal
Query the knowledge graph directly to verify entities were stored.

### Steps

#### 3.1 Get Graph Statistics
```bash
curl http://localhost:8000/api/v1/graph/stats
```

**Expected Response:**
```json
{
  "node_count": 9,  # 8 entities + 1 document node
  "relationship_count": 13,  # 5 entity relationships + 8 DOCUMENTED_IN
  "node_types": ["Document", "EQUIPMENT", "MEASUREMENT", "FAILURE_MODE", "PARAMETER", "REGULATION"],
  "relationship_types": ["DOCUMENTED_IN", "HAS_FAILURE", "OPERATES_AT", "CAUSED_BY", "GOVERNED_BY"]
}
```

#### 3.2 List Equipment Entities
```bash
curl "http://localhost:8000/api/v1/graph/entities?entity_type=EQUIPMENT"
```

**Expected Response:**
```json
{
  "entities": [
    {
      "id": "doc_xxx_ent_0",
      "type": "EQUIPMENT",
      "text": "P-101",
      "original_text": "P-101",
      "confidence": 0.95
    }
  ],
  "total": 1
}
```

#### 3.3 Search for Specific Equipment
```bash
curl "http://localhost:8000/api/v1/graph/search?query=P-101"
```

**Expected Response:**
```json
{
  "query": "P-101",
  "results": [
    {
      "id": "doc_xxx_ent_0",
      "type": "EQUIPMENT",
      "text": "P-101"
    }
  ]
}
```

#### 3.4 Get Entity Details with Relationships
```bash
# Use the entity ID from previous response
curl http://localhost:8000/api/v1/graph/entities/doc_xxx_ent_0
```

**Expected Response:**
```json
{
  "entity": {
    "id": "doc_xxx_ent_0",
    "type": "EQUIPMENT",
    "text": "P-101"
  },
  "relationships": [
    {
      "relation_type": "HAS_FAILURE",
      "target": {
        "id": "doc_xxx_ent_1",
        "type": "FAILURE_MODE",
        "text": "seal leak"
      }
    },
    {
      "relation_type": "OPERATES_AT",
      "target": {
        "id": "doc_xxx_ent_2",
        "type": "MEASUREMENT",
        "text": "45 Nm"
      }
    },
    {
      "relation_type": "GOVERNED_BY",
      "target": {
        "id": "doc_xxx_ent_5",
        "type": "REGULATION",
        "text": "OISD-STD-105"
      }
    }
  ]
}
```

✅ **Pass Criteria**:
- Can find "P-101" entity
- Entity has relationships (HAS_FAILURE, OPERATES_AT, GOVERNED_BY)
- Related entities are correct types

---

## Scenario 4: Graph-Augmented RAG ✅

### Goal
Verify that queries use knowledge graph to enhance answers.

### Steps

#### 4.1 Ask Question About Equipment
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What failures does P-101 have?",
    "strategy": "hybrid"
  }'
```

**Expected Response:**
```json
{
  "answer": "P-101 experienced a seal leak. The seal failure was caused by high temperature operation at 100°C, which exceeded normal operating range while operating at 45 Nm torque.",
  "citations": [
    {
      "document_id": "doc_...",
      "document_title": "test_document.txt",
      "text": "The pump P-101 experienced a seal leak...",
      "relevance_score": 0.95
    }
  ],
  "confidence": 0.85,
  "strategy_used": "hybrid",
  "kg_entities": [         # NEW! Graph context
    {
      "id": "doc_xxx_ent_0",
      "text": "P-101",
      "type": "EQUIPMENT"
    },
    {
      "id": "doc_xxx_ent_1",
      "text": "seal leak",
      "type": "FAILURE_MODE"
    }
  ]
}
```

#### 4.2 Ask About Regulations
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What regulations apply to P-101?",
    "strategy": "hybrid"
  }'
```

**Expected Response:**
```json
{
  "answer": "P-101 must comply with OISD-STD-105 and Factory Act requirements...",
  "kg_entities": [
    {
      "text": "OISD-STD-105",
      "type": "REGULATION"
    },
    {
      "text": "Factory Act",
      "type": "REGULATION"
    }
  ]
}
```

✅ **Pass Criteria**:
- Answer includes information from document
- `kg_entities` array is populated
- Graph entities are relevant to question

---

## Scenario 5: Visualization Data ✅

### Goal
Verify visualization data is in correct format for frontend.

### Steps

#### 5.1 Get Graph Visualization Data
```bash
curl "http://localhost:8000/api/v1/graph/visualize?depth=2&limit=50"
```

**Expected Response:**
```json
{
  "nodes": [
    {
      "data": {
        "id": "doc_xxx_ent_0",
        "label": "P-101",
        "type": "EQUIPMENT"
      }
    },
    {
      "data": {
        "id": "doc_xxx_ent_1",
        "label": "seal leak",
        "type": "FAILURE_MODE"
      }
    },
    {
      "data": {
        "id": "doc_xxx",
        "label": "test_document.txt",
        "type": "Document"
      }
    }
  ],
  "edges": [
    {
      "data": {
        "id": "doc_xxx_ent_0-doc_xxx_ent_1",
        "source": "doc_xxx_ent_0",
        "target": "doc_xxx_ent_1",
        "label": "HAS_FAILURE"
      }
    },
    {
      "data": {
        "source": "doc_xxx_ent_0",
        "target": "doc_xxx",
        "label": "DOCUMENTED_IN"
      }
    }
  ]
}
```

✅ **Pass Criteria**:
- Nodes array contains entities and document
- Edges array contains relationships
- Format is Cytoscape.js compatible
- All IDs are consistent

---

## Scenario 6: Path Finding ✅

### Goal
Find shortest path between two entities.

### Steps

#### 6.1 Find Path from Equipment to Regulation
```bash
# Get entity IDs from search first
curl "http://localhost:8000/api/v1/graph/search?query=P-101"
curl "http://localhost:8000/api/v1/graph/search?query=OISD"

# Then find path
curl "http://localhost:8000/api/v1/graph/path?source_id=doc_xxx_ent_0&target_id=doc_xxx_ent_5&max_depth=5"
```

**Expected Response:**
```json
{
  "source": "doc_xxx_ent_0",
  "target": "doc_xxx_ent_5",
  "found": true,
  "path": [
    {
      "type": "node",
      "data": {
        "id": "doc_xxx_ent_0",
        "text": "P-101",
        "type": "EQUIPMENT"
      }
    },
    {
      "type": "relationship",
      "data": {
        "type": "GOVERNED_BY"
      }
    },
    {
      "type": "node",
      "data": {
        "id": "doc_xxx_ent_5",
        "text": "OISD-STD-105",
        "type": "REGULATION"
      }
    }
  ]
}
```

✅ **Pass Criteria**:
- Path is found
- Path alternates between nodes and relationships
- Path makes logical sense

---

## 🐛 Troubleshooting

### Problem: No entities extracted
**Symptoms**: `kg_entities: 0` after upload

**Checks**:
1. Is `ENABLE_KNOWLEDGE_GRAPH=true` in .env?
2. Is Neo4j running? `docker ps | grep neo4j`
3. Check logs: Look for "Extracting entities"

**Solution**:
```bash
# Check config
curl http://localhost:8000/api/v1/health

# Restart with KG enabled
docker-compose restart
```

### Problem: Graph queries fail
**Symptoms**: 500 error from /graph endpoints

**Checks**:
1. Neo4j connection: `curl http://localhost:8000/api/v1/health`
2. Neo4j logs: `docker logs et-hackathon-neo4j-1`

**Solution**:
```bash
# Restart Neo4j
docker-compose restart neo4j

# Check Neo4j browser
open http://localhost:7474
```

### Problem: No graph context in queries
**Symptoms**: `kg_entities` array is empty in query response

**Checks**:
1. Are entities in graph? `curl http://localhost:8000/api/v1/graph/stats`
2. Do entities match query? Try exact entity text

**Solution**:
- Upload more documents
- Use exact entity names in queries
- Check entity extraction in logs

### Problem: Duplicate entities
**Symptoms**: Multiple nodes for same equipment (P-101, Pump 101)

**Expected**: This is normal! Entity resolution creates canonical forms
- Both stored as separate entities initially
- Linked via `canonical_id`
- Can improve resolution rules in `entity_resolution.py`

---

## ✅ Success Criteria

All scenarios should pass:
- [x] Health checks show all services connected
- [x] Document upload extracts entities (kg_entities > 0)
- [x] Can query entities by type
- [x] Can search entities
- [x] Entity details show relationships
- [x] Query responses include kg_entities
- [x] Visualization data is in correct format
- [x] Path finding works

---

## 📊 Expected Results Summary

After uploading the test document:

| Metric | Expected Value |
|--------|---------------|
| Entities Extracted | 6-8 |
| Relationships Found | 4-6 |
| Node Types | 5-6 (EQUIPMENT, MEASUREMENT, FAILURE_MODE, PARAMETER, REGULATION, Document) |
| Relationship Types | 4-5 (HAS_FAILURE, OPERATES_AT, CAUSED_BY, GOVERNED_BY, DOCUMENTED_IN) |
| Query Enhancement | kg_entities array populated |
| Visualization | Nodes + Edges returned |

---

## 🎯 Next Steps After Testing

Once all tests pass:

1. **Test with Real Documents**
   - Upload actual maintenance manuals
   - Upload failure reports
   - Upload regulatory documents

2. **Verify Entity Quality**
   - Check entity normalization
   - Verify relationships make sense
   - Adjust patterns if needed

3. **Performance Testing**
   - Upload 10 documents
   - Check extraction time
   - Monitor Neo4j memory

4. **Move to Agents**
   - Knowledge graph is validated
   - Ready for RCA Agent development
   - Can use graph queries confidently

---

**Testing Time**: 15-20 minutes  
**Status**: Ready to test! 🚀
