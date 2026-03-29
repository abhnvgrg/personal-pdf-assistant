"""
Streamlit UI for RAG PDF Assistant
Provides a user-friendly interface for PDF upload and Q&A.
"""
import streamlit as st
import requests
from datetime import datetime
import time

# API endpoint
API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="RAG PDF Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = set()


def upload_pdf(file):
    """Upload PDF to backend."""
    files = {'file': file}
    response = requests.post(f"{API_URL}/upload", files=files)
    return response.json()


def query_pdf(question, top_k=5, prompt_variant="structured", include_evaluation=False):
    """Query the PDF."""
    data = {
        "question": question,
        "top_k": top_k,
        "prompt_variant": prompt_variant,
        "include_evaluation": include_evaluation
    }
    response = requests.post(f"{API_URL}/query", json=data)
    return response.json()


def submit_feedback(question, answer, rating, feedback_text=None):
    """Submit user feedback."""
    data = {
        "question": question,
        "answer": answer,
        "rating": rating,
        "feedback_text": feedback_text
    }
    response = requests.post(f"{API_URL}/feedback", json=data)
    return response.json()


def get_system_info():
    """Get system information."""
    try:
        response = requests.get(f"{API_URL}/info")
        return response.json()
    except:
        return None


# Main UI
st.title("📚 RAG PDF Personal Assistant")
st.markdown("Upload a PDF and ask questions about its content!")

# Sidebar
with st.sidebar:
    st.header(" Settings")
    
    # System info
    info = get_system_info()
    if info and info.get('pdf_loaded'):
        st.success(f" PDF Loaded: {info.get('current_pdf', 'Unknown')}")
        st.info(f" Total chunks: {info.get('total_documents', 0)}")
    else:
        st.warning(" No PDF loaded")
    
    st.divider()
    
    # Query settings
    st.subheader("Query Settings")
    top_k = st.slider("Number of sources to retrieve", 1, 10, 5)
    
    prompt_variant = st.selectbox(
        "Prompt variant",
        ["simple", "structured", "conversational"],
        index=1
    )
    
    include_evaluation = st.checkbox("Compare with/without context", value=False)
    
    st.divider()
    
    # Clear conversation
    if st.button(" Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.feedback_submitted = set()
        try:
            requests.post(f"{API_URL}/reset")
        except:
            pass
        st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header(" Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button(" Process PDF", type="primary"):
            with st.spinner("Processing PDF..."):
                try:
                    result = upload_pdf(uploaded_file)
                    st.success(f" PDF processed successfully!")
                    st.json(result)
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with col2:
    st.header(" Ask Questions")
    
    # Check if PDF is loaded
    if info and info.get('pdf_loaded'):
        question = st.text_input("Enter your question:", placeholder="What is the main topic of this document?")
        
        if st.button(" Get Answer", type="primary"):
            if question:
                with st.spinner("Generating answer..."):
                    try:
                        result = query_pdf(question, top_k, prompt_variant, include_evaluation)
                        
                        # Add to conversation history
                        st.session_state.conversation_history.append({
                            'question': question,
                            'answer': result['answer'],
                            'sources': result['sources'],
                            'metadata': result.get('metadata', {}),
                            'timestamp': datetime.now().isoformat(),
                            'answer_without_context': result.get('answer_without_context')
                        })
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question")
    else:
        st.info(" Please upload a PDF first")

# Display conversation history
st.divider()
st.header(" Conversation History")

if st.session_state.conversation_history:
    for idx, exchange in enumerate(reversed(st.session_state.conversation_history)):
        with st.container():
            st.markdown(f"**Q{len(st.session_state.conversation_history) - idx}:** {exchange['question']}")
            
            # Answer section
            st.markdown(f"**A:** {exchange['answer']}")
            
            # Sources
            with st.expander(" View Sources"):
                for source in exchange['sources']:
                    st.markdown(f"""
                    **Source {source['source_num']}** - Page {source['page']}, Chunk {source['chunk_id']}
                    
                    {source['content']}
                    """)
                    st.divider()
            
            # Evaluation (if available)
            if exchange.get('answer_without_context'):
                with st.expander(" Evaluation: With vs Without Context"):
                    col_eval1, col_eval2 = st.columns(2)
                    with col_eval1:
                        st.markdown("**With RAG Context:**")
                        st.info(exchange['answer'])
                    with col_eval2:
                        st.markdown("**Without Context:**")
                        st.warning(exchange['answer_without_context'])
            
            # Feedback section
            feedback_key = f"feedback_{idx}"
            if feedback_key not in st.session_state.feedback_submitted:
                col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 4])
                
                with col_fb1:
                    if st.button("👍 Like", key=f"like_{idx}"):
                        try:
                            submit_feedback(exchange['question'], exchange['answer'], "like")
                            st.session_state.feedback_submitted.add(feedback_key)
                            st.success("Thanks for your feedback!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                with col_fb2:
                    if st.button("👎 Dislike", key=f"dislike_{idx}"):
                        st.session_state[f'show_feedback_{idx}'] = True
                        st.rerun()
                
                # Feedback text input
                if st.session_state.get(f'show_feedback_{idx}', False):
                    feedback_text = st.text_area(
                        "What could be improved?", 
                        key=f"feedback_text_{idx}",
                        placeholder="Please share your thoughts..."
                    )
                    if st.button("Submit Feedback", key=f"submit_fb_{idx}"):
                        try:
                            submit_feedback(
                                exchange['question'], 
                                exchange['answer'], 
                                "dislike", 
                                feedback_text
                            )
                            st.session_state.feedback_submitted.add(feedback_key)
                            st.success("Thanks for your feedback!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.success(" Feedback submitted")
            
            # Metadata
            with st.expander("ℹ️ Metadata"):
                st.json(exchange.get('metadata', {}))
            
            st.divider()
else:
    st.info("No conversation yet. Ask a question to get started!")


