"""
Retriever Module
Uses FAISS for efficient similarity search and retrieval.
"""
import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple


class FAISSRetriever:
    """Handles vector storage and similarity search using FAISS."""
    
    def __init__(self, embedding_dimension: int):
        """
        Initialize FAISS index.
        
        Args:
            embedding_dimension: Dimension of the embeddings
        """
        self.embedding_dimension = embedding_dimension
        self.index = faiss.IndexFlatL2(embedding_dimension)
        self.documents = []
        self.is_trained = False
    
    def add_documents(self, embeddings: np.ndarray, documents: List[dict]):
        """
        Add documents and their embeddings to the index.
        
        Args:
            embeddings: Numpy array of embeddings
            documents: List of document dictionaries with content and metadata
        """
        if embeddings.shape[0] != len(documents):
            raise ValueError("Number of embeddings must match number of documents")
        
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(documents)
        self.is_trained = True
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of retrieved documents with similarity scores
        """
        if not self.is_trained:
            raise ValueError("Index is empty. Add documents first.")
        
        # Ensure query is 2D array
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            min(top_k, len(self.documents))
        )
        
        # Prepare results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['similarity_score'] = float(1 / (1 + distance))  # Convert distance to similarity
                results.append(doc)
        
        return results
    
    def save_index(self, index_path: str, docs_path: str):
        """
        Save FAISS index and documents to disk.
        
        Args:
            index_path: Path to save the FAISS index
            docs_path: Path to save the documents
        """
        faiss.write_index(self.index, index_path)
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def load_index(self, index_path: str, docs_path: str):
        """
        Load FAISS index and documents from disk.
        
        Args:
            index_path: Path to the FAISS index
            docs_path: Path to the documents
        """
        if not os.path.exists(index_path) or not os.path.exists(docs_path):
            raise FileNotFoundError("Index or documents file not found")
        
        self.index = faiss.read_index(index_path)
        with open(docs_path, 'rb') as f:
            self.documents = pickle.load(f)
        self.is_trained = True
    
    def get_index_info(self) -> dict:
        """Get information about the current index."""
        return {
            'total_documents': len(self.documents),
            'embedding_dimension': self.embedding_dimension,
            'is_trained': self.is_trained
        }
