"""
Complete RAG pipeline
Integrates: loader → chunking → embeddings → vector store → retrieval → generation
"""
from typing import Dict, Any, List, Optional, BinaryIO
import time
from pathlib import Path
import tempfile

from app.rag.embeddings import embedding_service
from app.rag.chunking import chunker
from app.rag.vector_store import vector_store
from app.rag.bm25_search import bm25_search, HybridRetriever
from app.rag.llm_client import llm_client
from app.ingestion.loader import document_loader
from app.kg.ner import ner
from app.kg.relations import relationship_extractor
from app.kg.neo4j_client import neo4j_client
from app.kg.entity_resolution import entity_resolver
from app.core.config import settings
from app.core.logging import logger


class RAGPipeline:
    """
    End-to-end RAG pipeline
    
    Handles document ingestion, indexing, and querying
    """
    
    def __init__(self):
        """Initialize RAG pipeline"""
        self.vector_store = vector_store
        self.bm25_search = bm25_search
        self.embedding_service = embedding_service
        self.chunker = chunker
        self.llm_client = llm_client
        self.document_loader = document_loader
        
        # Knowledge Graph components
        self.ner = ner
        self.relationship_extractor = relationship_extractor
        self.neo4j_client = neo4j_client
        self.entity_resolver = entity_resolver
        
        # Initialize hybrid retriever
        self.hybrid_retriever = HybridRetriever(
            vector_store=self.vector_store,
            bm25_search=self.bm25_search
        )
        
        # Load existing indices
        self._load_indices()
        
        logger.info("RAG Pipeline initialized")
    
    def _load_indices(self):
        """Load existing vector and BM25 indices"""
        try:
            self.vector_store.load()
            logger.info("Loaded existing vector store")
        except Exception as e:
            logger.warning(f"Could not load vector store: {e}")
            logger.info("Starting with empty vector store")
        
        try:
            bm25_path = Path(settings.FAISS_INDEX_PATH) / "bm25.pkl"
            self.bm25_search.load(str(bm25_path))
            logger.info("Loaded existing BM25 index")
        except Exception as e:
            logger.warning(f"Could not load BM25 index: {e}")
            logger.info("Starting with empty BM25 index")
    
    def ingest_document(
        self,
        file_data: BinaryIO,
        filename: str,
        document_id: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Ingest a document into the RAG system
        
        Steps:
        1. Save to MinIO
        2. Extract text (PDF/XLSX/DOCX)
        3. Chunk the text
        4. Generate embeddings
        5. Add to vector store
        6. Add to BM25 index
        
        Returns:
            Dict with ingestion stats
        """
        start_time = time.time()
        logger.info(f"Starting ingestion for document: {filename}")
        
        # Save to MinIO
        object_name = self.document_loader.save_to_minio(
            file_data,
            filename,
            content_type=metadata.get('content_type', 'application/octet-stream')
        )
        
        # Save file temporarily for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            file_data.seek(0)
            tmp_file.write(file_data.read())
            tmp_path = tmp_file.name
        
        try:
            # Extract text
            extracted = self.document_loader.load_file(tmp_path)
            text = extracted['text']
            doc_metadata = extracted.get('metadata', {})
            
            logger.info(f"Extracted {len(text)} characters from {filename}")
            
            # Chunk the text
            base_metadata = metadata or {}
            base_metadata.update({
                'document_id': document_id,
                'filename': filename,
                'object_name': object_name,
                **doc_metadata
            })
            
            chunks = self.chunker.chunk_for_retrieval(
                text=text,
                document_id=document_id,
                metadata=base_metadata
            )
            
            logger.info(f"Created {len(chunks)} chunks")
            
            # Extract texts for embedding and BM25
            chunk_texts = [chunk['text'] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embedding_service.embed_batch(chunk_texts)
            logger.info(f"Generated embeddings: {embeddings.shape}")
            
            # Add to vector store
            self.vector_store.add_documents(embeddings, chunks)
            
            # Add to BM25 index
            # Note: We need to rebuild BM25 index with all documents
            # For now, we'll add to a temporary list and rebuild periodically
            self.bm25_search.index_documents(chunk_texts, chunks)
            
            # Extract entities and relationships for knowledge graph
            if settings.ENABLE_KNOWLEDGE_GRAPH:
                logger.info("Extracting entities and relationships for knowledge graph")
                kg_stats = self._extract_and_store_kg(
                    text=text,
                    chunks=chunks,
                    document_id=document_id,
                    filename=filename
                )
            else:
                kg_stats = {'entities': 0, 'relationships': 0}
            
            # Save indices
            self._save_indices()
            
            processing_time = time.time() - start_time
            
            stats = {
                'document_id': document_id,
                'filename': filename,
                'object_name': object_name,
                'chunk_count': len(chunks),
                'text_length': len(text),
                'processing_time_seconds': processing_time,
                'kg_entities': kg_stats.get('entities', 0),
                'kg_relationships': kg_stats.get('relationships', 0),
                'status': 'completed'
            }
            
            logger.info(f"Document ingestion completed in {processing_time:.2f}s")
            
            return stats
            
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
    
    def query(
        self,
        question: str,
        top_k: int = 10,
        strategy: str = "hybrid",
        confidence_threshold: float = 0.7,
        use_kg_expansion: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            strategy: 'vector', 'bm25', or 'hybrid'
            confidence_threshold: Minimum confidence for response
            use_kg_expansion: Whether to expand context using knowledge graph
        
        Returns:
            Dict with answer, citations, confidence, metadata
        """
        start_time = time.time()
        logger.info(f"Processing query: '{question[:100]}...'")
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(question)
        
        # Retrieve relevant chunks based on strategy
        if strategy == "vector":
            results = self.vector_store.search(query_embedding, k=top_k)
        elif strategy == "bm25":
            results = self.bm25_search.search(question, k=top_k)
        elif strategy == "hybrid":
            if settings.ENABLE_HYBRID_SEARCH:
                results = self.hybrid_retriever.search(
                    query=question,
                    query_embedding=query_embedding,
                    top_k=top_k
                )
            else:
                results = self.vector_store.search(query_embedding, k=top_k)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        logger.info(f"Retrieved {len(results)} chunks using {strategy} strategy")
        
        # Knowledge Graph expansion (if enabled)
        kg_context = []
        if use_kg_expansion and settings.ENABLE_KNOWLEDGE_GRAPH and results:
            try:
                kg_context = self._expand_context_with_kg(question, results)
                logger.info(f"Expanded context with {len(kg_context)} KG entities")
            except Exception as e:
                logger.warning(f"KG expansion failed: {e}")
        
        if not results:
            return {
                'answer': "I don't have enough information to answer this question. Please upload relevant documents first.",
                'citations': [],
                'confidence': 0.0,
                'strategy_used': strategy,
                'processing_time_ms': (time.time() - start_time) * 1000,
                'num_sources': 0,
                'kg_entities': []
            }
        
        # Generate answer with LLM
        context_chunks = results[:5]  # Use top 5 for generation
        
        # Add KG context to system prompt if available
        if kg_context:
            kg_context_text = self._format_kg_context(kg_context)
            # We'll pass this as additional context
        else:
            kg_context_text = ""
        
        llm_response = self.llm_client.generate_with_citations(
            query=question,
            context_chunks=context_chunks,
            additional_context=kg_context_text if kg_context else None
        )
        
        # Format citations
        citations = []
        for i, result in enumerate(results[:5], start=1):
            meta = result['metadata']
            citation = {
                'document_id': meta.get('document_id', 'unknown'),
                'document_title': meta.get('filename', 'Unknown Document'),
                'page': meta.get('page'),
                'chunk_id': meta.get('chunk_id'),
                'text': meta.get('text', '')[:200] + '...',  # Truncate
                'relevance_score': result.get('score', result.get('rrf_score', 0.0))
            }
            citations.append(citation)
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        response = {
            'answer': llm_response['answer'],
            'citations': citations,
            'confidence': llm_response['confidence'],
            'strategy_used': strategy,
            'processing_time_ms': processing_time_ms,
            'num_sources': len(results),
            'kg_entities': [{'id': e['id'], 'text': e['text'], 'type': e['type']} for e in kg_context[:10]]
        }
        
        logger.info(
            f"Query completed in {processing_time_ms:.2f}ms "
            f"(confidence: {llm_response['confidence']:.2f})"
        )
        
        return response
    
    def _save_indices(self):
        """Save both vector and BM25 indices"""
        try:
            self.vector_store.save()
            
            bm25_path = Path(settings.FAISS_INDEX_PATH) / "bm25.pkl"
            self.bm25_search.save(str(bm25_path))
            
            logger.info("Indices saved successfully")
        except Exception as e:
            logger.error(f"Error saving indices: {e}")
    
    def _extract_and_store_kg(
        self,
        text: str,
        chunks: List[Dict[str, Any]],
        document_id: str,
        filename: str
    ) -> Dict[str, Any]:
        """
        Extract entities and relationships and store in knowledge graph
        
        Args:
            text: Full document text
            chunks: Document chunks
            document_id: Document ID
            filename: Document filename
        
        Returns:
            Dict with extraction stats
        """
        try:
            # Create document node in graph
            self.neo4j_client.create_entity(
                entity_id=f"doc_{document_id}",
                entity_type="Document",
                text=filename,
                properties={
                    'document_id': document_id,
                    'title': filename,
                    'chunk_count': len(chunks)
                }
            )
            
            all_entities = []
            all_relationships = []
            
            # Extract entities from each chunk (better context than full document)
            for i, chunk in enumerate(chunks[:10]):  # Limit to first 10 chunks for performance
                chunk_text = chunk['text']
                chunk_id = chunk['metadata'].get('chunk_id', f'chunk_{i}')
                
                # Extract entities
                entities = self.ner.extract_with_context(
                    text=chunk_text,
                    document_id=document_id,
                    chunk_id=chunk_id
                )
                
                # Extract entity objects for relationship extraction
                entity_objects = self.ner.extract_all(chunk_text)
                
                # Extract relationships
                relationships = self.relationship_extractor.extract_with_context(
                    text=chunk_text,
                    entities=entity_objects,
                    document_id=document_id,
                    chunk_id=chunk_id,
                    use_llm=False  # Set to True for more accuracy but slower
                )
                
                all_entities.extend(entities)
                all_relationships.extend(relationships)
            
            # Resolve entities (deduplicate and normalize)
            resolved_entities = self.entity_resolver.resolve_entities(all_entities)
            
            logger.info(f"Resolved {len(all_entities)} entities to {len(resolved_entities)} unique entities")
            
            # Store entities in Neo4j
            stored_entities = 0
            for entity in resolved_entities:
                if not entity.get('is_duplicate', False):
                    entity_id = entity['entity_id']
                    canonical_text = entity.get('canonical_text', entity['text'])
                    
                    self.neo4j_client.create_entity(
                        entity_id=entity_id,
                        entity_type=entity['type'],
                        text=canonical_text,
                        properties={
                            'original_text': entity['text'],
                            'confidence': entity['confidence'],
                            **entity.get('metadata', {})
                        }
                    )
                    
                    # Link entity to document
                    self.neo4j_client.create_relationship(
                        source_id=entity_id,
                        target_id=f"doc_{document_id}",
                        relation_type="DOCUMENTED_IN",
                        properties=entity.get('provenance', {})
                    )
                    
                    stored_entities += 1
            
            # Store relationships in Neo4j
            stored_relationships = 0
            for rel in all_relationships:
                # Normalize entity names to match stored entities
                source_normalized = self.entity_resolver.normalize_entity(
                    rel['source'],
                    'EQUIPMENT'  # Default type, could be improved
                )
                target_normalized = self.entity_resolver.normalize_entity(
                    rel['target'],
                    'FAILURE_MODE'  # Default type, could be improved
                )
                
                # Find matching entity IDs (simplified - could be more robust)
                source_id = None
                target_id = None
                
                for entity in resolved_entities:
                    if entity.get('canonical_text', entity['text']).lower() == source_normalized.lower():
                        source_id = entity['entity_id']
                    if entity.get('canonical_text', entity['text']).lower() == target_normalized.lower():
                        target_id = entity['entity_id']
                
                if source_id and target_id:
                    success = self.neo4j_client.create_relationship(
                        source_id=source_id,
                        target_id=target_id,
                        relation_type=rel['relation_type'],
                        properties={
                            'confidence': rel['confidence'],
                            **rel.get('metadata', {})
                        }
                    )
                    if success:
                        stored_relationships += 1
            
            logger.info(
                f"Stored {stored_entities} entities and "
                f"{stored_relationships} relationships in knowledge graph"
            )
            
            return {
                'entities': stored_entities,
                'relationships': stored_relationships
            }
            
        except Exception as e:
            logger.error(f"Error extracting/storing knowledge graph: {e}")
            return {'entities': 0, 'relationships': 0}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            'vector_store': self.vector_store.get_stats(),
            'bm25': self.bm25_search.get_stats(),
            'hybrid_search_enabled': settings.ENABLE_HYBRID_SEARCH,
            'embedding_model': settings.EMBEDDING_MODEL,
            'llm_provider': settings.LLM_PROVIDER,
            'llm_model': settings.LLM_MODEL
        }
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document and all its chunks
        
        Returns stats about deletion
        """
        logger.info(f"Deleting document: {document_id}")
        
        # Delete from vector store
        deleted_count = self.vector_store.delete_by_document_id(document_id)
        
        # Note: BM25 requires full rebuild to remove documents
        # For now, we mark as deleted and rebuild index periodically
        
        self._save_indices()
        
        return {
            'document_id': document_id,
            'chunks_deleted': deleted_count,
            'status': 'deleted'
        }
    
    def rebuild_indices(self):
        """
        Rebuild all indices from scratch
        
        Useful after deletions or index corruption
        """
        logger.info("Rebuilding all indices...")
        
        # Get all valid metadata
        valid_metadata = [
            meta for meta in self.vector_store.metadata
            if 'document_id' in meta
        ]
        
        # Extract texts
        texts = [meta['text'] for meta in valid_metadata]
        
        # Rebuild BM25
        self.bm25_search.clear()
        self.bm25_search.index_documents(texts, valid_metadata)
        
        # Vector store doesn't need rebuild unless we want to remove deleted items
        
        self._save_indices()
        
        logger.info("Indices rebuilt successfully")
    
    def _expand_context_with_kg(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Expand context using knowledge graph
        
        Extracts entities from question and retrieved chunks,
        then queries graph for related entities
        
        Args:
            question: User question
            retrieved_chunks: Retrieved document chunks
        
        Returns:
            List of related entities from knowledge graph
        """
        # Extract entities from question
        question_entities = self.ner.extract_all(question)
        
        # Extract entities from top chunks
        chunk_entities = []
        for chunk in retrieved_chunks[:3]:  # Only top 3
            entities = self.ner.extract_all(chunk['metadata'].get('text', ''))
            chunk_entities.extend(entities)
        
        all_query_entities = question_entities + chunk_entities
        
        # Find these entities in the graph
        kg_entities = []
        for entity in all_query_entities[:5]:  # Limit to 5 entities
            # Search for entity in graph
            found = self.neo4j_client.find_entities(
                entity_type=entity.entity_type,
                text_pattern=entity.text,
                limit=1
            )
            
            if found:
                entity_data = found[0]
                
                # Get related entities (1-hop)
                related = self.neo4j_client.get_related_entities(
                    entity_id=entity_data['id'],
                    direction='both'
                )
                
                kg_entities.append({
                    'id': entity_data['id'],
                    'text': entity_data.get('text', ''),
                    'type': entity_data.get('type', ''),
                    'related': related[:5]  # Top 5 related
                })
        
        return kg_entities
    
    def _format_kg_context(self, kg_entities: List[Dict[str, Any]]) -> str:
        """
        Format KG entities as text context for LLM
        
        Args:
            kg_entities: List of entities with relationships
        
        Returns:
            Formatted context string
        """
        if not kg_entities:
            return ""
        
        lines = ["Additional context from knowledge graph:"]
        
        for entity in kg_entities:
            lines.append(f"\n- {entity['text']} ({entity['type']}):")
            
            for rel in entity.get('related', []):
                target = rel['target']
                rel_type = rel['relation_type']
                lines.append(f"  • {rel_type} → {target.get('text', 'unknown')}")
        
        return "\n".join(lines)


# Global RAG pipeline instance
rag_pipeline = RAGPipeline()
