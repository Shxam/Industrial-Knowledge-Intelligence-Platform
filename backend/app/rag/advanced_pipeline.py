"""
Advanced RAG pipeline with all enhancements
Integrates: reranking, query enhancement, guardrails, session memory
"""
from typing import Dict, Any, List, Optional
import time

from app.rag.pipeline import RAGPipeline
from app.rag.reranking import reranker
from app.rag.query_enhancement import query_enhancer
from app.rag.guardrails import guardrails
from app.services.session import session_manager
from app.core.config import settings
from app.core.logging import logger


class AdvancedRAGPipeline(RAGPipeline):
    """
    Enhanced RAG pipeline with advanced features:
    - Cross-encoder re-ranking
    - Query enhancement (rewriting, HyDE)
    - Guardrails (groundedness, hallucination detection)
    - Conversation memory
    """
    
    def __init__(self):
        super().__init__()
        self.reranker = reranker
        self.query_enhancer = query_enhancer
        self.guardrails = guardrails
        self.session_manager = session_manager
        
        logger.info("Advanced RAG Pipeline initialized")
    
    def query_with_enhancements(
        self,
        question: str,
        top_k: int = 10,
        strategy: str = "hybrid",
        confidence_threshold: float = 0.7,
        enable_reranking: bool = True,
        enable_query_enhancement: bool = False,
        query_enhancement_method: str = "rewrite",
        enable_guardrails: bool = True,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Advanced query with all enhancements
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            strategy: 'vector', 'bm25', or 'hybrid'
            confidence_threshold: Minimum confidence for response
            enable_reranking: Use cross-encoder re-ranking
            enable_query_enhancement: Enhance query before retrieval
            query_enhancement_method: 'rewrite', 'expand', 'hyde', 'decompose'
            enable_guardrails: Apply guardrails to response
            session_id: Session ID for conversation memory
        
        Returns:
            Dict with answer, citations, confidence, metadata
        """
        start_time = time.time()
        logger.info(f"Advanced query: '{question[:100]}...'")
        
        # Add conversation context if session exists
        conversation_context = ""
        if session_id:
            conversation_context = self.session_manager.get_context_window(session_id)
            if conversation_context:
                logger.info("Using conversation context from session")
        
        # Query enhancement
        queries = [question]
        if enable_query_enhancement:
            enhanced_queries = self.query_enhancer.enhance_for_retrieval(
                question,
                method=query_enhancement_method
            )
            queries = enhanced_queries
            logger.info(f"Enhanced query into {len(queries)} variants")
        
        # Retrieve for all query variants
        all_results = []
        for query in queries:
            query_embedding = self.embedding_service.embed_text(query)
            
            if strategy == "vector":
                results = self.vector_store.search(query_embedding, k=top_k * 2)
            elif strategy == "bm25":
                results = self.bm25_search.search(query, k=top_k * 2)
            elif strategy == "hybrid":
                if settings.ENABLE_HYBRID_SEARCH:
                    results = self.hybrid_retriever.search(
                        query=query,
                        query_embedding=query_embedding,
                        top_k=top_k * 2
                    )
                else:
                    results = self.vector_store.search(query_embedding, k=top_k * 2)
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            all_results.extend(results)
        
        # Deduplicate results
        seen = set()
        unique_results = []
        for result in all_results:
            chunk_id = result['metadata'].get('chunk_id')
            if chunk_id not in seen:
                seen.add(chunk_id)
                unique_results.append(result)
        
        logger.info(f"Retrieved {len(unique_results)} unique chunks")
        
        if not unique_results:
            return self._create_no_results_response(question, session_id, start_time)
        
        # Re-ranking
        if enable_reranking:
            unique_results = self.reranker.rerank(
                query=question,
                results=unique_results,
                top_k=top_k
            )
            logger.info(f"Re-ranked to top {len(unique_results)} results")
        else:
            unique_results = unique_results[:top_k]
        
        # Generate answer with LLM
        context_chunks = unique_results[:5]  # Use top 5 for generation
        
        # Build context
        context_text = self.llm_client._build_context(context_chunks)
        
        # Add conversation context if available
        if conversation_context:
            context_text = f"Previous conversation:\n{conversation_context}\n\nDocuments:\n{context_text}"
        
        # Generate answer
        llm_response = self.llm_client.generate_with_citations(
            query=question,
            context_chunks=context_chunks
        )
        
        answer = llm_response['answer']
        
        # Apply guardrails
        guardrail_result = None
        if enable_guardrails and settings.ENABLE_GUARDRAILS:
            retrieval_scores = [r.get('score', r.get('rrf_score', 0)) for r in context_chunks]
            
            guardrail_result = self.guardrails.validate_response(
                answer=answer,
                context=context_text,
                context_chunks=context_chunks,
                retrieval_scores=retrieval_scores
            )
            
            # Update confidence with guardrail score
            final_confidence = guardrail_result['confidence']
            
            # If guardrails fail significantly, add warning to answer
            if not guardrail_result['passed'] and guardrail_result['warnings']:
                warning_msg = " (Note: This answer may not be fully supported by available documents.)"
                answer = answer + warning_msg
        else:
            final_confidence = llm_response['confidence']
            guardrail_result = {'passed': True, 'warnings': [], 'checks': {}}
        
        # Format citations
        citations = []
        for result in context_chunks:
            meta = result['metadata']
            citation = {
                'document_id': meta.get('document_id', 'unknown'),
                'document_title': meta.get('filename', 'Unknown Document'),
                'page': meta.get('page'),
                'chunk_id': meta.get('chunk_id'),
                'text': meta.get('text', '')[:200] + '...',
                'relevance_score': result.get('score', result.get('rrf_score', 0.0))
            }
            citations.append(citation)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Build response
        response = {
            'answer': answer,
            'citations': citations,
            'confidence': final_confidence,
            'strategy_used': strategy,
            'processing_time_ms': processing_time_ms,
            'num_sources': len(unique_results),
            'enhancements_used': {
                'reranking': enable_reranking,
                'query_enhancement': enable_query_enhancement,
                'guardrails': enable_guardrails,
                'conversation_memory': session_id is not None
            },
            'guardrail_checks': guardrail_result if enable_guardrails else None
        }
        
        # Store in session if provided
        if session_id:
            self.session_manager.add_message(
                session_id=session_id,
                role='user',
                content=question
            )
            self.session_manager.add_message(
                session_id=session_id,
                role='assistant',
                content=answer,
                metadata={
                    'confidence': final_confidence,
                    'citations_count': len(citations)
                }
            )
        
        logger.info(
            f"Advanced query completed in {processing_time_ms:.2f}ms "
            f"(confidence: {final_confidence:.2f})"
        )
        
        return response
    
    def _create_no_results_response(
        self,
        question: str,
        session_id: Optional[str],
        start_time: float
    ) -> Dict[str, Any]:
        """Create response when no results found"""
        answer = "I don't have enough information to answer this question. Please upload relevant documents first."
        
        if session_id:
            self.session_manager.add_message(session_id, 'user', question)
            self.session_manager.add_message(session_id, 'assistant', answer)
        
        return {
            'answer': answer,
            'citations': [],
            'confidence': 0.0,
            'strategy_used': 'none',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'num_sources': 0,
            'enhancements_used': {},
            'guardrail_checks': None
        }


# Global advanced RAG pipeline instance
advanced_rag_pipeline = AdvancedRAGPipeline()
