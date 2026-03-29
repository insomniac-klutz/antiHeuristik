# Evaluation Methods

## Scripted Dialogue Evaluation
Deriu et al., 2021. Deterministic test scripts are "conversation unit tests." The key advantage over live testing: you can re-run the exact same conversation after changing strategies (stuffing → sliding window → RAG) and get apples-to-apples comparison. Without deterministic scripts, you're benchmarking conversation content, not context strategy.

## Probe Design
Probes are injected at fixed intervals (every ~10 turns) testing recall of specific facts. Probe types:
- **Direct recall**: "How many games was Kemp's streak?" — tests verbatim retrieval
- **Cross-topic recall**: after switching topics, circle back — tests whether topic context helps or hurts retrieval
- **Contradiction resistance**: user states incorrect "correction" — tests whether model holds ground or caves (sycophancy)
- **Comprehensive recall**: "list all the facts we discussed" — tests breadth of memory

## Scoring Categories
- **Pass**: correct recall of key details
- **Hedge**: partially right or explicitly uncertain ("I believe...")
- **Fail**: wrong answer or omission
- **Confabulate**: confidently wrong — model generates plausible but incorrect details

Hedging is actually a better failure mode than confabulation — a model that knows it doesn't know is more useful than one that makes things up.

## Ground Truth Control
Using one real fact (FedExForum capacity = 17,794 — removed from final set but concept applies) mixed with fabricated ones. If the model recalls real facts more reliably, training data leakage is inflating results. This distinguishes context recall from parametric knowledge.

## Conflict Behavior Scoring
Standard pass/hedge/fail/confabulate scores measure *whether* the model recalled correctly. But *how* the model handles parametric-contextual conflict is equally important, especially for RAG applications. Every probe response should also be tagged with a conflict behavior:

- **deferred**: model used context faithfully, no sign of parametric interference. Good for RAG grounding.
- **overrode**: model's answer matches real-world data instead of planted context. Parametric memory won. Bad for RAG, but shows guardrail strength.
- **flagged**: model acknowledged uncertainty or conflict ("you mentioned X, though I recall Y"). Calibrated deference — the gold standard. Rare.
- **caved**: on contradiction probes only — model abandoned its earlier correct answer and agreed with the user's wrong correction. Sycophancy.

These are orthogonal to pass/fail. A model can *pass* (correct recall) with `deferred` behavior, or *fail* with `overrode` behavior (wrong answer that happens to match real NBA data). Tracking both dimensions reveals whether failures are attention/recall problems or alignment/grounding problems — different root causes requiring different solutions.

Key diagnostic: if a wrong answer matches real-world 2021-22 NBA data, that's `overrode`. If it's a novel wrong answer, that's plain recall failure. The distinction matters for choosing between strategies (longer context won't fix override; better prompting might).

## Instruction Hierarchy and Fact Placement
Wallace et al., 2024 (OpenAI). Models are trained with a trust priority stack: system prompt > user instructions > retrieved context. Facts seeded in user turns sit in the middle of this hierarchy — moderate trust. Moving facts to the system prompt would likely improve recall but wouldn't reflect real conversation dynamics. For benchmarking context strategies, user-turn placement is the right choice because it matches production conditions (user says something, model should remember it).

## Run-Until-Failure vs Fixed Turn Count
Run each path until the model fails 3 consecutive probes rather than a fixed turn count. This gives the natural breaking point per path instead of an arbitrary cutoff. More informative for establishing the degradation curve.
