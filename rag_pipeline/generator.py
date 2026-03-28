"""
LLM Generator Module
Uses HuggingFace transformers for generating answers based on retrieved context.
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch
from typing import List, Dict


class LLMGenerator:
    """Generates answers using HuggingFace LLM based on context."""
    
    def __init__(self, model_name: str = "google/flan-t5-base"):
        """
        Initialize the LLM.
        
        Args:
            model_name: HuggingFace model name
                       Default: google/flan-t5-large (better quality for synthesis)
                       Alternatives: "mistralai/Mistral-7B-Instruct-v0.1" (even better)
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading model {model_name} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Check if it's a seq2seq or causal model
        if "t5" in model_name.lower():
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.is_seq2seq = True
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.is_seq2seq = False
            
        self.model.to(self.device)
        print(f"Model loaded successfully! Type: {'Seq2Seq' if self.is_seq2seq else 'Causal'}")
    
    def generate_answer(
        self, 
        query: str, 
        context: str, 
        max_length: int = 4096,
        min_length: int = 100
    ) -> str:
        """
        Generate answer based on context with proper synthesis.
        
        Args:
            query: User's question
            context: Retrieved context from documents
            max_length: Maximum length of generated answer (tokens, ~3000+ words)
            min_length: Minimum length of generated answer (tokens)
            
        Returns:
            Generated answer
        """
        # Enhanced prompt for comprehensive synthesis
        prompt = f"""Read the following information carefully and provide a comprehensive, thorough, well-written answer covering all relevant details.

Information:
{context}

Question: {query}

Instructions: Synthesize ALL the information above to answer the question comprehensively. Write a detailed, complete response with as many paragraphs as needed to cover all relevant points. Include all important details, explanations, and examples. Do not summarize or skip information - provide a thorough, exhaustive answer in proper English.

Answer:"""
        
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            max_length=1500, 
            truncation=True,
            padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        if self.is_seq2seq:
            # T5-style generation - allowing very long outputs
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,  # Very high limit for comprehensive answers
                min_length=min_length,
                temperature=0.75,
                do_sample=True,
                top_p=0.92,
                top_k=50,
                num_beams=5,
                no_repeat_ngram_size=3,
                early_stopping=False,  # Let it generate fully
                repetition_penalty=1.2,
                length_penalty=1.2  # Strongly encourages longer, comprehensive outputs
            )
        else:
            # Causal LM generation
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                min_new_tokens=min_length,
                temperature=0.7,
                do_sample=True,
                top_p=0.92,
                top_k=50,
                repetition_penalty=1.15,
                no_repeat_ngram_size=3
            )
        
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # For causal models, extract only the answer part
        if not self.is_seq2seq and "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        return answer.strip()
    
    def generate_without_context(
        self, 
        query: str, 
        max_length: int = 300
    ) -> str:
        """
        Generate answer without context (for evaluation).
        
        Args:
            query: User's question
            max_length: Maximum length of generated answer
            
        Returns:
            Generated answer without context
        """
        prompt = f"Answer the following question in detail.\n\nQuestion: {query}\n\nAnswer:"
        
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            max_length=512, 
            truncation=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        if self.is_seq2seq:
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                min_length=30,
                temperature=0.8,
                do_sample=True,
                top_p=0.92,
                num_beams=4
            )
        else:
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True,
                top_p=0.92
            )
        
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if not self.is_seq2seq and "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
            
        return answer.strip()
    
    def batch_generate(
        self, 
        prompts: List[str], 
        max_length: int = 512
    ) -> List[str]:
        """
        Generate answers for multiple prompts.
        
        Args:
            prompts: List of prompts
            max_length: Maximum length of generated answers
            
        Returns:
            List of generated answers
        """
        answers = []
        for prompt in prompts:
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=0.7,
                do_sample=True
            )
            
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answers.append(answer.strip())
        
        return answers
