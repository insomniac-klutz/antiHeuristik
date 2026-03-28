# Build 02: Multi-Tenant Support Bot

## The Ask
Build an agentic support bot that serves multiple tenants (companies), each with their own knowledge base, tools, and access controls. An agent that can search docs, check order status, escalate to humans — but never leak data across tenants.

## Constraints
- 3+ simulated tenants with distinct knowledge bases
- Agent must use tool calling (not hardcoded flows)
- Strict tenant isolation — Tenant A's agent must never see Tenant B's data
- Must handle: "I don't know" gracefully, tool errors, ambiguous requests
- Conversation memory within a session

## What This Forces You to Learn
- Agent architectures (ReAct loop, planning)
- Tool use / function calling patterns
- Prompt injection attack/defense
- RBAC and data isolation in LLM systems
- Memory architectures (short-term session, long-term knowledge)
- Guardrails (input validation, output filtering)
- Multi-agent vs single-agent tradeoffs
- Human-in-the-loop escalation design

## The Real Lesson
Every real agent system serves multiple customers with different data. Tenant isolation, guardrails, and escalation design are the skills you only develop by building a system that has to enforce boundaries — not just hope for them.

## Stretch
- Add a red-team mode that tries to break tenant isolation
- Implement conversation summarization for long sessions
- Add admin dashboard showing agent performance per tenant
