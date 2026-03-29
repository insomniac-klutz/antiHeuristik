# nlp — Theo Log

## 2026-03-28 — build-08-long-conversation-agent

- recall-and-behavior.md → evaluation.md (created)
  - Needle in a Haystack (NIAH)
  - Sycophancy at Long Context
  - Schema-Consistent vs Schema-Inconsistent Retrieval
- evaluation-methods.md → evaluation.md (appended)
  - Scripted Dialogue Evaluation
  - Probe Design
  - Scoring Categories
  - Ground Truth Control
  - Run-Until-Failure vs Fixed Turn Count

## 2026-03-29 — build-08-long-conversation-agent

- architecture-eval.md → evaluation.md (appended)
  - The Core Question (→ Failure Modes)
  - Reasoning vs General Tuning
  - Parametric vs Contextual Memory Conflict (merged with recall-and-behavior.md)
  - Training Pipeline Diversity
  - Conflict Behavior + 4x4 matrix (merged with evaluation-methods.md)
  - Silent Truncation
  - Context Overflow vs Recall Degradation
  - Domain Specificity
  - YaRN Extension vs Native Context
  - CoT Token Overhead
- evaluation-methods.md → evaluation.md (appended)
  - Conflict Behavior Scoring (merged with architecture-eval.md)
  - Instruction Hierarchy and Fact Placement
- recall-and-behavior.md → evaluation.md (appended)
  - Schema-Consistent vs Schema-Inconsistent Retrieval (text update)
  - Parametric vs Contextual Memory Conflict (merged with architecture-eval.md)
  - Knowledge Conflict as Eval Dimension
  - Conversational Grounding
- evaluation.md restructured:
  - Scoring Categories renamed → Recall Score
  - New Scoring Framework H2 with Recall Score + Conflict Behavior axes
