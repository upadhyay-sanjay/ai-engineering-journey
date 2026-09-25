"""
Run this once (and again any time you add new documents to data/docs/)
to build the searchable vector store:

    python3 build_index.py

It loads every PDF in data/docs/, splits them into chunks, converts each
chunk into a vector embedding, and saves everything into the local
vector store folder at data/vector_store/.
"""

from src.data_loader import load_all_documents, chunk_documents
from src.embedding import EmbeddingManager
from src.vector_store import VectorStore


def main():
    documents = load_all_documents()
    chunks = chunk_documents(documents)

    embedding_manager = EmbeddingManager()
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)

    vector_store = VectorStore()
    vector_store.add_documents(chunks, embeddings)

    print("\nIndex built successfully. Your vector store is saved in data/vector_store/.")


if __name__ == "__main__":
    main()
