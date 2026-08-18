# log_cleaner.py
# Day 5 — List and Dict Comprehensions
#
# Takes a messy list of AI API log entries and cleans them up
# using list and dict comprehensions.
# No for loops used for data transformation — comprehensions only.


# ── Raw Log Data ──────────────────────────────────────────────────────────────
# Messy data: duplicate entries, whitespace in model names,
# failed calls mixed in, inconsistent formatting.

raw_logs = [
    {"call_id": 1,  "model": "  gpt-4o  ",          "latency_ms": 823,  "tokens": 512,  "status": "success"},
    {"call_id": 2,  "model": "claude-3-5-sonnet",    "latency_ms": 1204, "tokens": 891,  "status": "success"},
    {"call_id": 3,  "model": "  GPT-4O  ",           "latency_ms": 312,  "tokens": 0,    "status": "error"},
    {"call_id": 4,  "model": "claude-3-haiku",       "latency_ms": 198,  "tokens": 210,  "status": "success"},
    {"call_id": 5,  "model": "gpt-4o-mini",          "latency_ms": 289,  "tokens": 178,  "status": "success"},
    {"call_id": 6,  "model": "  Claude-3-5-Sonnet ", "latency_ms": 956,  "tokens": 634,  "status": "success"},
    {"call_id": 7,  "model": "gpt-4o",               "latency_ms": 2341, "tokens": 0,    "status": "error"},
    {"call_id": 8,  "model": "claude-3-haiku",       "latency_ms": 201,  "tokens": 198,  "status": "success"},
    {"call_id": 9,  "model": "  gpt-4o-mini  ",      "latency_ms": 301,  "tokens": 165,  "status": "success"},
    {"call_id": 10, "model": "Claude-3-5-Sonnet",    "latency_ms": 887,  "tokens": 0,    "status": "error"},
]


# ── Step 1: Clean model names ─────────────────────────────────────────────────
# Strip whitespace and convert to lowercase so "  GPT-4O  " == "gpt-4o"

cleaned_logs = [
    {**log, "model": log["model"].strip().lower()}
    for log in raw_logs
]


# ── Step 2: Separate successes and errors ─────────────────────────────────────

successful = [log for log in cleaned_logs if log["status"] == "success"]
failed     = [log for log in cleaned_logs if log["status"] == "error"]


# ── Step 3: Extract unique models ─────────────────────────────────────────────

all_models    = [log["model"] for log in cleaned_logs]
unique_models = sorted(set(all_models))


# ── Step 4: Build a lookup dict by call_id ────────────────────────────────────

logs_by_id = {log["call_id"]: log for log in cleaned_logs}


# ── Step 5: Classify each call as fast, medium, or slow ──────────────────────

speed_labels = {
    log["call_id"]: (
        "fast"   if log["latency_ms"] < 400  else
        "medium" if log["latency_ms"] < 1000 else
        "slow"
    )
    for log in cleaned_logs
}


# ── Step 6: Total tokens per model (successful calls only) ───────────────────

token_totals = {
    model: sum(log["tokens"] for log in successful if log["model"] == model)
    for model in unique_models
}


# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  AI API LOG CLEANER")
print(f"  {len(raw_logs)} raw entries processed")
print("=" * 60)

print(f"\nOVERALL")
print(f"  Successful : {len(successful)}")
print(f"  Failed     : {len(failed)}")

print(f"\nUNIQUE MODELS DETECTED")
for model in unique_models:
    print(f"  {model}")

print(f"\nFAILED CALLS")
for log in failed:
    print(f"  call_{log['call_id']:03d} | {log['model']:<22} | {log['latency_ms']}ms")

print(f"\nSPEED BREAKDOWN")
for log in cleaned_logs:
    label = speed_labels[log["call_id"]]
    print(f"  call_{log['call_id']:03d} | {log['model']:<22} | {log['latency_ms']}ms | {label}")

print(f"\nTOTAL TOKENS PER MODEL (successful calls only)")
for model, tokens in sorted(token_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model:<22} | {tokens} tokens")

print("=" * 60)
