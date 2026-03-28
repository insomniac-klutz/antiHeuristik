# Build 08: Long-Conversation Agent

## The Ask
Build a conversational agent that maintains coherent context across 50+ turn conversations. The agent should remember what was discussed 40 turns ago, refer back to earlier topics, and never contradict itself. Test three strategies: long-context stuffing, sliding window + summarization, and retrieval-augmented memory.

## Constraints
- Test with conversations that naturally span 50-100+ turns
- Must maintain factual consistency across the full conversation
- Measure quality degradation as conversation length increases for each strategy
- Latency must stay acceptable even at turn 80+
- Must handle: topic switches, callbacks to earlier topics, contradictory user statements

## What This Forces You to Learn
- Context window management — packing, arithmetic, budgeting
- Summarization chains — compress history without losing critical facts
- Sliding window patterns — rolling context with a summary prefix
- Map-reduce over conversation history — parallel summarization then synthesis
- Why long-context models behave differently from short-context ones
- Lost-in-the-middle effect — you'll hit it directly when key info is buried at turn 25
- KV cache mechanics — why long contexts cost what they cost
- Constitutional AI patterns — use self-critique to keep the agent consistent and safe over long sessions
- Retrieval beats stuffing — empirical proof from your own benchmarks

## The Real Lesson
Every production chatbot hits context limits. "Just use a bigger window" is the answer people give when they haven't built one. Three memory strategies benchmarked against each other is how you learn what actually works — and what breaks at scale.

## Stretch
- Add persistent memory across sessions ("remember me next time")
- Implement a memory importance scoring system (what to keep vs what to forget)
- Test with adversarial users who deliberately try to confuse the agent about earlier statements
