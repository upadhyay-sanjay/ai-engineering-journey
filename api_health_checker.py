# api_health_checker.py
# Day 3 — Control Flow + Functions
#
# Simulates sending requests to an AI API endpoint.
# Classifies response codes, retries on failure,
# and produces a health report across multiple models.

# ── Data ─────────────────────────────────────────────────────────────────────

api_requests = [
    {"id": "r001", "model": "gpt-4o",            "status_code": 200, "latency_ms": 834,  "tokens": 512},
    {"id": "r002", "model": "claude-3-5-sonnet",  "status_code": 429, "latency_ms": 120,  "tokens": 0},
    {"id": "r003", "model": "claude-3-5-sonnet",  "status_code": 429, "latency_ms": 120,  "tokens": 0},
    {"id": "r004", "model": "claude-3-5-sonnet",  "status_code": 200, "latency_ms": 952,  "tokens": 789},
    {"id": "r005", "model": "gpt-4o-mini",        "status_code": 200, "latency_ms": 301,  "tokens": 210},
    {"id": "r006", "model": "gpt-4o",            "status_code": 500, "latency_ms": 3200, "tokens": 0},
    {"id": "r007", "model": "gpt-4o",            "status_code": 500, "latency_ms": 3200, "tokens": 0},
    {"id": "r008", "model": "gpt-4o",            "status_code": 200, "latency_ms": 870,  "tokens": 634},
    {"id": "r009", "model": "claude-3-haiku",     "status_code": 401, "latency_ms": 50,   "tokens": 0},
    {"id": "r010", "model": "gpt-4o-mini",        "status_code": 200, "latency_ms": 289,  "tokens": 198},
]


# ── Functions ─────────────────────────────────────────────────────────────────

def classify_status(code: int) -> str:
    """Return a human-readable label for an HTTP status code."""
    if 200 <= code <= 299:
        return "success"
    elif code == 401:
        return "unauthorized"
    elif code == 403:
        return "forbidden"
    elif code == 404:
        return "not_found"
    elif code == 422:
        return "validation_error"
    elif code == 429:
        return "rate_limited"
    elif 400 <= code <= 499:
        return "client_error"
    elif 500 <= code <= 599:
        return "server_error"
    else:
        return "unknown"


def is_retryable(code: int) -> bool:
    """Return True if this status code is worth retrying."""
    return code in (429, 500, 502, 503, 504)


def compute_model_stats(requests: list, model: str) -> tuple:
    """
    Compute success rate and average latency for a given model.
    Returns (total, successes, success_rate, avg_latency_ms).
    """
    model_requests = [r for r in requests if r["model"] == model]
    total = len(model_requests)
    successes = sum(1 for r in model_requests if 200 <= r["status_code"] <= 299)
    success_rate = round((successes / total) * 100, 1) if total > 0 else 0.0

    successful_latencies = [r["latency_ms"] for r in model_requests if 200 <= r["status_code"] <= 299]
    avg_latency = round(sum(successful_latencies) / len(successful_latencies), 1) if successful_latencies else 0.0

    return total, successes, success_rate, avg_latency


def simulate_retry(request: dict, max_retries: int = 3) -> str:
    """
    Simulate retry logic for a failed request.
    Returns the outcome after retries.
    """
    code = request["status_code"]
    attempts = 0

    while attempts < max_retries:
        attempts += 1
        if not is_retryable(code):
            return f"not retried ({classify_status(code)})"
        if attempts < max_retries:
            continue  # keep retrying
        else:
            break

    return f"failed after {attempts} retries"


# ── Main Report ───────────────────────────────────────────────────────────────

print("=" * 60)
print("  AI API HEALTH CHECKER")
print(f"  {len(api_requests)} requests processed")
print("=" * 60)

# Classify each request
successes = [r for r in api_requests if 200 <= r["status_code"] <= 299]
failures  = [r for r in api_requests if not (200 <= r["status_code"] <= 299)]

print(f"\nOVERALL")
print(f"  Successful : {len(successes)}")
print(f"  Failed     : {len(failures)}")
print(f"  Success rate: {round(len(successes) / len(api_requests) * 100, 1)}%")

# Failed request details with retry simulation
print(f"\nFAILED REQUESTS")
for r in failures:
    label   = classify_status(r["status_code"])
    outcome = simulate_retry(r)
    print(f"  {r['id']} | {r['model']:<22} | {r['status_code']} {label:<18} | {outcome}")

# Per-model breakdown
models = sorted(set(r["model"] for r in api_requests))
print(f"\nPER-MODEL BREAKDOWN")
for model in models:
    total, successes_count, rate, avg_lat = compute_model_stats(api_requests, model)
    print(f"  {model:<22} | {successes_count}/{total} succeeded ({rate}%) | avg latency: {avg_lat}ms")

# Healthiest model (highest success rate)
best_model = max(models, key=lambda m: compute_model_stats(api_requests, m)[2])
_, _, best_rate, _ = compute_model_stats(api_requests, best_model)
print(f"\nHEALTHIEST MODEL")
print(f"  {best_model} ({best_rate}% success rate)")

print("=" * 60)
