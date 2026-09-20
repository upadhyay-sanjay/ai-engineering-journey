# RAG Study Buddy

A personal RAG (Retrieval-Augmented Generation) assistant that answers questions
about my own AI-engineering learning materials - course transcripts, papers, and
docs - with source citations, a confidence score, and an honest "I don't know"
when the answer isn't grounded in the corpus.

Built as a hands-on follow-up to Krish Naik's "Complete RAG Crash Course With LangChain."

## Status
Step 1 complete: project scaffolding + first corpus document in place.
See PROGRESS.md for the full build plan and current status.

## Structure
- `data/docs/` - source documents (the corpus)
- `src/data_loader.py` - loads and parses documents
- `src/embedding.py` - converts text chunks into vector embeddings
- `src/vector_store.py` - stores and retrieves embeddings
- `src/search.py` - retrieval + LLM generation with citations
- `app.py` - Streamlit app entry point
