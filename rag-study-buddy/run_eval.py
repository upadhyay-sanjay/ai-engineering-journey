"""
Runs every question in data/eval_questions.json through the RAG pipeline and
prints a side-by-side comparison against the expected answer, so you can see
for yourself where retrieval/generation is working well and where it's
falling short -- before moving on to Step 6 (breaking it on purpose).

Run this with:
    python3 run_eval.py
"""

import json
from src.search import RAGSearch


def main():
    with open("data/eval_questions.json") as f:
        eval_questions = json.load(f)

    searcher = RAGSearch()

    for item in eval_questions:
        result = searcher.answer(item["question"])

        print("=" * 80)
        print(f"Q{item['id']} ({item['type']}): {item['question']}")
        print(f"\nEXPECTED: {item['expected_answer']}")
        print(f"\nGOT:      {result['answer']}")
        print(f"\nConfidence: {result['confidence']}")
        if result["sources"]:
            print("Sources used:")
            for src in result["sources"]:
                print(f"  - {src['source_file']} page {src['page']} (score {src['similarity_score']})")
        else:
            print("Sources used: none (fell back to 'I don't know')")
        print()


if __name__ == "__main__":
    main()
