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
Facts that fit a narrative schema (e.g., the Grizzlies playoff arc: trade → coaching drama → rookie breakout → conference semis) are easier to recall because the schema acts as a retrieval cue. The model can reconstruct from the narrative even if exact attention is weak.

Independent facts (e.g., "Thunder average age 23.1") have no schema support — they're pure episodic recall from context.

Critical distinction: reconstruction (schema-based) is where **confabulation hides**. The model reconstructs a plausible-sounding answer from the schema but gets specific details wrong. This is why probes need to test exact numbers, not just topic recall.

The stress test should measure schema-consistent and independent facts separately to understand which type of recall degrades first.
