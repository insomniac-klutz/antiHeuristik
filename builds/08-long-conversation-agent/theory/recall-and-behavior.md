# Recall Patterns & Model Behavior

## Needle in a Haystack (NIAH)
Kamradt, 2023. Standard test: bury a single random sentence in filler text, check retrieval at varying depths. Most models fail retrieval when the needle is in the 40-60% depth range of context. Build 08's approach improves on NIAH: (a) multiple needles that relate to each other, (b) haystack is actual conversation not filler, (c) probes test reasoning over facts, not just verbatim retrieval.

## Sycophancy at Long Context
Perez et al., 2022 (Anthropic). Models tend to agree with the user even when the user is wrong. This gets *worse* at longer contexts because:
- Model's confidence in its own earlier statements decays (attention scores to its own past outputs weaken)
- Recent user pressure stays strong (recency bias in attention)
- The model "forgets" that it's right and defaults to agreeing with the closest strong signal

The HIGH path's gaslighting probes ("actually you said X" when the model said Y) directly test this. The turn at which the model stops pushing back is a direct measure of effective context for self-consistency.

## Schema-Consistent vs Schema-Inconsistent Retrieval
Facts that fit a narrative schema (e.g., the Warriors resurgence arc: trade → coaching change → rookie breakout → playoff push) are easier to recall because the schema acts as a retrieval cue. The model can reconstruct from the narrative even if exact attention is weak.

Independent facts (e.g., "Thunder average age 23.1") have no schema support — they're pure episodic recall from context.

Critical distinction: reconstruction (schema-based) is where **confabulation hides**. The model reconstructs a plausible-sounding answer from the schema but gets specific details wrong. This is why probes need to test exact numbers, not just topic recall.

The stress test should measure schema-consistent and independent facts separately to understand which type of recall degrades first.

## Parametric vs Contextual Memory Conflict
Longpre et al., 2021. LLMs have two knowledge sources — parametric (baked into weights during training) and contextual (provided in the prompt). When they conflict, models show a *popularity bias*: they defer to parametric memory for well-known facts and to context for obscure ones.

By anchoring fabricated facts to the 2021-22 NBA season — a period the model *definitely* has training data for — every fact becomes a direct collision with parametric memory. The model's behavior under conflict (cave to training data, hedge, or faithfully use context) is a direct measurement of contextual grounding strength. This is exactly what RAG systems struggle with in production: user-provided context that contradicts what the model "knows."

Contrast with future-dated facts (e.g., 2025-26 season): the model has no competing knowledge, so it *must* use context. That tests recall but not the harder problem — can the model prioritize context over its own priors?

## Knowledge Conflict as Eval Dimension
Most NIAH benchmarks use neutral filler text that doesn't conflict with training data. That tests attention/retrieval in isolation. Planting *contradictory* facts (OKC oldest when training says youngest, 3PA declining when training says rising) tests a compound capability: retrieval + override.

This is harder and more production-relevant. Facts should be categorized by expected parametric conflict strength:
- **High conflict**: salary cap number, OKC roster age, 3PA trend, Celtics road record — these contradict well-known real data
- **Low conflict**: fictional player names (Marcus Kemp, Terrence Okafor, Viktor Dragas), fictional venues (Balboa Park Arena, Arena CDMX) — no real data to compete with

When a high-conflict fact fails a probe, it could mean either (a) context recall failed or (b) parametric memory overrode context. Distinguishing the two: if the model's wrong answer matches real-world data, that's override. If it's a novel wrong answer, that's recall failure. Track both separately.

## Conversational Grounding
Clark & Brennan, 1991. In human dialogue, facts become "common ground" through acknowledgment — one party states, the other confirms or builds on it. If the model acknowledges a fact in its response ("yeah the Kemp trade really shook things up"), that's stronger grounding than if the fact just sits in a user turn unacknowledged.

This matters for path design: facts the model explicitly engages with in its responses may be recalled better later — the model's own output acts as a second encoding of the fact in context. Facts that appear only in user turns and get a generic response have weaker grounding. The eval should track whether model acknowledgment correlates with later recall success — grounded facts vs ungrounded facts.
