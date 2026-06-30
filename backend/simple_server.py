"""
Simplified backend server for testing frontend
This version supports Groq API for fast, free LLM responses
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="IKIP - Simple Backend with Groq", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
documents_db = {}
sessions_db = {}
knowledge_nodes = {}
knowledge_edges = []

# Groq client setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_REAL_AI = GROQ_API_KEY and GROQ_API_KEY != "your-groq-api-key-here"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if USE_REAL_AI:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq API configured - using real AI responses")
    except Exception as e:
        print(f"⚠️ Groq setup failed: {e}")
        USE_REAL_AI = False
else:
    print("⚠️ Groq API key not set - using mock responses")
    print("💡 Set GROQ_API_KEY in .env file for real AI responses")

# Models
class DocumentStatus(BaseModel):
    document_id: str
    filename: str
    status: str
    upload_date: str
    size: Optional[int] = None
    chunks: Optional[int] = None

class QueryRequest(BaseModel):
    question: str
    strategy: str = "hybrid"

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict] = []

class RCARequest(BaseModel):
    failure_description: str

class GraphStats(BaseModel):
    nodes: int
    relationships: int
    node_types: dict
    relationship_types: dict


def _upsert_node(node_id: str, label: str, node_type: str, **properties):
    existing = knowledge_nodes.get(node_id)
    if existing:
        existing["label"] = label or existing.get("label", node_id)
        existing["type"] = node_type or existing.get("type", "entity")
        existing["properties"].update(properties)
        return existing

    node = {
        "id": node_id,
        "label": label or node_id,
        "type": node_type or "entity",
        "properties": properties,
    }
    knowledge_nodes[node_id] = node
    return node


def _add_edge(source: str, target: str, relationship: str, **properties):
    edge = {
        "source": source,
        "target": target,
        "relationship": relationship,
        "properties": properties,
    }
    if edge not in knowledge_edges:
        knowledge_edges.append(edge)
    return edge


def _extract_equipment(content: str):
    patterns = [
        r"\b[A-Z]{1,3}-\d{2,4}\b",
        r"\b[A-Z]{1,3}\d{2,4}\b",
        r"\b(?:Pump|Valve|Motor|Compressor|Tank|Boiler|Seal|Filter|Generator|Heater)\s*[- ]?\d+\b",
    ]
    matches = set()
    for pattern in patterns:
        for match in re.findall(pattern, content, flags=re.IGNORECASE):
            matches.add(match.strip())
    return sorted(matches)


def _extract_regulations(content: str):
    patterns = [
        r"\bOISD[-\w]*\b",
        r"\bPESO\b",
        r"\bFactory Act\b",
        r"\bISO\s?\d{3,5}\b",
        r"\bASME\b",
    ]
    matches = set()
    for pattern in patterns:
        for match in re.findall(pattern, content, flags=re.IGNORECASE):
            matches.add(match.strip())
    return sorted(matches)


def _extract_failure_modes(content: str):
    keywords = [
        "leak",
        "overheat",
        "overheating",
        "corrosion",
        "vibration",
        "shutdown",
        "trip",
        "crack",
        "failure",
    ]
    findings = []
    lowered = content.lower()
    for keyword in keywords:
        if keyword in lowered:
            findings.append(keyword)
    return findings


def _index_document_graph(doc_id: str, filename: str, content: str):
    doc_node_id = f"doc_{doc_id}"
    _upsert_node(
        doc_node_id,
        filename,
        "document",
        document_id=doc_id,
        filename=filename,
    )

    equipment = _extract_equipment(content)
    regulations = _extract_regulations(content)
    failures = _extract_failure_modes(content)

    for item in equipment:
        node_id = f"eq_{re.sub(r'[^a-zA-Z0-9]+', '_', item).strip('_').lower()}"
        _upsert_node(node_id, item, "equipment")
        _add_edge(node_id, doc_node_id, "DOCUMENTED_IN")

    for item in regulations:
        node_id = f"reg_{re.sub(r'[^a-zA-Z0-9]+', '_', item).strip('_').lower()}"
        _upsert_node(node_id, item, "regulation")
        _add_edge(node_id, doc_node_id, "MENTIONED_IN")

    for item in failures:
        node_id = f"failure_{item}"
        _upsert_node(node_id, item.title(), "failure_mode")
        _add_edge(doc_node_id, node_id, "MENTIONS")

    for item in equipment[:1]:
        for failure in failures[:2]:
            source_id = f"eq_{re.sub(r'[^a-zA-Z0-9]+', '_', item).strip('_').lower()}"
            target_id = f"failure_{failure}"
            if target_id in knowledge_nodes:
                _add_edge(source_id, target_id, "HAS_FAILURE")

@app.get("/")
async def root():
    return {
        "name": "IKIP",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document"""
    doc_id = str(uuid.uuid4())
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Store document info
    documents_db[doc_id] = {
        "document_id": doc_id,
        "filename": file.filename,
        "status": "completed",  # Simulating instant processing
        "upload_date": datetime.now().isoformat(),
        "size": file_size,
        "chunks": file_size // 500,  # Simulate chunking
        "content": content.decode('utf-8', errors='ignore')[:1000]  # Store snippet
    }

    _index_document_graph(
        doc_id=doc_id,
        filename=file.filename,
        content=documents_db[doc_id]["content"],
    )
    
    return {
        "document_id": doc_id,
        "filename": file.filename,
        "status": "processing",
        "message": "Document uploaded successfully"
    }

@app.get("/api/v1/documents/{document_id}/status")
async def get_document_status(document_id: str):
    """Get document processing status"""
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return documents_db[document_id]

@app.get("/api/v1/documents")
async def list_documents():
    """List all documents"""
    return {
        "documents": [
            {
                "id": doc_id,
                "filename": doc["filename"],
                "status": doc["status"],
                "upload_date": doc["upload_date"],
                "size": doc.get("size"),
                "chunks": doc.get("chunks")
            }
            for doc_id, doc in documents_db.items()
        ]
    }

@app.delete("/api/v1/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    filename = documents_db[document_id]["filename"]
    doc_node_id = f"doc_{document_id}"
    del documents_db[document_id]
    knowledge_nodes.pop(doc_node_id, None)
    knowledge_edges[:] = [
        edge
        for edge in knowledge_edges
        if edge["source"] != doc_node_id and edge["target"] != doc_node_id
    ]
    
    return {"message": f"Document {filename} deleted successfully"}

@app.post("/api/v1/query")
async def query_documents(request: QueryRequest):
    """Query documents with Groq AI"""
    if not documents_db:
        return QueryResponse(
            answer="Please upload documents first before asking questions.",
            citations=[]
        )
    
    # Get document contents
    doc_contents = []
    for doc_id, doc in documents_db.items():
        doc_contents.append(f"Document: {doc['filename']}\n{doc.get('content', '')}")
    
    context = "\n\n".join(doc_contents[:3])  # Use first 3 documents
    
    if USE_REAL_AI:
        try:
            # Use Groq API for real AI response
            system_prompt = """You are an expert industrial AI assistant. 
            You help with equipment maintenance, safety procedures, and operational questions.
            Answer based on the provided document context. Be specific and cite information from the documents."""
            
            user_prompt = f"""Context from uploaded documents:
{context}

Question: {request.question}

Please provide a detailed answer based on the context above. If the information isn't in the documents, say so."""

            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            # Extract citations from context
            doc_names = [doc["filename"] for doc in documents_db.values()]
            citations = [
                {
                    "text": context[:200] + "...",
                    "source": doc_names[0] if doc_names else "document.txt",
                    "score": 0.85
                }
            ]
            
            return QueryResponse(answer=answer, citations=citations)
            
        except Exception as e:
            return QueryResponse(
                answer=f"Error calling Groq API: {str(e)}. Please check your API key.",
                citations=[]
            )
    else:
        # Mock response if no API key
        doc_names = [doc["filename"] for doc in documents_db.values()]
        
        return QueryResponse(
            answer=f"Based on your question '{request.question}', I found relevant information in the uploaded documents. "
                   f"The documents contain detailed information about industrial equipment maintenance, safety procedures, and operational guidelines. "
                   f"\n\n💡 Set GROQ_API_KEY in .env file to get real AI-powered answers!",
            citations=[
                {
                    "text": f"Sample content from {doc_names[0] if doc_names else 'document'}...",
                    "source": doc_names[0] if doc_names else "document.txt",
                    "score": 0.85
                }
            ]
        )

@app.post("/api/v1/rca/analyze")
async def analyze_rca(request: RCARequest):
    """Root cause analysis with Groq AI"""
    
    if USE_REAL_AI:
        try:
            # Use Groq API for real RCA analysis
            system_prompt = """You are an expert in root cause analysis for industrial failures.
            Provide detailed 5-Why analysis, Fishbone diagram factors, and actionable recommendations."""
            
            user_prompt = f"""Perform a root cause analysis for the following failure:

{request.failure_description}

Please provide:
1. Five levels of "Why" analysis
2. Contributing factors in 6 categories (People, Process, Equipment, Materials, Environment, Management)
3. 5 specific recommendations
4. A brief evidence summary

Format your response clearly with these sections."""

            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the response (simplified - in production would use structured output)
            # For now, use the AI response to generate structured data
            return {
                "failure_description": request.failure_description,
                "five_why_analysis": {
                    "why_1": "Why did the failure occur? - Primary symptom identified",
                    "why_2": "Why did that happen? - Underlying condition discovered",
                    "why_3": "Why did that condition exist? - Process or system gap found",
                    "why_4": "Why was there a gap? - Root organizational issue",
                    "why_5": "Why was this not prevented? - Systematic root cause"
                },
                "fishbone_diagram": {
                    "people": ["Training gaps", "Awareness issues", "Skill deficiencies"],
                    "process": ["Inadequate procedures", "Missing checks", "Poor documentation"],
                    "equipment": ["Design limitations", "Wear and tear", "Inadequate capacity"],
                    "materials": ["Quality issues", "Wrong specifications", "Supply problems"],
                    "environment": ["Temperature effects", "Contamination", "Poor conditions"],
                    "management": ["Resource constraints", "Poor planning", "Inadequate oversight"]
                },
                "recommendations": [
                    "Implement preventive maintenance program",
                    "Enhance training for all personnel",
                    "Update procedures and documentation",
                    "Install monitoring and early warning systems",
                    "Conduct regular audits and inspections"
                ],
                "evidence_summary": analysis_text[:500] + "...",
                "confidence_score": 0.85,
                "ai_analysis": analysis_text  # Full AI response
            }
            
        except Exception as e:
            # Fallback to mock if error
            return {
                "failure_description": request.failure_description,
                "five_why_analysis": {
                    "why_1": "Why did the failure occur? - Initial symptom observed",
                    "why_2": "Why did that happen? - Underlying condition identified",
                    "why_3": "Why did that condition exist? - Process gap discovered",
                    "why_4": "Why was there a process gap? - Training or resource issue",
                    "why_5": "Why was training insufficient? - Root cause: systematic issue"
                },
                "fishbone_diagram": {
                    "people": ["Insufficient training", "Lack of awareness"],
                    "process": ["No preventive maintenance schedule", "Inadequate procedures"],
                    "equipment": ["Aging equipment", "Design limitations"],
                    "materials": ["Substandard parts", "Supply chain issues"],
                    "environment": ["Harsh conditions", "Inadequate ventilation"],
                    "management": ["Resource constraints", "Prioritization issues"]
                },
                "recommendations": [
                    "Implement comprehensive preventive maintenance program",
                    "Provide targeted training for all personnel",
                    "Upgrade critical equipment components",
                    "Establish regular inspection schedules",
                    "Improve documentation and procedures"
                ],
                "evidence_summary": f"Analysis based on: {request.failure_description[:200]}... Error: {str(e)}",
                "confidence_score": 0.75
            }
    else:
        # Mock response if no API key
        return {
            "failure_description": request.failure_description,
            "five_why_analysis": {
                "why_1": "Why did the failure occur? - Initial symptom observed",
                "why_2": "Why did that happen? - Underlying condition identified",
                "why_3": "Why did that condition exist? - Process gap discovered",
                "why_4": "Why was there a process gap? - Training or resource issue",
                "why_5": "Why was training insufficient? - Root cause: systematic issue"
            },
            "fishbone_diagram": {
                "people": ["Insufficient training", "Lack of awareness"],
                "process": ["No preventive maintenance schedule", "Inadequate procedures"],
                "equipment": ["Aging equipment", "Design limitations"],
                "materials": ["Substandard parts", "Supply chain issues"],
                "environment": ["Harsh conditions", "Inadequate ventilation"],
                "management": ["Resource constraints", "Prioritization issues"]
            },
            "recommendations": [
                "Implement comprehensive preventive maintenance program",
                "Provide targeted training for all personnel",
                "Upgrade critical equipment components",
                "Establish regular inspection schedules",
                "Improve documentation and procedures"
            ],
            "evidence_summary": f"Analysis based on the failure description: {request.failure_description[:200]}... "
                              "💡 Set GROQ_API_KEY in .env file for AI-powered RCA!",
            "confidence_score": 0.75
        }

@app.get("/api/v1/graph/stats")
async def get_graph_stats():
    """Get knowledge graph statistics from indexed documents"""
    node_types = {}
    for node in knowledge_nodes.values():
        node_types[node["type"].title()] = node_types.get(node["type"].title(), 0) + 1

    relationship_types = {}
    for edge in knowledge_edges:
        relationship_types[edge["relationship"]] = relationship_types.get(edge["relationship"], 0) + 1

    return GraphStats(
        nodes=len(knowledge_nodes),
        relationships=len(knowledge_edges),
        node_types=node_types,
        relationship_types=relationship_types,
    )

@app.get("/api/v1/graph/visualize")
async def visualize_graph(limit: int = 100):
    """Get graph data for visualization from the in-memory graph"""
    if not knowledge_nodes:
        return {"nodes": [], "edges": []}

    nodes = list(knowledge_nodes.values())[:limit]
    allowed_ids = {node["id"] for node in nodes}
    edges = [
        edge
        for edge in knowledge_edges
        if edge["source"] in allowed_ids and edge["target"] in allowed_ids
    ][:limit]

    return {
        "nodes": nodes,
        "edges": edges,
    }

@app.get("/api/v1/graph/search")
async def search_graph(entity_name: str):
    """Search for entities in the in-memory graph"""
    needle = entity_name.lower()
    matches = [
        node
        for node in knowledge_nodes.values()
        if needle in node["label"].lower()
    ]
    return {
        "query": entity_name,
        "results": matches,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
