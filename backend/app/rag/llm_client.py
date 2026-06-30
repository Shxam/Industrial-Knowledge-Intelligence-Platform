"""
LLM client for text generation
Supports OpenAI, Ollama, and Azure OpenAI
"""
from typing import Iterator, Optional, List, Dict, Any
from openai import OpenAI, AzureOpenAI
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import logger


class LLMClient:
    """
    Multi-provider LLM client
    
    Supports:
    - OpenAI (GPT-4, GPT-3.5)
    - Ollama (Llama3, Mistral, local models)
    - Azure OpenAI
    """
    
    def __init__(self):
        """Initialize LLM client based on configuration"""
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.client = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate client"""
        if self.provider == "openai":
            if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
                # Check if using Groq instead
                if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
                    logger.warning("OPENAI_API_KEY not set but GROQ_API_KEY found. Consider setting LLM_PROVIDER=groq")
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info(f"Initialized OpenAI client with model: {self.model}")
            
        elif self.provider == "groq":
            if not hasattr(settings, 'GROQ_API_KEY') or not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not set")
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=settings.GROQ_API_KEY
            )
            logger.info(f"Initialized Groq client with model: {self.model}")
            
        elif self.provider == "azure":
            if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
                raise ValueError("Azure OpenAI credentials not set")
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2024-02-01",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
            logger.info(f"Initialized Azure OpenAI client")
            
        elif self.provider == "ollama":
            self.client = OpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama"  # Ollama doesn't need a real key
            )
            logger.info(f"Initialized Ollama client with model: {self.model}")
            
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> str:
        """
        Generate text completion
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
        
        Returns:
            Generated text (or iterator if stream=True)
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return self._stream_response(response)
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    def _stream_response(self, response) -> Iterator[str]:
        """Stream response chunks"""
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def generate_with_citations(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        additional_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Generate answer with citations from context
        
        Args:
            query: User question
            context_chunks: List of relevant document chunks
            additional_context: Optional additional context (e.g., from KG)
            temperature: Sampling temperature
            max_tokens: Maximum tokens
        
        Returns:
            Dict with answer, confidence, and used_chunks
        """
        # Build context from chunks
        context_text = self._build_context(context_chunks)
        
        # Add additional context if provided
        if additional_context:
            context_text = f"{context_text}\n\n{additional_context}"
        
        # System prompt for RAG
        system_prompt = """You are an expert assistant helping with industrial documentation. 
Answer questions based ONLY on the provided context. 
If the context doesn't contain enough information, say so.
Always cite which part of the context you used for your answer."""
        
        # User prompt with context
        prompt = f"""Context:
{context_text}

Question: {query}

Instructions:
1. Answer based only on the context above
2. Be specific and cite relevant parts
3. If unsure, express uncertainty
4. Keep the answer clear and concise

Answer:"""
        
        try:
            answer = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            
            # Calculate confidence (simple heuristic)
            confidence = self._calculate_confidence(answer, context_chunks)
            
            return {
                'answer': answer,
                'confidence': confidence,
                'used_chunks': [chunk['metadata'].get('chunk_id') for chunk in context_chunks]
            }
            
        except Exception as e:
            logger.error(f"Error generating answer with citations: {e}")
            raise
    
    def _build_context(self, chunks: List[Dict[str, Any]], max_length: int = 4000) -> str:
        """
        Build context string from chunks
        
        Truncates if too long
        """
        context_parts = []
        total_length = 0
        
        for i, chunk in enumerate(chunks, start=1):
            # Get text from chunk
            text = chunk['metadata'].get('text', '')
            doc_title = chunk['metadata'].get('document_title', 'Document')
            page = chunk['metadata'].get('page', 'N/A')
            
            chunk_text = f"[{i}] From '{doc_title}' (Page {page}):\n{text}\n"
            
            if total_length + len(chunk_text) > max_length:
                break
            
            context_parts.append(chunk_text)
            total_length += len(chunk_text)
        
        return "\n".join(context_parts)
    
    def _calculate_confidence(
        self,
        answer: str,
        context_chunks: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate confidence score for the answer
        
        Simple heuristic based on:
        - Answer length (not too short, not too long)
        - Presence of uncertainty phrases
        - Number of context chunks used
        """
        # Start with base confidence
        confidence = 0.7
        
        # Check for uncertainty phrases
        uncertainty_phrases = [
            "i don't know",
            "not sure",
            "unclear",
            "insufficient information",
            "cannot determine",
            "not mentioned",
            "doesn't say"
        ]
        
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in uncertainty_phrases):
            confidence -= 0.2
        
        # Adjust based on answer length
        if len(answer) < 50:
            confidence -= 0.1
        elif len(answer) > 1000:
            confidence -= 0.05
        
        # Adjust based on context availability
        if len(context_chunks) < 2:
            confidence -= 0.1
        
        # Clamp between 0 and 1
        confidence = max(0.0, min(1.0, confidence))
        
        return confidence
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Iterator[str]:
        """
        Async streaming generation (for SSE)
        
        Yields text chunks as they're generated
        """
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> str:
        """
        Chat completion with message history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            stream: Whether to stream
        
        Returns:
            Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return self._stream_response(response)
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise


# Global LLM client instance
llm_client = LLMClient()
