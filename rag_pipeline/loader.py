"""
PDF Loader Module
Uses LangChain's PyPDFLoader to extract text from PDF documents.
"""
try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    from langchain.document_loaders import PyPDFLoader
from typing import List
import os


class PDFDocumentLoader:
    """Handles loading and extracting text from PDF files."""
    
    def __init__(self):
        pass
    
    def load_pdf(self, pdf_path: str) -> List[dict]:
        """
        Load PDF and extract text with metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of documents with page content and metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF")
        
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Convert to dict format with metadata
        processed_docs = []
        for doc in documents:
            processed_docs.append({
                'content': doc.page_content,
                'metadata': {
                    'page': doc.metadata.get('page', 0),
                    'source': doc.metadata.get('source', pdf_path)
                }
            })
        
        return processed_docs
    
    def get_total_pages(self, documents: List[dict]) -> int:
        """Get total number of pages in the loaded document."""
        return len(documents)
