# Evaluation

## Methods & Frameworks

### Needle in a Haystack (NIAH)
Kamradt, 2023. Standard test: bury a single random sentence in filler text, check retrieval at varying depths. Most models fail retrieval when the needle is in the 40-60% depth range of context. Probe design for long-context evaluation improves on NIAH: (a) multiple needles that relate to each other, (b) haystack is actual conversation not filler, (c) probes test reasoning over facts, not just verbatim retrieval.

### Scripted Dialogue Evaluation
Deriu et al., 2021. Deterministic test scripts are "conversation unit tests." The key advantage over live testing: you can re-run the exact same conversation after changing strategies (stuffing → sliding window → RAG) and get apples-to-apples comparison. Without deterministic scripts, you're benchmarking conversation content, not context strategy.

### Probe Design
Probes are injected at fixed intervals (every ~10 turns) testing recall of specific facts. Probe types:
- **Direct recall**: "How many games was Kemp's streak?" — tests verbatim retrieval
- **Cross-topic recall**: after switching topics, circle back — tests whether topic context helps or hurts retrieval
- **Contradiction resistance**: user states incorrect "correction" — tests whether model holds ground or caves (sycophancy)
- **Comprehensive recall**: "list all the facts we discussed" — tests breadth of memory

### Scoring Categories
- **Pass**: correct recall of key details
- **Hedge**: partially right or explicitly uncertain ("I believe...")
- **Fail**: wrong answer or omission
- **Confabulate**: confidently wrong — model generates plausible but incorrect details

Hedging is actually a better failure mode than confabulation — a model that knows it doesn't know is more useful than one that makes things up.

### Ground Truth Control
Using one real fact mixed with fabricated ones. If the model recalls real facts more reliably, training data leakage is inflating results. This distinguishes context recall from parametric knowledge.

### Run-Until-Failure vs Fixed Turn Count
Run each path until the model fails 3 consecutive probes rather than a fixed turn count. This gives the natural breaking point per path instead of an arbitrary cutoff. More informative for establishing the degradation curve.

## Behavioral Patterns

### Sycophancy at Long Context
Perez et al., 2022 (Anthropic). Models tend to agree with the user even when the user is wrong. This gets *worse* at longer contexts because:
- Model's confidence in its own earlier statements decays (attention scores to its own past outputs weaken)
- Recent user pressure stays strong (recency bias in attention)
- The model "forgets" that it's right and defaults to agreeing with the closest strong signal

Gaslighting probes ("actually you said X" when the model said Y) directly test this. The turn at which the model stops pushing back is a direct measure of effective context for self-consistency.

### Schema-Consistent vs Schema-Inconsistent Retrieval
Facts that fit a narrative schema (e.g., a playoff arc: trade → coaching drama → rookie breakout → conference semis) are easier to recall because the schema acts as a retrieval cue. The model can reconstruct from the narrative even if exact attention is weak.

Independent facts (e.g., "Thunder average age 23.1") have no schema support — they're pure episodic recall from context.

Critical distinction: reconstruction (schema-based) is where **confabulation hides**. The model reconstructs a plausible-sounding answer from the schema but gets specific details wrong. This is why probes need to test exact numbers, not just topic recall.

The stress test should measure schema-consistent and independent facts separately to understand which type of recall degrades first.
