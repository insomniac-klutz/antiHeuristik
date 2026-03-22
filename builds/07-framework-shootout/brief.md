# Build 07: Framework Shootout — Same Agent, Three Ways

## The Ask
Build the same system three times: a research assistant that searches a doc corpus, summarizes findings, and handles multi-turn follow-ups. Build it with LangChain/LangGraph, with LlamaIndex, and with raw Python (no framework). Benchmark all three.

## Constraints
- Identical functionality across all three implementations
- Benchmark on: latency, token cost, code complexity (LOC), debuggability, error handling clarity
- Must handle at least: search, summarization, follow-up questions, tool use
- Write a comparison doc at the end with a clear "when to use which" recommendation

## What This Forces You to Learn
- LangChain — abstractions, chains, callback system, when it helps vs when it's overhead
- LangGraph — stateful workflows, nodes/edges, when state machines matter
- LlamaIndex — index types, query engines, data connectors, when data-framework-first wins
- CrewAI / AutoGen patterns — review while building, even if not implemented
- Rolling your own — minimal orchestration, when frameworks hurt more than help
- The interview answer: "why did you / didn't you use LangChain?"
- Vendor lock-in and abstraction layers — how framework choice constrains provider switching
- Type hints and typed interfaces — framework comparison requires clean typed abstractions

## Interview Translation
"What orchestration framework do you use and why?" — every team has an opinion. Having built with all three and being able to articulate tradeoffs from experience is the power answer.

## Stretch
- Add a CrewAI or AutoGen multi-agent variant as a 4th implementation
- Measure: "how long does it take a new team member to understand each implementation?"
- Simulate a provider migration (switch from OpenAI to Anthropic) in each — which framework makes it easiest?
