# Build Plan & Progress

- [x] Step 1: Repo + corpus setup
- [x] Step 2: Data loader + chunking
- [x] Step 3: Embeddings + vector store
- [ ] Step 4: Evaluation question set (15-20 Q&A pairs)
- [ ] Step 5: Retrieval + generation with citations/confidence
- [ ] Step 6: Break it on purpose - FAILURES.md log
- [ ] Step 7: Streamlit UI + final README/post

## Lessons learned along the way

- **Step 3 edge case (found and fixed):** `build_index.py` was run more than
  once before the vector store had been cleared, and `vector_store.py`
  assigns a brand-new random ID to every chunk on every run instead of
  checking what's already stored. Result: the collection silently grew to
  296 duplicate chunks (2x the real 148) before this was caught by noticing
  "Existing documents in collection" was not 0 on what should have been a
  fresh build.
  - Fix applied: deleted `data/vector_store/` and re-ran `build_index.py`
    once for a clean baseline (confirmed: 0 existing -> 148 total).
  - Known limitation still in the code: if you add a new PDF to
    `data/docs/` later and just re-run `build_index.py`, it will
    re-embed and re-add ALL chunks (old + new), duplicating the old ones
    again. A real fix would check for existing IDs (e.g. hash the chunk
    text + source + page into a deterministic ID) before adding, or clear
    the store before every rebuild. Revisit this in Step 6.
