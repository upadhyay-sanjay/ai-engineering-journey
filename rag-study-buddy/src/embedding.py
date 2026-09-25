"""
Step 3: Embeddings

This file turns text into vectors ("embeddings") using a small, free,
open-source model that runs entirely on your own computer - no API key,
no cost, and no internet needed once the model has been downloaded once.

A vector is just a list of numbers that represents the meaning of a
piece of text, so that pieces of text with similar meaning end up with
similar numbers. That is what lets us search by "what does this sound
like" later, instead of only "does this exact word appear."
"""

from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        print(f"Loading embedding model: {self.model_name} (first run downloads it)")
        self.model = SentenceTransformer(self.model_name)
        print(f"Model loaded. Each piece of text becomes a vector of "
              f"{self.get_embedding_dimension()} numbers.")

    def get_embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def generate_embeddings(self, texts: list):
        """
        Takes a list of strings and returns a numpy array of vectors,
        one vector per string.
        """
        return self.model.encode(texts, show_progress_bar=True)


if __name__ == "__main__":
    manager = EmbeddingManager()
    sample_texts = [
        "Retrieval augmented generation reduces hallucination.",
        "The cat sat on the mat.",
    ]
    vectors = manager.generate_embeddings(sample_texts)
    print(f"\nGenerated {len(vectors)} vectors, each with {len(vectors[0])} numbers.")
    print("First 5 numbers of vector #1:", vectors[0][:5])
