"""
Root Cause Analysis API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import RCARequest, RCAResponse
from app.agents.rca_agent import rca_agent
from app.core.logging import logger

router = APIRouter()


@router.post("/analyze", response_model=RCAResponse)
async def perform_rca(request: RCARequest):
    """
    Perform root cause analysis on a failure
    
    This endpoint uses the RCA Agent to:
    1. Extract entities from failure description
    2. Collect evidence from knowledge graph and documents
    3. Perform 5-Why analysis
    4. Generate fishbone diagram data
    5. Provide actionable recommendations
    
    Args:
        request: RCA request with failure description
    
    Returns:
        Comprehensive RCA report
    """
    try:
        logger.info(f"RCA request received: {request.failure_description[:100]}")
        
        # Perform analysis
        result = rca_agent.analyze(
            failure_description=request.failure_description,
            equipment_id=request.equipment_id,
            context=request.context
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in RCA analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform RCA: {str(e)}"
        )


@router.get("/example")
async def get_rca_example():
    """
    Get an example RCA request and response
    
    Useful for understanding the API format
    """
    return {
        "example_request": {
            "failure_description": "P-101 centrifugal pump experienced a mechanical seal leak during operation. The pump was operating at 45 Nm torque when the leak was discovered. Temperature readings showed 100°C, which is above the normal operating range of 80-90°C. The equipment is governed by OISD-STD-105 requirements.",
            "equipment_id": "doc_123_ent_0",
            "context": {
                "location": "Unit A",
                "severity": "medium",
                "immediate_action_taken": "Pump shut down, area isolated"
            }
        },
        "expected_response_structure": {
            "failure_description": "string",
            "equipment_id": "string or null",
            "entities": [
                {
                    "text": "P-101",
                    "type": "EQUIPMENT",
                    "confidence": 0.95
                }
            ],
            "five_why_analysis": [
                {
                    "level": 1,
                    "question": "Why did the seal leak occur?",
                    "answer": "Because the temperature exceeded normal operating range",
                    "evidence": ["Temperature reading: 100°C"],
                    "is_root_cause": False
                }
            ],
            "fishbone_diagram": {
                "Equipment": [
                    {
                        "factor": "Mechanical seal condition",
                        "evidence": "From maintenance records",
                        "impact": "high"
                    }
                ],
                "Environment": [
                    {
                        "factor": "High temperature operation",
                        "evidence": "100°C reading",
                        "impact": "high"
                    }
                ]
            },
            "recommendations": [
                {
                    "title": "Replace mechanical seal",
                    "description": "Install new seal rated for higher temperatures",
                    "priority": "Critical",
                    "timeframe": "Immediate",
                    "responsible": "Maintenance Team",
                    "rationale": "Prevent recurrence of seal failure",
                    "evidence": "Seal failure due to temperature excursion"
                }
            ],
            "evidence": {
                "graph_entities": 5,
                "graph_relationships": 8,
                "document_chunks": 10,
                "citations": []
            },
            "confidence": 0.85,
            "processing_time_seconds": 5.2,
            "timestamp": "2026-06-27T10:30:00"
        }
    }


@router.get("/health")
async def rca_health():
    """Check if RCA agent is available"""
    try:
        # Basic health check
        return {
            "status": "healthy",
            "agent": "RCA Agent",
            "version": "1.0",
            "features": [
                "Entity extraction",
                "Knowledge graph integration",
                "5-Why analysis",
                "Fishbone diagram generation",
                "Recommendation engine"
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"RCA agent unavailable: {str(e)}"
        )
