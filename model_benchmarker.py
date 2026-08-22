# model_benchmarker.py
# Day 8 — Async/Await
#
# Benchmarks multiple AI models concurrently.
# Streams each response word by word, handles failures gracefully,
# and produces a report showing speed, output size, and status.
#
# Combines: asyncio.gather(), async generators, error handling.

import asyncio
import time


# ── Mock Model Responses ──────────────────────────────────────────────────────
# In production these would be real API calls.
# Here we simulate different response times and occasional failures.

MOCK_RESPONSES = {
    "gpt-4o": {
        "text":    "GPT-4o provides fast and accurate responses suitable for most production use cases.",
        "delay":   0.8,
        "succeed": True,
    },
    "claude-3-5-sonnet": {
        "text":    "Claude 3.5 Sonnet excels at nuanced reasoning and long context understanding.",
        "delay":   1.2,
        "succeed": True,
    },
    "gemini-1.5-pro": {
        "text":    "Gemini 1.5 Pro handles multimodal inputs and very long contexts efficiently.",
        "delay":   1.0,
        "succeed": True,
    },
    "gpt-4o-mini": {
        "text":    "GPT-4o-mini is optimised for speed and cost at the expense of some capability.",
        "delay":   0.5,
        "succeed": True,
    },
    "claude-3-haiku": {
        "text":    "",
        "delay":   0.3,
        "succeed": False,  # simulated failure
    },
}


# ── Async Functions ───────────────────────────────────────────────────────────

async def fake_stream(text: str, delay: float = 0.03):
    """Async generator — yields one word at a time with a small delay."""
    for word in text.split():
        await asyncio.sleep(delay)
        yield word + " "


async def call_model(model: str) -> dict:
    """
    Simulate calling a single AI model.
    Streams the response, measures latency, handles failures.
    Returns a result dict with status, latency, and word count.
    """
    config     = MOCK_RESPONSES[model]
    start_time = time.perf_counter()

    try:
        # Simulate network latency
        await asyncio.sleep(config["delay"])

        if not config["succeed"]:
            raise ConnectionError(f"{model} returned a 503 Service Unavailable")

        # Stream the response
        full_text  = ""
        word_count = 0
        async for token in fake_stream(config["text"]):
            full_text  += token
            word_count += 1

        latency = round(time.perf_counter() - start_time, 2)

        return {
            "model":      model,
            "status":     "success",
            "latency_s":  latency,
            "word_count": word_count,
            "preview":    full_text.strip()[:60] + "...",
        }

    except Exception as e:
        latency = round(time.perf_counter() - start_time, 2)
        return {
            "model":      model,
            "status":     "error",
            "latency_s":  latency,
            "word_count": 0,
            "preview":    str(e),
        }


async def benchmark_all(models: list) -> list:
    """Call all models concurrently and return results."""
    tasks   = [call_model(model) for model in models]
    results = await asyncio.gather(*tasks)
    return list(results)


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    models = list(MOCK_RESPONSES.keys())

    print("=" * 60)
    print("  AI MODEL BENCHMARKER")
    print(f"  {len(models)} models benchmarked concurrently")
    print("=" * 60)

    start = time.perf_counter()
    results = await benchmark_all(models)
    total_time = round(time.perf_counter() - start, 2)

    # Sort by latency
    results.sort(key=lambda r: r["latency_s"])

    successes = [r for r in results if r["status"] == "success"]
    failures  = [r for r in results if r["status"] == "error"]

    print(f"\nOVERALL")
    print(f"  Total time (concurrent) : {total_time}s")
    print(f"  Sequential would take   : {sum(MOCK_RESPONSES[m]['delay'] for m in models):.1f}s")
    print(f"  Succeeded : {len(successes)}")
    print(f"  Failed    : {len(failures)}")

    print(f"\nRESULTS (fastest to slowest)")
    for r in results:
        status = "✓" if r["status"] == "success" else "✗"
        print(f"  {status} {r['model']:<22} | {r['latency_s']}s | {r['word_count']} words")

    if successes:
        print(f"\nRESPONSE PREVIEWS")
        for r in successes:
            print(f"  {r['model']}")
            print(f"    \"{r['preview']}\"")

    if failures:
        print(f"\nFAILURES")
        for r in failures:
            print(f"  {r['model']}: {r['preview']}")

    fastest = successes[0] if successes else None
    if fastest:
        print(f"\nFASTEST MODEL")
        print(f"  {fastest['model']} at {fastest['latency_s']}s")

    print("=" * 60)


asyncio.run(main())
