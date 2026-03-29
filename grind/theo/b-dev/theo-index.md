# b-dev — Theo Index

## Files
- patterns.md — software engineering patterns: abstraction, retry, event sourcing, API integration, and observability

## patterns.md
- Proxy Abstraction Layer — wrapping provider-specific interfaces behind unified APIs, portability vs optimization tradeoff
- Repository Pattern Applied to LLM Calls — abstracting model communication behind a single interface
- Exponential Backoff — retry with increasing delays to avoid thundering herd on local inference
- Event Sourcing for Conversation State — append-only turn logs as the canonical state, enabling replay and re-scoring
- API Documentation vs API Reality (Impedance Mismatch) — defensive patterns for inconsistent API naming and response shapes
- Observability Over Configuration — detecting runtime state instead of hardcoding it, twelve-factor methodology
- Thinking Model Output Routing — handling polymorphic API responses from reasoning vs instruction-tuned models
