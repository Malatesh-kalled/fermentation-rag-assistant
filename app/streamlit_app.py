import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings
from app.ingestion import build_vector_store
from app.rag import answer_question


st.set_page_config(
    page_title="Fermentation RAG Assistant",
    layout="wide",
)

st.title("Fermentation RAG Assistant")
st.caption("Ask technical questions grounded in pre-loaded fermentation research papers.")

with st.sidebar:
    st.header("Knowledge Base")
    st.write(f"PDF folder: `{settings.papers_dir}`")
    st.write(f"Vector store: `{settings.chroma_dir}`")
    st.write(f"Embedding model: `{settings.embedding_model}`")
    st.write(f"LLM: `{settings.groq_model}`")

    if st.button("Rebuild Vector Store", use_container_width=True):
        with st.spinner("Loading PDFs, chunking documents, and creating embeddings..."):
            try:
                build_vector_store(force_rebuild=True)
                st.success("Vector store rebuilt successfully.")
            except Exception as exc:
                st.error(str(exc))

question = st.text_area(
    "Question",
    placeholder="Example: What factors influence fermentation yield?",
    height=120,
)

ask_clicked = st.button("Ask", type="primary")

if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving relevant chunks and generating answer..."):
            try:
                answer = answer_question(question.strip())
                st.subheader("Answer")
                st.write(answer)
            except Exception as exc:
                st.error(str(exc))
