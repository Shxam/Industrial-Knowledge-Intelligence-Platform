# 🧪 Testing Guide - Frontend & Backend Integration

**Date**: June 29, 2026  
**Purpose**: Step-by-step guide to test the complete application

---

## 🚀 Quick Start

### 1. Start Backend (Terminal 1)

```bash
# Navigate to backend directory
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\backend

# Activate virtual environment (if not already active)
# Windows CMD:
venv\Scripts\activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend**:
- Open browser: http://localhost:8000
- Should see: `{"name": "IKIP", "version": "0.1.0", ...}`
- API Docs: http://localhost:8000/docs

---

### 2. Start Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\frontend

# Start Vite dev server
npm run dev
```

**Expected Output**:
```
VITE v8.1.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Verify Frontend**:
- Open browser: http://localhost:5173
- Should see: Industrial AI Assistant interface with 4 tabs

---

## ✅ Feature Testing Checklist

### Test 1: Document Upload 📤

**Steps**:
1. Click on "Upload Documents" tab
2. Drag and drop a PDF, TXT, or DOCX file
3. OR click the upload area to select a file

**Expected Results**:
- ✅ File appears in upload status list
- ✅ Loading spinner shows during upload
- ✅ Green checkmark appears on success
- ✅ Document ID is returned from backend
- ✅ Error message shows if upload fails

**Test Files** (create if needed):
```bash
# Create a test text file
echo "This is a test document about industrial equipment maintenance." > test_doc.txt
```

**Backend Logs to Check**:
```
INFO: Document uploaded: test_doc.txt
INFO: Document ID: <uuid>
INFO: Processing started
```

---

### Test 2: Chat/Query Interface 💬

**Steps**:
1. First, upload at least one document (from Test 1)
2. Click on "Ask Questions" tab
3. Type a question in the input field
4. Click "Send" or press Enter

**Example Questions**:
- "What is this document about?"
- "Summarize the main points"
- "What are the safety procedures mentioned?"

**Expected Results**:
- ✅ Your question appears on the right (blue bubble)
- ✅ Loading spinner appears on the left
- ✅ AI response appears on the left (gray bubble)
- ✅ Citations show below AI response
- ✅ Citations include source and relevance score
- ✅ Chat auto-scrolls to latest message

**Backend Logs to Check**:
```
INFO: Query received: "What is this document about?"
INFO: Strategy: hybrid
INFO: Retrieved X chunks
INFO: Response generated
```

---

### Test 3: Root Cause Analysis 🔍

**Steps**:
1. Click on "Root Cause Analysis" tab
2. Enter a failure description in the text area
3. Click "Analyze Root Cause"

**Example Failure Description**:
```
The production line stopped unexpectedly at 2:00 PM. 
The conveyor belt motor overheated and triggered the safety shutdown. 
Maintenance logs show no recent inspections. 
The cooling fan was found to be clogged with dust.
```

**Expected Results**:
- ✅ "Analyzing..." button shows during processing
- ✅ Confidence score displays (green banner)
- ✅ 5-Why Analysis shows 5 numbered steps
- ✅ Fishbone Diagram shows 6 categories with factors
- ✅ Recommendations list shows numbered items
- ✅ Evidence summary displays

**Fishbone Categories** (should see all 6):
- People
- Process
- Equipment
- Materials
- Environment
- Management

**Backend Logs to Check**:
```
INFO: RCA analysis started
INFO: Failure description length: X chars
INFO: 5-Why analysis complete
INFO: Fishbone analysis complete
INFO: Recommendations generated
```

---

### Test 4: Knowledge Graph 🕸️

**Steps**:
1. Click on "Knowledge Graph" tab
2. View graph statistics

**Expected Results**:
- ✅ Graph Statistics card shows:
  - Total Nodes count
  - Total Relationships count
- ✅ Node Types card shows breakdown by type
- ✅ Relationship Types section shows all types
- ✅ Placeholder message for interactive visualization

**Note**: Graph will only have data if documents have been processed with NER and relation extraction enabled.

**Backend Logs to Check**:
```
INFO: Graph stats requested
INFO: Nodes: X, Relationships: Y
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Cannot connect to backend
**Symptoms**: 
- "Network Error" in browser console
- Frontend shows error messages
- CORS errors in console

**Solutions**:
1. Verify backend is running on port 8000
2. Check backend terminal for errors
3. Verify CORS is enabled in `backend/app/main.py`
4. Check `.env` file has correct `VITE_API_URL`

**Check**:
```bash
# Test backend directly
curl http://localhost:8000/api/v1/health
```

---

### Issue 2: Documents upload but can't query
**Symptoms**:
- Upload succeeds
- Query returns "no results" or error

**Solutions**:
1. Check document processing status
2. Verify vector store is initialized
3. Check backend logs for processing errors
4. Ensure at least one document is fully processed

**Check Backend**:
```python
# In backend terminal (Python REPL)
from app.rag.vector_store import vector_store
print(vector_store.count())  # Should be > 0
```

---

### Issue 3: RCA analysis fails
**Symptoms**:
- Error message after clicking "Analyze"
- Timeout error

**Solutions**:
1. Check OpenAI API key is set in `.env`
2. Verify LLM provider is configured correctly
3. Check backend logs for detailed error
4. Ensure failure description is not empty

**Check**:
```bash
# Verify environment variables
cd backend
python -c "from app.core.config import settings; print(settings.OPENAI_API_KEY[:10])"
```

---

### Issue 4: Graph shows 0 nodes
**Symptoms**:
- All graph stats show 0
- No node types displayed

**Solutions**:
1. This is expected if no documents have been processed yet
2. Upload documents first
3. Wait for document processing to complete
4. Check if Neo4j is running
5. Verify `ENABLE_KNOWLEDGE_GRAPH=true` in `.env`

**Check Neo4j**:
```bash
# Check Neo4j is running
curl http://localhost:7474
```

---

## 🔍 Debugging Tips

### Browser Developer Tools

**Console Tab**:
- Shows API requests and responses
- Shows JavaScript errors
- Check for CORS errors

**Network Tab**:
- View all API calls
- Check request/response payloads
- Verify response status codes (200, 400, 500, etc.)

**React DevTools** (if installed):
- Inspect component state
- View props
- Check re-renders

---

### Backend Debugging

**Check Logs**:
```bash
# Backend logs show in terminal where you ran uvicorn
# Look for:
- INFO: Successful operations
- WARNING: Potential issues
- ERROR: Failures
```

**API Docs**:
- Open http://localhost:8000/docs
- Test endpoints directly from Swagger UI
- Verify request/response formats

**Python REPL Testing**:
```bash
cd backend
python

# Test components
from app.rag.vector_store import vector_store
from app.kg.neo4j_client import neo4j_client

# Check vector store
print(vector_store.count())

# Check Neo4j
stats = neo4j_client.get_stats()
print(stats)
```

---

## 📊 Expected Behavior Summary

### Successful Test Run

1. **Backend Starts**: ✅
   - No errors in terminal
   - Health check returns 200
   - API docs accessible

2. **Frontend Starts**: ✅
   - Vite server runs on 5173
   - Page loads without errors
   - All 4 tabs visible

3. **Document Upload**: ✅
   - Files upload successfully
   - Status updates in real-time
   - Backend processes documents

4. **Query Interface**: ✅
   - Questions sent to backend
   - Responses received
   - Citations displayed

5. **RCA Analysis**: ✅
   - Analysis completes
   - All sections populated
   - Confidence score shown

6. **Knowledge Graph**: ✅
   - Stats displayed
   - No errors loading

---

## 🎯 Performance Benchmarks

### Expected Response Times

| Operation | Expected Time | Acceptable Range |
|-----------|--------------|------------------|
| Document Upload | 1-5s | < 10s |
| Query Response | 2-5s | < 10s |
| RCA Analysis | 10-20s | < 30s |
| Graph Stats | < 1s | < 3s |

**Note**: Times depend on:
- Document size
- Query complexity
- LLM response speed
- Network latency

---

## 📝 Test Data Recommendations

### Sample Documents to Upload

1. **Simple Text File** (`maintenance_guide.txt`):
```
Equipment Maintenance Guide

Safety First:
- Always wear protective equipment
- Follow lockout/tagout procedures
- Report hazards immediately

Weekly Checks:
- Inspect belts for wear
- Check fluid levels
- Test emergency stops
- Clean filters

Monthly Maintenance:
- Lubricate moving parts
- Calibrate sensors
- Replace worn components
```

2. **Technical Document** (create a PDF with):
- Equipment specifications
- Troubleshooting procedures
- Safety warnings
- Maintenance schedules

---

## ✅ Final Verification Checklist

Before demo/submission:

### Frontend
- [ ] All 4 tabs load without errors
- [ ] Document upload works
- [ ] Chat interface works
- [ ] RCA display works
- [ ] Graph stats display
- [ ] Loading states show
- [ ] Error messages are clear
- [ ] Mobile responsive (test browser resize)

### Backend
- [ ] Health check responds
- [ ] All API endpoints work
- [ ] CORS configured
- [ ] Neo4j connected (if enabled)
- [ ] Vector store initialized
- [ ] LLM provider configured
- [ ] No errors in logs

### Integration
- [ ] Frontend connects to backend
- [ ] API calls succeed
- [ ] Data flows correctly
- [ ] Error handling works
- [ ] Performance acceptable

---

## 🎉 Success Criteria

**You'll know it's working when**:
1. You can upload a document and see the success checkmark
2. You can ask a question and get an answer with citations
3. You can run RCA and see all 5 whys + fishbone + recommendations
4. You can view graph statistics (even if counts are low initially)

**Ready for demo when**:
- All success criteria met
- No console errors
- Clean user experience
- Professional appearance

---

## 📞 Quick Commands Reference

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend  
cd frontend
npm run dev

# Terminal 3: Testing (optional)
curl http://localhost:8000/api/v1/health
curl http://localhost:5173
```

---

**Happy Testing! 🚀**

**Next**: Once everything works, take screenshots for demo! 📸
