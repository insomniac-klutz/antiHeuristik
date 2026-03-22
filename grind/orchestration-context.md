# Orchestration & Context Management

Gaps identified in audit — no build directly covered these.

## Orchestration Frameworks
- [ ] LangChain — what it does, when it helps, when it's overhead
- [ ] LangGraph — stateful agent workflows, when to use vs raw code
- [ ] LlamaIndex — data framework, index types, when it beats LangChain
- [ ] CrewAI / AutoGen — multi-agent frameworks, tradeoffs
- [ ] Roll your own — when frameworks hurt, minimal orchestration patterns
- [ ] "Why did you / didn't you use LangChain?" — the interview answer

## Context Window Management
- [ ] Context packing — fitting maximum useful info in limited tokens
- [ ] Summarization chains — compress history to stay in window
- [ ] Sliding window patterns — rolling context for long conversations
- [ ] Map-reduce over documents — parallel processing then synthesis
- [ ] Context window arithmetic — system prompt + examples + user input + output budget
