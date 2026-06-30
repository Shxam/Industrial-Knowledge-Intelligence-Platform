"""
Knowledge Graph endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any

from app.kg.neo4j_client import neo4j_client
from app.core.logging import logger

router = APIRouter()


@router.get("/entities")
async def list_entities(
    entity_type: Optional[str] = None,
    limit: int = 100
):
    """List entities from the knowledge graph"""
    try:
        entities = neo4j_client.find_entities(
            entity_type=entity_type,
            limit=limit
        )
        
        return {
            "entities": entities,
            "total": len(entities)
        }
    except Exception as e:
        logger.error(f"Error listing entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entities/{entity_id}")
async def get_entity(entity_id: str):
    """Get detailed information about an entity"""
    try:
        # Get entity
        entity = neo4j_client.get_entity(entity_id)
        
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Get relationships
        relationships = neo4j_client.get_related_entities(
            entity_id=entity_id,
            direction="both"
        )
        
        return {
            "entity": entity,
            "relationships": relationships
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entity {entity_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_graph(
    query: str,
    entity_types: Optional[List[str]] = None,
    limit: int = 20
):
    """Search the knowledge graph"""
    try:
        results = []
        
        # If entity types specified, search each type
        if entity_types:
            for entity_type in entity_types:
                entities = neo4j_client.find_entities(
                    entity_type=entity_type,
                    text_pattern=query,
                    limit=limit
                )
                results.extend(entities)
        else:
            # Search all types
            results = neo4j_client.find_entities(
                text_pattern=query,
                limit=limit
            )
        
        return {
            "query": query,
            "results": results[:limit]  # Ensure limit
        }
    except Exception as e:
        logger.error(f"Error searching graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/path")
async def find_path(
    source_id: str,
    target_id: str,
    max_depth: int = 5
):
    """Find shortest path between two entities"""
    try:
        path = neo4j_client.find_shortest_path(
            source_id=source_id,
            target_id=target_id,
            max_depth=max_depth
        )
        
        if not path:
            return {
                "source": source_id,
                "target": target_id,
                "path": [],
                "found": False
            }
        
        return {
            "source": source_id,
            "target": target_id,
            "path": path,
            "found": True
        }
    except Exception as e:
        logger.error(f"Error finding path: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualize")
async def visualize_graph(
    center_entity_id: Optional[str] = None,
    depth: int = 2,
    entity_types: Optional[List[str]] = None
):
    """Get graph data for visualization"""
    try:
        graph_data = neo4j_client.get_graph_for_visualization(
            center_entity_id=center_entity_id,
            depth=depth,
            entity_types=entity_types,
            limit=100
        )
        
        return graph_data
    except Exception as e:
        logger.error(f"Error getting visualization data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_graph_stats():
    """Get knowledge graph statistics"""
    try:
        stats = neo4j_client.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting graph stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
