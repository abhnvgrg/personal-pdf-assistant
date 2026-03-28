"""
Text Chunking Module
Uses LangChain's RecursiveCharacterTextSplitter to split text into manageable chunks.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict


class TextChunker:
    """Handles splitting text into smaller chunks for better retrieval."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between consecutive chunks for context preservation
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_documents(self, documents: List[dict]) -> List[dict]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of documents with content and metadata
            
        Returns:
            List of chunked documents with preserved metadata
        """
        chunked_docs = []
        chunk_id = 0
        
        for doc in documents:
            content = doc['content']
            page_num = doc['metadata'].get('page', 0)
            source = doc['metadata'].get('source', '')
            
            # Split the content
            chunks = self.splitter.split_text(content)
            
            # Add metadata to each chunk
            for chunk in chunks:
                if chunk.strip():  # Skip empty chunks
                    chunked_docs.append({
                        'content': chunk,
                        'metadata': {
                            'chunk_id': chunk_id,
                            'page': page_num,
                            'source': source
                        }
                    })
                    chunk_id += 1
        
        return chunked_docs
    
    def get_chunk_info(self, chunked_docs: List[dict]) -> dict:
        """Get information about the chunking process."""
        return {
            'total_chunks': len(chunked_docs),
            'chunk_size': self.chunk_size,
            'overlap': self.chunk_overlap
        }
