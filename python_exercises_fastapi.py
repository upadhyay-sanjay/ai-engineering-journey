# =============================================================================
#  PYTHON EXERCISES — FastAPI
#  AI Engineering Prerequisites
# =============================================================================
#
#  HOW TO RUN THIS FILE
#  --------------------
#  This is a FastAPI server, not a script. Run it like this:
#
#    uvicorn python_exercises_fastapi:app --reload
#
#  Then open your browser to:  http://localhost:8000/docs
#  That gives you an interactive UI to test every endpoint.
#
#  SETUP:
#    pip install fastapi uvicorn pydantic python-dotenv httpx
#
#  HOW TO WORK THROUGH THESE EXERCISES
#  ------------------------------------
#  Each exercise has a # TODO comment where you write your solution.
#  Start the server, hit the /docs page, test your endpoint, fix it, repeat.
#  There is a test script at the bottom — run it in a SECOND terminal:
#    python python_exercises_fastapi.py --test
#
#  COMPLETION STANDARD
#  -------------------
#  You are done when every endpoint in /docs works correctly,
#  auth blocks bad keys, validation rejects bad data with a 422,
#  and all tests in the test script pass.
# =============================================================================

import sys
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Header, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, Field

# =============================================================================
#  THE APP
# =============================================================================

app = FastAPI(
    title="AI Document Q&A API",
    description="Practice FastAPI server for AI Engineering prerequisites",
    version="1.0.0",
)

# CORS — allows any frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database" — a dict acting as storage for this exercise
# In real projects this would be PostgreSQL, MongoDB, etc.
documents_db: Dict[str, dict] = {}
queries_db: Dict[str, dict] = {}


# =============================================================================
#  EXERCISE 1: Pydantic Request/Response Models
# =============================================================================
# TODO: Define these Pydantic models. Every field type must be correct.
# These models are used by the endpoints below.

# DocumentCreate — used when a user uploads a document
#   title: str (required, min 3 characters)
#   content: str (required, cannot be empty/whitespace)
#   source: str (required)
#   tags: list of str (optional, default empty list)

# Document — returned when a document is retrieved
#   All fields from DocumentCreate, plus:
#   id: str
#   created_at: str
#   word_count: int

# QueryRequest — used when a user asks a question
#   question: str (required, min 10 characters)
#   collection: str (optional, default "default")
#   top_k: int (optional, default 5, must be between 1 and 20)

# QueryResponse — returned after processing a question
#   answer: str
#   sources: list of str (document ids used)
#   model_used: str
#   latency_ms: int

# TODO: Write your models here:

class DocumentCreate(BaseModel):
    title: str
    content: str
    source: str
    tags: List[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_title = value.strip()

        if len(cleaned_title) < 3:
            raise ValueError(
                "title must be at least 3 characters"
            )

        return cleaned_title

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned_content = value.strip()

        if not cleaned_content:
            raise ValueError(
                "content cannot be empty or whitespace"
            )

        return cleaned_content


class Document(DocumentCreate):
    id: str
    created_at: str
    word_count: int


class QueryRequest(BaseModel):
    question: str
    collection: str = "default"
    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned_question = value.strip()

        if len(cleaned_question) < 10:
            raise ValueError(
                "question must be at least 10 characters"
            )

        return cleaned_question


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    model_used: str
    latency_ms: int







# =============================================================================
#  EXERCISE 2: Authentication Dependency
# =============================================================================
# TODO: Write a dependency function called verify_api_key.
#
# It should:
#   - Accept x_api_key: str = Header(...) as a parameter
#     (FastAPI converts the header "X-API-Key" to x_api_key automatically)
#   - Compare it to the APP_API_KEY environment variable
#   - If the key is missing or wrong, raise HTTPException with status 401
#     and detail "Invalid or missing API key"
#   - If correct, return the key
#
# Create a .env file with:  APP_API_KEY=dev-secret-key-123
# Then test: calling with the right key works, wrong key gets 401.

# TODO: Write verify_api_key here:
def verify_api_key(x_api_key: str = Header(...)):
    expected = os.environ.get("APP_API_KEY", "dev-secret-key-123")
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key

# =============================================================================
#  EXERCISE 3: Basic Endpoints
# =============================================================================

# ── Endpoint 3.1: Health Check ────────────────────────────────────────────
# GET /health
# No auth required.
# Returns: {"status": "ok", "timestamp": "<current ISO timestamp>"}

@app.get("/health")
async def health_check():
    # TODO: Return the correct response
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
    #pass


# ── Endpoint 3.2: Create a Document ──────────────────────────────────────
# POST /documents
# Requires auth (use Depends(verify_api_key)).
# Accepts a DocumentCreate body.
# Does:
#   - Generates a UUID for the id: str(uuid.uuid4())
#   - Counts words in content: len(content.split())
#   - Sets created_at to current ISO timestamp: datetime.utcnow().isoformat()
#   - Stores the full document in documents_db[new_id] = {...}
#   - Returns the Document model (includes id, word_count, created_at)
# Status code: 201 Created

@app.post("/documents", status_code=status.HTTP_201_CREATED)
async def create_document(
    doc: DocumentCreate,
    api_key: str = Depends(verify_api_key)
):
    new_id = str(uuid.uuid4())
    document = {
        "id": new_id,
        "title": doc.title,
        "content": doc.content,
        "source": doc.source,
        "tags": doc.tags,
        "created_at": datetime.utcnow().isoformat(),
        "word_count": len(doc.content.split())
    }
    documents_db[new_id] = document
    return document

"""
@app.post("/documents", status_code=status.HTTP_201_CREATED)
async def create_document(
    # TODO: Add the request body parameter and the auth dependency
):
    # TODO: Implement
    pass
"""

# ── Endpoint 3.3: Get a Document by ID ───────────────────────────────────
# GET /documents/{document_id}
# No auth required.
# Path parameter: document_id (str)
# If document not found: raise 404 with detail "Document not found"
# Returns the Document

@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    # TODO: Implement

    doc = documents_db.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
    #pass


# ── Endpoint 3.4: List Documents ─────────────────────────────────────────
# GET /documents
# No auth required.
# Query parameters:
#   source: Optional[str] = None  — filter by source if provided
#   limit: int = 10               — max results to return (1-100)
# Returns: {"documents": [...], "total": N}

@app.get("/documents")
async def list_documents(
    source: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
):
    # TODO: Implement — filter and limit the documents_db
    docs = list(documents_db.values())
    if source:
        docs = [d for d in docs if d["source"] == source]
    return {"documents": docs[:limit], "total": len(docs)}
    #pass


# ── Endpoint 3.5: Delete a Document ──────────────────────────────────────
# DELETE /documents/{document_id}
# Requires auth.
# If document not found: raise 404
# Removes from documents_db.
# Returns: {"message": "Document deleted", "id": document_id}


@app.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    api_key: str = Depends(verify_api_key)
):
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    del documents_db[document_id]
    return {"message": "Document deleted", "id": document_id}

"""
@app.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    # TODO: Add auth dependency
):
    # TODO: Implement
    pass
"""

# =============================================================================
#  EXERCISE 4: Query Endpoint with Simulated LLM
# =============================================================================

# ── Endpoint 4.1: Ask a Question ─────────────────────────────────────────
# POST /query
# Requires auth.
# Accepts a QueryRequest body.
#
# Simulate what a real RAG system does:
#   1. Find documents whose content contains any word from the question
#      (simple keyword search — no real embeddings needed for this exercise)
#   2. Take the top_k most relevant documents (for now, just take the first top_k matches)
#   3. Build a fake "answer" string:
#      "Based on {len(relevant_docs)} source(s): {question} [simulated answer]"
#   4. Store the query in queries_db with a generated id
#   5. Return a QueryResponse:
#      answer = the fake answer string
#      sources = list of document ids used
#      model_used = "gpt-4o-simulated"
#      latency_ms = a random int between 200 and 1500
#      (use: import random; random.randint(200, 1500))
#
# If no documents exist yet, raise 400 with detail "No documents in collection"

import random

@app.post("/query")
async def query_documents(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    if not documents_db:
        raise HTTPException(status_code=400, detail="No documents in collection")
    
    words = request.question.lower().split()
    relevant_docs = [
        doc for doc in documents_db.values()
        if any(word in doc["content"].lower() for word in words)
    ][:request.top_k]
    
    answer = f"Based on {len(relevant_docs)} source(s): {request.question} [simulated answer]"
    query_id = str(uuid.uuid4())
    
    result = {
        "id": query_id,
        "question": request.question,
        "answer": answer,
        "sources": [doc["id"] for doc in relevant_docs],
        "model_used": "gpt-4o-simulated",
        "latency_ms": random.randint(200, 1500)
    }
    queries_db[query_id] = result
    return result


"""
async def query_documents(
    # TODO: Add request body and auth dependency
):
    # TODO: Implement
    pass
"""


# =============================================================================
#  EXERCISE 5: Query History
# =============================================================================

# ── Endpoint 5.1: Get All Queries ─────────────────────────────────────────
# GET /queries
# No auth required.
# Returns all past queries with their responses.
# Query parameter: limit: int = 20 (max 100)
# Returns: {"queries": [...], "total": N}

@app.get("/queries")
async def get_queries(limit: int = Query(default=20, ge=1, le=100)):
    # TODO: Implement
    queries = list(queries_db.values())
    return {"queries": queries[:limit], "total": len(queries)}
    #pass


# =============================================================================
#  EXERCISE 6: Error Handling and Edge Cases
# =============================================================================

# ── Endpoint 6.1: Simulate API Errors ────────────────────────────────────
# GET /simulate-error/{error_code}
# No auth required.
# For learning purposes: raise the right HTTPException for each code.
#   400 → "Bad request: invalid parameters"
#   401 → "Unauthorized: authentication required"
#   403 → "Forbidden: insufficient permissions"
#   404 → "Not found: resource does not exist"
#   422 → "Unprocessable entity: validation failed"
#   429 → "Too many requests: rate limit exceeded"
#   500 → "Internal server error"
#   Anything else → 400 with "Unknown error code"

@app.get("/simulate-error/{error_code}")
async def simulate_error(error_code: int):
    messages = {
        400: "Bad request: invalid parameters",
        401: "Unauthorized: authentication required",
        403: "Forbidden: insufficient permissions",
        404: "Not found: resource does not exist",
        422: "Unprocessable entity: validation failed",
        429: "Too many requests: rate limit exceeded",
        500: "Internal server error",
    }
    detail = messages.get(error_code, "Unknown error code")
    status_code = error_code if error_code in messages else 400
    raise HTTPException(status_code=status_code, detail=detail)
    
"""
@app.get("/simulate-error/{error_code}")
async def simulate_error(error_code: int):
    # TODO: Implement
    pass
"""

# =============================================================================
#  STARTUP EVENT
# =============================================================================

@app.on_event("startup")
async def startup():
    # Pre-populate with sample documents so you can test /query immediately
    sample_docs = [
        {
            "title": "Introduction to RAG",
            "content": "Retrieval augmented generation combines search with language models to produce grounded answers from specific documents.",
            "source": "ai_textbook",
            "tags": ["rag", "llm", "retrieval"],
        },
        {
            "title": "Vector Databases",
            "content": "Vector databases store embeddings and enable fast semantic similarity search using approximate nearest neighbor algorithms.",
            "source": "ai_textbook",
            "tags": ["vectors", "embeddings", "search"],
        },
        {
            "title": "Prompt Engineering",
            "content": "Effective prompts use clear instructions, examples, and constraints to guide language model behavior toward desired outputs.",
            "source": "ai_textbook",
            "tags": ["prompts", "llm"],
        },
    ]
    for doc in sample_docs:
        doc_id = str(uuid.uuid4())
        documents_db[doc_id] = {
            "id": doc_id,
            "title": doc["title"],
            "content": doc["content"],
            "source": doc["source"],
            "tags": doc["tags"],
            "word_count": len(doc["content"].split()),
            "created_at": datetime.utcnow().isoformat(),
        }
    print(f"[startup] Pre-loaded {len(documents_db)} sample documents.")


# =============================================================================
#  TEST SCRIPT
#  Run in a second terminal: python python_exercises_fastapi.py --test
#  The server must already be running in the first terminal.
# =============================================================================

def run_tests():
    import httpx

    BASE = "http://localhost:8000"
    API_KEY = os.getenv("APP_API_KEY", "dev-secret-key-123")
    GOOD_HEADERS = {"X-API-Key": API_KEY}
    BAD_HEADERS  = {"X-API-Key": "wrong-key"}

    passed = 0
    failed = 0

    def check(label, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  PASS  {label}")
            passed += 1
        else:
            print(f"  FAIL  {label}  {detail}")
            failed += 1

    print("\n" + "="*60)
    print("Running FastAPI Exercise Tests")
    print("="*60)

    # Health check
    r = httpx.get(f"{BASE}/health")
    check("GET /health returns 200",          r.status_code == 200)
    check("GET /health has 'status': 'ok'",   r.json().get("status") == "ok")
    check("GET /health has 'timestamp'",       "timestamp" in r.json())

    # Auth
    r = httpx.post(f"{BASE}/documents", json={"title": "Test", "content": "x"*50, "source": "test"}, headers=BAD_HEADERS)
    check("POST /documents with bad key returns 401", r.status_code == 401)

    # Create document
    payload = {"title": "My Test Doc", "content": "This document is about retrieval augmented generation systems.", "source": "manual", "tags": ["test"]}
    r = httpx.post(f"{BASE}/documents", json=payload, headers=GOOD_HEADERS)
    check("POST /documents with good key returns 201", r.status_code == 201)
    check("POST /documents returns id",                "id" in r.json())
    check("POST /documents returns word_count",        r.json().get("word_count", 0) > 0)
    doc_id = r.json().get("id", "")

    # Validation: title too short
    r = httpx.post(f"{BASE}/documents", json={"title": "Hi", "content": "Some content here", "source": "test"}, headers=GOOD_HEADERS)
    check("POST /documents with short title returns 422", r.status_code == 422)

    # Get document
    r = httpx.get(f"{BASE}/documents/{doc_id}")
    check("GET /documents/{id} returns 200",           r.status_code == 200)
    check("GET /documents/{id} has correct title",     r.json().get("title") == "My Test Doc")

    # Get missing document
    r = httpx.get(f"{BASE}/documents/nonexistent-id")
    check("GET /documents/bad-id returns 404",         r.status_code == 404)

    # List documents
    r = httpx.get(f"{BASE}/documents")
    check("GET /documents returns 200",                r.status_code == 200)
    check("GET /documents has 'documents' list",       "documents" in r.json())
    check("GET /documents has 'total'",                "total" in r.json())

    # List with source filter
    r = httpx.get(f"{BASE}/documents?source=ai_textbook")
    check("GET /documents?source= filters correctly",  all(d["source"] == "ai_textbook" for d in r.json()["documents"]))

    # Query
    r = httpx.post(f"{BASE}/query", json={"question": "What is retrieval augmented generation?"}, headers=GOOD_HEADERS)
    check("POST /query returns 200",                   r.status_code == 200)
    check("POST /query returns answer",                "answer" in r.json())
    check("POST /query returns sources list",          isinstance(r.json().get("sources"), list))
    check("POST /query returns latency_ms",            isinstance(r.json().get("latency_ms"), int))

    # Query validation: question too short
    r = httpx.post(f"{BASE}/query", json={"question": "Short"}, headers=GOOD_HEADERS)
    check("POST /query with short question returns 422", r.status_code == 422)

    # Query history
    r = httpx.get(f"{BASE}/queries")
    check("GET /queries returns 200",                  r.status_code == 200)
    check("GET /queries has at least 1 result",        r.json().get("total", 0) >= 1)

    # Error simulation
    r = httpx.get(f"{BASE}/simulate-error/404")
    check("GET /simulate-error/404 returns 404",       r.status_code == 404)
    r = httpx.get(f"{BASE}/simulate-error/429")
    check("GET /simulate-error/429 returns 429",       r.status_code == 429)

    # Delete
    r = httpx.delete(f"{BASE}/documents/{doc_id}", headers=GOOD_HEADERS)
    check("DELETE /documents/{id} returns 200",        r.status_code == 200)

    # Confirm deleted
    r = httpx.get(f"{BASE}/documents/{doc_id}")
    check("GET deleted document returns 404",          r.status_code == 404)

    # Delete with no auth
    r = httpx.delete(f"{BASE}/documents/any-id", headers=BAD_HEADERS)
    check("DELETE with bad key returns 401",           r.status_code == 401)

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed. FastAPI prerequisite COMPLETE.")
    else:
        print(f"{failed} test(s) failed. Fix the failing endpoints and re-run.")
    print("="*60)


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        print("To run the server:  uvicorn python_exercises_fastapi:app --reload")
        print("To run the tests:   python python_exercises_fastapi.py --test")
