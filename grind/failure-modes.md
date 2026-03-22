# Failure Mode Catalog

Things that break in production AI systems. Be able to diagnose each on a whiteboard cold.

## Retrieval Failures
- [ ] RAG returning irrelevant chunks — stale embeddings, bad chunking, wrong similarity metric
- [ ] Empty retrieval — query outside knowledge base domain
- [ ] Embedding drift — model update changes embedding space, old vectors become stale

## Agent Failures
- [ ] Infinite loops — circular tool calls, no termination condition
- [ ] Hallucinated tool calls — calling tools that don't exist or with wrong params
- [ ] Planning failures — wrong decomposition, missed dependencies

## Generation Failures
- [ ] Hallucination cascades — one wrong answer feeds into next step
- [ ] Format violations — JSON that doesn't parse, SQL that doesn't execute
- [ ] Token limit exceeded mid-generation

## Infrastructure Failures
- [ ] Latency spikes — one model call takes 30s, breaks the pipeline
- [ ] Provider outage — API returns 500s, no fallback
- [ ] Rate limit storms — retry logic amplifies the problem
- [ ] Cost spikes — 10x normal due to retry storms or prompt explosion
- [ ] Stale cache — serving outdated responses

## Safety Failures
- [ ] Prompt injection succeeds — user breaks out of instructions
- [ ] PII leaks in output — model memorization or retrieval of sensitive data
- [ ] Bias amplification — system consistently fails for certain user groups
