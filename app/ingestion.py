from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


def load_pdf_documents(papers_dir: Path | None = None):
    papers_path = papers_dir or settings.papers_dir
    pdf_paths = sorted(papers_path.glob("*.pdf"))

    if not pdf_paths:
        raise FileNotFoundError(
            f"No PDF files found in {papers_path}. Add fermentation research papers first."
        )

    documents = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(documents)


def build_vector_store(force_rebuild: bool = False) -> Chroma:
    settings.papers_dir.mkdir(parents=True, exist_ok=True)
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)

    embeddings = get_embeddings()

    if settings.chroma_dir.exists() and any(settings.chroma_dir.iterdir()) and not force_rebuild:
        return Chroma(
            persist_directory=str(settings.chroma_dir),
            embedding_function=embeddings,
        )

    documents = load_pdf_documents(settings.papers_dir)
    chunks = split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(settings.chroma_dir),
    )
    return vector_store


if __name__ == "__main__":
    store = build_vector_store(force_rebuild=True)
    print(f"Vector store ready at: {settings.chroma_dir}")
    print(f"Indexed papers from: {settings.papers_dir}")
