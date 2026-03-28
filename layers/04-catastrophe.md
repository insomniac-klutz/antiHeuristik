# Layer 4: Catastrophe

**Apply after**: All other layers — the system is measured, optimized, and learning. Now break it.
**This is the final layer.** Debrief comes after this.

---

## The Ask
Inject 5+ realistic failure modes into this build. Debug them live, under time pressure, as if it's a production incident. Write the post-mortem for each.

## Failure Menu (pick 5+ relevant to THIS build)

### Retrieval Failures
- RAG returning irrelevant chunks (embedding drift, stale index)
- Vector DB index corrupted / returns wrong nearest neighbors
- Stale data served from cache after knowledge base update

### Agent Failures
- Agent stuck in infinite loop (circular tool calls)
- Hallucination cascade (one wrong answer feeds into next step)
- Tool returns unexpected format, agent can't recover

### Infrastructure Failures
- Latency spike (one model call takes 30s, breaks the pipeline)
- Model provider outage (API returns 500s)
- Rate limit hit on external API mid-pipeline
- Cost spike (10x normal due to retry storms)
- Token limit exceeded mid-conversation

### Safety Failures
- Prompt injection attack succeeds
- PII leaks in output
- Cross-tenant data leak (for multi-tenant systems)

## What This Forces You to Learn
- Failure diagnosis methodology (not guessing — systematic)
- Observability design (logging, tracing, metrics for LLM systems)
- Guardrails implementation (input/output validation)
- Circuit breakers and fallback strategies
- Drift detection (data drift, embedding drift, concept drift)
- Incident response for AI systems
- Graceful degradation patterns

## What You Must Produce
- Per-incident post-mortem: what happened, how you found it, how you fixed it, how you'd prevent it
- Monitoring additions: what alerts would have caught this before a user did
- Architecture changes: what you'd change in the system design to be resilient

## The Real Lesson
You don't truly understand a system until you've broken it. This layer gives you a catalog of failure modes and the debugging instincts for each — the kind of knowledge that normally takes a year of on-call to build.

## Stretch
- Build a chaos engineering harness for LLM systems
- Create automated alerts for each failure mode
- Quantify blast radius: "this failure affects X% of queries and takes Y minutes to detect"
