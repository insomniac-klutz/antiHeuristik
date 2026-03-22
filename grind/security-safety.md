# Security & Safety

Not in the original plan. Critical for production AI at Series B-D companies.

## Prompt Injection
- [ ] Direct injection — user input becomes part of prompt
- [ ] Indirect injection — retrieved content contains adversarial instructions
- [ ] Defense patterns — input sanitization, output validation, instruction hierarchy
- [ ] Sandwich defense, system prompt hardening

## Data Privacy
- [ ] PII detection and redaction in LLM inputs/outputs
- [ ] Tenant isolation in multi-tenant AI systems
- [ ] Data residency — which data goes to which provider
- [ ] Logging sanitization — don't log PII in traces

## Content Safety
- [ ] Content moderation pipelines — pre-filter, post-filter, classifier-based
- [ ] RBAC for LLM features — who can access what capabilities
- [ ] Output safety — preventing harmful/biased/toxic generation
- [ ] Compliance considerations — GDPR, SOC2 implications for AI systems
