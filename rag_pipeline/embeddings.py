"""
Embeddings Module
Uses HuggingFace sentence-transformers to convert text into vector embeddings.
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingsGenerator:
    """Generates vector embeddings from text using HuggingFace models."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embeddings model.
        
        Args:
            model_name: HuggingFace model name for embeddings
                       Default: all-MiniLM-L6-v2 (fast, good performance)
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            Numpy array of embeddings
        """
        if not texts:
            return np.array([])
        
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Numpy array of the query embedding
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.embedding_dimension
