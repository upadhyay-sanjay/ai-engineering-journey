
# AI Engineering Journey
Learning AI Engineering from scratch. Each file covers one topic with a real, runnable example.

## Day 1: api_log_analyzer.py
Analyzes AI API call logs — cleans model names, computes cost and latency stats, surfaces errors.
Covers: str, int, float, bool, None, string methods, f-strings, multi-line strings.

Run it: python3 api_log_analyzer.py

## Day 2: model_usage_analyzer.py
Analyzes AI API call logs across multiple days — groups by model, finds slowest and most expensive calls, removes duplicate models with sets.
Covers: lists, dicts, sets, list comprehensions, grouping patterns.

Run it: python3 model_usage_analyzer.py

## Day 3: api_health_checker.py
Simulates AI API requests across multiple models — classifies response codes, retries on failure, and produces a health report with per-model success rates and latency.
Covers: functions, default arguments, type hints, docstrings, return values, if/elif/else, while loops, break/continue.

Run it: python3 api_health_checker.py

## python_exercises_week1.py
Weekly exercise file covering Topics 1-5: Variables & Data Types, Lists/Dicts/Sets, Control Flow, Functions, and Error Handling.

Run it: python3 python_exercises_week1.py

## Day 4: api_response_parser.py
Parses mock AI API responses. It handles missing fields, wrong data types, and HTTP errors using custom exceptions.
Covers: try/except, custom exception classes, raising errors, ValueError, KeyError.

Run it: python3 api_response_parser.py

## Day 5: log_cleaner.py
Cleans messy AI API log entries using list and dict comprehensions — strips whitespace from model names, separates successes from errors, removes duplicates, classifies call speed, and totals tokens per model.
Covers: list comprehensions, dict comprehensions, filtering, transforming, set deduplication.

Run it: python3 log_cleaner.py

## Day 6: llm_client.py
A client that sends requests to both OpenAI and Anthropic using the same code structure. Demonstrates inheritance — one base class holds shared logic, each provider only defines what is different.
Covers: classes, __init__, inheritance, super(), __repr__, methods.

Run it: python3 llm_client.py

## Day 7: doc_processor.py
Reads raw documents, enriches each one with word count, character count, and timestamp, saves results to disk, and loads config securely from environment variables.
Covers: json.load, json.dump, datetime, os.environ, environment variables, file I/O.

Run it: python3 doc_processor.py
