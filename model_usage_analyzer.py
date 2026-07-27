
api_calls = [
    {"id": "c001", "model": "gpt-4o",            "day": 1, "latency_ms": 823,  "tokens": 450,  "cost": 0.0062, "status": "success"},
    {"id": "c002", "model": "claude-3-5-sonnet",  "day": 1, "latency_ms": 1204, "tokens": 892,  "cost": 0.0027, "status": "success"},
    {"id": "c003", "model": "gpt-4o-mini",        "day": 1, "latency_ms": 312,  "tokens": 201,  "cost": 0.0001, "status": "success"},
    {"id": "c004", "model": "gpt-4o",             "day": 1, "latency_ms": 2341, "tokens": 1823, "cost": 0.0182, "status": "error"},
    {"id": "c005", "model": "claude-3-5-sonnet",  "day": 2, "latency_ms": 956,  "tokens": 634,  "cost": 0.0019, "status": "success"},
    {"id": "c006", "model": "gemini-1.5-pro",     "day": 2, "latency_ms": 445,  "tokens": 312,  "cost": 0.0008, "status": "success"},
    {"id": "c007", "model": "gpt-4o",             "day": 2, "latency_ms": 1102, "tokens": 987,  "cost": 0.0099, "status": "success"},
    {"id": "c008", "model": "claude-3-haiku",     "day": 2, "latency_ms": 198,  "tokens": 150,  "cost": 0.0002, "status": "success"},
    {"id": "c009", "model": "gemini-1.5-pro",     "day": 2, "latency_ms": 3201, "tokens": 2100, "cost": 0.0021, "status": "error"},
    {"id": "c010", "model": "gpt-4o-mini",        "day": 2, "latency_ms": 289,  "tokens": 178,  "cost": 0.0001, "status": "success"},
]

print(f"Loaded {len(api_calls)} records")

# Step 2: Unique models
all_models = set(call["model"] for call in api_calls)
print(f"\nUnique models used: {all_models}")
print(f"Total unique models: {len(all_models)}")

# Step 3: Separate successes and errors
successful = [call for call in api_calls if call["status"] == "success"]
errors = [call for call in api_calls if call["status"] == "error"]

print(f"\nSuccessful: {len(successful)}")
print(f"Errors: {len(errors)}")

# Group successful calls by model
by_model = {}
for call in successful:
    model = call["model"]
    if model not in by_model:
        by_model[model] = []
    by_model[model].append(call)

print("\nSuccessful calls per model:")
for model, calls in by_model.items():
    print(f"  {model}: {len(calls)} calls")

# Step 4: Slowest and most expensive
slowest = max(api_calls, key=lambda call: call["latency_ms"])
most_expensive = max(api_calls, key=lambda call: call["cost"])

print(f"\nSlowest call: {slowest['id']} | {slowest['model']} | {slowest['latency_ms']}ms")
print(f"Most expensive: {most_expensive['id']} | {most_expensive['model']} | ${most_expensive['cost']}")

# Step 5: Final report
total_tokens = sum(call["tokens"] for call in successful)
total_cost = sum(call["cost"] for call in successful)
avg_latency = sum(call["latency_ms"] for call in successful) / len(successful)

report = f"""
============================================================
  MODEL USAGE ANALYZER
  {len(api_calls)} calls across 2 days
============================================================

UNIQUE MODELS: {len(all_models)}
  {', '.join(sorted(all_models))}

SUMMARY
  Successful : {len(successful)}
  Errors     : {len(errors)}

ERRORS
  {errors[0]['id']} | {errors[0]['model']} | day {errors[0]['day']}
  {errors[1]['id']} | {errors[1]['model']} | day {errors[1]['day']}

STATISTICS (successful calls only)
  Total tokens : {total_tokens}
  Total cost   : ${round(total_cost, 4)}
  Avg latency  : {round(avg_latency, 1)}ms

MOST EXPENSIVE : {most_expensive['id']} | {most_expensive['model']} | ${most_expensive['cost']}
SLOWEST        : {slowest['id']} | {slowest['model']} | {slowest['latency_ms']}ms
============================================================
"""

print(report)