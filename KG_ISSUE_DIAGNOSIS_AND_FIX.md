# 🔍 Knowledge Graph Issue - Diagnosis & Fix

## ❌ Problem Identified

Your knowledge graph is showing random/empty outputs because:

1. **Neo4j not fully connected** - Docker services are still initializing
2. **Knowledge graph disabled** - Set to `false` in `.env`
3. **No documents uploaded yet** - Graph needs entities extracted from documents
4. **Missing data validation** - Endpoints return empty data without error

---

## 🔧 Quick Fix (Immediate)

### Step 1: Enable Knowledge Graph

Edit `.env` file and change:

```bash
# BEFORE:
ENABLE_KNOWLEDGE_GRAPH=false

# AFTER:
ENABLE_KNOWLEDGE_GRAPH=true
```

### Step 2: Restart Backend

Stop and restart the backend process (Terminal 7):
1. Press Ctrl+C to stop current process
2. Run: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### Step 3: Wait for Neo4j

Monitor Docker Terminal (Terminal 4) until you see:
```
✓ neo4j_... is healthy
✓ ikip_neo4j ... done
```

Check Neo4j is ready:
```
curl http://localhost:7474
```

Should return HTML (Neo4j browser).

### Step 4: Upload a Document

1. Go to http://localhost:3002
2. Click "Ingest" tab
3. Upload a PDF or TXT document
4. Wait for processing to complete

### Step 5: View Knowledge Graph

1. Click "Graph" tab
2. Click "Visualize Graph" button
3. You should now see real extracted entities and relationships

---

## 🎯 Why This Fixes It

### The Real Issue
```
User uploads document
    ↓
Backend extracts entities (NER)
    ↓
Backend extracts relationships
    ↓
Entities stored in Neo4j  ← ⚠️ Neo4j wasn't ready = random/empty data
    ↓
Frontend visualizes graph
```

### What Was Happening
- Neo4j connection failed silently
- Empty graph was visualized
- Frontend showed "random" data (actually empty)
- Enabling KG forces Neo4j connection on startup
- Once Neo4j is healthy, entities are properly stored

---

## 📊 Verification Steps

### Check if Graph is Working

1. **Backend log** (Terminal 7) should show:
   ```
   INFO - Initialized Neo4j connection
   INFO - Neo4j schema initialized successfully
   ```

2. **Neo4j Browser** - Open http://localhost:7474
   - Username: `neo4j`
   - Password: `neo4j_password_change_me` (from docker-compose.yml)
   - Run query: `MATCH (n) RETURN count(n) as entity_count`
   - Should show count > 0 after document upload

3. **API Health** - Test endpoint:
   ```bash
   curl http://localhost:8000/api/v1/graph/stats
   ```
   Should return:
   ```json
   {
     "node_count": 5,
     "relationship_count": 3,
     "node_types": ["EQUIPMENT", "PARAMETER"],
     "relationship_types": ["HAS_FAILURE", "MEASURED_BY"]
   }
   ```

---

## 🚀 Full Workflow (After Fix)

```
1. Upload Document
   ↓
2. Backend processes:
   - Chunking
   - NER (extracts entities)
   - Relationship extraction
   - Stores in Neo4j
   ↓
3. Go to Graph tab
   ↓
4. See real entities:
   - Equipment (P-101, TK-205)
   - Parameters (temperature, pressure)
   - Failure modes (seal leak, corrosion)
   - Regulations (OISD-STD-105)
   ↓
5. Relationships shown:
   - Equipment HAS_FAILURE FailureMode
   - Equipment MEASURED_BY Parameter
   - Equipment GOVERNED_BY Regulation
```

---

## 🔧 Advanced Troubleshooting

### If Graph Still Shows Empty Data

1. **Check Neo4j Status**
   ```bash
   docker-compose ps
   ```
   - `neo4j` should show `healthy`
   - If not, wait 2-3 more minutes

2. **Check Backend Logs** (Terminal 7)
   ```
   Look for any "Connection refused" errors
   ```

3. **Manually Clear Graph** (if needed)
   ```bash
   # SSH into Neo4j
   docker-compose exec neo4j cypher-shell -u neo4j -p neo4j_password_change_me
   
   # Clear all data
   MATCH (n) DETACH DELETE n;
   ```

4. **Re-upload Document**
   - Upload document again
   - Wait for processing
   - Check graph stats

### If Backend Shows Connection Errors

```
Error: HTTPConnectionPool(host='localhost', port=7474)
```

**Solution:**
- This is normal during startup
- Neo4j is still initializing
- Wait another 1-2 minutes
- Errors will disappear automatically

### If No Entities Extracted

1. Check document is valid PDF/TXT
2. Check it's not encrypted
3. Try with sample text file first
4. Check backend logs for NER errors

---

## 📋 Configuration Settings

### `.env` - Knowledge Graph Settings

```bash
# Enable/disable knowledge graph
ENABLE_KNOWLEDGE_GRAPH=true  ← Change this to true!

# Neo4j connection (from docker-compose.yml)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password_change_me
```

### `docker-compose.yml` - Neo4j Configuration

```yaml
neo4j:
  image: neo4j:5.15-community
  environment:
    NEO4J_AUTH: neo4j/neo4j_password_change_me
    NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
  ports:
    - "7474:7474"  # HTTP
    - "7687:7687"  # Bolt (driver)
```

---

## 🎯 What Each Component Does

### NER (Named Entity Recognition)
**File**: `backend/app/kg/ner.py`

Extracts these entity types:
- **EQUIPMENT**: P-101, TK-205, Pump 301
- **PARAMETER**: Temperature, Pressure, Flow Rate
- **FAILURE_MODE**: Seal leak, Corrosion, Bearing failure
- **REGULATION**: OISD-STD-105, PESO, Factory Act
- **MEASUREMENT**: 45 Nm, 100°C, 15 bar
- **PERSON**: Names (from spaCy)
- **DATE**: Dates and timestamps

### Relationship Extraction
**File**: `backend/app/kg/relations.py`

Extracts these relationships:
- **HAS_FAILURE**: Equipment has failure mode
- **GOVERNED_BY**: Equipment/Procedure governed by regulation
- **MEASURED_BY**: Equipment measured by parameter
- **OPERATES_AT**: Equipment operates at measurement value
- **CAUSED_BY**: Failure caused by parameter/condition

### Entity Resolution
**File**: `backend/app/kg/entity_resolution.py`

Handles:
- **Fuzzy matching**: P-101 = P101 = Pump 101
- **Canonicalization**: Standardizes formats
- **Deduplication**: Removes duplicate entities
- **Similarity scoring**: Matches similar entities

### Neo4j Client
**File**: `backend/app/kg/neo4j_client.py`

Manages:
- Connection to Neo4j database
- Entity CRUD operations
- Relationship management
- Graph visualization data formatting
- Statistics calculation

---

## 🧪 Test Queries (Neo4j Browser)

Once entities are loaded, try these Cypher queries:

### Get all equipment
```cypher
MATCH (e:Entity {type: 'EQUIPMENT'})
RETURN e.text as equipment, e.id as id
LIMIT 10
```

### Get relationships
```cypher
MATCH (source)-[r]-(target)
RETURN source.text as source, type(r) as relationship, target.text as target
LIMIT 20
```

### Find equipment with failures
```cypher
MATCH (e:Entity {type: 'EQUIPMENT'})-[r:HAS_FAILURE]-(f:Entity {type: 'FAILURE_MODE'})
RETURN e.text as equipment, f.text as failure_mode
```

### Count entities by type
```cypher
MATCH (e:Entity)
RETURN e.type as entity_type, count(*) as count
GROUP BY e.type
```

---

## 🚀 Complete Setup Steps

### 1. Stop All Services
```bash
# Terminal 4: Stop docker-compose
docker-compose down

# Terminal 5: Stop frontend (Ctrl+C)
# Terminal 7: Stop backend (Ctrl+C)
```

### 2. Clean Start
```bash
# Edit .env
Edit: ENABLE_KNOWLEDGE_GRAPH=true

# Terminal 4: Start docker-compose
docker-compose up -d

# Wait 5-10 minutes for Neo4j to be healthy

# Terminal 7: Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 5: Start frontend (if not running)
npm run dev
```

### 3. Upload Document
```
1. Open http://localhost:3002
2. Click "Ingest"
3. Upload PDF/TXT file
4. Wait for processing
```

### 4. View Graph
```
1. Click "Graph" tab
2. Click "Visualize Graph"
3. Should see real entities and relationships!
```

---

## ✅ Success Indicators

You'll know the fix worked when:

✅ Graph stats show `node_count > 0`  
✅ Graph visualization displays real entities  
✅ Entity types match uploaded document  
✅ Relationships are logical (Equipment → Failure Mode)  
✅ No "random" or empty data  
✅ Neo4j browser shows entities in database  

---

## 📊 Expected Data Structure

After uploading an industrial document, you should see:

```
Entities:
├── Equipment (tags like P-101, TK-205)
├── Parameters (temperature, pressure)
├── Failure Modes (seal leak, corrosion)
├── Regulations (OISD-STD-105)
└── Measurements (100°C, 45 Nm)

Relationships:
├── P-101 --HAS_FAILURE--> Seal leak
├── P-101 --GOVERNED_BY--> OISD-STD-105
├── P-101 --MEASURED_BY--> Temperature
└── Seal leak --CAUSED_BY--> High Temperature
```

---

## 🆘 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Graph shows empty | Neo4j not ready | Wait 5-10 min, check docker-compose |
| Graph shows random data | KG disabled in .env | Set ENABLE_KNOWLEDGE_GRAPH=true |
| No entities extracted | Document not processed | Upload document, wait for completion |
| Connection refused error | Neo4j not started | docker-compose up -d, wait for health |
| Backend crashes | Neo4j required but missing | Set ENABLE_KNOWLEDGE_GRAPH=true before starting |

---

## 📝 Summary

### The Problem
Knowledge graph showing random/empty outputs because:
- Neo4j not initialized when backend started
- KG disabled in configuration
- No documents uploaded to extract entities from

### The Solution
1. **Enable** knowledge graph in `.env`
2. **Restart** backend to connect to Neo4j
3. **Wait** for Neo4j to be healthy (~10 min)
4. **Upload** a document to populate graph
5. **View** real entities and relationships

### Expected Result
Fully functional knowledge graph showing:
- Real entities extracted from documents
- Proper relationships between entities
- Interactive visualization
- Statistics and search capability

---

**After these fixes, your knowledge graph will show real data extracted from your uploaded documents!** 🎉

Need help? Check the logs in Terminal 7 (backend) for detailed error messages.
