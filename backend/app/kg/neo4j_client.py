"""
Neo4j client for knowledge graph operations
"""
from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from app.core.config import settings
from app.core.logging import logger


class Neo4jClient:
    """
    Neo4j database client for knowledge graph
    
    Manages:
    - Connection to Neo4j
    - Entity and relationship CRUD
    - Graph queries
    - Schema management
    """
    
    def __init__(self):
        """Initialize Neo4j client"""
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self.driver = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Neo4j"""
        try:
            logger.info(f"Connecting to Neo4j at {self.uri}")
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                result.single()
            logger.info("Connected to Neo4j successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    @contextmanager
    def session(self):
        """Context manager for Neo4j session"""
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def create_schema(self):
        """
        Create graph schema with indexes and constraints
        
        Indexes improve query performance
        Constraints ensure data integrity
        """
        logger.info("Creating Neo4j schema")
        
        with self.session() as session:
            # Create constraints (unique identifiers)
            constraints = [
                "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
                "CREATE CONSTRAINT equipment_tag IF NOT EXISTS FOR (e:Equipment) REQUIRE e.tag IS UNIQUE",
                "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.debug(f"Created: {constraint}")
                except Exception as e:
                    logger.debug(f"Constraint may already exist: {e}")
            
            # Create indexes
            indexes = [
                "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
                "CREATE INDEX entity_text IF NOT EXISTS FOR (e:Entity) ON (e.text)",
                "CREATE INDEX document_title IF NOT EXISTS FOR (d:Document) ON (d.title)",
            ]
            
            for index in indexes:
                try:
                    session.run(index)
                    logger.debug(f"Created: {index}")
                except Exception as e:
                    logger.debug(f"Index may already exist: {e}")
        
        logger.info("Schema creation complete")
    
    def create_entity(
        self,
        entity_id: str,
        entity_type: str,
        text: str,
        properties: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create an entity node in the graph
        
        Args:
            entity_id: Unique identifier
            entity_type: Type (EQUIPMENT, PARAMETER, etc.)
            text: Entity text
            properties: Additional properties
        
        Returns:
            Created node properties
        """
        properties = properties or {}
        properties.update({
            'id': entity_id,
            'type': entity_type,
            'text': text
        })
        
        with self.session() as session:
            query = f"""
            MERGE (e:Entity {{id: $entity_id}})
            SET e += $properties
            SET e:{entity_type}
            RETURN e
            """
            result = session.run(query, entity_id=entity_id, properties=properties)
            node = result.single()
            return dict(node['e']) if node else None
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        properties: Dict[str, Any] = None
    ) -> bool:
        """
        Create a relationship between two entities
        
        Args:
            source_id: Source entity ID
            target_id: Target entity ID
            relation_type: Relationship type
            properties: Additional properties
        
        Returns:
            Success boolean
        """
        properties = properties or {}
        
        with self.session() as session:
            query = f"""
            MATCH (source:Entity {{id: $source_id}})
            MATCH (target:Entity {{id: $target_id}})
            MERGE (source)-[r:{relation_type}]->(target)
            SET r += $properties
            RETURN r
            """
            try:
                result = session.run(
                    query,
                    source_id=source_id,
                    target_id=target_id,
                    properties=properties
                )
                return result.single() is not None
            except Exception as e:
                logger.error(f"Error creating relationship: {e}")
                return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID"""
        with self.session() as session:
            query = "MATCH (e:Entity {id: $entity_id}) RETURN e"
            result = session.run(query, entity_id=entity_id)
            node = result.single()
            return dict(node['e']) if node else None
    
    def find_entities(
        self,
        entity_type: Optional[str] = None,
        text_pattern: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Find entities matching criteria
        
        Args:
            entity_type: Filter by type
            text_pattern: Search text (case-insensitive)
            limit: Max results
        
        Returns:
            List of entity dicts
        """
        with self.session() as session:
            conditions = []
            params = {'limit': limit}
            
            if entity_type:
                conditions.append("e.type = $entity_type")
                params['entity_type'] = entity_type
            
            if text_pattern:
                conditions.append("toLower(e.text) CONTAINS toLower($text_pattern)")
                params['text_pattern'] = text_pattern
            
            where_clause = " AND ".join(conditions) if conditions else "true"
            
            query = f"""
            MATCH (e:Entity)
            WHERE {where_clause}
            RETURN e
            LIMIT $limit
            """
            
            result = session.run(query, **params)
            return [dict(record['e']) for record in result]
    
    def get_related_entities(
        self,
        entity_id: str,
        relation_type: Optional[str] = None,
        direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """
        Get entities related to a given entity
        
        Args:
            entity_id: Source entity ID
            relation_type: Filter by relationship type
            direction: "outgoing", "incoming", or "both"
        
        Returns:
            List of (relationship, target_entity) tuples
        """
        with self.session() as session:
            if direction == "outgoing":
                arrow = "-[r]->"
            elif direction == "incoming":
                arrow = "<-[r]-"
            else:
                arrow = "-[r]-"
            
            rel_filter = f":{relation_type}" if relation_type else ""
            
            query = f"""
            MATCH (source:Entity {{id: $entity_id}}){arrow}(target:Entity)
            RETURN type(r) as relation_type, properties(r) as rel_props, target
            """
            
            result = session.run(query, entity_id=entity_id)
            
            relations = []
            for record in result:
                relations.append({
                    'relation_type': record['relation_type'],
                    'properties': record['rel_props'],
                    'target': dict(record['target'])
                })
            
            return relations
    
    def find_shortest_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Find shortest path between two entities
        
        Returns:
            List of nodes and relationships in path
        """
        with self.session() as session:
            query = """
            MATCH path = shortestPath(
                (source:Entity {id: $source_id})-[*..%d]-(target:Entity {id: $target_id})
            )
            RETURN path
            """ % max_depth
            
            result = session.run(query, source_id=source_id, target_id=target_id)
            record = result.single()
            
            if not record:
                return None
            
            path = record['path']
            path_data = []
            
            for node in path.nodes:
                path_data.append({'type': 'node', 'data': dict(node)})
            
            for rel in path.relationships:
                path_data.append({
                    'type': 'relationship',
                    'data': {
                        'type': type(rel).__name__,
                        'properties': dict(rel)
                    }
                })
            
            return path_data
    
    def get_graph_for_visualization(
        self,
        center_entity_id: Optional[str] = None,
        depth: int = 2,
        entity_types: Optional[List[str]] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get graph data formatted for frontend visualization
        
        Returns dict with 'nodes' and 'edges' arrays
        """
        with self.session() as session:
            if center_entity_id:
                # Get subgraph around a center node
                query = """
                MATCH (center:Entity {id: $center_id})
                OPTIONAL MATCH path = (center)-[*1..%d]-(connected:Entity)
                WITH collect(center) + collect(connected) as nodes, 
                     collect(relationships(path)) as rels
                UNWIND nodes as n
                WITH collect(DISTINCT n) as unique_nodes, rels
                UNWIND rels as rel_list
                UNWIND rel_list as r
                RETURN unique_nodes, collect(DISTINCT r) as unique_rels
                LIMIT $limit
                """ % depth
                
                result = session.run(query, center_id=center_entity_id, limit=limit)
            else:
                # Get random sample of graph
                type_filter = ""
                params = {'limit': limit}
                
                if entity_types:
                    type_filter = "WHERE e.type IN $entity_types"
                    params['entity_types'] = entity_types
                
                query = f"""
                MATCH (e:Entity)
                {type_filter}
                WITH e LIMIT $limit
                OPTIONAL MATCH (e)-[r]-(connected:Entity)
                RETURN collect(DISTINCT e) + collect(DISTINCT connected) as nodes,
                       collect(DISTINCT r) as rels
                """
                
                result = session.run(query, **params)
            
            record = result.single()
            if not record:
                return {'nodes': [], 'edges': []}
            
            # Format for visualization (Cytoscape.js format)
            nodes = []
            for node in record['nodes'] or []:
                if node:
                    nodes.append({
                        'data': {
                            'id': node['id'],
                            'label': node.get('text', node['id']),
                            'type': node.get('type', 'Entity'),
                            **{k: v for k, v in dict(node).items() if k not in ['id', 'text', 'type']}
                        }
                    })
            
            edges = []
            for rel in record.get('unique_rels', []) or []:
                if rel:
                    edges.append({
                        'data': {
                            'id': f"{rel.start_node['id']}-{rel.end_node['id']}",
                            'source': rel.start_node['id'],
                            'target': rel.end_node['id'],
                            'label': type(rel).__name__,
                            **dict(rel)
                        }
                    })
            
            return {
                'nodes': nodes,
                'edges': edges
            }
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete entity and all its relationships"""
        with self.session() as session:
            query = """
            MATCH (e:Entity {id: $entity_id})
            DETACH DELETE e
            """
            session.run(query, entity_id=entity_id)
            return True
    
    def clear_graph(self):
        """Delete all nodes and relationships (USE WITH CAUTION!)"""
        logger.warning("Clearing entire Neo4j graph!")
        with self.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Graph cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        with self.session() as session:
            query = """
            MATCH (n)
            OPTIONAL MATCH ()-[r]->()
            RETURN count(DISTINCT n) as node_count,
                   count(DISTINCT r) as relationship_count,
                   collect(DISTINCT labels(n)) as node_labels,
                   collect(DISTINCT type(r)) as relationship_types
            """
            result = session.run(query)
            record = result.single()
            
            if record:
                # Flatten label lists
                labels = []
                for label_list in record['node_labels']:
                    labels.extend(label_list)
                
                return {
                    'node_count': record['node_count'],
                    'relationship_count': record['relationship_count'],
                    'node_types': list(set(labels)),
                    'relationship_types': [rt for rt in record['relationship_types'] if rt]
                }
            
            return {
                'node_count': 0,
                'relationship_count': 0,
                'node_types': [],
                'relationship_types': []
            }


# Global Neo4j client
neo4j_client = Neo4jClient()
