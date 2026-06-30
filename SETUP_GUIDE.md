# 🔧 Complete Setup Guide for IKIP

**Last Updated**: June 29, 2026  
**Purpose**: Step-by-step guide to configure your Industrial AI Assistant

---

## 📋 Quick Status

### ✅ What's Already Working
- Frontend UI (http://localhost:5173) - Running with all features
- Backend API (http://localhost:8000) - Running in simplified mode
- Document Upload - Works with simplified backend
- All UI components - Fully functional

### ⚠️ What Needs Configuration
- OpenAI API Key (for AI responses)
- Neo4j Database (for knowledge graph)
- Full backend dependencies (for real AI processing)

---

## 🎯 Three Setup Options

### Option 1: Quick Demo (Current) ⚡
**Status**: ✅ ALREADY RUNNING

**What you have**:
- Simplified backend with mock responses
- All UI features working
- Document upload working
- Can test the entire application

**Limitations**:
- Mock AI responses (not real intelligence)
- No real knowledge graph
- No vector search

**Good for**: Testing UI/UX, demos, development

**No configuration needed!** Just use it as-is.

---

### Option 2: Partial Setup (AI Responses Only) 🤖
**What you get**:
- Real AI-powered responses
- Actual RCA analysis
- Query understanding
- No knowledge graph

**Requirements**:
- OpenAI API key (or other LLM provider)
- Install additional dependencies

**Setup Time**: ~15 minutes

---

### Option 3: Full Setup (Complete System) 🚀
**What you get**:
- Real AI responses
- Knowledge graph with Neo4j
- Vector search with FAISS
- Full RAG pipeline
- All features working

**Requirements**:
- OpenAI API key
- Neo4j database
- PostgreSQL (optional)
- Redis (optional)
- Full dependency installation

**Setup Time**: ~30-45 minutes

---

## 🔑 API Keys Setup

### 1. OpenAI API Key (Most Important)

#### Step 1: Get Your API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)

**Cost**: 
- GPT-4: ~$0.03 per 1K tokens
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Estimate: $5-10 for testing

#### Step 2: Configure the Key

**Create `.env` file in project root**:
```bash
# In: c:\Users\sham3\OneDrive\Desktop\ET-hackathon\.env

# Copy from .env.example and add your key
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=true

# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
LLM_MODEL=gpt-4-turbo-preview

# Or use cheaper model
# LLM_MODEL=gpt-3.5-turbo

# Embedding Model (free, runs locally)
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DIMENSION=384

# Enable features
ENABLE_KNOWLEDGE_GRAPH=false  # Set true if using Neo4j
ENABLE_HYBRID_SEARCH=true
ENABLE_GUARDRAILS=true
```

**Alternative: Set environment variable** (Windows):
```powershell
# PowerShell (temporary, current session only)
$env:OPENAI_API_KEY="sk-proj-your-key-here"

# Or set permanently in System Properties
# Windows Key → "environment variables" → Add user variable
```

---

### 2. Alternative LLM Providers

#### Option A: Azure OpenAI
```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
LLM_MODEL=gpt-4
```

#### Option B: Ollama (Free, Local)
1. Install Ollama: https://ollama.ai/
2. Pull a model: `ollama pull llama3`
3. Configure:
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3
```

#### Option C: Other OpenAI-Compatible APIs
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_API_BASE=https://api.together.xyz/v1  # Example: Together AI
LLM_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
```

---

## 🗄️ Database Setup (Optional)

### Neo4j Knowledge Graph

#### Step 1: Install Neo4j

**Option A: Docker (Recommended)**:
```powershell
# Run Neo4j in Docker
docker run -d `
  --name neo4j `
  -p 7474:7474 -p 7687:7687 `
  -e NEO4J_AUTH=neo4j/password123 `
  neo4j:latest

# Access at: http://localhost:7474
# Username: neo4j
# Password: password123
```

**Option B: Download Desktop App**:
1. Go to https://neo4j.com/download/
2. Download Neo4j Desktop
3. Create a new database
4. Set password

#### Step 2: Configure Neo4j
```env
# In .env file
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
ENABLE_KNOWLEDGE_GRAPH=true
```

---

### PostgreSQL (Optional)

**Only needed for user authentication, sessions, audit logs**

#### Using Docker:
```powershell
docker run -d `
  --name postgres `
  -p 5432:5432 `
  -e POSTGRES_DB=ikip_db `
  -e POSTGRES_USER=ikip_user `
  -e POSTGRES_PASSWORD=ikip_password `
  postgres:15
```

#### Configure:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ikip_db
POSTGRES_USER=ikip_user
POSTGRES_PASSWORD=ikip_password
```

---

### Redis (Optional)

**Only needed for caching, rate limiting**

#### Using Docker:
```powershell
docker run -d --name redis -p 6379:6379 redis:latest
```

#### Configure:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 📦 Full Backend Setup

### Step 1: Install All Dependencies

```powershell
# Navigate to backend
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\backend

# Activate virtual environment (already created)
.\venv\Scripts\Activate.ps1

# Install all dependencies (this takes 10-15 minutes)
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 2: Start Services

```powershell
# Terminal 1: Neo4j (if using)
docker start neo4j

# Terminal 2: Backend
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

---

## 🚀 Recommended Setup for You

Based on your situation, here's what I recommend:

### If you want to test RIGHT NOW:
**✅ You're already set!** Use the simplified backend that's running.

### If you want real AI responses:
1. **Get OpenAI API key** (5 minutes, $5-10 budget)
2. **Create `.env` file** with your key
3. **Install minimal dependencies**:
   ```powershell
   cd backend
   .\venv\Scripts\pip.exe install openai langchain langchain-openai sentence-transformers
   ```
4. **Restart backend with main.py** instead of simple_server.py

### If you want the complete system:
1. Follow all steps above
2. Install Docker Desktop
3. Run Neo4j in Docker
4. Install all dependencies
5. Configure everything

---

## 🎯 Minimal Setup for AI Features

**Minimum requirements for real AI**:

1. **OpenAI API Key** - Get from https://platform.openai.com/api-keys
2. **Create `.env` file**:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
   LLM_MODEL=gpt-3.5-turbo  # Cheaper
   ```
3. **Install minimal packages**:
   ```powershell
   .\venv\Scripts\pip.exe install openai langchain langchain-openai tiktoken
   ```
4. **Update simple_server.py** to use real AI instead of mock

---

## 🔍 Testing Your Setup

### Test Backend API
```powershell
# Health check
curl http://localhost:8000/api/v1/health

# Should return: {"status": "healthy", ...}
```

### Test Frontend
```
Open: http://localhost:5173
Upload a document
Try asking a question
```

### Test OpenAI Connection
```powershell
# In backend directory
.\venv\Scripts\python.exe

# Python REPL
import openai
from openai import OpenAI
client = OpenAI(api_key="your-key-here")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

---

## 💰 Cost Estimates

### Development/Testing
- OpenAI API: $5-10 for development
- Neo4j Desktop: Free
- All other tools: Free

### Production
- OpenAI API: $20-100/month (depends on usage)
- Neo4j: Free (Community) or $150+/month (Enterprise)
- Cloud hosting: $50-200/month

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution**: Install missing package
```powershell
.\venv\Scripts\pip.exe install package-name
```

### Issue: "OpenAI API key not found"
**Solution**: 
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=your-key`
3. Restart backend

### Issue: "Neo4j connection failed"
**Solution**:
1. Check Neo4j is running: `docker ps`
2. Verify credentials in `.env`
3. Test connection: http://localhost:7474

### Issue: "Port already in use"
**Solution**:
```powershell
# Find process using port
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Kill process (replace PID)
taskkill /PID <PID> /F
```

---

## 📝 Quick Commands Reference

```powershell
# Start Neo4j (if using Docker)
docker start neo4j

# Start Backend (simplified - already running)
cd backend
.\venv\Scripts\python.exe simple_server.py

# Start Backend (full - requires setup)
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

# Start Frontend (already running)
cd frontend
npm run dev
```

---

## 🎯 What Should YOU Do?

### Immediate (No Setup Required):
1. ✅ **Upload your test documents** using the running frontend
2. ✅ **Test all UI features** with the simplified backend
3. ✅ **Explore the interface** - everything is functional

### If You Want Real AI (15 minutes):
1. Get OpenAI API key
2. Create `.env` file with the key
3. I can update the simple_server.py to use real AI

### If You Want Full System (45 minutes):
1. Install Docker Desktop
2. Run Neo4j in Docker
3. Install all backend dependencies
4. Configure everything

---

## 🚀 My Recommendation

**For now:**
1. **Use the simplified backend** that's already running
2. **Upload the test documents** I created
3. **Test all the UI features**
4. **Get a feel for the application**

**Later:**
1. Get an OpenAI API key when ready
2. I'll help you integrate it
3. Upgrade to full AI responses

---

## 📞 Next Steps

1. **Tell me which option you prefer**:
   - Continue with simplified backend (works now)
   - Add OpenAI API key (I'll help configure)
   - Full setup (I'll guide through each step)

2. **I'll help you with**:
   - Creating the `.env` file
   - Installing dependencies
   - Configuring services
   - Testing everything

---

**You're already running! Just upload those documents and start testing! 🎉**
