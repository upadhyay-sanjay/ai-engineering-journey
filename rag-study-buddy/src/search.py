"""
Step 5: Retrieval + Generation (the "answering" half of RAG Study Buddy)

This file ties everything built so far into one working pipeline:

1. Take a question from a user.
2. Convert it into an embedding using the same model that indexed the documents.
3. Search the vector store for the most similar chunks.
4. If nothing similar enough is found, honestly say so instead of guessing.
5. Otherwise, hand the retrieved chunks ("context") to an LLM, along with the
   question, and ask it to answer using ONLY that context.
6. Return the answer along with its sources (which page it came from) and a
   confidence score, so you can see WHY the app gave the answer it gave.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.embedding import EmbeddingManager
from src.vector_store import VectorStore

load_dotenv()

# Below this similarity score, we don't trust the match enough to use it as
# context. This number is a starting guess -- Step 6 (breaking it on purpose)
# is where you'll actually tune this based on what you observe.
MIN_SIMILARITY_SCORE = 0.3


class RAGSearch:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-20b",
            temperature=0.1,
            max_tokens=1024,
        )

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """
        Turn the query into an embedding, search the vector store, and
        return the matching chunks along with a similarity score for each.
        """
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]

        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
        )

        retrieved = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc_text, metadata, distance in zip(documents, metadatas, distances):
            similarity_score = 1 - distance
            retrieved.append({
                "text": doc_text,
                "metadata": metadata,
                "similarity_score": similarity_score,
            })

        return retrieved

    def answer(self, query: str, top_k: int = 3) -> dict:
        """
        The full pipeline: retrieve relevant chunks, and if there are any
        good enough matches, generate an answer using the LLM. Otherwise,
        honestly say the document doesn't cover this -- this is the
        "I don't know" fallback from the product spec.
        """
        retrieved_docs = self.retrieve(query, top_k=top_k)

        good_matches = [
            doc for doc in retrieved_docs
            if doc["similarity_score"] >= MIN_SIMILARITY_SCORE
        ]

        if not good_matches:
            return {
                "answer": "I don't have enough information in this document to answer that confidently.",
                "sources": [],
                "confidence": 0.0,
            }

        context = "\n\n".join(doc["text"] for doc in good_matches)

        prompt = f"""Use the following context to answer the question. If the context doesn't contain the answer, say so honestly instead of guessing.

Context:
{context}

Question: {query}

Answer concisely:"""

        response = self.llm.invoke(prompt)

        sources = [
            {
                "page": doc["metadata"].get("page", "unknown"),
                "source_file": doc["metadata"].get("source_file", "unknown"),
                "similarity_score": round(doc["similarity_score"], 3),
            }
            for doc in good_matches
        ]

        # A simple, honest confidence score: the average similarity of the
        # chunks actually used. Not a fancy formula -- easy to reason about
        # and easy to explain later.
        confidence = round(
            sum(doc["similarity_score"] for doc in good_matches) / len(good_matches), 3
        )

        return {
            "answer": response.content,
            "sources": sources,
            "confidence": confidence,
        }


if __name__ == "__main__":
    searcher = RAGSearch()
    test_query = "What does the acronym RAG stand for?"
    result = searcher.answer(test_query)

    print(f"\nQuestion: {test_query}")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
    print("Sources:")
    for src in result["sources"]:
        print(f"  - {src['source_file']} (page {src['page']}, score {src['similarity_score']})")
