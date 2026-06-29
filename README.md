# Fermentation RAG Assistant

A domain-specific AI application that answers technical questions from fermentation research papers using Retrieval-Augmented Generation (RAG).

Loads PDF research papers, chunks and embeds them into ChromaDB, retrieves the most relevant context for a user question, and generates a grounded answer using Groq Llama 3.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red) ![LangChain](https://img.shields.io/badge/LangChain-enabled-green) ![Groq](https://img.shields.io/badge/Groq-Llama_3-purple)

---

## What it does

- Add fermentation research PDFs to a local folder
- Ask any technical question about fermentation
- Get back answers grounded strictly in the research paper content — not hallucinated from general knowledge
- Accessible via a Streamlit UI or a FastAPI REST endpoint

---

## Demo

> Live app: [your-app-name.streamlit.app](https://your-app-name.streamlit.app)

---

## Tech stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Backend API | FastAPI |
| LLM | Groq Llama 3 (llama-3.1-8b-instant) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Orchestration | LangChain |
| Language | Python 3.8+ |

---

## How it works

1. Research paper PDFs are placed inside `data/papers/`
2. LangChain loads and splits documents into chunks using recursive text splitting
3. Each chunk is embedded using SentenceTransformers and stored in ChromaDB
4. When a user asks a question, it is converted to an embedding
5. ChromaDB retrieves the most semantically similar chunks
6. The retrieved context and question are sent to Groq Llama 3
7. The model returns an answer grounded in the research paper content — if the answer isn't in the papers, it says so

---

## Project structure

```
fermentation-rag-assistant/
├── app/
│   ├── api.py              # FastAPI endpoints
│   ├── config.py           # App configuration and environment variables
│   ├── ingestion.py        # PDF loading, chunking, embedding, and indexing
│   ├── prompts.py          # RAG prompt templates
│   ├── rag.py              # Retrieval and answer generation logic
│   └── streamlit_app.py    # Streamlit frontend
├── data/
│   └── papers/             # Place fermentation research PDFs here
├── vector_store/           # Generated ChromaDB vector store (local only)
├── .env.example            # Template — copy to .env and add your key
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Local setup

**1. Clone the repo**
```bash
git clone https://github.com/Malatesh-Kalled/fermentation-rag-assistant.git
cd fermentation-rag-assistant
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**

Get a free key at [console.groq.com](https://console.groq.com).

```bash
copy .env.example .env
```

Open `.env` and fill in:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

> `.env` is listed in `.gitignore` — it will never be committed to GitHub.

**5. Add research papers**

Place fermentation PDF papers in `data/papers/`:
```
data/papers/lactic_acid_fermentation.pdf
data/papers/beer_fermentation_optimization.pdf
```

**6. Build the vector database**
```bash
python -m app.ingestion
```

Creates a local ChromaDB vector store in `vector_store/`. Re-run this whenever you add new papers.

---

## Run the app

**Streamlit UI**
```bash
streamlit run app/streamlit_app.py
```
Opens at `http://localhost:8501`

**FastAPI backend**
```bash
uvicorn app.api:app --reload
```
API docs at `http://127.0.0.1:8000/docs`

---

## Example questions

- What factors affect fermentation yield?
- How does temperature influence fermentation?
- What is the role of pH in fermentation?
- How can fermentation conditions be optimized?
- What are common challenges in lactic acid fermentation?

---

## API example

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What factors affect fermentation yield?\"}"
```

---

## Hallucination control

The prompt explicitly instructs the model to answer only using the retrieved research paper context. If the answer is not available in the provided chunks, it responds that it does not know based on the available papers — it does not fall back to general knowledge.

---

## Notes

- Only add open-access or legally usable PDFs to `data/papers/`
- `vector_store/` is generated locally and does not need to be pushed to GitHub
- Keep `.env` private — it contains your Groq API key

---

## Author

**Malatesh M Kalled**
[linkedin.com/in/malatesh-kalled](https://www.linkedin.com/in/malatesh-kalled) · [github.com/malateshkalled](https://github.com/malateshkalled)
