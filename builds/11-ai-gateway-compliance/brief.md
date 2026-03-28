# Build 11: Multi-Provider AI Gateway with Compliance Layer

## The Ask
Build an API gateway that sits in front of multiple LLM providers (OpenAI, Anthropic, a local model). It routes requests based on data classification — PII goes to self-hosted only, non-sensitive goes to cheapest provider. Enforce data residency rules, log everything with PII redaction, and expose webhooks for async completion.

## Constraints
- 3+ providers (at least one self-hosted, even if it's a small model)
- Data classifier: automatically detect PII/sensitive content and route accordingly
- Request routing: cost-optimal by default, compliance-override when sensitive
- All logs must be PII-redacted before storage
- Webhook endpoint for async job completion notifications
- Must track per-provider cost, latency, and availability
- Bias audit: run a fairness check on outputs across demographic groups

## What This Forces You to Learn
- Multi-provider abstraction layers — unified interface across OpenAI/Anthropic/self-hosted
- Data residency — which data is allowed to leave your infrastructure
- Compliance considerations — GDPR (right to deletion, data minimization), SOC2 implications
- PII detection and redaction in both inputs and logs
- Webhook design — receiving and sending async callbacks
- Self-hosted vs managed cost crossover — when self-hosting a model becomes cheaper
- Managed vs self-hosted vector DB comparison — if you add embedding routing
- Bias amplification testing — systematic fairness evaluation
- Logging sanitization — the gap between "log everything for debugging" and "don't store PII"
- Provider failover and health checking

## The Real Lesson
Production AI systems don't live in a vacuum — they have users, regulations, and data that can't leave certain boundaries. This is the infrastructure layer most people ignore until legal comes knocking. Building it teaches you to think about compliance as architecture, not afterthought.

## Stretch
- Add request-level cost budgets ("this user's requests cannot exceed $X/day")
- Implement circuit breakers per provider with automatic failover
- Add a provider comparison dashboard (cost, quality, latency side-by-side)
- GDPR data deletion: when a user requests deletion, purge their data from all logs and caches
