# doc_processor.py
# Day 7 — Modules, Imports, and File I/O
#
# Reads raw documents from a JSON file, enriches each one
# with metadata, saves the results to disk, and loads
# configuration securely from environment variables.
#
# This is step one of any RAG pipeline.

import json
import os
from datetime import datetime


# ── Config Loader ─────────────────────────────────────────────────────────────

def load_config() -> dict:
    """
    Load configuration from environment variables.
    Raises EnvironmentError if required keys are missing.
    API keys are never hardcoded in the file.
    """
    required = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing  = [key for key in required if not os.environ.get(key)]

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return {
        "openai_api_key":    os.environ.get("OPENAI_API_KEY"),
        "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
        "app_env":           os.environ.get("APP_ENV", "development"),
        "max_tokens":        int(os.environ.get("MAX_TOKENS", "1024")),
    }


# ── Document Processor ────────────────────────────────────────────────────────

def process_document(doc: dict) -> dict:
    """
    Enrich a raw document with metadata.
    Returns a new dict with added fields — does not modify the original.
    """
    text = doc["text"]
    return {
        **doc,
        "word_count":      len(text.split()),
        "char_count":      len(text),
        "processed_at":    datetime.now().isoformat(),
        "status":          "processed",
    }


def load_documents(filepath: str) -> list:
    """Read raw documents from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def save_documents(docs: list, filepath: str) -> None:
    """Save processed documents to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(docs, f, indent=2)


# ── Raw Data ──────────────────────────────────────────────────────────────────

raw_documents = [
    {
        "id":     "d001",
        "title":  "RAG Overview",
        "source": "internal",
        "text":   "Retrieval-Augmented Generation is a technique that gives language models access to external knowledge by retrieving relevant documents before generating a response."
    },
    {
        "id":     "d002",
        "title":  "Embeddings Explained",
        "source": "internal",
        "text":   "Text embeddings are dense vector representations that capture semantic meaning. Similar texts produce vectors that are close together in high-dimensional space."
    },
    {
        "id":     "d003",
        "title":  "Vector Search",
        "source": "internal",
        "text":   "Vector search finds semantically similar documents by comparing embedding distances. It enables searching by meaning rather than exact keyword matches."
    },
    {
        "id":     "d004",
        "title":  "Chunking Strategy",
        "source": "internal",
        "text":   "Chunking splits documents into smaller pieces before embedding. Chunk size affects retrieval quality — too large loses precision, too small loses context."
    },
    {
        "id":     "d005",
        "title":  "Prompt Engineering",
        "source": "internal",
        "text":   "Prompt engineering is the practice of designing inputs to AI models to get reliable, accurate, and useful outputs. It is a core skill in AI Engineering."
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────

RAW_FILE       = "raw_documents.json"
PROCESSED_FILE = "processed_documents.json"

# Step 1: Save raw documents to disk
save_documents(raw_documents, RAW_FILE)

# Step 2: Load them back
loaded_docs = load_documents(RAW_FILE)

# Step 3: Process each document
processed_docs = [process_document(doc) for doc in loaded_docs]

# Step 4: Save processed documents
save_documents(processed_docs, PROCESSED_FILE)

# Step 5: Load config from environment variables
os.environ["OPENAI_API_KEY"]    = "sk-openai-test"
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"

try:
    config = load_config()
    config_status = f"APP_ENV={config['app_env']} | MAX_TOKENS={config['max_tokens']}"
except EnvironmentError as e:
    config_status = f"Config error: {e}"

# Step 6: Print report
print("=" * 60)
print("  DOCUMENT PROCESSOR")
print(f"  {len(processed_docs)} documents processed")
print("=" * 60)

print(f"\nCONFIG")
print(f"  {config_status}")
print(f"  API keys loaded from environment — not hardcoded in file")

print(f"\nPROCESSED DOCUMENTS")
for doc in processed_docs:
    print(f"  {doc['id']} | {doc['title']:<25} | {doc['word_count']} words | {doc['char_count']} chars")

print(f"\nFILES WRITTEN")
print(f"  {RAW_FILE:<30} — raw input")
print(f"  {PROCESSED_FILE:<30} — enriched with word count, char count, timestamp")

print(f"\nWHY THIS MATTERS")
print(f"  In a RAG pipeline, you process documents once and save")
print(f"  them to disk. Next time the pipeline runs, it loads the")
print(f"  processed file instead of reprocessing everything.")
print("=" * 60)
