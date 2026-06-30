"""
Smart chunking strategies for documents
"""
from typing import List, Dict, Any
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)
from app.core.config import settings
from app.core.logging import logger


class ChunkMetadata:
    """Metadata for a chunk"""
    def __init__(
        self,
        chunk_id: str,
        document_id: str,
        chunk_index: int,
        page: int = None,
        section: str = None
    ):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.chunk_index = chunk_index
        self.page = page
        self.section = section


class SmartChunker:
    """Smart chunking with multiple strategies"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
    def chunk_recursive(self, text: str, separators: List[str] = None) -> List[str]:
        """
        Recursive chunking - preserves structure
        
        Default separators: paragraphs -> sentences -> words
        """
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=separators,
            length_function=len
        )
        
        chunks = splitter.split_text(text)
        return chunks
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """Sentence-aware chunking"""
        splitter = CharacterTextSplitter(
            separator=". ",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        
        chunks = splitter.split_text(text)
        return chunks
    
    def chunk_with_context(
        self,
        text: str,
        context_prefix: str = None,
        context_suffix: str = None
    ) -> List[str]:
        """
        Context-aware chunking
        
        Adds contextual information to each chunk
        (e.g., document title, section heading)
        """
        base_chunks = self.chunk_recursive(text)
        
        # Add context to each chunk
        contextualized_chunks = []
        for chunk in base_chunks:
            contextualized = chunk
            
            if context_prefix:
                contextualized = f"{context_prefix}\n\n{contextualized}"
            
            if context_suffix:
                contextualized = f"{contextualized}\n\n{context_suffix}"
            
            contextualized_chunks.append(contextualized)
        
        return contextualized_chunks
    
    def chunk_for_retrieval(
        self,
        text: str,
        document_id: str,
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk text and prepare for retrieval
        
        Returns chunks with metadata
        """
        chunks = self.chunk_recursive(text)
        
        result = []
        for i, chunk_text in enumerate(chunks):
            chunk_data = {
                "chunk_id": f"{document_id}_chunk_{i}",
                "document_id": document_id,
                "chunk_index": i,
                "text": chunk_text,
                "metadata": metadata or {}
            }
            result.append(chunk_data)
        
        return result


# Global chunker instance
chunker = SmartChunker()
