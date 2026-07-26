api_calls = [
    {"id": "c001", "model": "  gpt-4o  ",           "tokens": 1240, "cost": 0.0062, "latency": 1.8, "success": True,  "error": None},
    {"id": "c002", "model": "claude-3-5-sonnet",     "tokens": 890,  "cost": 0.0027, "latency": 0.9, "success": True,  "error": None},
    {"id": "c003", "model": "GPT-4O",                "tokens": 0,    "cost": 0.0,    "latency": 3.1, "success": False, "error": "Rate limit exceeded"},
    {"id": "c004", "model": "claude-3-haiku",         "tokens": 450,  "cost": 0.0006, "latency": 0.4, "success": True,  "error": None},
    {"id": "c005", "model": "  Claude-3-5-Sonnet ",  "tokens": 2100, "cost": 0.0063, "latency": 2.2, "success": True,  "error": None},
    {"id": "c006", "model": "gpt-4o-mini",           "tokens": 310,  "cost": 0.0001, "latency": 0.5, "success": False, "error": "context_length_exceeded"},
]

print(f"Loaded {len(api_calls)} records")

# Step 2: Clean model names
for call in api_calls:
    call["model"] = call["model"].strip().lower()

print("\nCleaned model names:")
for call in api_calls:
    print(f"  {call['id']} | {call['model']}")

# Step 3: Separate successes and failures
successful = []
failed = []

for call in api_calls:
    if call["success"]:
        successful.append(call)
    else:
        failed.append(call)

print(f"\nSuccessful calls: {len(successful)}")
print(f"Failed calls:     {len(failed)}")

print("\nFailed calls detail:")
for call in failed:
    error_msg = call["error"] if isinstance(call["error"], str) else "no error message"
    print(f"  {call['id']} | {call['model']} | {error_msg}")

    # Step 4: Compute statistics (successful calls only)
total_tokens = 0
total_cost = 0.0
total_latency = 0.0

for call in successful:
    total_tokens += call["tokens"]
    total_cost += call["cost"]
    total_latency += call["latency"]

avg_latency = total_latency / len(successful)

print(f"\nStatistics (successful calls only):")
print(f"  Total tokens : {total_tokens}")
print(f"  Total cost   : ${round(total_cost, 4)}")
print(f"  Avg latency  : {round(avg_latency, 2)}s")

# Step 5: Find most expensive call
most_expensive = successful[0]
for call in successful:
    if call["cost"] > most_expensive["cost"]:
        most_expensive = call

# Step 6: Print the final report
report = f"""
============================================================
  AI API CALL LOG ANALYZER
  {len(api_calls)} calls processed
============================================================

SUMMARY
  Successful calls : {len(successful)}
  Failed calls     : {len(failed)}

FAILED CALLS
  c003 | {failed[0]['model']:<20} | {failed[0]['error']}
  c006 | {failed[1]['model']:<20} | {failed[1]['error']}

STATISTICS (successful calls only)
  Total tokens : {total_tokens}
  Total cost   : ${round(total_cost, 4)}
  Avg latency  : {round(avg_latency, 2)}s

MOST EXPENSIVE CALL
  {most_expensive['id']} | {most_expensive['model']} | {most_expensive['tokens']} tokens | ${most_expensive['cost']}
============================================================
"""

print(report)