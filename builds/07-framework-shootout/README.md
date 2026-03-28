# cageMatch

> same agent. three frameworks. one winner.

build the exact same research assistant three times: LangChain/LangGraph, LlamaIndex, and raw Python. benchmark all three. find out which framework earns its abstractions and which one just adds indirection.

## what you're building

- identical functionality: search a doc corpus, summarize findings, handle multi-turn follow-ups
- benchmark on: latency, token cost, code complexity (LOC), debuggability, error handling
- tool use in all three implementations
- a comparison doc with "when to use which" recommendation

## what will break you

- **LangChain**: the abstractions help until they don't, and debugging through 8 layers of callbacks is pain
- **LlamaIndex**: data-framework-first is great until you need custom orchestration
- **raw Python**: freedom is wonderful until you're reimplenting retry logic at 2am
- **vendor lock-in**: switching providers mid-framework reveals tight coupling fast
- **fair comparison**: keeping functionality truly identical across three codebases

## why this matters

most people pick a framework based on a blog post and stick with it forever. building the same thing three ways gives you real opinions backed by real numbers — not vibes.

## stretch

- 4th implementation with CrewAI or AutoGen
- measure team onboarding time for each
- simulate provider migration (OpenAI → Anthropic) in each
