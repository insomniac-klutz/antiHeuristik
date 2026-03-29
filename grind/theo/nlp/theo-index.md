# nlp — Theo Index

## Files
- evaluation.md — LLM evaluation: failure modes, scoring frameworks, behavioral patterns, and experimental confounds

## evaluation.md
- Failure Modes — taxonomy of root causes when LLMs fail to recall facts from long context
- Methods & Frameworks — tools and protocols for testing LLM context handling
  - Needle in a Haystack (NIAH) — standard buried-fact retrieval benchmark and its limitations
  - Scripted Dialogue Evaluation — deterministic conversation scripts for reproducible testing
  - Probe Design — injected recall questions at fixed intervals with four probe types
  - Ground Truth Control — mixing real and fabricated facts to detect training data leakage
  - Instruction Hierarchy and Fact Placement — trust priority stack and why user-turn placement matches production conditions
  - Reasoning vs General Tuning — three hypotheses on how CoT fine-tuning affects conversational recall
  - Training Pipeline Diversity — training data composition as an independent variable across model providers
  - Run-Until-Failure vs Fixed Turn Count — finding natural breaking points instead of arbitrary cutoffs
- Scoring Framework — two-axis scoring system for probe responses
  - Recall Score — pass/hedge/fail/confabulate taxonomy for factual accuracy
  - Conflict Behavior — deferred/overrode/flagged/caved taxonomy for parametric-contextual conflict handling
- Behavioral Patterns — observed LLM failure modes in extended conversations
  - Sycophancy at Long Context — models increasingly agree with users as context grows
  - Schema-Consistent vs Schema-Inconsistent Retrieval — narrative-supported vs isolated fact recall and where confabulation hides
  - Parametric vs Contextual Memory Conflict — how models handle training data contradicting provided context
  - Knowledge Conflict as Eval Dimension — using contradictory facts to test retrieval + override as a compound capability
  - Conversational Grounding — Clark & Brennan's common ground theory applied to model acknowledgment and recall
- Experimental Confounds — threats to validity in long-context evaluation
  - Silent Truncation — inference engines silently drop early context, mimicking recall failure
  - Context Overflow vs Recall Degradation — distinguishing physical truncation from attention failure
  - Domain Specificity — reasoning-tuned models may underperform from domain mismatch, not recall deficiency
  - YaRN Extension vs Native Context — positional embedding artifacts from context extension beyond training length
  - CoT Token Overhead — reasoning chains consume context budget, confounding turn-based recall comparisons
