"""
Evaluation Module
Compare RAG responses with and without context.
"""
import time
from typing import List, Dict
from datetime import datetime


class RAGEvaluator:
    """Evaluates RAG system performance."""
    
    def __init__(self, llm_generator, retriever, embeddings_gen):
        """
        Initialize evaluator.
        
        Args:
            llm_generator: LLM generator instance
            retriever: FAISS retriever instance
            embeddings_gen: Embeddings generator instance
        """
        self.llm = llm_generator
        self.retriever = retriever
        self.embeddings = embeddings_gen
    
    def evaluate_query(
        self, 
        question: str, 
        context: str = None,
        top_k: int = 5
    ) -> Dict:
        """
        Evaluate a single query with and without RAG context.
        
        Args:
            question: User's question
            context: Optional pre-retrieved context
            top_k: Number of documents to retrieve if context not provided
            
        Returns:
            Dictionary with evaluation results
        """
        results = {
            'question': question,
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate answer WITHOUT context
        start_time = time.time()
        answer_no_context = self.llm.generate_without_context(question)
        time_no_context = time.time() - start_time
        
        results['without_context'] = {
            'answer': answer_no_context,
            'generation_time': time_no_context
        }
        
        # Generate answer WITH context
        if context is None:
            # Retrieve context
            query_embedding = self.embeddings.generate_query_embedding(question)
            retrieved_docs = self.retriever.search(query_embedding, top_k=top_k)
            context = "\n\n".join([doc['content'] for doc in retrieved_docs])
            sources = retrieved_docs
        else:
            sources = []
        
        start_time = time.time()
        answer_with_context = self.llm.generate_answer(question, context)
        time_with_context = time.time() - start_time
        
        results['with_context'] = {
            'answer': answer_with_context,
            'generation_time': time_with_context,
            'num_sources': len(sources)
        }
        
        # Compare
        results['comparison'] = {
            'speedup_factor': time_no_context / time_with_context if time_with_context > 0 else 0,
            'answers_differ': answer_no_context.lower() != answer_with_context.lower()
        }
        
        return results
    
    def batch_evaluate(
        self, 
        questions: List[str], 
        top_k: int = 5
    ) -> List[Dict]:
        """
        Evaluate multiple queries.
        
        Args:
            questions: List of questions
            top_k: Number of documents to retrieve
            
        Returns:
            List of evaluation results
        """
        results = []
        for question in questions:
            result = self.evaluate_query(question, top_k=top_k)
            results.append(result)
        
        return results
    
    def generate_report(self, evaluation_results: List[Dict]) -> str:
        """
        Generate evaluation report.
        
        Args:
            evaluation_results: List of evaluation results
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("RAG EVALUATION REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Queries Evaluated: {len(evaluation_results)}\n")
        
        for i, result in enumerate(evaluation_results, 1):
            report.append(f"\n--- Query {i} ---")
            report.append(f"Question: {result['question']}")
            report.append(f"\nWithout Context:")
            report.append(f"  Answer: {result['without_context']['answer']}")
            report.append(f"  Time: {result['without_context']['generation_time']:.2f}s")
            report.append(f"\nWith Context (RAG):")
            report.append(f"  Answer: {result['with_context']['answer']}")
            report.append(f"  Time: {result['with_context']['generation_time']:.2f}s")
            report.append(f"  Sources: {result['with_context']['num_sources']}")
            report.append(f"\nAnswers Differ: {result['comparison']['answers_differ']}")
            report.append("-" * 80)
        
        return "\n".join(report)
    
    def save_report(self, evaluation_results: List[Dict], filename: str):
        """Save evaluation report to file."""
        report = self.generate_report(evaluation_results)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
