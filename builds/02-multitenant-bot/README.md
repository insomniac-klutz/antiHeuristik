# noLeaks

> three tenants. one agent. zero data bleed.

agentic support bot serving multiple companies, each with their own knowledge base, tools, and access controls. tenant A's agent never touches tenant B's data. one prompt injection and you've failed.

## what you're building

- 3+ simulated tenants with distinct knowledge bases
- agent uses tool calling (not hardcoded if/else flows)
- strict tenant isolation — enforced, not hoped-for
- graceful handling of "I don't know", tool errors, ambiguous requests
- conversation memory within a session

## what will break you

- **prompt injection**: a user will try to trick the agent into accessing another tenant's data
- **tool use design**: which tools to expose, how to scope them per-tenant
- **RBAC in LLM land**: traditional auth patterns don't map cleanly to agent architectures
- **guardrails**: input validation and output filtering without killing usability
- **escalation**: when should the agent hand off to a human?

## why this matters

real agent systems serve multiple customers with different data. you don't learn isolation, guardrails, and escalation from tutorials — you learn them when a prompt injection leaks tenant data.

## stretch

- red-team mode: actively try to break tenant isolation
- conversation summarization for handoff
- per-tenant performance dashboard
