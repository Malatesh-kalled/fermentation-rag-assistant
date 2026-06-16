# Fermentation RAG Assistant

A domain-specific Retrieval-Augmented Generation (RAG) assistant for answering technical questions from fermentation research papers.

This project matches the resume/interview description:

- Pre-loaded fermentation research PDFs
- PDF loading and chunking with LangChain
- Embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- Vector search with ChromaDB
- Grounded answers using Groq-hosted Llama 3
- FastAPI backend and Streamlit user interface

## Project Structure

```text
fermentation-rag-assistant/
  app/
    api.py              # FastAPI REST API
    config.py           # Environment-driven settings
    ingestion.py        # PDF loading, chunking, embeddings, Chroma indexing
    prompts.py          # Grounding prompt for hallucination control
    rag.py              # Retrieval and answer generation chain
    streamlit_app.py    # Streamlit UI
  data/
    papers/             # Add fermentation research PDFs here
  vector_store/         # ChromaDB persists here after ingestion
  .env.example
  requirements.txt
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create your environment file.

```bash
copy .env.example .env
```

4. Add your Groq API key to `.env`.

```env
GROQ_API_KEY=your_groq_api_key_here
```

5. Place fermentation research papers in:

```text
data/papers/
```

## Run the API

Build the vector database:

```bash
python -m app.ingestion
```

Start FastAPI:

```bash
uvicorn app.api:app --reload
```

Ask a question:

```bash
curl -X POST http://127.0.0.1:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What are the key factors affecting fermentation yield?\"}"
```

## Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

## RAG Flow

1. Load pre-loaded fermentation PDFs from `data/papers/`.
2. Split long research papers into chunks of about 500-800 characters.
3. Create semantic embeddings with `all-MiniLM-L6-v2`.
4. Store chunks and embeddings in ChromaDB.
5. Convert the user question into an embedding.
6. Retrieve the top relevant chunks using similarity search.
7. Send the retrieved context and user question to Groq Llama 3.
8. Return an answer grounded only in the retrieved paper content.

## Hallucination Control

The assistant uses a strict system prompt that instructs the model to answer only from the retrieved context. If the answer is not present in the retrieved papers, the model is told to say that it does not know based on the available context.

## Interview Summary

This project demonstrates an end-to-end GenAI application using modern RAG architecture. It covers document ingestion, chunking, embeddings, vector search, prompt engineering, API design, and a user-facing interface.
