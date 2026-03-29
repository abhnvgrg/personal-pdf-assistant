# RAG-based PDF Knowledge Assistant

A Retrieval-Augmented Generation (RAG) system that enables natural language querying over PDF documents by combining semantic retrieval with large language model-based answer synthesis.

---

## Problem Statement

Large documents such as research papers, reports, and technical manuals are difficult to navigate efficiently. Traditional keyword search fails to capture semantic meaning, while standalone language models may generate ungrounded or hallucinated responses.

This project addresses the problem by building a system that retrieves relevant document context and generates grounded, context-aware answers with traceable sources.

---

## Approach

The system follows a structured RAG pipeline:

### 1. Document Processing
- Extract text from PDFs using PyPDFLoader  
- Split text into overlapping chunks (chunk size: 1000, overlap: 200)

### 2. Semantic Indexing
- Generate embeddings using `all-MiniLM-L6-v2`  
- Store embeddings in FAISS for efficient similarity search  

### 3. Query Processing
- Convert user query into embedding  
- Retrieve top-k (k=8) semantically relevant chunks  

### 4. Answer Generation
- Construct structured prompts combining query and retrieved context  
- Generate responses using `Flan-T5`  
- Synthesize information across multiple chunks instead of returning raw text  

### 5. Post-processing
- Provide source attribution (page numbers, chunk IDs)  
- Maintain conversation memory  
- Collect user feedback for evaluation  

---

## System Architecture


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
---

## Key Features

- Context-aware question answering over PDF documents  
- Multi-source answer synthesis using retrieved context  
- Source attribution with page-level traceability  
- REST API built with FastAPI  
- Interactive frontend using Streamlit  
- Conversation memory for context-aware queries  
- Human-in-the-loop feedback collection  
- Evaluation pipeline for comparing RAG vs non-RAG responses  

---

## Tech Stack

- **Language Models**: Flan-T5 (HuggingFace Transformers)  
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Vector Database**: FAISS  
- **Backend**: FastAPI  
- **Frontend**: Streamlit  
- **Frameworks**: LangChain  
- **Language**: Python  

---

## Results and Observations

- Retrieval-based grounding improved answer relevance compared to direct LLM responses  
- Structured prompting improved coherence and reduced fragmented outputs  
- Increasing top-k improved coverage but introduced redundancy  
- Chunk size and overlap significantly impacted retrieval quality  

---

## Challenges

- Selecting optimal chunk size and overlap for effective retrieval  
- Preventing the model from copying chunks instead of synthesizing answers  
- Managing latency due to retrieval + generation pipeline  
- Ensuring relevance of retrieved chunks for ambiguous queries  

---

## Future Work

- Multi-document retrieval and indexing  
- Advanced evaluation metrics (semantic similarity, groundedness)  
- Persistent storage for embeddings and feedback  
- Streaming responses to reduce perceived latency  
- Support for additional document formats (DOCX, TXT)  

---

## Installation

### Prerequisites
- Python 3.8+
- 4GB+ RAM (8GB recommended)

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/RAG-PDF-Assistant.git
cd RAG-PDF-Assistant

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```
### Run the Application

Backend:
```bash
python main.py
```
Frontend:
```bash
streamlit run app.py
```
## Usage

### Web Interface

1. Open your browser and go to:
http://localhost:8501

2. Upload a PDF document using the file uploader

3. Click "Process PDF" and wait for indexing to complete

4. Enter your query in natural language

5. (Optional) Adjust parameters:
   - Top-K: Number of retrieved chunks (default: 8)
   - Prompt Variant: structured / simple / conversational

6. View the generated answer along with:
   - Source citations (page numbers, chunk IDs)
   - Retrieved context
   - Evaluation comparison (if enabled)

7. Provide feedback using 👍 / 👎 buttons

---

### API Usage

#### 1. Upload PDF
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

#### 2. Query Document
```bash
curl -X POST "http://localhost:8000/query
"
-H "Content-Type: application/json"
-d '{
"question": "What are the main concepts?",
"top_k": 8,
"prompt_variant": "structured"
}'
```

#### 3. Submit Feedback
```bash
curl -X POST "http://localhost:8000/feedback
"
-H "Content-Type: application/json"
-d '{
"question": "What is X?",
"answer": "X is...",
"rating": "like"
}'
```


---

##  Configuration

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

---

## Performance

- PDF Processing: ~1–2 seconds per page
- Query Response: ~2–5 seconds (CPU)
- Memory Usage: ~3–4GB (base model)

Performance may vary depending on document size and hardware.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a new branch:
   git checkout -b feature/your-feature-name
3. Commit your changes:
   git commit -m "Add your feature"

4. Push to your branch:
   git push origin feature/your-feature-name
5. Open a Pull Request

### Suggested Areas for Contribution

- Multi-document support
- Improved evaluation metrics
- Performance optimization
- Additional document formats (DOCX, TXT)
- UI/UX improvements

---

## License

This project is licensed under the MIT License.         




