# Layer 2: Cost Killer

**Apply after**: Eval layer — you need a quality baseline before optimizing.
**Apply before**: Feedback — optimize the system before adding learning loops.

---

## The Ask
The MVP costs $X/day to run. Cut inference cost by 70% without degrading quality below the threshold your eval layer established.

## What You Must Produce
- Baseline cost measurement (per-query, per-day, projected at scale)
- Cost-quality tradeoff curve — show quality at each optimization level
- At least 3 optimization techniques applied and measured independently
- Serving architecture diagram — how requests flow through the optimized system
- Cost projection: "at 10x current traffic, this costs Y"

## What This Forces You to Learn
- Token economics and cost modeling
- Prompt caching (exact match, semantic cache, provider-level prompt caching)
- Model routing / cascading (cheap model for easy, expensive for hard)
- Prompt compression and optimization
- Batch vs streaming tradeoffs
- KV cache mechanics
- Embedding cost vs recomputation tradeoffs
- Request deduplication
- Async processing for non-urgent queries

## Serving Layer (you must speak this language to optimize cost)
- Model serving options: vLLM, TGI, TRT-LLM — what they are, when each matters
- API gateway design, rate limiting, load balancing
- Failover between providers (OpenAI down → Anthropic → self-hosted)
- Online vs offline: when to precompute vs serve live
- Queue-based architectures for async AI tasks

## Observability (you can't cut cost if you can't see cost)
- Logging every LLM call: inputs, outputs, latency, cost, token counts
- Tracing multi-step agent calls end-to-end
- Drift detection: is the system degrading over time?

## Interview Translation
"This pipeline costs $50K/month. The CEO wants it under $15K. What do you do?" — this is THE question for production AI roles. Theory people fumble here. You won't.

## Stretch
- Build a model router that classifies query difficulty and routes accordingly
- Implement semantic caching with cache invalidation
- Build a cost dashboard that shows per-query and per-tenant breakdown
