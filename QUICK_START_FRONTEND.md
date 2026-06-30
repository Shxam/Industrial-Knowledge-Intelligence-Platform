# ⚡ Quick Start - Frontend

**Last Updated**: June 29, 2026

---

## 🚀 Start Both Services

### Option 1: Two Terminals (Recommended)

**Terminal 1 - Backend**:
```bash
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\frontend
npm run dev
```

### Option 2: One Command (Windows)
```bash
# Create start-all.bat if needed:
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload"
start cmd /k "cd frontend && npm run dev"
```

---

## 🌐 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Main UI |
| **Backend** | http://localhost:8000 | API Server |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Neo4j** | http://localhost:7474 | Graph DB |

---

## ✅ Quick Test

1. Open http://localhost:5173
2. You should see: "Industrial AI Assistant"
3. See 4 tabs: Upload | Ask Questions | Root Cause Analysis | Knowledge Graph
4. Click each tab - they should all load

---

## 🧪 Quick Feature Test

### 1. Upload a Document (30 seconds)
```bash
# Create test file
echo "Industrial equipment requires regular maintenance for safety and efficiency." > test.txt

# Then in browser:
1. Go to "Upload Documents" tab
2. Drag test.txt onto upload area
3. See green checkmark = success!
```

### 2. Ask a Question (1 minute)
```bash
1. Go to "Ask Questions" tab
2. Type: "What is this document about?"
3. Click Send
4. See AI response with citation
```

### 3. Run RCA (2 minutes)
```bash
1. Go to "Root Cause Analysis" tab
2. Paste:
   "Motor overheated and stopped. 
    Cooling fan was clogged with dust.
    No recent maintenance was performed."
3. Click "Analyze Root Cause"
4. See 5-Why, Fishbone, and Recommendations
```

### 4. View Graph (10 seconds)
```bash
1. Go to "Knowledge Graph" tab
2. See statistics
3. (Graph may show 0 if no documents processed yet)
```

---

## 🐛 Troubleshooting

### Problem: Frontend shows "Network Error"
**Solution**:
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Should return: {"status": "healthy"}
```

### Problem: Backend won't start
**Solution**:
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Restart backend
```

### Problem: Frontend won't start
**Solution**:
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Kill process if needed
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 5174
```

### Problem: Changes not showing
**Solution**:
```bash
# Hard refresh browser
Ctrl + Shift + R (Windows)
Cmd + Shift + R (Mac)

# Or clear cache and reload
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `frontend/src/App.tsx` | Main application |
| `frontend/src/api/client.ts` | API calls |
| `frontend/.env` | Configuration |
| `TESTING_GUIDE.md` | Detailed testing |
| `DAY4_SUCCESS.md` | What we built |

---

## 🎯 Expected Behavior

### Backend Logs (Terminal 1)
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Frontend Logs (Terminal 2)
```
VITE v8.1.0  ready in XXX ms
➜  Local:   http://localhost:5173/
```

### Browser Console (F12)
```
No errors = good!
Check Network tab for API calls
```

---

## 📊 Status Check

### Everything Working When:
- ✅ Both terminals show no errors
- ✅ Frontend loads at localhost:5173
- ✅ Backend responds at localhost:8000
- ✅ All 4 tabs visible
- ✅ No console errors (F12)

---

## 🔥 Pro Tips

1. **Keep terminals open** - you'll see live logs
2. **Check browser console** - F12 for debugging
3. **Use API docs** - Test endpoints at /docs
4. **Save test files** - Reuse for quick testing
5. **Read TESTING_GUIDE.md** - For detailed help

---

## 📞 Need Help?

1. Check browser console (F12)
2. Check backend terminal logs
3. Read TESTING_GUIDE.md
4. Check FRONTEND_COMPLETE.md
5. Verify .env file settings

---

## 🎉 Next Steps

Once everything works:
1. ✅ Upload real documents
2. ✅ Test all features
3. ✅ Take screenshots
4. ✅ Prepare demo
5. ✅ Show off your work!

---

**Happy Coding! 🚀**
