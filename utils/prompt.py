"""
Prompt Templates Module
Provides simple and structured prompt variants for better LLM responses.
"""
from typing import List, Dict


class PromptTemplate:
    """Manages different prompt templates for the RAG system."""
    
    @staticmethod
    def simple_prompt(context: str, question: str) -> str:
        """
        Simple prompt template.
        
        Args:
            context: Retrieved context
            question: User's question
            
        Returns:
            Formatted prompt
        """
        return f"""Context: {context}

Question: {question}

Answer:"""
    
    @staticmethod
    def structured_prompt(context: str, question: str) -> str:
        """
        Structured prompt template with clear instructions.
        
        Args:
            context: Retrieved context
            question: User's question
            
        Returns:
            Formatted prompt with structure
        """
        return f"""You are a helpful assistant. Answer the question based ONLY on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer based only on the information in the context
- If the context doesn't contain relevant information, say "I cannot find the answer in the provided document"
- Be concise and accurate
- Cite specific parts of the context when possible

Answer:"""
    
    @staticmethod
    def conversational_prompt(
        context: str, 
        question: str, 
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Conversational prompt with chat history.
        
        Args:
            context: Retrieved context
            question: Current question
            chat_history: Previous Q&A pairs
            
        Returns:
            Formatted prompt with conversation history
        """
        history_text = ""
        if chat_history:
            for entry in chat_history[-3:]:  # Last 3 exchanges
                history_text += f"Q: {entry['question']}\nA: {entry['answer']}\n\n"
        
        return f"""Context: {context}

Previous conversation:
{history_text if history_text else "None"}

Current question: {question}

Answer based on the context and conversation history:"""
    
    @staticmethod
    def evaluation_prompt(question: str) -> str:
        """
        Prompt for evaluation (without context).
        
        Args:
            question: User's question
            
        Returns:
            Simple question prompt
        """
        return f"""Question: {question}

Answer:"""
    
    @staticmethod
    def format_context_with_sources(retrieved_docs: List[Dict]) -> tuple:
        """
        Format retrieved documents into context string with source tracking.
        
        Args:
            retrieved_docs: List of retrieved documents with metadata
            
        Returns:
            Tuple of (context_string, sources_list)
        """
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            page = metadata.get('page', 'Unknown')
            chunk_id = metadata.get('chunk_id', 'Unknown')
            
            context_parts.append(f"[Source {i}] {content}")
            sources.append({
                'source_num': i,
                'page': page,
                'chunk_id': chunk_id,
                'content': content[:200] + "..." if len(content) > 200 else content
            })
        
        context = "\n\n".join(context_parts)
        return context, sources


class PromptVariants:
    """Manages different prompt variants for A/B testing."""
    
    VARIANTS = {
        'simple': PromptTemplate.simple_prompt,
        'structured': PromptTemplate.structured_prompt,
        'conversational': PromptTemplate.conversational_prompt
    }
    
    @classmethod
    def get_variant(cls, variant_name: str):
        """Get a specific prompt variant."""
        return cls.VARIANTS.get(variant_name, cls.VARIANTS['simple'])
    
    @classmethod
    def list_variants(cls) -> List[str]:
        """List all available variants."""
        return list(cls.VARIANTS.keys())
