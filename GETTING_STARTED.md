# Getting Started with IKIP - 10 Minute Guide

## 👋 Welcome!

This guide will get you from zero to running the IKIP platform in 10 minutes.

---

## ⚡ Prerequisites Check (2 minutes)

Make sure you have:

- [ ] **Docker Desktop** installed and running
  - Windows: https://docs.docker.com/desktop/install/windows-install/
  - Check: `docker --version`

- [ ] **Python 3.11+** installed
  - Download: https://www.python.org/downloads/
  - Check: `python --version`

- [ ] **Git** installed (optional but recommended)
  - Download: https://git-scm.com/download/win
  - Check: `git --version`

- [ ] **8GB+ RAM** available (16GB recommended)

- [ ] **OpenAI API Key** OR willingness to use local Ollama
  - Get key: https://platform.openai.com/api-keys
  - Alternative: Install Ollama for free local LLM

---

## 🚀 Installation (5 minutes)

### Step 1: Get the Code (30 seconds)

```bash
# If you have git
git clone <repository-url>
cd ET-hackathon

# OR extract the zip file and cd into it
cd ET-hackathon
```

### Step 2: Configure Environment (1 minute)

```bash
# Copy the example environment file
copy .env.example .env

# Open .env in any text editor and set:
# OPENAI_API_KEY=sk-your-key-here
# OR
# LLM_PROVIDER=ollama (for local/free option)
```

**Windows**: Use Notepad
```bash
notepad .env
```

### Step 3: Start Docker Services (2 minutes)

```bash
# Start all backend services
docker-compose up -d

# Wait 30 seconds for services to start
timeout /t 30

# Check if services are running
docker-compose ps
```

You should see:
- ✅ postgres (healthy)
- ✅ neo4j (healthy)
- ✅ redis (healthy)
- ✅ minio (healthy)

### Step 4: Setup Python Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies (this takes ~2 minutes)
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

**Note**: If you see "pip is not recognized", try `python -m pip` instead.

---

## ✅ Verify Installation (2 minutes)

### Test 1: Start the Backend

```bash
# Make sure you're in backend/ with venv activated
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Test 2: Check Health

Open a **new terminal** and run:

```bash
curl http://localhost:8000/api/v1/health
```

Or open in browser: http://localhost:8000/api/v1/health

You should see JSON response:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0"
}
```

### Test 3: View API Docs

Open in browser: http://localhost:8000/docs

You should see interactive API documentation (Swagger UI).

### Test 4: Check All Services

Open these in your browser:

- ✅ **API Docs**: http://localhost:8000/docs
- ✅ **Neo4j Browser**: http://localhost:7474
  - Login: neo4j / neo4j_password_change_me
- ✅ **MinIO Console**: http://localhost:9001
  - Login: minioadmin / minioadmin

---

## 🎯 What's Next?

### For Developers

**Read these in order:**

1. **[INDEX.md](./INDEX.md)** - Complete project overview
2. **[NEXT_STEPS.md](./NEXT_STEPS.md)** - Implementation guide
3. **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Development workflow

**Start coding:**
- Core task: Implement document loader → FAISS → RAG pipeline
- See [NEXT_STEPS.md](./NEXT_STEPS.md) for detailed instructions

### For Project Managers

**Review these:**

1. **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Full overview
2. **[PRD.md](./PRD.md)** - Requirements and goals
3. **[STATUS.md](./STATUS.md)** - Current progress
4. **[TASKS.md](./TASKS.md)** - Task breakdown

### For QA/Testing

**Test the API:**

```bash
# From project root
python test_api.py
```

---

## 🐛 Troubleshooting

### Docker services won't start

```bash
# Stop everything
docker-compose down -v

# Start fresh
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Port already in use

If you see "port 8000 is already allocated":

```bash
# Change port in backend
uvicorn app.main:app --reload --port 8001
```

### Virtual environment issues

```bash
# Delete and recreate
cd backend
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Python not found

Make sure Python is in your PATH:
1. Search "Edit system environment variables"
2. Add Python installation directory to PATH
3. Restart terminal

### pip install fails

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

### Still stuck?

1. Check [DEVELOPMENT.md](./DEVELOPMENT.md#troubleshooting)
2. Review Docker Desktop logs
3. Make sure you have 8GB+ RAM available
4. Restart Docker Desktop

---

## 📚 Project Structure Overview

```
ET-hackathon/
├── backend/           # FastAPI backend (you'll work here)
│   ├── app/
│   │   ├── main.py   # Entry point ← START HERE
│   │   ├── api/      # REST endpoints
│   │   ├── rag/      # RAG engine components
│   │   └── ...
│   └── requirements.txt
├── data/              # Data storage (auto-created)
├── docs/              # Documentation
├── .env               # Your configuration (edit this)
└── docker-compose.yml # Services definition
```

---

## 🎓 Key Concepts

### What does each service do?

- **FastAPI (port 8000)** - Your main application API
- **PostgreSQL (port 5432)** - Stores document metadata, users
- **Neo4j (port 7474/7687)** - Knowledge graph database
- **Redis (port 6379)** - Cache and session storage
- **MinIO (port 9000/9001)** - Object storage for documents

### What's implemented?

✅ **Ready to use:**
- API skeleton with all endpoints
- Embedding service (BGE)
- Smart chunking
- Configuration management
- Logging

⏳ **Need to implement (your tasks):**
- Document loader
- FAISS vector store
- BM25 search
- LLM integration
- RAG pipeline

See [NEXT_STEPS.md](./NEXT_STEPS.md) for implementation details.

---

## 💡 Quick Tips

### Development Workflow

```bash
# 1. Start Docker services once
docker-compose up -d

# 2. Activate Python environment (in backend/)
venv\Scripts\activate

# 3. Start backend (leave running)
uvicorn app.main:app --reload

# 4. Code in your editor
# - Backend auto-reloads on file changes
# - Check http://localhost:8000/docs for API changes

# 5. Test your changes
python test_api.py
```

### Useful Commands

```bash
# View backend logs
docker-compose logs -f backend

# Restart a service
docker-compose restart postgres

# Stop everything
docker-compose down

# See running services
docker-compose ps

# Access Neo4j shell
docker exec -it ikip_neo4j cypher-shell -u neo4j -p neo4j_password_change_me
```

---

## 🎯 Your First Task

Once everything is running, your first task is to implement the document loader:

1. Open `backend/app/ingestion/loader.py`
2. Follow the implementation guide in [NEXT_STEPS.md](./NEXT_STEPS.md)
3. Test with `python test_api.py`

---

## ✅ Success Checklist

Before you start developing, verify:

- [x] Docker services are running (green in `docker-compose ps`)
- [x] Backend starts without errors
- [x] Health endpoint returns 200 OK
- [x] API docs are accessible at /docs
- [x] Neo4j browser loads
- [x] MinIO console loads
- [x] You can activate Python venv
- [x] test_api.py runs (even if tests fail, it should run)

**All good?** → Proceed to [NEXT_STEPS.md](./NEXT_STEPS.md)! 🚀

**Issues?** → Check troubleshooting section above or [DEVELOPMENT.md](./DEVELOPMENT.md)

---

## 📞 Need Help?

### Documentation
- **[INDEX.md](./INDEX.md)** - Navigation hub
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Detailed dev guide
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Complete overview

### External Resources
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Docker Compose**: https://docs.docker.com/compose/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

### Team
- Ask questions in team chat
- Review code together
- Pair program for complex features

---

## 🎉 You're Ready!

You now have:
- ✅ All services running
- ✅ Backend development environment set up
- ✅ Understanding of the project structure
- ✅ Knowledge of where to go next

**Time to build!** Head to [NEXT_STEPS.md](./NEXT_STEPS.md) for implementation! 💪

---

_Setup complete in < 10 minutes? Give yourself a high-five! 🙌_
