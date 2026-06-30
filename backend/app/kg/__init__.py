"""
Knowledge Graph module
Handles entity extraction, relationship extraction, and graph operations
"""
from app.kg.ner import ner, IndustrialNER, Entity
from app.kg.relations import relationship_extractor, RelationshipExtractor, Relationship
from app.kg.neo4j_client import neo4j_client, Neo4jClient
from app.kg.entity_resolution import entity_resolver, EntityResolver

__all__ = [
    'ner',
    'IndustrialNER',
    'Entity',
    'relationship_extractor',
    'RelationshipExtractor',
    'Relationship',
    'neo4j_client',
    'Neo4jClient',
    'entity_resolver',
    'EntityResolver'
]
