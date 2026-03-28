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
