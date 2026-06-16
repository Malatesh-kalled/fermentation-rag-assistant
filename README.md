# Fermentation RAG Assistant

Fermentation RAG Assistant is a domain-specific Generative AI application that answers technical questions from fermentation research papers using Retrieval-Augmented Generation (RAG).

The system loads pre-added PDF research papers, splits them into chunks, creates embeddings, stores them in ChromaDB, retrieves the most relevant context for a user question, and generates a grounded answer using Groq Llama 3.

## Features

- PDF-based knowledge base for fermentation research papers
- Automatic document loading and text chunking
- Semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB vector database for similarity search
- Groq Llama 3 integration for fast answer generation
- Streamlit web interface for easy interaction
- FastAPI backend for REST API access
- Prompt design to reduce hallucinations by forcing answers to use retrieved context

## Tech Stack

- Python
- Streamlit
- FastAPI
- LangChain
- ChromaDB
- SentenceTransformers
- Groq Llama 3
- Pydantic

## Project Structure

```text
fermentation-rag-assistant/
  app/
    api.py              # FastAPI endpoints
    config.py           # App configuration and environment variables
    ingestion.py        # PDF loading, chunking, embedding, and indexing
    prompts.py          # RAG prompt templates
    rag.py              # Retrieval and answer generation logic
    streamlit_app.py    # Streamlit frontend
  data/
    papers/             # Place fermentation research PDFs here
  vector_store/         # Generated ChromaDB vector store
  .env.example          # Example environment variables
  requirements.txt      # Python dependencies
  README.md
```

## How It Works

1. Research paper PDFs are placed inside `data/papers/`.
2. LangChain loads the PDF documents.
3. Documents are split into smaller chunks using recursive text splitting.
4. Each chunk is converted into an embedding using SentenceTransformers.
5. Embeddings and chunk text are stored in ChromaDB.
6. When a user asks a question, the question is converted into an embedding.
7. ChromaDB retrieves the most relevant chunks.
8. The retrieved context and question are sent to Groq Llama 3.
9. The model returns an answer grounded in the research paper content.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Malatesh-Kalled/fermentation-rag-assistant.git
cd fermentation-rag-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Environment File

```bash
copy .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Do not upload your `.env` file to GitHub.

### 5. Add Research Papers

Place fermentation research paper PDFs in:

```text
data/papers/
```

Example:

```text
data/papers/lactic_acid_fermentation.pdf
data/papers/beer_fermentation_optimization.pdf
```

### 6. Build the Vector Database

```bash
python -m app.ingestion
```

This creates a local ChromaDB vector store inside `vector_store/`.

## Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Run the FastAPI Backend

```bash
uvicorn app.api:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Questions

- What factors affect fermentation yield?
- How does temperature influence fermentation?
- What is the role of pH in fermentation?
- How can fermentation conditions be optimized?
- What are common challenges in lactic acid fermentation?

## API Example

```bash
curl -X POST http://127.0.0.1:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What factors affect fermentation yield?\"}"
```

## Hallucination Control

The assistant is instructed to answer only using the retrieved research paper context. If the answer is not available in the provided context, it responds that it does not know based on the available research papers.

## Notes

- Add only open-access or legally usable PDFs to `data/papers/`.
- Keep `.env` private because it contains the Groq API key.
- The `vector_store/` folder is generated locally and does not need to be uploaded to GitHub.

## Author

**Malatesh M Kalled**

AI/ML and Generative AI enthusiast with hands-on experience in RAG pipelines, FastAPI, LangChain, vector databases, and LLM-powered applications.
