"""
FastAPI Backend for RAG System
Handles PDF upload and query processing.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import shutil
from datetime import datetime

from rag_pipeline.loader import PDFDocumentLoader
from rag_pipeline.chunking import TextChunker
from rag_pipeline.embeddings import EmbeddingsGenerator
from rag_pipeline.retriever import FAISSRetriever
from rag_pipeline.generator import LLMGenerator
from utils.prompt import PromptTemplate, PromptVariants

app = FastAPI(title="RAG PDF Assistant API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
PDF_DIR = "data"
VECTOR_STORE_DIR = "vector_store"
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Initialize components
embeddings_gen = None
retriever = None
llm_generator = None
current_pdf_name = None
conversation_history = []


class QueryRequest(BaseModel):
    question: str
    top_k: int = 8  # Increased default for comprehensive answers
    prompt_variant: str = "structured"
    include_evaluation: bool = False


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict]
    answer_without_context: Optional[str] = None
    query_time: float
    metadata: Dict


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: str  # "like" or "dislike"
    feedback_text: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup."""
    global embeddings_gen, llm_generator
    print("Initializing models...")
    embeddings_gen = EmbeddingsGenerator()
    llm_generator = LLMGenerator()
    print("Models loaded successfully!")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "RAG PDF Assistant API",
        "status": "running",
        "pdf_loaded": current_pdf_name is not None
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    Creates embeddings and builds FAISS index.
    """
    global retriever, current_pdf_name, conversation_history
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Save uploaded file
        pdf_path = os.path.join(PDF_DIR, file.filename)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF
        start_time = datetime.now()
        
        # 1. Load PDF
        loader = PDFDocumentLoader()
        documents = loader.load_pdf(pdf_path)
        
        # 2. Chunk text
        chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
        chunked_docs = chunker.chunk_documents(documents)
        
        # 3. Generate embeddings
        texts = [doc['content'] for doc in chunked_docs]
        embeddings = embeddings_gen.generate_embeddings(texts)
        
        # 4. Build FAISS index
        retriever = FAISSRetriever(embeddings_gen.get_embedding_dimension())
        retriever.add_documents(embeddings, chunked_docs)
        
        # 5. Save index
        index_path = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
        docs_path = os.path.join(VECTOR_STORE_DIR, "documents.pkl")
        retriever.save_index(index_path, docs_path)
        
        current_pdf_name = file.filename
        conversation_history = []  # Reset conversation history
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "total_pages": len(documents),
            "total_chunks": len(chunked_docs),
            "processing_time": processing_time
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_pdf(request: QueryRequest):
    """
    Query the loaded PDF with a question.
    Returns answer with sources and optional evaluation.
    """
    global conversation_history
    
    if retriever is None or not retriever.is_trained:
        raise HTTPException(
            status_code=400, 
            detail="No PDF loaded. Please upload a PDF first."
        )
    
    try:
        start_time = datetime.now()
        
        # 1. Generate query embedding
        query_embedding = embeddings_gen.generate_query_embedding(request.question)
        
        # 2. Retrieve more documents for comprehensive answers
        top_k = min(request.top_k, 8)  # Get up to 8 chunks for maximum coverage
        retrieved_docs = retriever.search(query_embedding, top_k=top_k)
        
        # 3. Format context with full sources (no truncation for comprehensive answers)
        context_parts = []
        sources = []
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            # Keep full chunks - no truncation
            context_parts.append(f"[Source {i}]: {content}")
            sources.append({
                'source_num': i,
                'page': metadata.get('page', 'Unknown'),
                'chunk_id': metadata.get('chunk_id', 'Unknown'),
                'content': content[:200] + "..." if len(content) > 200 else content
            })
        
        context = "\n\n".join(context_parts)
        
        # 4. Generate answer
        answer = llm_generator.generate_answer(request.question, context)
        
        # 5. Optional: Generate answer without context for evaluation
        answer_without_context = None
        if request.include_evaluation:
            answer_without_context = llm_generator.generate_without_context(request.question)
        
        query_time = (datetime.now() - start_time).total_seconds()
        
        # 6. Update conversation history
        conversation_history.append({
            "question": request.question,
            "answer": answer
        })
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            answer_without_context=answer_without_context,
            query_time=query_time,
            metadata={
                "pdf_name": current_pdf_name,
                "prompt_variant": request.prompt_variant,
                "top_k": request.top_k,
                "conversation_length": len(conversation_history)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback on a response.
    Implements human-in-the-loop feedback collection.
    """
    try:
        # Store feedback (in production, save to database)
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "question": request.question,
            "answer": request.answer,
            "rating": request.rating,
            "feedback_text": request.feedback_text,
            "pdf_name": current_pdf_name
        }
        
        # Append to feedback log
        feedback_file = os.path.join(VECTOR_STORE_DIR, "feedback.txt")
        with open(feedback_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {feedback_data['timestamp']}\n")
            f.write(f"PDF: {feedback_data['pdf_name']}\n")
            f.write(f"Question: {feedback_data['question']}\n")
            f.write(f"Answer: {feedback_data['answer']}\n")
            f.write(f"Rating: {feedback_data['rating']}\n")
            if feedback_data['feedback_text']:
                f.write(f"Feedback: {feedback_data['feedback_text']}\n")
        
        return {
            "message": "Feedback recorded successfully",
            "feedback_id": feedback_data['timestamp']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving feedback: {str(e)}")


@app.get("/history")
async def get_conversation_history():
    """Get current conversation history."""
    return {
        "conversation_history": conversation_history,
        "total_exchanges": len(conversation_history)
    }


@app.post("/reset")
async def reset_conversation():
    """Reset conversation history."""
    global conversation_history
    conversation_history = []
    return {"message": "Conversation history reset"}


@app.get("/info")
async def get_system_info():
    """Get system information."""
    info = {
        "current_pdf": current_pdf_name,
        "pdf_loaded": current_pdf_name is not None,
        "conversation_length": len(conversation_history),
        "prompt_variants": PromptVariants.list_variants()
    }
    
    if retriever:
        info.update(retriever.get_index_info())
    
    return info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
