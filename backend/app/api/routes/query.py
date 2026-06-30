"""
Query and RAG endpoints
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import asyncio

from app.core.logging import logger

router = APIRouter()


class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    session_id: Optional[str] = None
    strategy: Optional[str] = "auto"  # auto | vector | hybrid | graph | rca
    stream: bool = True
    top_k: int = 10
    confidence_threshold: float = 0.7


class Citation(BaseModel):
    """Citation model"""
    document_id: str
    document_title: str
    page: Optional[int] = None
    chunk_id: str
    text: str
    relevance_score: float


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    citations: List[Citation]
    confidence: float
    strategy_used: str
    processing_time_ms: float
    session_id: str


async def generate_streaming_response(query: str, session_id: str, request: QueryRequest):
    """Generate streaming SSE response with real RAG"""
    
    try:
        from app.rag.pipeline import rag_pipeline
        import time
        
        start_time = time.time()
        
        # Get query embedding
        query_embedding = rag_pipeline.embedding_service.embed_text(query)
        
        # Retrieve relevant chunks
        if request.strategy == "auto" or request.strategy == "hybrid":
            if rag_pipeline.vector_store.get_stats()['total_documents'] > 0:
                results = rag_pipeline.hybrid_retriever.search(
                    query=query,
                    query_embedding=query_embedding,
                    top_k=request.top_k
                )
            else:
                results = []
        elif request.strategy == "vector":
            results = rag_pipeline.vector_store.search(query_embedding, k=request.top_k)
        else:
            results = rag_pipeline.bm25_search.search(query, k=request.top_k)
        
        if not results:
            # No documents indexed
            yield f"data: {json.dumps({'type': 'content', 'content': 'No documents have been uploaded yet. Please upload documents first.', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
            yield f"data: {json.dumps({'type': 'metadata', 'confidence': 0.0, 'strategy_used': request.strategy, 'processing_time_ms': (time.time() - start_time) * 1000, 'session_id': session_id})}\n\n"
            yield "data: [DONE]\n\n"
            return
        
        # Build context
        context_chunks = results[:5]
        
        # Generate answer with streaming
        system_prompt = """You are an expert assistant helping with industrial documentation. 
Answer questions based ONLY on the provided context. 
If the context doesn't contain enough information, say so.
Be specific and cite relevant parts."""
        
        context_text = rag_pipeline.llm_client._build_context(context_chunks)
        prompt = f"""Context:
{context_text}

Question: {query}

Answer based only on the context above:"""
        
        # Stream LLM response
        async for chunk in rag_pipeline.llm_client.generate_stream(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        ):
            data = {
                "type": "content",
                "content": chunk,
                "timestamp": datetime.utcnow().isoformat()
            }
            yield f"data: {json.dumps(data)}\n\n"
        
        # Send citations
        citations = []
        for result in context_chunks:
            meta = result['metadata']
            citations.append({
                "document_id": meta.get('document_id', 'unknown'),
                "document_title": meta.get('filename', 'Unknown Document'),
                "page": meta.get('page'),
                "chunk_id": meta.get('chunk_id'),
                "text": meta.get('text', '')[:200] + '...',
                "relevance_score": result.get('score', result.get('rrf_score', 0.0))
            })
        
        citation_data = {
            "type": "citations",
            "citations": citations,
            "timestamp": datetime.utcnow().isoformat()
        }
        yield f"data: {json.dumps(citation_data)}\n\n"
        
        # Send metadata
        processing_time = (time.time() - start_time) * 1000
        metadata = {
            "type": "metadata",
            "confidence": 0.85,  # TODO: Calculate actual confidence
            "strategy_used": request.strategy,
            "processing_time_ms": processing_time,
            "session_id": session_id,
            "num_sources": len(results)
        }
        yield f"data: {json.dumps(metadata)}\n\n"
        
        # End stream
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        logger.error(f"Error in streaming response: {e}")
        error_data = {
            "type": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
        yield f"data: {json.dumps(error_data)}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main query endpoint with RAG
    
    Supports streaming and non-streaming responses
    """
    
    if request.stream:
        # Return SSE stream
        session_id = request.session_id or f"session-{datetime.utcnow().timestamp()}"
        return StreamingResponse(
            generate_streaming_response(request.query, session_id, request),
            media_type="text/event-stream"
        )
    else:
        # Return complete response using RAG pipeline
        try:
            from app.rag.pipeline import rag_pipeline
            
            result = rag_pipeline.query(
                question=request.query,
                top_k=request.top_k,
                strategy=request.strategy if request.strategy != "auto" else "hybrid",
                confidence_threshold=request.confidence_threshold
            )
            
            # Format citations
            citations = [
                Citation(
                    document_id=c['document_id'],
                    document_title=c['document_title'],
                    page=c.get('page'),
                    chunk_id=c['chunk_id'],
                    text=c['text'],
                    relevance_score=c['relevance_score']
                )
                for c in result['citations']
            ]
            
            return QueryResponse(
                answer=result['answer'],
                citations=citations,
                confidence=result['confidence'],
                strategy_used=result['strategy_used'],
                processing_time_ms=result['processing_time_ms'],
                session_id=request.session_id or f"session-{datetime.utcnow().timestamp()}"
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/rca")
async def root_cause_analysis(equipment_tag: str, failure_mode: str):
    """
    Root Cause Analysis endpoint
    
    Fuses work orders, failure history, OEM data, inspections
    """
    
    # TODO: Implement RCA agent
    
    return {
        "equipment_tag": equipment_tag,
        "failure_mode": failure_mode,
        "analysis": {
            "immediate_cause": "Seal deterioration",
            "root_causes": [
                "Operating temperature exceeds design specification",
                "Inadequate preventive maintenance schedule"
            ],
            "contributing_factors": [
                "Delayed replacement of cooling system",
                "Operator training gap on monitoring"
            ],
            "evidence": [
                {
                    "source": "Work Order #12345",
                    "content": "Seal temperature recorded at 85°C..."
                }
            ],
            "recommendations": [
                "Upgrade cooling system capacity",
                "Revise PM schedule to monthly inspections",
                "Conduct operator training on thermal monitoring"
            ]
        }
    }


@router.post("/compliance/check")
async def compliance_check(regulation: str, scope: str):
    """
    Compliance check endpoint
    
    Maps regulations to procedures and identifies gaps
    """
    
    # TODO: Implement compliance agent
    
    return {
        "regulation": regulation,
        "scope": scope,
        "requirements": [
            {
                "requirement_id": "OISD-STD-105-3.2.1",
                "description": "Emergency shutdown valves must be tested quarterly",
                "status": "compliant",
                "evidence": [
                    {
                        "document": "Q4-2025 Test Report",
                        "date": "2025-12-15"
                    }
                ]
            },
            {
                "requirement_id": "OISD-STD-105-3.2.5",
                "description": "Pressure relief valves must be recalibrated annually",
                "status": "gap",
                "gap_description": "Last calibration was 14 months ago",
                "risk_level": "medium"
            }
        ],
        "overall_compliance": 85.5,
        "gaps_count": 3
    }
