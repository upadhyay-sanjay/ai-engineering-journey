"""
Step 3: Vector Store

Stores the vectors from embedding.py in a small local database (Chroma)
so you can search over them later, and so they persist on disk between
runs - you do not have to re-embed everything every single time.
"""

import os
import uuid
import chromadb


class VectorStore:
    def __init__(self, collection_name: str = "rag_study_buddy", persist_directory: str = "data/vector_store"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        print(f"Vector store ready. Existing documents in collection: {self.collection.count()}")

    def add_documents(self, documents: list, embeddings) -> None:
        """
        documents: list of LangChain Document objects (the chunks from data_loader.py)
        embeddings: the matching list/array of vectors from EmbeddingManager
        """
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents and embeddings must match")

        ids = []
        metadatas = []
        texts = []
        embedding_list = []

        for doc, embedding in zip(documents, embeddings):
            doc_id = str(uuid.uuid4())
            ids.append(doc_id)
            metadatas.append(dict(doc.metadata))
            texts.append(doc.page_content)
            embedding_list.append(embedding.tolist())

        self.collection.add(
            ids=ids,
            embeddings=embedding_list,
            metadatas=metadatas,
            documents=texts,
        )
        print(f"Added {len(documents)} chunks to the vector store. "
              f"Total now: {self.collection.count()}")
