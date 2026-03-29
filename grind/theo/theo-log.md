# Theo Log

Master integration log. Organized by build, then by date within each build. Append only.

---

## build-08-long-conversation-agent

### 2026-03-28

**context-and-attention.md** → `dl/attention.md` (created)
- Grouped Query Attention (GQA)
- Flash Attention
- KV Cache Mechanics
- PagedAttention
- Lost-in-the-Middle Effect
- Attention Score Degradation at Long Context
- Compound Effect of Optimizations

**quantization-effects.md** → `dl/attention.md` (appended)
- Perplexity
- Q4 Quantization and Attention Precision
- Systematic Flattening
- Effective vs Advertised Context
- Expected Degradation Pattern

**recall-and-behavior.md** → `nlp/evaluation.md` (created)
- Needle in a Haystack (NIAH)
- Sycophancy at Long Context
- Schema-Consistent vs Schema-Inconsistent Retrieval

**evaluation-methods.md** → `nlp/evaluation.md` (appended)
- Scripted Dialogue Evaluation
- Probe Design
- Scoring Categories
- Ground Truth Control
- Run-Until-Failure vs Fixed Turn Count

> notes: merged all 4 source files into 2 target files (dl/attention.md, nlp/evaluation.md) to keep broad sub-topics. Headings reorganized internally into Mechanisms/Scaling/Quantization (dl) and Methods/Behavioral Patterns (nlp). Stripped build-specific reference ("Build 08's approach") from NIAH section. Kept Qwen3.5 reference as concrete technical fact.

### 2026-03-29

**context-and-attention.md** → `dl/attention.md` (appended)
- Static Pre-Allocation vs Dynamic KV Cache Growth

**architecture-eval.md** → `dl/attention.md` (appended)
- The Lineup
  - Qwen 3.5 9B — Q4_K_M (~6.6GB)
  - Gemma 3 4B — Q8_0 (4.98GB)
  - Phi-4 Mini Instruct — Q8_0 (4.08GB)
  - Phi-4 Mini Reasoning — Q8_0 (4.08GB)
- Capacity vs Precision
- Attention Architecture
- Predicted Degradation Patterns
  - Qwen 3.5 9B Q4
  - Gemma 3 4B Q8
  - Phi-4 Mini Instruct Q8
  - Phi-4 Mini Reasoning Q8

**architecture-eval.md** → `nlp/evaluation.md` (appended)
- The Core Question (→ Failure Modes)
- Reasoning vs General Tuning
- Parametric vs Contextual Memory Conflict (merged with recall-and-behavior.md)
- Training Pipeline Diversity
- Confounds to Watch
  - Silent Truncation
  - Context Overflow vs Recall Degradation
  - Domain Specificity
  - YaRN Extension vs Native Context
  - CoT Token Overhead
- Scoring Framework > Conflict Behavior + 4x4 matrix (merged with evaluation-methods.md)

**evaluation-methods.md** → `nlp/evaluation.md` (appended)
- Conflict Behavior Scoring (merged with architecture-eval.md Scoring Framework)
- Instruction Hierarchy and Fact Placement

**recall-and-behavior.md** → `nlp/evaluation.md` (appended)
- Schema-Consistent vs Schema-Inconsistent Retrieval (text update: Grizzlies → Warriors)
- Parametric vs Contextual Memory Conflict (merged with architecture-eval.md)
- Knowledge Conflict as Eval Dimension
- Conversational Grounding

**client-patterns.md** → `b-dev/patterns.md` (created)
- Proxy Abstraction Layer
- Repository Pattern Applied to LLM Calls
- Exponential Backoff
- Event Sourcing for Conversation State
- API Documentation vs API Reality (Impedance Mismatch)
- Observability Over Configuration
- Thinking Model Output Routing

**nlp/evaluation.md** restructured:
- Scoring Categories renamed → Recall Score, promoted to new Scoring Framework H2
- Scoring Framework becomes standalone section with Recall Score + Conflict Behavior axes

> notes: 6 source files → 3 targets (dl/attention.md, nlp/evaluation.md, b-dev/patterns.md). Merged overlapping content: Conflict Behavior from eval-methods + architecture-eval; Parametric Conflict from recall-and-behavior + architecture-eval. Stripped build-specific "Our paths max out" sentence and "DeepSeek dropped from lineup" detail. Renamed Scoring Categories → Recall Score to form two-axis scoring framework. architecture-eval § Run Plan skipped (build-specific execution plan, not theory). architecture-eval § Scoring Framework > Recall Score skipped (duplicates existing Scoring Categories content).
