# Production & System Design

The stuff that separates "I built a demo" from "I shipped it."

## Latency / Cost / Quality
- [ ] Token economics — pricing models, cost per query, cost at scale
- [ ] Caching strategies — semantic cache, KV cache, exact match cache
- [ ] Model routing — cheap model for easy, expensive for hard, classifier in front
- [ ] Batch vs streaming tradeoffs
- [ ] Async processing for non-urgent queries
- [ ] Prompt caching (provider-level, e.g. Anthropic prompt caching)
- [ ] Request deduplication

## Serving Infrastructure
- [ ] Model serving — vLLM, TGI, TRT-LLM (what they are, when each matters)
- [ ] API gateway design for LLM services
- [ ] Rate limiting — per-user, per-tenant, global
- [ ] Load balancing across model replicas
- [ ] Failover between providers (OpenAI → Anthropic → self-hosted)
- [ ] Self-hosted vs managed — cost crossover points

## Observability
- [ ] Logging LLM calls — inputs, outputs, latency, cost, token counts
- [ ] Tracing multi-step agents end-to-end
- [ ] Drift detection — data drift, embedding drift, concept drift
- [ ] Feedback loops — user signals back into system improvement
- [ ] A/B testing LLM outputs
- [ ] Alerting on quality degradation

## Online vs Offline
- [ ] When to precompute vs serve live
- [ ] Batch pipelines for enrichment vs real-time inference
- [ ] Queue-based architectures for async AI tasks
- [ ] Pre-embedding vs embed-on-query tradeoffs

## Data Pipelines for AI
- [ ] Document ingestion at scale
- [ ] Embedding pipelines — batch, incremental, refresh strategies
- [ ] Vector DB operations — index management, updates, deletes
- [ ] Knowledge base refresh — how often, full vs incremental
- [ ] Vector DB internals — HNSW vs IVF, quantization (PQ, SQ), index tuning
- [ ] When pgvector is enough vs dedicated vector DB (Pinecone/Qdrant/Weaviate)
