# Next Steps - Immediate Action Plan

## 🎯 Current Status
✅ **Foundation Complete** - Project structure, Docker setup, API skeleton, core modules initialized

## 🚀 What to Do Right Now

### Step 1: Get the Environment Running (15 minutes)

```bash
# 1. Create .env file
copy .env.example .env

# 2. Edit .env and add your OpenAI API key (or set LLM_PROVIDER=ollama for local)
# Required: OPENAI_API_KEY=sk-...

# 3. Start Docker services
docker-compose up -d

# 4. Wait for services to be healthy (30 seconds)
docker-compose ps

# 5. Setup Python environment
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 6. Start the backend
uvicorn app.main:app --reload
```

**Verify**: Open http://localhost:8000/docs - you should see the API documentation

---

### Step 2: Implement Core RAG Pipeline (Next 4-6 hours)

This is the **critical path** for getting a working demo.

#### A. Document Loader (1 hour)

**File**: `backend/app/ingestion/loader.py`

```python
"""
Implement:
- load_pdf(file_path) -> text
- load_xlsx(file_path) -> text 
- save_to_minio(file, bucket)
"""
```

**Key libraries**:
- PyMuPDF (fitz) for PDF
- openpyxl for Excel
- minio for storage

#### B. Vector Store (1.5 hours)

**File**: `backend/app/rag/vector_store.py`

```python
"""
Implement:
- FaissVectorStore class
  - create_index()
  - add_documents(chunks, embeddings)
  - search(query_embedding, k=10)
  - save() / load()
"""
```

**Key points**:
- Use FAISS Flat index for simplicity first
- Store chunk metadata separately (dict or JSON)
- Save index to disk at `data/faiss_index/`

#### C. BM25 Search (45 minutes)

**File**: `backend/app/rag/bm25_search.py`

```python
"""
Implement:
- BM25Search class
  - index_documents(chunks)
  - search(query, k=10)
"""
```

**Key library**: rank-bm25

#### D. LLM Client (1 hour)

**File**: `backend/app/rag/llm_client.py`

```python
"""
Implement:
- LLMClient class
  - generate(prompt, stream=False)
  - generate_with_citations(context, query)
"""
```

**Support**:
- OpenAI (primary)
- Ollama (optional, for local)

#### E. RAG Pipeline (1.5 hours)

**File**: `backend/app/rag/pipeline.py`

```python
"""
Implement:
- RAGPipeline class
  - ingest_document(file)
  - query(question, top_k=10)
  - hybrid_search(query)  # Vector + BM25
"""
```

**Flow**:
```
1. Query comes in
2. Embed query with BGE
3. Search FAISS (get top-k)
4. Search BM25 (get top-k) 
5. Combine results (simple: take union)
6. Build context from top chunks
7. Generate answer with LLM
8. Extract citations
9. Return response
```

#### F. Wire Up Endpoints (30 minutes)

**Update**: `backend/app/api/routes/documents.py` and `query.py`

Connect the skeleton endpoints to actual RAG pipeline.

---

### Step 3: Test End-to-End (30 minutes)

```bash
# 1. Create a test PDF
# Use any industrial document or create a sample

# 2. Upload it
curl -F "file=@test.pdf" http://localhost:8000/api/v1/documents/upload

# 3. Wait for processing (implement status check)

# 4. Query it
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this document about?",
    "stream": false,
    "top_k": 5
  }'

# 5. Verify you get:
#    - An answer
#    - Citations with source chunks
#    - Confidence score
```

**Success Criteria**:
- Document uploads successfully
- Query returns relevant answer
- Citations point to correct source chunks
- Response time < 10 seconds

---

## 📋 Detailed Implementation Guide

### Document Loader Implementation

```python
# backend/app/ingestion/loader.py
import fitz  # PyMuPDF
from minio import Minio
from app.core.config import settings
import uuid

class DocumentLoader:
    def __init__(self):
        self.minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
    
    def load_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
    def save_to_minio(self, file_data, filename: str):
        """Save file to MinIO"""
        object_name = f"{uuid.uuid4()}_{filename}"
        self.minio_client.put_object(
            settings.MINIO_BUCKET,
            object_name,
            file_data,
            length=-1,
            part_size=10*1024*1024
        )
        return object_name
```

### FAISS Vector Store Implementation

```python
# backend/app/rag/vector_store.py
import faiss
import numpy as np
import pickle
from pathlib import Path
from app.core.config import settings

class FaissVectorStore:
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.index = None
        self.metadata = []
        
    def create_index(self):
        """Create FAISS index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        
    def add_documents(self, embeddings: np.ndarray, metadata: list):
        """Add document embeddings to index"""
        if self.index is None:
            self.create_index()
        
        self.index.add(embeddings.astype('float32'))
        self.metadata.extend(metadata)
    
    def search(self, query_embedding: np.ndarray, k: int = 10):
        """Search for similar documents"""
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'),
            k
        )
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results.append({
                    'metadata': self.metadata[idx],
                    'distance': float(dist),
                    'score': 1 / (1 + float(dist))  # Convert to similarity
                })
        
        return results
    
    def save(self, path: str = None):
        """Save index to disk"""
        path = path or settings.FAISS_INDEX_PATH
        Path(path).mkdir(parents=True, exist_ok=True)
        
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/metadata.pkl", 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load(self, path: str = None):
        """Load index from disk"""
        path = path or settings.FAISS_INDEX_PATH
        
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/metadata.pkl", 'rb') as f:
            self.metadata = pickle.load(f)
```

### RAG Pipeline Implementation

```python
# backend/app/rag/pipeline.py
from app.rag.embeddings import embedding_service
from app.rag.chunking import chunker
from app.rag.vector_store import FaissVectorStore
from app.rag.llm_client import llm_client

class RAGPipeline:
    def __init__(self):
        self.vector_store = FaissVectorStore()
        self.vector_store.load()  # Load existing index if available
        
    def ingest_document(self, text: str, doc_id: str, metadata: dict):
        """Process and index a document"""
        # 1. Chunk the text
        chunks = chunker.chunk_for_retrieval(text, doc_id, metadata)
        
        # 2. Extract chunk texts
        chunk_texts = [c['text'] for c in chunks]
        
        # 3. Generate embeddings
        embeddings = embedding_service.embed_batch(chunk_texts)
        
        # 4. Add to vector store
        self.vector_store.add_documents(embeddings, chunks)
        
        # 5. Save index
        self.vector_store.save()
        
        return len(chunks)
    
    def query(self, question: str, top_k: int = 10):
        """Query the RAG system"""
        # 1. Embed the question
        query_embedding = embedding_service.embed_text(question)
        
        # 2. Search vector store
        results = self.vector_store.search(query_embedding, k=top_k)
        
        # 3. Build context from top results
        context_chunks = []
        for result in results[:5]:  # Top 5 for context
            context_chunks.append(result['metadata']['text'])
        
        context = "\n\n".join(context_chunks)
        
        # 4. Generate answer
        prompt = f"""Based on the following context, answer the question.
        
Context:
{context}

Question: {question}

Answer with citations to the relevant parts of the context:"""
        
        answer = llm_client.generate(prompt)
        
        # 5. Format response
        return {
            'answer': answer,
            'citations': results[:5],
            'confidence': 0.85,  # TODO: Calculate actual confidence
            'num_sources': len(results)
        }
```

---

## 🎯 Success Metrics for Today

By end of today, you should have:

- [ ] Backend running without errors
- [ ] Can upload a PDF document
- [ ] Can query the document
- [ ] Receive relevant answers with citations
- [ ] Response time < 15 seconds

---

## 🚧 Common Issues & Solutions

### Issue: FAISS import error
```bash
pip install faiss-cpu
```

### Issue: MinIO bucket doesn't exist
```python
# Add to loader.py __init__
if not self.minio_client.bucket_exists(settings.MINIO_BUCKET):
    self.minio_client.make_bucket(settings.MINIO_BUCKET)
```

### Issue: Embeddings too slow
```python
# Reduce batch size or use GPU
embeddings = embedding_service.embed_batch(texts, batch_size=8)
```

### Issue: LLM rate limits
```python
# Add retry logic with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate(self, prompt):
    # ... LLM call
```

---

## 📝 Code Review Checklist

Before moving to next phase:

- [ ] All core modules have proper error handling
- [ ] Logging added for debugging
- [ ] Type hints used throughout
- [ ] Docstrings for public functions
- [ ] Configuration pulled from settings
- [ ] No hardcoded paths or credentials
- [ ] Basic input validation
- [ ] At least one successful end-to-end test

---

## 🎓 Learning Resources

If you get stuck:

- **FAISS**: https://github.com/facebookresearch/faiss/wiki/Getting-started
- **LangChain RAG**: https://python.langchain.com/docs/use_cases/question_answering/
- **FastAPI Upload**: https://fastapi.tiangolo.com/tutorial/request-files/
- **MinIO Python**: https://min.io/docs/minio/linux/developers/python/minio-py.html

---

## 💡 Pro Tips

1. **Start Simple**: Get basic vector search working before hybrid retrieval
2. **Test Incrementally**: Test each module independently
3. **Use Sample Data**: Create a small test PDF for fast iteration
4. **Log Everything**: Add debug logging to trace issues
5. **Mock Slow Parts**: If LLM is slow, mock it initially with placeholder text

---

## ⏭️ After Core RAG Works

Once basic RAG is working (tomorrow), priorities shift to:

1. **BM25 + Hybrid Retrieval** (make search better)
2. **Cross-encoder Re-ranking** (improve relevance)
3. **Knowledge Graph** (start entity extraction)
4. **Frontend** (make it usable)

But don't move on until basic RAG works end-to-end!

---

**Current Goal**: Working RAG pipeline by end of Day 2

**Time Budget**: 6-8 hours of focused development

**Confidence**: High - all foundations are in place

Good luck! 🚀
