# routeOrDie

> classify, route, redact, log — or explain to legal why you didn't.

API gateway sitting in front of multiple LLM providers. PII goes to self-hosted only, non-sensitive goes to cheapest provider. enforce data residency, redact logs, expose webhooks. compliance isn't a feature you bolt on — it's the architecture.

## what you're building

- 3+ providers (at least one self-hosted, even a small model)
- data classifier: auto-detect PII/sensitive content and route accordingly
- request routing: cost-optimal by default, compliance-override when sensitive
- all logs PII-redacted before storage
- webhook endpoint for async job completion
- per-provider cost, latency, and availability tracking

## what will break you

- **PII detection**: false negatives mean compliance violations. false positives mean everything routes to expensive self-hosted
- **data residency**: which data is allowed to leave your infrastructure — and proving it doesn't
- **the logging paradox**: "log everything for debugging" vs "don't store PII" — pick both
- **provider failover**: health checking and circuit breakers across 3+ providers
- **bias auditing**: systematic fairness evaluation across providers and demographic groups

## why this matters

production AI systems don't live in a vacuum — they have users, regulations, and data that can't leave certain boundaries. this is the infrastructure layer most people ignore until legal comes knocking.

## stretch

- per-user request cost budgets ("this user can't exceed $X/day")
- circuit breakers with automatic failover
- GDPR data deletion on user request
