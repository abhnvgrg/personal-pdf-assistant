#  RAG PDF Personal Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-red.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**A production-ready RAG system for intelligent PDF question-answering with comprehensive synthesis and source attribution**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api-reference)

</div>

---

##  Overview

This is a complete **Retrieval Augmented Generation (RAG)** system that transforms any PDF document into an intelligent Q&A assistant. Upload PDFs, ask questions in natural language, and receive comprehensive, well-synthesized answers with source citations.

**Key Highlights:**
-  Comprehensive answers (up to 3000+ words) synthesized from multiple sources
-  Full source attribution with page numbers and chunk IDs
-  Advanced LLM with synthesis-focused prompting (no chunk dumping)
-  Conversation memory and context awareness
-  Human-in-the-loop feedback system
-  Fast semantic search with FAISS
-  RESTful API for easy integration

---

##  Features

### Core RAG Pipeline
 **PDF Processing**: Extract text from multi-page PDFs using PyPDFLoader  
 **Smart Chunking**: RecursiveCharacterTextSplitter with configurable overlap  
 **Vector Embeddings**: Sentence-transformers (all-MiniLM-L6-v2) for semantic search  
 **FAISS Vector Store**: Efficient similarity search across thousands of chunks  
 **Intelligent Synthesis**: Flan-T5 with advanced prompting for comprehensive answers  
 **Source Attribution**: Transparent citations with page numbers and chunk references  

### Advanced Features
 **Interactive Web UI**: Beautiful Streamlit interface with real-time chat  
 **REST API**: FastAPI backend with 8 endpoints for full control  
 **Conversation Memory**: Maintains chat history for context-aware responses  
 **HITL Feedback**: Like/dislike buttons + text feedback for continuous improvement  
 **LLM Evaluation**: Compare RAG vs non-RAG responses  
 **Comprehensive Answers**: Up to 3000+ words with no artificial limits  
 **Multiple Sources**: Retrieves and synthesizes up to 8 chunks per query  

---

##  Demo

### Sample Interaction

**Input:** 211-page technical PDF on Machine Learning

**Question:** *"Explain the main concepts discussed in this document"*

**Output:** 
```
The document provides an extensive exploration of machine learning and its 
transformative applications across multiple domains. 

Machine learning, as described in the text, represents a fundamental shift 
in how we approach problem-solving with computers. Rather than explicitly 
programming solutions, ML systems learn patterns from data...

[Continues for multiple paragraphs with detailed explanations]

The key takeaway is that machine learning has evolved from a theoretical 
concept to a practical tool that drives innovation across industries...
```

 **Complete sentences**  
 **Multiple paragraphs**  
 **Synthesized from 8 sources**  
 **Source citations included**  

---

##  Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│              Streamlit Web App (localhost:8501)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                    (localhost:8000)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   /upload    │  │    /query    │  │  /feedback   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       RAG PIPELINE                               │
│                                                                  │
│  PDF → [PyPDFLoader] → [Text Chunks] → [Embeddings] → [FAISS]  │
│                                                                  │
│  Query → [Embedding] → [Similarity Search] → [Top 8 Chunks]     │
│                                                                  │
│  Context + Query → [Flan-T5] → [Comprehensive Answer]           │
└─────────────────────────────────────────────────────────────────┘
```

**Flow:**
1. **Upload**: PDF → Text extraction → Chunking → Embedding → FAISS indexing
2. **Query**: Question → Embedding → Retrieve 8 similar chunks → LLM synthesis
3. **Response**: Comprehensive answer + sources + page numbers
4. **Feedback**: User rates response (HITL)

##  Project Structure

```
Personal-Assistant-PDF/
│
├──  Main Applications
│   ├── app.py                  # Streamlit Web UI
│   ├── main.py                 # FastAPI REST API
│   └── requirements.txt        # Python dependencies
│
├──  RAG Pipeline
│   └── rag_pipeline/
│       ├── loader.py           # PDF text extraction (PyPDFLoader)
│       ├── chunking.py         # Intelligent text splitting
│       ├── embeddings.py       # Sentence transformer embeddings
│       ├── retriever.py        # FAISS vector search
│       └── generator.py        # Flan-T5 answer synthesis
│
├──  Utilities
│   └── utils/
│       ├── prompt.py           # Synthesis-focused prompts
│       └── evaluation.py       # RAG performance evaluation
│
├──  Data (gitignored)
│   ├── data/                   # Uploaded PDF files
│   └── vector_store/           # FAISS index + feedback logs
│
└──  Documentation
    ├── README.md               # This file
    ├── TESTING_GUIDE.md        # Testing instructions
    ├── SYNTHESIS_UPGRADE.md    # Answer quality improvements
    └── .env.example            # Configuration template
```

##  Installation & Setup

### Prerequisites
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB for models and dependencies

### Quick Start

#### 1️ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/RAG-PDF-Assistant.git
cd RAG-PDF-Assistant
```

#### 2️ Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3️ Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First run downloads models (~1GB total):
-  Embeddings: `all-MiniLM-L6-v2` (~90MB)
-  LLM: `google/flan-t5-base` (~900MB)

#### 4️ Run the Application

**Option A: Full System (Recommended)**

Terminal 1 - Backend:
```bash
python main.py
```
 API running at `http://localhost:8000`

Terminal 2 - Frontend:
```bash
streamlit run app.py
```
 UI running at `http://localhost:8501`

**Option B: API Only**
```bash
python main.py
# Access API docs at http://localhost:8000/docs
```

---

##  Usage Guide

### Using the Web Interface

1. **Open Browser** → Navigate to `http://localhost:8501`

2. **Upload PDF**
   - Click "Choose a PDF file"
   - Select your document
   - Click "Process PDF"
   - Wait for processing (~1-2 sec/page)

3. **Ask Questions**
   - Type question in input box
   - Adjust settings in sidebar:
     - **Top-K**: Number of sources (default: 8)
     - **Prompt Variant**: structured/simple/conversational
   - Click " Get Answer"

4. **Review Response**
   - Read comprehensive answer
   - Expand " View Sources" for citations
   - Check page numbers and chunk IDs
   - Provide feedback with 👍/👎

5. **Advanced Features**
   - Enable "Compare with/without context" for evaluation
   - View conversation history
   - Clear history to start fresh

### Using the API

**1. Upload PDF**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "message": "PDF processed successfully",
  "filename": "document.pdf",
  "total_pages": 211,
  "total_chunks": 1245,
  "processing_time": 45.3
}
```

**2. Query Document**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main concepts?",
    "top_k": 8,
    "prompt_variant": "structured",
    "include_evaluation": false
  }'
```

**Response:**
```json
{
  "answer": "The document discusses...",
  "sources": [
    {"source_num": 1, "page": 5, "chunk_id": 42, "content": "..."},
    {"source_num": 2, "page": 12, "chunk_id": 89, "content": "..."}
  ],
  "query_time": 8.5,
  "metadata": {...}
}
```

**3. Submit Feedback**
```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is X?",
    "answer": "X is...",
    "rating": "like"
  }'
```

---

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```bash
# LLM Model
LLM_MODEL=google/flan-t5-base  # or flan-t5-large for better quality

# Embeddings Model
EMBEDDINGS_MODEL=all-MiniLM-L6-v2

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval
DEFAULT_TOP_K=8

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Model Options

| Model | Size | Quality | Speed | RAM |
|-------|------|---------|-------|-----|
| flan-t5-small | 300MB | Good | Fast | 2GB |
| **flan-t5-base** | 900MB | Better | Medium | 4GB |
| flan-t5-large | 3GB | Best | Slow | 8GB |

**Current:** flan-t5-base (balanced performance)

##  Key Features Explained

### 1. Comprehensive Answer Synthesis
Unlike basic RAG systems that simply concatenate chunks, this system:
-  Synthesizes information from up to 8 sources
-  Generates coherent, multi-paragraph responses
-  No artificial word limits (up to 3000+ words)
-  Uses advanced prompting to prevent chunk dumping
-  Maintains proper grammar and flow

### 2. Source Attribution
Every answer includes:
-  Page numbers from original PDF
-  Chunk IDs for precise location
-  Preview of source text
-  Expandable full source view

### 3. Human-in-the-Loop Feedback
-  Like/dislike buttons for quick feedback
-  Text feedback for detailed suggestions
-  Feedback logged to `vector_store/feedback.txt`
-  Enables continuous improvement

### 4. Conversation Memory
-  Maintains chat history within session
-  Context-aware follow-up questions
-  Clear history to start fresh
-  View full conversation log

##  Evaluation

The system includes built-in evaluation to compare RAG vs non-RAG responses:

```python
from utils.evaluation import RAGEvaluator

evaluator = RAGEvaluator(llm_generator, retriever, embeddings_gen)
results = evaluator.evaluate_query("What is the main topic?")
print(evaluator.generate_report([results]))
```

Enable in UI by checking "Compare with/without context"

##  Development

### Adding Custom Prompt Templates

Edit `utils/prompt.py`:
```python
@staticmethod
def custom_prompt(context: str, question: str) -> str:
    return f"Custom format: {context}\n\nQ: {question}\nA:"
```

### Extending the API

Add endpoints in `main.py`:
```python
@app.get("/custom-endpoint")
async def custom_function():
    return {"message": "Custom response"}
```

##  Performance

- **Embedding Generation**: ~1-2 seconds per page
- **Query Response**: ~2-5 seconds (CPU), ~0.5-2s (GPU)
- **Memory Usage**: ~2-4GB (base model), ~8-12GB (large model)

##  Troubleshooting

**Issue**: Models not downloading
- **Solution**: Check internet connection, may need HuggingFace token for some models

**Issue**: Out of memory
- **Solution**: Use smaller models (`flan-t5-small`) or reduce batch size

**Issue**: API not connecting
- **Solution**: Ensure backend is running on port 8000, check firewall

**Issue**: Slow responses
- **Solution**: Use GPU if available, reduce `top_k`, use smaller models

##  Feedback Data

User feedback is stored in `vector_store/feedback.txt` for HITL improvements:
```
===========================================
Timestamp: 2026-03-28T10:00:00
Question: What is X?
Answer: X is...
Rating: like
Feedback: Very accurate!
```

##  Security Notes

- PDFs are stored in `data/` directory
- Do not expose API publicly without authentication
- Sanitize user inputs in production
- Use environment variables for sensitive config

##  Future Enhancements

- [ ] Multi-document support
- [ ] Advanced evaluation metrics (BLEU, ROUGE)
- [ ] User authentication
- [ ] Database for feedback storage
- [ ] Real-time streaming responses
- [ ] Support for other document formats (DOCX, TXT)
- [ ] Fine-tuning on user feedback

##  Performance

### Benchmarks
- **PDF Processing**: ~1-2 seconds per page
- **Query Response**: 8-15 seconds (comprehensive answers)
- **Embedding Generation**: ~0.5 seconds per chunk
- **Memory Usage**: ~3-4GB RAM (base model)

### Optimization Tips
1. **Use GPU**: Set `CUDA_VISIBLE_DEVICES=0` for 5x speedup
2. **Reduce Chunks**: Lower `top_k` to 3-5 for faster responses
3. **Smaller Model**: Use `flan-t5-small` for speed (lower quality)
4. **Batch Processing**: Process multiple PDFs in advance

---

##  Testing

Run the test suite:
```bash
# Quick functionality test
python -c "from rag_pipeline import *; print(' All modules imported')"

# API health check
curl http://localhost:8000/

# Full system test
python -m pytest tests/  # (if tests implemented)
```

See `TESTING_GUIDE.md` for detailed testing instructions.

---

##  Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- [ ] Multi-document support
- [ ] Advanced evaluation metrics (BLEU, ROUGE)
- [ ] User authentication
- [ ] Database for persistent feedback storage
- [ ] Support for DOCX, TXT formats
- [ ] Real-time streaming responses
- [ ] Fine-tuning on user feedback

---

##  Troubleshooting

### Models Not Downloading
- Check internet connection
- Some models need HuggingFace token: `export HF_TOKEN=your_token`

### Out of Memory
- Use smaller model: `flan-t5-small`
- Reduce `top_k` to 3-5
- Lower `max_new_tokens` to 1000

### Slow Responses
- Enable GPU if available
- Reduce `num_beams` to 3
- Use `flan-t5-small` model

### API Not Connecting
- Check if port 8000/8501 is free
- Verify firewall settings
- Check backend logs for errors

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

