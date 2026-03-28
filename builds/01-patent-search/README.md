# needleStack

> 10K patents. one buried prior art. find it.

RAG system that takes a patent abstract and surfaces related prior art with exact passage references. not "here's a similar document" — here's the paragraph, here's why it's relevant, here's the citation.

## what you're building

- ingest 10K+ patent documents (claims, abstracts, descriptions — each has different chunking needs)
- process multi-paragraph queries, not single questions
- return top-10 results in under 3 seconds with grounded citations
- show *why* each result is relevant

## what will break you

- **chunking**: patents have structure. ignore it and your retrieval tanks
- **embedding model selection**: general-purpose embeddings miss domain-specific similarity
- **reranking**: cross-encoder vs ColBERT — you'll need to pick and defend it
- **hybrid search**: dense-only won't cut it. BM25 + embeddings, weighted
- **multi-hop retrieval**: patent A references patent B which contains the actual prior art

## why this matters

every production AI team has a RAG system somewhere. this is the fastest way to learn retrieval engineering without waiting to inherit one at work.

## stretch

- metadata filtering (date, classification code, inventor)
- natural language queries alongside structured search
- user feedback loops for relevance tuning
