# =============================================================================
#  PYTHON EXERCISES — WEEK 1
#  AI Engineering Prerequisites
# =============================================================================
#
#  HOW TO USE THIS FILE
#  --------------------
#  1. Open this file in VS Code (or any editor)
#  2. Each problem has a description, starter data, and a YOUR SOLUTION section
#  3. Write your code where it says "# YOUR SOLUTION"
#  4. Run the file: python python_exercises_week1.py
#  5. Check your output against the EXPECTED OUTPUT comment
#
#  The data in these problems looks like what you'll actually work with
#  in AI Engineering: API responses, document metadata, query logs, etc.
#
#  Do NOT look at any solutions until you have made a genuine attempt.
#  Being stuck for 10 minutes is normal and part of learning.
# =============================================================================


# =============================================================================
#  TOPIC 1: Variables and Data Types
# =============================================================================
print("\n" + "="*60)
print("TOPIC 1: Variables and Data Types")
print("="*60)

# ── Problem 1.1 ──────────────────────────────────────────────
# You received an API response header that looks messy.
# Clean it up and check if it signals an error.
#
# Tasks:
#   a) Strip leading/trailing whitespace
#   b) Convert to lowercase
#   c) Check if it starts with "error"
#   d) Replace "gpt-4o" with "claude-3-5-sonnet"
#   e) Print all four results

raw_header = "  ERROR: Rate limit exceeded for model gpt-4o  "

# YOUR SOLUTION:

cleaned = raw_header.strip()
lowered = cleaned.lower()
print(lowered)
print(lowered.startswith("error"))
print(lowered.replace("gpt-4o", "claude-3-5-sonnet"))


# EXPECTED OUTPUT:
# error: rate limit exceeded for model gpt-4o
# True
# error: rate limit exceeded for model claude-3-5-sonnet


# ── Problem 1.2 ──────────────────────────────────────────────
# You have a model identifier string and need to extract parts of it.
# Model identifiers look like: "provider/model-name/version"
#
# Tasks:
#   a) Split the model_id into its three parts using "/"
#   b) Print provider, model name, and version separately
#   c) Check if the model name contains "claude" (case-insensitive)
#   d) Build a display string using an f-string:
#      "Model: claude-3-5-sonnet (v20241022) by Anthropic"

model_id = "Anthropic/claude-3-5-sonnet/v20241022"

# YOUR SOLUTION:
# YOUR SOLUTION:
# a) and b)
parts = model_id.split("/")
print(f"Provider: {parts[0]}")
print(f"Model: {parts[1]}")
print(f"Version: {parts[2]}")

# c)
print(f"Contains 'claude': {'claude' in parts[1].lower()}")

# d)
print(f"Model: {parts[1]} ({parts[2]}) by {parts[0]}")

# EXPECTED OUTPUT:
# Provider: Anthropic
# Model: claude-3-5-sonnet
# Version: v20241022
# Contains 'claude': True
# Model: claude-3-5-sonnet (v20241022) by Anthropic


# ── Problem 1.3 ──────────────────────────────────────────────
# Work with Python's different data types and understand how
# type() and isinstance() behave.
#
# Tasks:
#   a) Print the type of each variable below
#   b) Check: is token_count an int? (use isinstance)
#   c) Check: is temperature a float? (use isinstance)
#   d) Check: is model_name either a str or bytes? (isinstance can take a tuple)
#   e) Convert token_count to float, then check its type again

token_count = 1847
temperature = 0.7
model_name = "gpt-4o"
stream_enabled = True
system_prompt = None

# YOUR SOLUTION:
# a)
print(type(token_count))
print(type(temperature))
print(type(model_name))
print(type(stream_enabled))
print(type(system_prompt))

# b)
print(f"Is int: {isinstance(token_count, int)}")

# c)
print(f"Is float: {isinstance(temperature, float)}")

# d)
print(f"Is str or bytes: {isinstance(model_name, (str, bytes))}")

# e)
token_as_float = float(token_count)
print(f"After conversion: {type(token_as_float)}")



# EXPECTED OUTPUT (approximately):
# <class 'int'>
# <class 'float'>
# <class 'str'>
# <class 'bool'>
# <class 'NoneType'>
# Is int: True
# Is float: True
# Is str or bytes: True
# After conversion: <class 'float'>


# ── Problem 1.4 ──────────────────────────────────────────────
# Multi-line strings are used constantly for system prompts.
# Write a system prompt as a properly formatted multi-line string.
#
# Tasks:
#   a) Create a multi-line string variable called system_prompt that contains:
#        Line 1: "You are a helpful AI assistant specialized in legal documents."
#        Line 2: "Always cite the specific section you are drawing from."
#        Line 3: "If you are unsure, say so rather than guessing."
#   b) Print the prompt
#   c) Count how many lines it has (hint: splitlines())
#   d) Print the second line only

# YOUR SOLUTION:

# a) and b)
system_prompt = """You are a helpful AI assistant specialized in legal documents.
Always cite the specific section you are drawing from.
If you are unsure, say so rather than guessing."""

print(system_prompt)

# c)
lines = system_prompt.splitlines()
print(f"Number of lines: {len(lines)}")

# d)
print(f"Second line: {lines[1]}")

# EXPECTED OUTPUT:
# You are a helpful AI assistant specialized in legal documents.
# Always cite the specific section you are drawing from.
# If you are unsure, say so rather than guessing.
# Number of lines: 3
# Second line: Always cite the specific section you are drawing from.


# =============================================================================
#  TOPIC 2: Lists, Tuples, Sets, Dictionaries
# =============================================================================
print("\n" + "="*60)
print("TOPIC 2: Lists, Tuples, Sets, Dictionaries")
print("="*60)

# ── Problem 2.1 ──────────────────────────────────────────────
# You have a list of LLM API call records. Each record is a dict.
# This is exactly the kind of data you will process constantly.
#
# Tasks:
#   a) Print the number of records
#   b) Print the model used in the third call (index 2)
#   c) Print the last record using negative indexing
#   d) Create a new list containing only the 2nd through 4th records (slice)
#   e) Sort the records by latency_ms (lowest to highest) and print the sorted list
#   f) Find the record with the highest token_count

api_calls = [
    {"id": 1, "model": "gpt-4o",              "latency_ms": 823,  "token_count": 450,  "status": "success"},
    {"id": 2, "model": "claude-3-5-sonnet",   "latency_ms": 1204, "token_count": 892,  "status": "success"},
    {"id": 3, "model": "gpt-4o-mini",         "latency_ms": 312,  "token_count": 201,  "status": "success"},
    {"id": 4, "model": "claude-3-haiku",      "latency_ms": 198,  "token_count": 150,  "status": "success"},
    {"id": 5, "model": "gpt-4o",              "latency_ms": 2341, "token_count": 1823, "status": "error"},
    {"id": 6, "model": "claude-3-5-sonnet",   "latency_ms": 956,  "token_count": 634,  "status": "success"},
]

# YOUR SOLUTION:
# a)
print(f"Total records: {len(api_calls)}")

# b)
print(f"Third call model: {api_calls[2]['model']}")

# c)
print(f"Last record: {api_calls[-1]}")

# d)
records_2_to_4 = api_calls[1:4]
print(f"Records 2-4: {records_2_to_4}")

# e)
sorted_calls = sorted(api_calls, key=lambda call: call["latency_ms"])
for call in sorted_calls:
    print(f"  id {call['id']} | {call['model']} | {call['latency_ms']}ms")

# f)
highest = max(api_calls, key=lambda call: call["token_count"])
print(f"Highest token count: record id {highest['id']} with {highest['token_count']} tokens")




# EXPECTED OUTPUT:
# Total records: 6
# Third call model: gpt-4o-mini
# Last record: {'id': 6, 'model': 'claude-3-5-sonnet', ...}
# Records 2-4: [{'id': 2,...}, {'id': 3,...}, {'id': 4,...}]
# Sorted by latency (fastest first): id 4 (198ms), id 3 (312ms), ...
# Highest token count: record id 5 with 1823 tokens


# ── Problem 2.2 ──────────────────────────────────────────────
# Work with dictionaries — the data structure you will use most.
#
# Tasks:
#   a) Print all the keys in the config dict
#   b) Get the value of "max_tokens" safely (use .get() with a default of 1024)
#   c) Get a key that does NOT exist — "temperature" — safely with .get(),
#      default to 0.7
#   d) Add a new key "stream" with value True
#   e) Update "max_tokens" to 2048
#   f) Remove "stop_sequences" and print what was removed
#   g) Print all key-value pairs using .items()

config = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "system": "You are a helpful assistant.",
    "stop_sequences": ["\n\nHuman:", "\n\nAssistant:"],
    "top_p": 0.95,
}

# YOUR SOLUTION:
# ── Problem 2.2 ──────────────────────────────────────────────
# Work with dictionaries — the data structure you will use most.
#
# Tasks:
#   a) Print all the keys in the config dict
#   b) Get the value of "max_tokens" safely (use .get() with a default of 1024)
#   c) Get a key that does NOT exist — "temperature" — safely with .get(),
#      default to 0.7
#   d) Add a new key "stream" with value True
#   e) Update "max_tokens" to 2048
#   f) Remove "stop_sequences" and print what was removed
#   g) Print all key-value pairs using .items()

#a)
# ── Problem 2.2 ──────────────────────────────────────────────
# Work with dictionaries — the data structure you will use most.
#
# Tasks:
#   a) Print all the keys in the config dict
#   b) Get the value of "max_tokens" safely (use .get() with a default of 1024)
#   c) Get a key that does NOT exist — "temperature" — safely with .get(),
#      default to 0.7
#   d) Add a new key "stream" with value True
#   e) Update "max_tokens" to 2048
#   f) Remove "stop_sequences" and print what was removed
#   g) Print all key-value pairs using .items()

config = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "system": "You are a helpful assistant.",
    "stop_sequences": ["\n\nHuman:", "\n\nAssistant:"],
    "top_p": 0.95,
}

# YOUR SOLUTION:
# a)
print(f"Keys: {list(config.keys())}")

# b)
max_tokens = config.get("max_tokens", 1024)
print(f"max_tokens: {max_tokens}")

# c)
temperature = config.get("temperature", 0.7)
print(f"temperature: {temperature}")

# d)
config["stream"] = True

# e)
config["max_tokens"] = 2048

print(f"Updated config: {config}")

# f)
removed = config.pop("stop_sequences")
print(f"Removed: {removed}")

# g)
for key, value in config.items():
    print(f"  {key}: {value}")


# EXPECTED OUTPUT:
# Keys: dict_keys(['model', 'max_tokens', 'system', 'stop_sequences', 'top_p'])
# max_tokens: 1024
# temperature (default): 0.7
# After adding stream: True
# After updating max_tokens: 2048
# Removed stop_sequences: ['\n\nHuman:', '\n\nAssistant:']
# model: claude-3-5-sonnet-20241022
# max_tokens: 2048
# ...


# ── Problem 2.3 ──────────────────────────────────────────────
# Use sets for deduplication — a common data cleaning task.
#
# Tasks:
#   a) Find all UNIQUE models used across both days (union)
#   b) Find models used on BOTH days (intersection)
#   c) Find models used on day1 but NOT day2 (difference)
#   d) How many unique models were used across both days? (len of union)

day1_models = ["gpt-4o", "claude-3-5-sonnet", "gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet", "gpt-4o"]
day2_models = ["claude-3-5-sonnet", "gemini-1.5-pro", "gpt-4o", "gemini-1.5-pro", "claude-3-haiku"]

# YOUR SOLUTION:

# a)
set1 = set(day1_models)
set2 = set(day2_models)
all_unique = set1 | set2
print(f"All unique models: {all_unique}")

# b)
both_days = set1 & set2
print(f"Used both days: {both_days}")

# c)
only_day1 = set1 - set2
print(f"Only on day1: {only_day1}")

# d)
print(f"Total unique count: {len(all_unique)}")

# EXPECTED OUTPUT:
# All unique models: {'gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini', 'gemini-1.5-pro', 'claude-3-haiku'}
# Used both days: {'gpt-4o', 'claude-3-5-sonnet'}
# Only on day1: {'gpt-4o-mini'}
# Total unique count: 5


# ── Problem 2.4 ──────────────────────────────────────────────
# Build a lookup dictionary from a list — a pattern you'll use constantly
# when you need to quickly find a record by its ID.
#
# Tasks:
#   a) Build a dict called docs_by_id where the key is doc["id"]
#      and the value is the full doc dict
#   b) Look up doc with id "d002" directly
#   c) Check if "d005" exists in the lookup
#   d) Build a second dict called docs_by_source where the key is the source
#      and the value is a LIST of all docs from that source

documents = [
    {"id": "d001", "title": "Q3 Earnings Report", "source": "finance", "pages": 24},
    {"id": "d002", "title": "Privacy Policy v3",  "source": "legal",   "pages": 8},
    {"id": "d003", "title": "Q4 Earnings Report", "source": "finance", "pages": 31},
    {"id": "d004", "title": "Terms of Service",   "source": "legal",   "pages": 12},
    {"id": "d005", "title": "Employee Handbook",  "source": "hr",      "pages": 67},
]

# YOUR SOLUTION:

# a)
docs_by_id = {doc["id"]: doc for doc in documents}
print(f"Keys: {list(docs_by_id.keys())}")

# b)
print(f"d002: {docs_by_id['d002']}")

# c)
print(f"d005 exists: {'d005' in docs_by_id}")

# d)
docs_by_source = {}
for doc in documents:
    source = doc["source"]
    if source not in docs_by_source:
        docs_by_source[source] = []
    docs_by_source[source].append(doc["title"])

for source, titles in docs_by_source.items():
    print(f"  {source}: {titles}")


# EXPECTED OUTPUT:
# Doc d002: {'id': 'd002', 'title': 'Privacy Policy v3', 'source': 'legal', 'pages': 8}
# d005 exists: True
# finance docs: [{'id': 'd001'...}, {'id': 'd003'...}]
# legal docs: [{'id': 'd002'...}, {'id': 'd004'...}]
# hr docs: [{'id': 'd005'...}]


# =============================================================================
#  TOPIC 3: Control Flow
# =============================================================================
print("\n" + "="*60)
print("TOPIC 3: Control Flow")
print("="*60)

# ── Problem 3.1 ──────────────────────────────────────────────
# Write a function that categorizes an HTTP status code.
# This is exactly what you write when handling API responses.
#
# Tasks:
#   Write a function classify_status(code) that returns:
#     "success"           for 200-299
#     "redirect"          for 300-399
#     "client_error"      for 400-499, with special cases:
#                           401 → "unauthorized"
#                           403 → "forbidden"
#                           404 → "not_found"
#                           422 → "validation_error"
#                           429 → "rate_limited"
#     "server_error"      for 500-599
#     "unknown"           for anything else
#
# Test it against all the codes in test_codes

def classify_status(code):
    if 200 <= code <= 299:
        return "success"
    elif 300 <= code <= 399:
        return "redirect"
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


test_codes = [200, 201, 301, 400, 401, 403, 404, 422, 429, 500, 503, 999]

for code in test_codes:
    print(f"  {code} → {classify_status(code)}")

# EXPECTED OUTPUT:
#   200 → success
#   201 → success
#   301 → redirect
#   400 → client_error
#   401 → unauthorized
#   403 → forbidden
#   404 → not_found
#   422 → validation_error
#   429 → rate_limited
#   500 → server_error
#   503 → server_error
#   999 → unknown


# ── Problem 3.2 ──────────────────────────────────────────────
# Process a list of API calls and compute a summary.
# Use a for loop with conditionals.
#
# Tasks:
#   Loop through api_calls (from Problem 2.1 above).
#   Track and print:
#     a) Total number of calls
#     b) Number of successful calls
#     c) Number of error calls
#     d) Total tokens across ALL calls
#     e) Total tokens for successful calls only
#     f) The model with the most calls

api_calls_2 = [
    {"model": "gpt-4o",            "tokens": 450,  "status": "success"},
    {"model": "claude-3-5-sonnet", "tokens": 892,  "status": "success"},
    {"model": "gpt-4o-mini",       "tokens": 201,  "status": "success"},
    {"model": "claude-3-5-sonnet", "tokens": 150,  "status": "error"},
    {"model": "gpt-4o",            "tokens": 1823, "status": "error"},
    {"model": "claude-3-5-sonnet", "tokens": 634,  "status": "success"},
    {"model": "gpt-4o",            "tokens": 310,  "status": "success"},
    {"model": "gpt-4o-mini",       "tokens": 98,   "status": "success"},
]

# YOUR SOLUTION:
total = 0
successful = 0
errors = 0
total_tokens = 0
success_tokens = 0
model_counts = {}

for call in api_calls_2:
    total += 1
    total_tokens += call["tokens"]

    if call["status"] == "success":
        successful += 1
        success_tokens += call["tokens"]
    else:
        errors += 1

    model = call["model"]
    if model not in model_counts:
        model_counts[model] = 0
    model_counts[model] += 1

top_model = max(model_counts, key=lambda m: model_counts[m])

print(f"Total calls: {total}")
print(f"Successful: {successful}")
print(f"Errors: {errors}")
print(f"Total tokens (all calls): {total_tokens}")
print(f"Total tokens (successful only): {success_tokens}")
print(f"Most used model: {top_model} ({model_counts[top_model]} calls)")


# EXPECTED OUTPUT:
# Total calls: 8
# Successful: 6
# Errors: 2
# Total tokens (all calls): 4558
# Total tokens (successful only): 2585
# Most used model: claude-3-5-sonnet (3 calls)


# ── Problem 3.3 ──────────────────────────────────────────────
# Use a while loop with break and continue for a retry pattern.
# Retry logic is something you write for every AI API integration.
#
# Tasks:
#   Simulate a retry loop:
#   - You have a list of mock "responses" (some fail, some succeed)
#   - Try each response in order (use an index with a while loop)
#   - If the response is "rate_limited", print "Rate limited, retrying..." and continue
#   - If the response is "server_error", print "Server error, retrying..." and continue
#   - If the response is "success", print "Got response on attempt N" and break
#   - If you exhaust all attempts, print "All retries failed"
#   - Max 5 attempts

mock_responses = ["rate_limited", "rate_limited", "server_error", "success", "success"]

# YOUR SOLUTION:
# Sample responses from a server
responses = [
    "rate_limited",
    "server_error",
    "rate_limited",
    "server_error",
    "success"
]

index = 0
max_attempts = 5

while index < max_attempts:
    response = responses[index]
    index += 1

    if response == "rate_limited":
        print("Rate limited. Trying again...")
        continue

    if response == "server_error":
        print("Server error. Trying again...")
        continue

    if response == "success":
        print("Success! Request completed.")
        break

else:
    print("All retries failed")


# EXPECTED OUTPUT:
# Attempt 1: Rate limited, retrying...
# Attempt 2: Rate limited, retrying...
# Attempt 3: Server error, retrying...
# Got response on attempt 4
# Done.


# =============================================================================
#  TOPIC 4: Functions
# =============================================================================
print("\n" + "="*60)
print("TOPIC 4: Functions")
print("="*60)

# ── Problem 4.1 ──────────────────────────────────────────────
# Write a function to build an API request payload.
# Practice: required args, default args, type hints, docstrings, return value.
#
# Tasks:
#   Write build_message_payload(model, messages, max_tokens=1024,
#                               temperature=0.7, stream=False) -> dict
#   It should return a dict with all those fields.
#   Add a docstring explaining what it does and what each parameter is.
#   Call it three ways:
#     1. With only required arguments
#     2. With max_tokens=2048
#     3. With stream=True and temperature=0.0

# YOUR SOLUTION:
def build_message_payload(
    model: str,
    messages: list,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    stream: bool = False
) -> dict:
    """
    Build and return an API request payload.

    Parameters:
        model (str): The name of the model to use.
        messages (list): A list of messages to send to the model.
        max_tokens (int): Maximum number of tokens to generate.
                          Default is 1024.
        temperature (float): Controls randomness of the response.
                             Default is 0.7.
        stream (bool): Whether the response should be streamed.
                       Default is False.

    Returns:
        dict: A dictionary containing the API request settings.
    """

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream
    }

    return payload


# Sample messages
messages = [
    {"role": "user", "content": "Explain cloud computing."}
]


# 1. Only required arguments
payload1 = build_message_payload("example-model", messages)
print(payload1)


# 2. Change max_tokens to 2048
payload2 = build_message_payload(
    "example-model",
    messages,
    max_tokens=2048
)
print(payload2)


# 3. stream=True and temperature=0.0
payload3 = build_message_payload(
    "example-model",
    messages,
    stream=True,
    temperature=0.0
)
print(payload3)

# EXPECTED OUTPUT:
# {'model': 'claude-3-5-sonnet', 'messages': [...], 'max_tokens': 1024, 'temperature': 0.7, 'stream': False}
# {'model': 'claude-3-5-sonnet', 'messages': [...], 'max_tokens': 2048, 'temperature': 0.7, 'stream': False}
# {'model': 'claude-3-5-sonnet', 'messages': [...], 'max_tokens': 1024, 'temperature': 0.0, 'stream': True}


# ── Problem 4.2 ──────────────────────────────────────────────
# Write a function using **kwargs to build flexible API headers.
#
# Tasks:
#   Write build_headers(api_key: str, **extra_headers) -> dict
#   It must always include:
#     "Authorization": f"Bearer {api_key}"
#     "Content-Type": "application/json"
#   Any **extra_headers passed in should be merged in too.
#
#   Call it:
#     1. With just api_key
#     2. With api_key + anthropic_version="2023-06-01"
#     3. With api_key + x_request_id="req-abc123" + anthropic_version="2023-06-01"

# YOUR SOLUTION:
def build_headers(api_key: str, **extra_headers) -> dict:
    """
    Build API request headers.

    Parameters:
        api_key (str): The API key used for authorization.
        **extra_headers: Additional optional headers to include.

    Returns:
        dict: A dictionary containing the API headers.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Add any extra headers passed to the function
    headers.update(extra_headers)

    return headers


# 1. Just api_key
headers1 = build_headers("sk-test-key")
print(headers1)


# 2. api_key + anthropic_version
headers2 = build_headers(
    "sk-test-key",
    anthropic_version="2023-06-01"
)
print(headers2)


# 3. api_key + x_request_id + anthropic_version
headers3 = build_headers(
    "sk-test-key",
    x_request_id="req-abc123",
    anthropic_version="2023-06-01"
)
print(headers3)



# EXPECTED OUTPUT:
# {'Authorization': 'Bearer sk-test-key', 'Content-Type': 'application/json'}
# {'Authorization': 'Bearer sk-test-key', 'Content-Type': 'application/json', 'anthropic_version': '2023-06-01'}
# {'Authorization': 'Bearer sk-test-key', 'Content-Type': 'application/json', 'x_request_id': 'req-abc123', 'anthropic_version': '2023-06-01'}


# ── Problem 4.3 ──────────────────────────────────────────────
# Write a function that returns multiple values and use a lambda for sorting.
#
# Tasks:
#   a) Write compute_stats(latencies: list[int]) -> tuple
#      Returns (min, max, average, count) as a tuple.
#      Round the average to 1 decimal place.
#
#   b) Sort the model_results list by average_latency using a lambda.
#      Print from fastest to slowest average latency.

def compute_stats(latencies: list[int]) -> tuple:
    minimum = min(latencies)
    maximum = max(latencies)
    average = round(sum(latencies) / len(latencies), 1)
    count = len(latencies)
    return minimum, maximum, average, count

model_results = [
    {"model": "gpt-4o",            "latencies": [823, 956, 1102, 799, 2341]},
    {"model": "gpt-4o-mini",       "latencies": [312, 298, 341, 287, 325]},
    {"model": "claude-3-5-sonnet", "latencies": [1204, 892, 1056, 934, 1187]},
    {"model": "claude-3-haiku",    "latencies": [198, 221, 187, 243, 201]},
]

for result in model_results:
    mn, mx, avg, count = compute_stats(result["latencies"])
    print(f"  {result['model']}: min={mn}ms  max={mx}ms  avg={avg}ms  n={count}")

sorted_results = sorted(model_results, key=lambda r: compute_stats(r["latencies"])[2])

print("\nSorted fastest to slowest:")
for result in sorted_results:
    avg = compute_stats(result["latencies"])[2]
    print(f"  {result['model']}: {avg}ms avg")


# EXPECTED OUTPUT (stats):
#   gpt-4o: min=799ms  max=2341ms  avg=1204.2ms  n=5
#   gpt-4o-mini: min=287ms  max=341ms  avg=312.6ms  n=5
#   claude-3-5-sonnet: min=892ms  max=1204ms  avg=1054.6ms  n=5
#   claude-3-haiku: min=187ms  max=243ms  avg=210.0ms  n=5
#
# Sorted fastest to slowest:
#   claude-3-haiku: 210.0ms avg
#   gpt-4o-mini: 312.6ms avg
#   claude-3-5-sonnet: 1054.6ms avg
#   gpt-4o: 1204.2ms avg


# =============================================================================
#  TOPIC 5: Error Handling
# =============================================================================
print("\n" + "="*60)
print("TOPIC 5: Error Handling")
print("="*60)

# ── Problem 5.1 ──────────────────────────────────────────────
# Write a function that safely parses an API response.
# In real AI Engineering, API responses can be malformed, have
# missing fields, or contain unexpected types.
#
# Tasks:
#   Write parse_llm_response(raw: dict) -> dict that:
#     - Extracts: content (from raw["choices"][0]["message"]["content"])
#     - Extracts: model (from raw["model"])
#     - Extracts: total_tokens (from raw["usage"]["total_tokens"])
#     - If ANY key is missing (KeyError), raise a ValueError with message:
#       "Malformed response: missing field '{field_name}'"
#     - If content is not a string (TypeError), raise a ValueError:
#       "Malformed response: content must be a string"
#     - Returns {"content": ..., "model": ..., "total_tokens": ...}
#
#   Test with: good_response, missing_usage, wrong_type

def parse_llm_response(raw: dict) -> dict:
    try:
        content = raw["choices"][0]["message"]["content"]
        model = raw["model"]
        total_tokens = raw["usage"]["total_tokens"]
    except KeyError as error:
        field_name = error.args[0]
        raise ValueError(
            f"Malformed response: missing field '{field_name}'"
        ) from error

    if not isinstance(content, str):
        raise ValueError(
            "Malformed response: content must be a string"
        )

    return {
        "content": content,
        "model": model,
        "total_tokens": total_tokens,
    }


good_response = {
    "choices": [
        {
            "message": {
                "content": "The capital of France is Paris."
            }
        }
    ],
    "model": "gpt-4o",
    "usage": {
        "total_tokens": 23
    },
}

missing_usage = {
    "choices": [
        {
            "message": {
                "content": "The capital of France is Paris."
            }
        }
    ],
    "model": "gpt-4o",
    "usage": {
        # total_tokens is intentionally missing
    },
}

wrong_type = {
    "choices": [
        {
            "message": {
                "content": ["The capital of France is Paris."]
            }
        }
    ],
    "model": "gpt-4o",
    "usage": {
        "total_tokens": 23
    },
}


# Test the valid response
result = parse_llm_response(good_response)
print(
    f"good: content='{result['content']}', "
    f"tokens={result['total_tokens']}"
)


# Test the malformed responses
for test_name, response in [
    ("missing_usage", missing_usage),
    ("wrong_type", wrong_type),
]:
    try:
        parse_llm_response(response)
    except ValueError as error:
        print(f"{test_name}: ValueError — {error}")

# EXPECTED OUTPUT:
#   good: content='The capital of France is Paris.', tokens=23
#   missing_usage: ValueError — Malformed response: missing field 'total_tokens'
#   wrong_type: ValueError — Malformed response: content must be a string


# ── Problem 5.2 ──────────────────────────────────────────────
# Create a custom exception hierarchy for an AI API client.
# Custom exceptions let callers handle different failure modes differently.
#
# Tasks:
#   Create these exception classes:
#     AIClientError(Exception)          — base class for all errors in your client
#     AuthenticationError(AIClientError) — bad API key (401)
#     RateLimitError(AIClientError)      — too many requests (429)
#     ModelNotFoundError(AIClientError)  — model doesn't exist (404)
#
#   Write handle_api_error(status_code: int, message: str) that:
#     raises AuthenticationError if status_code == 401
#     raises RateLimitError if status_code == 429
#     raises ModelNotFoundError if status_code == 404
#     raises AIClientError for anything else >= 400
#
#   Test it with codes: 401, 429, 404, 500

# YOUR SOLUTION:
# Base exception for every error produced by the AI client
class AIClientError(Exception):
    pass


# Specific AI client exceptions
class AuthenticationError(AIClientError):
    pass


class RateLimitError(AIClientError):
    pass


class ModelNotFoundError(AIClientError):
    pass


def handle_api_error(status_code: int, message: str) -> None:
    if status_code == 401:
        raise AuthenticationError(message)

    if status_code == 429:
        raise RateLimitError(message)

    if status_code == 404:
        raise ModelNotFoundError(message)

    if status_code >= 400:
        raise AIClientError(message)


# Test data
test_errors = [
    (401, "Invalid API key"),
    (429, "Too many requests"),
    (404, "Model not found"),
    (500, "Internal server error"),
]


# Run the tests
for status_code, message in test_errors:
    try:
        handle_api_error(status_code, message)
    except AIClientError as error:
        print(
            f"{status_code} \u2192 "
            f"{type(error).__name__}: {error}"
        )



# EXPECTED OUTPUT:
#   401 → AuthenticationError: Invalid API key
#   429 → RateLimitError: Too many requests
#   404 → ModelNotFoundError: Model not found
#   500 → AIClientError: Internal server error


# =============================================================================
#  TOPIC 6: List and Dict Comprehensions
# =============================================================================
print("\n" + "="*60)
print("TOPIC 6: List and Dict Comprehensions")
print("="*60)

# ── Problem 6.1 ──────────────────────────────────────────────
# Transform raw API call logs with comprehensions.
# Comprehensions are more readable and faster than equivalent for loops.
#
# Tasks (solve each with a SINGLE comprehension — no for loops):
#   a) Extract just the model names from api_log into a list
#   b) Extract model names for SUCCESSFUL calls only
#   c) Build a list of strings: "call_001: 823ms" (zero-pad the id to 3 digits)
#   d) Build a dict: {call_id: latency_ms} for all calls
#   e) Build a dict: {call_id: "fast"/"slow"} where fast = latency < 500

api_log = [
    {"call_id": 1, "model": "gpt-4o",            "latency_ms": 823,  "status": "success"},
    {"call_id": 2, "model": "claude-3-5-sonnet",  "latency_ms": 1204, "status": "success"},
    {"call_id": 3, "model": "gpt-4o-mini",        "latency_ms": 312,  "status": "success"},
    {"call_id": 4, "model": "claude-3-haiku",     "latency_ms": 198,  "status": "error"},
    {"call_id": 5, "model": "gpt-4o",             "latency_ms": 2341, "status": "error"},
    {"call_id": 6, "model": "claude-3-5-sonnet",  "latency_ms": 456,  "status": "success"},
]

# YOUR SOLUTION:
# a)
# b)
# c)
# d)
# e)


# EXPECTED OUTPUT:
# a) ['gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini', 'claude-3-haiku', 'gpt-4o', 'claude-3-5-sonnet']
# b) ['gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini', 'claude-3-5-sonnet']
# c) ['call_001: 823ms', 'call_002: 1204ms', 'call_003: 312ms', 'call_004: 198ms', 'call_005: 2341ms', 'call_006: 456ms']
# d) {1: 823, 2: 1204, 3: 312, 4: 198, 5: 2341, 6: 456}
# e) {1: 'slow', 2: 'slow', 3: 'fast', 4: 'fast', 5: 'slow', 6: 'fast'}


# ── Problem 6.2 ──────────────────────────────────────────────
# Clean a list of raw document chunks before sending them to an LLM.
# Bad chunks (empty, too short, duplicate) cause poor RAG performance.
#
# Tasks (each must be a single comprehension):
#   a) Strip whitespace from every chunk's "text" field
#      (produce a new list of dicts with the text stripped)
#   b) Filter out chunks where text length < 50 characters (after stripping)
#   c) Build a set of unique chunk texts (for deduplication)
#   d) Build a dict: {chunk["id"]: chunk["text"]} for all chunks > 50 chars

raw_chunks = [
    {"id": "c01", "text": "  Retrieval-Augmented Generation (RAG) is a technique that gives language models access to external knowledge.  "},
    {"id": "c02", "text": "   "},
    {"id": "c03", "text": "See above."},
    {"id": "c04", "text": "The vector database stores embeddings and enables semantic similarity search across millions of documents."},
    {"id": "c05", "text": "  Retrieval-Augmented Generation (RAG) is a technique that gives language models access to external knowledge.  "},
    {"id": "c06", "text": "Chunking strategy determines how documents are split before embedding."},
    {"id": "c07", "text": "  "},
]

# YOUR SOLUTION:
# a)
# b)
# c)
# d)


# EXPECTED OUTPUT:
# a) [{'id':'c01','text':'Retrieval-Augmented Generation...'}, {'id':'c02','text':''}, ...]
# b) 4 chunks remain (c01, c04, c05, c06)
# c) 3 unique texts (c01 and c05 are duplicates)
# d) {'c01': 'Retrieval-Augmented Generation...', 'c04': '...', 'c05': '...', 'c06': '...'}


# =============================================================================
#  TOPIC 7: Object-Oriented Programming
# =============================================================================
print("\n" + "="*60)
print("TOPIC 7: Object-Oriented Programming")
print("="*60)

# ── Problem 7.1 ──────────────────────────────────────────────
# Build an LLMClient class. This is the foundation of every
# AI application you will build.
#
# Tasks:
#   Build LLMClient with:
#     __init__(self, api_key: str, model: str, max_tokens: int = 1024)
#       Stores all three as instance variables.
#       Raises ValueError if api_key is empty or None.
#
#     build_payload(self, user_message: str, system: str = None) -> dict
#       Returns a dict with model, max_tokens, and messages.
#       If system is provided, prepend a system message to the messages list.
#
#     from_env() classmethod
#       Creates an LLMClient by reading OPENAI_API_KEY and
#       OPENAI_MODEL (default "gpt-4o") from environment variables.
#       Raises EnvironmentError if OPENAI_API_KEY is not set.
#
#     __repr__(self) -> str
#       Returns: "LLMClient(model='gpt-4o', max_tokens=1024)"

import os

class LLMClient:
    # YOUR SOLUTION:
    pass


# Test it:
client = LLMClient(api_key="sk-test-123", model="claude-3-5-sonnet", max_tokens=2048)
print(client)  # Should use __repr__

payload = client.build_payload("What is RAG?")
print(payload)

payload_with_system = client.build_payload(
    "What is RAG?",
    system="You are an expert in AI systems."
)
print(payload_with_system)

# Test ValueError:
try:
    bad_client = LLMClient(api_key="", model="gpt-4o")
except ValueError as e:
    print(f"Error: {e}")

# EXPECTED OUTPUT:
# LLMClient(model='claude-3-5-sonnet', max_tokens=2048)
# {'model': 'claude-3-5-sonnet', 'max_tokens': 2048, 'messages': [{'role': 'user', 'content': 'What is RAG?'}]}
# {'model': 'claude-3-5-sonnet', 'max_tokens': 2048, 'messages': [{'role': 'system', 'content': 'You are an expert in AI systems.'}, {'role': 'user', 'content': 'What is RAG?'}]}
# Error: api_key cannot be empty


# ── Problem 7.2 ──────────────────────────────────────────────
# Extend LLMClient with inheritance.
#
# Tasks:
#   Create AnthropicClient(LLMClient) that:
#     __init__ calls super().__init__ but hardcodes model to "claude-3-5-sonnet-20241022"
#       (caller can still override max_tokens)
#     build_headers(self) -> dict returns Anthropic-specific headers:
#       "x-api-key": self.api_key
#       "anthropic-version": "2023-06-01"
#       "content-type": "application/json"
#     __repr__ returns: "AnthropicClient(model='claude-3-5-sonnet-20241022', max_tokens=1024)"
#
#   AnthropicClient should inherit build_payload from LLMClient without changes.

class AnthropicClient(LLMClient):
    # YOUR SOLUTION:
    pass


ac = AnthropicClient(api_key="sk-ant-test")
print(ac)
print(ac.build_headers())
payload = ac.build_payload("Explain embeddings briefly.")
print(payload)

# EXPECTED OUTPUT:
# AnthropicClient(model='claude-3-5-sonnet-20241022', max_tokens=1024)
# {'x-api-key': 'sk-ant-test', 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}
# {'model': 'claude-3-5-sonnet-20241022', 'max_tokens': 1024, 'messages': [{'role': 'user', 'content': 'Explain embeddings briefly.'}]}


# =============================================================================
#  TOPIC 8: Modules, Imports, and Project Structure
# =============================================================================
print("\n" + "="*60)
print("TOPIC 8: Modules, Imports, and File I/O")
print("="*60)

# ── Problem 8.1 ──────────────────────────────────────────────
# Read, transform, and write JSON — the most common I/O pattern in AI Engineering.
#
# Tasks:
#   a) Read the data below as if it came from a file — parse the JSON string
#   b) Add a new field "word_count" to each document (count words in the "text" field)
#   c) Add a field "processed_at" with the current timestamp (use datetime)
#   d) Write the result to "processed_docs.json" with indentation of 2
#   e) Read it back and verify the word counts are correct

import json
from datetime import datetime

raw_json_string = '''
[
    {"id": "d001", "title": "RAG Overview", "text": "Retrieval augmented generation is a technique for grounding LLM responses in specific documents."},
    {"id": "d002", "title": "Embeddings", "text": "Text embeddings are dense vector representations that capture semantic meaning."},
    {"id": "d003", "title": "Vector Search", "text": "Vector search finds semantically similar documents by comparing embedding distances in high dimensional space."}
]
'''

# YOUR SOLUTION:


# EXPECTED OUTPUT:
# Wrote 3 documents to processed_docs.json
# d001: 14 words, processed_at: 2026-...
# d002: 10 words, processed_at: 2026-...
# d003: 14 words, processed_at: 2026-...


# ── Problem 8.2 ──────────────────────────────────────────────
# Load environment variables safely — a pattern you use on line 1
# of every real project.
#
# Tasks:
#   Write load_config() -> dict that:
#     - Reads these env vars: OPENAI_API_KEY, ANTHROPIC_API_KEY,
#       PINECONE_API_KEY, APP_ENV (default: "development"), MAX_TOKENS (default: "1024")
#     - Returns a dict with all five values
#     - Raises EnvironmentError listing ALL missing required keys
#       (OPENAI_API_KEY and ANTHROPIC_API_KEY are required; others have defaults)
#     - Converts MAX_TOKENS to int in the returned dict
#
#   Test it by temporarily setting/unsetting env vars with os.environ

def load_config() -> dict:
    # YOUR SOLUTION:
    pass


# Simulate having some keys set
os.environ["OPENAI_API_KEY"] = "sk-openai-test"
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"

config = load_config()
print(f"Loaded config: APP_ENV={config['APP_ENV']}, MAX_TOKENS={config['MAX_TOKENS']} (type: {type(config['MAX_TOKENS']).__name__})")

# Now test with a missing required key
del os.environ["ANTHROPIC_API_KEY"]
try:
    load_config()
except EnvironmentError as e:
    print(f"Caught: {e}")

# EXPECTED OUTPUT:
# Loaded config: APP_ENV=development, MAX_TOKENS=1024 (type: int)
# Caught: Missing required environment variables: ANTHROPIC_API_KEY


# =============================================================================
#  END OF WEEK 1 EXERCISES
# =============================================================================
print("\n" + "="*60)
print("Week 1 complete. Move to python_exercises_week2.py")
print("="*60)
