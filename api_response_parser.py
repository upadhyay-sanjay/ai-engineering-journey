# api_response_parser.py
# Day 4 — Error Handling
#
# Parses mock AI API responses safely.
# Handles missing fields, wrong data types, and HTTP errors
# using try/except and a custom exception hierarchy.


# ── Custom Exceptions ─────────────────────────────────────────────────────────

class AIClientError(Exception):
    """Base class for all AI client errors."""
    pass

class AuthenticationError(AIClientError):
    """Raised when the API key is invalid or missing (401)."""
    pass

class RateLimitError(AIClientError):
    """Raised when too many requests are sent (429)."""
    pass

class ModelNotFoundError(AIClientError):
    """Raised when the requested model does not exist (404)."""
    pass


# ── Mock API Responses ────────────────────────────────────────────────────────

responses = [
    {
        "id": "resp_001",
        "status_code": 200,
        "body": {
            "model": "gpt-4o",
            "choices": [{"message": {"content": "The capital of France is Paris."}}],
            "usage": {"total_tokens": 23}
        }
    },
    {
        "id": "resp_002",
        "status_code": 429,
        "body": {}
    },
    {
        "id": "resp_003",
        "status_code": 200,
        "body": {
            "model": "claude-3-5-sonnet",
            "choices": [{"message": {"content": "RAG stands for Retrieval-Augmented Generation."}}],
            "usage": {"total_tokens": 41}
        }
    },
    {
        "id": "resp_004",
        "status_code": 401,
        "body": {}
    },
    {
        "id": "resp_005",
        "status_code": 200,
        "body": {
            "model": "gpt-4o-mini",
            "choices": [{"message": {"content": 99}}],  # content is int, not str
            "usage": {"total_tokens": 10}
        }
    },
    {
        "id": "resp_006",
        "status_code": 404,
        "body": {}
    },
    {
        "id": "resp_007",
        "status_code": 200,
        "body": {
            "model": "claude-3-haiku",
            "choices": [{"message": {"content": "Embeddings are dense vector representations."}}]
            # "usage" key is missing
        }
    },
    {
        "id": "resp_008",
        "status_code": 500,
        "body": {}
    },
]


# ── Functions ─────────────────────────────────────────────────────────────────

def handle_http_error(status_code: int) -> None:
    """Raise the appropriate custom exception for a failed HTTP status code."""
    if status_code == 401:
        raise AuthenticationError("Invalid or missing API key")
    elif status_code == 429:
        raise RateLimitError("Too many requests — slow down and retry")
    elif status_code == 404:
        raise ModelNotFoundError("Requested model does not exist")
    elif status_code >= 400:
        raise AIClientError(f"Request failed with status {status_code}")


def parse_response(response: dict) -> dict:
    """
    Safely parse a single API response.
    Raises AIClientError subclasses for HTTP errors.
    Raises ValueError for malformed response bodies.
    Returns parsed content, model, and token count on success.
    """
    status_code = response["status_code"]

    # Handle HTTP errors first
    if status_code != 200:
        handle_http_error(status_code)

    body = response["body"]

    # Extract fields safely
    try:
        content = body["choices"][0]["message"]["content"]
        model   = body["model"]
        tokens  = body["usage"]["total_tokens"]
    except KeyError as e:
        raise ValueError(f"Malformed response: missing field {e}")

    # Validate content type
    if not isinstance(content, str):
        raise ValueError("Malformed response: content must be a string")

    return {"content": content, "model": model, "tokens": tokens}


# ── Main Report ───────────────────────────────────────────────────────────────

parsed     = []
auth_errors    = []
rate_errors    = []
model_errors   = []
server_errors  = []
malformed      = []

for response in responses:
    rid = response["id"]
    try:
        result = parse_response(response)
        parsed.append((rid, result))
    except AuthenticationError as e:
        auth_errors.append((rid, str(e)))
    except RateLimitError as e:
        rate_errors.append((rid, str(e)))
    except ModelNotFoundError as e:
        model_errors.append((rid, str(e)))
    except AIClientError as e:
        server_errors.append((rid, str(e)))
    except ValueError as e:
        malformed.append((rid, str(e)))

print("=" * 60)
print("  AI API RESPONSE PARSER")
print(f"  {len(responses)} responses processed")
print("=" * 60)

print(f"\nSUMMARY")
print(f"  Parsed successfully : {len(parsed)}")
print(f"  Authentication errors : {len(auth_errors)}")
print(f"  Rate limit errors     : {len(rate_errors)}")
print(f"  Model not found       : {len(model_errors)}")
print(f"  Server errors         : {len(server_errors)}")
print(f"  Malformed responses   : {len(malformed)}")

print(f"\nSUCCESSFULLY PARSED")
for rid, result in parsed:
    print(f"  {rid} | {result['model']:<22} | {result['tokens']} tokens | \"{result['content'][:45]}...\"")

print(f"\nFAILURES")
for rid, msg in auth_errors:
    print(f"  {rid} | AuthenticationError  — {msg}")
for rid, msg in rate_errors:
    print(f"  {rid} | RateLimitError       — {msg}")
for rid, msg in model_errors:
    print(f"  {rid} | ModelNotFoundError   — {msg}")
for rid, msg in server_errors:
    print(f"  {rid} | AIClientError        — {msg}")
for rid, msg in malformed:
    print(f"  {rid} | Malformed            — {msg}")

print("=" * 60)
