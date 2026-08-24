# rag_validator.py
# Day 9 — Pydantic
#
# Validates incoming queries and document chunks before they
# enter a RAG pipeline. Bad data is caught at the entry point
# with clear error messages before it touches any logic.

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Dict, List
from datetime import datetime


# ── Pydantic Models ───────────────────────────────────────────────────────────

class DocumentMetadata(BaseModel):
    source:      str
    page_number: Optional[int]  = None
    author:      Optional[str]  = None


class DocumentChunk(BaseModel):
    id:              str
    content:         str
    metadata:        DocumentMetadata
    embedding_model: str            = "text-embedding-3-small"
    score:           Optional[float] = None

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("content cannot be empty or whitespace")
        return v.strip()


class QueryRequest(BaseModel):
    question:   str
    collection: str                      = "default"
    top_k:      int                      = 5
    filters:    Optional[Dict[str, str]] = None

    @field_validator("question")
    @classmethod
    def question_min_length(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("question must be at least 10 characters")
        return v.strip()

    @field_validator("top_k")
    @classmethod
    def top_k_range(cls, v):
        if not (1 <= v <= 20):
            raise ValueError("top_k must be between 1 and 20")
        return v


class QueryResponse(BaseModel):
    answer:     str
    sources:    List[DocumentChunk]
    model_used: str
    latency_ms: int
    tokens_used: int


# ── Safe Parser ───────────────────────────────────────────────────────────────

def safe_parse_request(data: dict) -> tuple:
    """
    Safely parse a query request.
    Returns (QueryRequest, None) on success.
    Returns (None, error_message) on failure.
    """
    try:
        return QueryRequest(**data), None
    except Exception as e:
        return None, str(e)


def safe_parse_chunk(data: dict) -> tuple:
    """
    Safely parse a document chunk.
    Returns (DocumentChunk, None) on success.
    Returns (None, error_message) on failure.
    """
    try:
        return DocumentChunk(**data), None
    except Exception as e:
        return None, str(e)


# ── Test Data ─────────────────────────────────────────────────────────────────

incoming_requests = [
    {
        "label": "valid request",
        "data": {
            "question":   "What is retrieval augmented generation?",
            "collection": "ai_docs",
            "top_k":      3,
        }
    },
    {
        "label": "question too short",
        "data": {
            "question":   "What?",
            "collection": "default",
            "top_k":      5,
        }
    },
    {
        "label": "top_k too high",
        "data": {
            "question":   "How does vector search work in a RAG pipeline?",
            "collection": "default",
            "top_k":      50,
        }
    },
    {
        "label": "missing question field",
        "data": {
            "collection": "default",
            "top_k":      5,
        }
    },
    {
        "label": "valid request with filters",
        "data": {
            "question":   "What chunking strategy works best for legal documents?",
            "collection": "legal_docs",
            "top_k":      5,
            "filters":    {"author": "Jane Smith", "year": "2024"},
        }
    },
]

incoming_chunks = [
    {
        "label": "valid chunk",
        "data": {
            "id":       "c001",
            "content":  "RAG combines retrieval with generation to ground LLM responses in specific documents.",
            "metadata": {"source": "rag_overview.pdf", "page_number": 3},
        }
    },
    {
        "label": "empty content",
        "data": {
            "id":       "c002",
            "content":  "   ",
            "metadata": {"source": "rag_overview.pdf"},
        }
    },
    {
        "label": "missing metadata",
        "data": {
            "id":      "c003",
            "content": "Vector search finds semantically similar documents.",
        }
    },
    {
        "label": "valid chunk with score",
        "data": {
            "id":       "c004",
            "content":  "Chunking strategy determines how documents are split before embedding.",
            "metadata": {"source": "chunking_guide.pdf", "page_number": 1, "author": "Jane Smith"},
            "score":    0.87,
        }
    },
]


# ── Main Report ───────────────────────────────────────────────────────────────

print("=" * 60)
print("  RAG REQUEST VALIDATOR")
print(f"  {len(incoming_requests)} requests | {len(incoming_chunks)} chunks")
print("=" * 60)

# Validate requests
print(f"\nQUERY REQUESTS")
valid_requests = []
for item in incoming_requests:
    request, error = safe_parse_request(item["data"])
    if request:
        valid_requests.append(request)
        print(f"  ✓ {item['label']}")
        print(f"    question : \"{request.question[:50]}...\"" if len(request.question) > 50 else f"    question : \"{request.question}\"")
        print(f"    top_k    : {request.top_k} | collection: {request.collection}")
    else:
        first_error = error.split("Value error,")[-1].strip().split("\n")[0]
        print(f"  ✗ {item['label']}")
        print(f"    rejected : {first_error}")

# Validate chunks
print(f"\nDOCUMENT CHUNKS")
valid_chunks = []
for item in incoming_chunks:
    chunk, error = safe_parse_chunk(item["data"])
    if chunk:
        valid_chunks.append(chunk)
        score_str = f" | score: {chunk.score}" if chunk.score else ""
        print(f"  ✓ {item['label']}")
        print(f"    source   : {chunk.metadata.source}{score_str}")
        print(f"    content  : \"{chunk.content[:55]}...\"" if len(chunk.content) > 55 else f"    content  : \"{chunk.content}\"")
    else:
        first_error = error.split("Value error,")[-1].strip().split("\n")[0]
        print(f"  ✗ {item['label']}")
        print(f"    rejected : {first_error}")

# Summary
print(f"\nSUMMARY")
print(f"  Requests : {len(valid_requests)}/{len(incoming_requests)} passed validation")
print(f"  Chunks   : {len(valid_chunks)}/{len(incoming_chunks)} passed validation")
print(f"\nWHY THIS MATTERS")
print(f"  Bad data caught here never reaches the retrieval")
print(f"  or generation step. Failures are specific and")
print(f"  immediate instead of silent and hard to debug.")
print("=" * 60)
