# elephantBrain

> turn 80. still coherent. prove it.

conversational agent that maintains context across 50-100+ turn conversations. remembers what was discussed 40 turns ago, refers back, never contradicts itself. test three memory strategies and find out why "just use a bigger context window" is wrong.

## what you're building

- three memory strategies: long-context stuffing, sliding window + summarization, retrieval-augmented memory
- test with conversations spanning 50-100+ turns
- measure quality degradation as length increases for each strategy
- latency must stay acceptable at turn 80+
- handle topic switches, callbacks to earlier topics, contradictory user statements

## what will break you

- **lost-in-the-middle**: key info buried at turn 25 will get ignored — you'll prove it empirically
- **summarization chains**: compress history without losing critical facts — harder than it sounds
- **KV cache costs**: long contexts cost what they cost and you need to know why
- **conflict behavior**: when the user contradicts earlier statements, does the agent cave, flag, or override?
- **context budgeting**: token arithmetic becomes a first-class engineering concern

## why this matters

every production chatbot hits context limits eventually. "just use a bigger window" is the answer people give when they haven't built one. three memory strategies benchmarked against each other is how you actually learn what works.

## stretch

- persistent memory across sessions ("remember me next time")
- memory importance scoring (what to keep vs forget)
- adversarial testing to confuse agent about earlier statements
