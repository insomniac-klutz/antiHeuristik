# Build 01: Patent Prior-Art Search

## The Ask
Build a RAG system that takes a patent abstract and finds related prior art from a corpus of patent documents. Results must include citations with exact passage references.

## Constraints
- Corpus: 10K+ patent documents (use USPTO open data or synthetic)
- Must handle multi-paragraph queries (not just single questions)
- Results must show *why* each result is relevant (grounded citations)
- Latency target: <3s for top-10 results

## What This Forces You to Learn
- Chunking strategies (patents have structure — claims, abstracts, descriptions)
- Embedding model selection and evaluation
- Reranking (cross-encoder vs ColBERT)
- Hybrid search (dense + sparse, BM25 + embeddings)
- Vector DB setup and index tuning
- Citation/grounding — not just retrieval but *showing your work*
- Multi-hop retrieval (one patent references another)

## Interview Translation
"Design a RAG system for [domain]" — this is the most common system design question in Applied AI interviews. This build IS the prep.

## Stretch
- Add metadata filtering (by date, classification code, inventor)
- Handle queries in natural language ("find patents about using transformers for protein folding")
- Add a feedback loop where users mark results as relevant/irrelevant
