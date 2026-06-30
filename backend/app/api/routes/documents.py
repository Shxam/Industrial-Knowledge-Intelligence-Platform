"""
Document ingestion endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
from datetime import datetime
import uuid

from app.rag.pipeline import rag_pipeline
from app.core.logging import logger

router = APIRouter()

# In-memory status tracking (use Redis in production)
document_status = {}


async def process_document_background(doc_id: str, file_data: bytes, filename: str, content_type: str):
    """Background task for document processing"""
    try:
        document_status[doc_id] = {
            "status": "processing",
            "progress": 50,
            "stages": {
                "upload": "completed",
                "extraction": "in_progress",
                "chunking": "pending",
                "embedding": "pending",
                "indexing": "pending"
            }
        }
        
        # Process document
        from io import BytesIO
        file_io = BytesIO(file_data)
        
        result = rag_pipeline.ingest_document(
            file_data=file_io,
            filename=filename,
            document_id=doc_id,
            metadata={"content_type": content_type}
        )
        
        # Update status
        document_status[doc_id] = {
            "status": "completed",
            "progress": 100,
            "stages": {
                "upload": "completed",
                "extraction": "completed",
                "chunking": "completed",
                "embedding": "completed",
                "indexing": "completed"
            },
            "stats": result
        }
        
        logger.info(f"Document {doc_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Error processing document {doc_id}: {e}")
        document_status[doc_id] = {
            "status": "failed",
            "error": str(e),
            "progress": 0
        }


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a document for ingestion and processing
    
    Supports: PDF, XLSX, DOCX
    """
    
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Supported: PDF, XLSX, DOCX"
        )
    
    # Generate document ID
    doc_id = str(uuid.uuid4())
    
    # Read file data
    file_data = await file.read()
    
    # Initialize status
    document_status[doc_id] = {
        "status": "queued",
        "progress": 10,
        "stages": {
            "upload": "completed",
            "extraction": "pending",
            "chunking": "pending",
            "embedding": "pending",
            "indexing": "pending"
        }
    }
    
    # Queue background processing
    background_tasks.add_task(
        process_document_background,
        doc_id,
        file_data,
        file.filename,
        file.content_type
    )
    
    logger.info(f"Document {doc_id} queued for processing: {file.filename}")
    
    return {
        "document_id": doc_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "queued",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/{document_id}/status")
async def get_document_status(document_id: str):
    """Get processing status of a document"""
    
    status = document_status.get(document_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "document_id": document_id,
        **status
    }


@router.get("/")
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    doc_type: str = None
):
    """List all ingested documents"""
    
    # TODO: Implement actual document listing from database
    
    return {
        "total": 0,
        "documents": []
    }


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and all associated data"""
    
    try:
        result = rag_pipeline.delete_document(document_id)
        
        # Remove from status tracking
        if document_id in document_status:
            del document_status[document_id]
        
        return result
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
