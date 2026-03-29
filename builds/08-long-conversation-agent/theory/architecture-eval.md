# Architecture & Evaluation Design

A comprehensive record of the architectural reasoning, experimental design, and theoretical foundations behind the Build 08 model evaluation. This doc captures why we chose these models, what each isolates, and how to interpret the results.

---

## The Core Question

When an LLM fails to recall a fact from earlier in a long conversation, what caused the failure? Possible root causes:

1. **Attention dilution** — softmax spread scores across too many tokens, signal drowned in noise
2. **Quantization noise** — reduced weight precision corrupted attention score rankings
3. **Architectural bottleneck** — model's attention pattern physically can't reach the target tokens
4. **Parametric override** — model's training data contradicted context, and training won
5. **Context truncation** — the information was silently dropped from the context window
6. **Capacity limitation** — model has too few parameters to maintain distinct representations of many facts

A single model can't distinguish these. You need a controlled lineup where each model changes one variable.

---

## The Lineup

### Qwen 3.5 9B — Q4_K_M (~6.6GB)
**Role**: High-capacity, low-precision baseline.

- 9B params, GQA (grouped query attention), 128K native context
- Full attention at every layer — every token attends to every other token
- Q4_K_M quantization reduces weights to ~1-1.5 digits of effective precision
- Most parameters in the lineup = most representational capacity for routing attention
- Q4 = lowest precision = most vulnerable to attention score flattening at long context

**Prediction**: Should hold recall longest due to raw capacity, but Q4 noise will compound turn-over-turn in the KV cache. Expect gradual degradation starting around turn 30-40, with the lost-in-the-middle zone (facts at 40-60% depth) failing first.

### Gemma 3 4B — Q8_0 (4.98GB)
**Role**: Sliding window architecture + high precision.

- 4B params, sliding window (1024) interleaved with global attention at 5:1 ratio, 128K native
- Only 1/6 of layers do global attention — the other 5/6 only see the nearest 1024 tokens
- Q8_0 = ~3x the effective precision of Q4
- RoPE base frequency 1M (vs 10K in Gemma 2)
- KV cache overhead <15% vs ~60% for global-only architectures

**Prediction**: Recent facts should be recalled extremely well (all 6 layers see them). Distant facts degrade faster than Qwen because only global layers (1/6) carry that information. The degradation curve should have a different *shape* — steeper drop-off for distant facts, flatter for recent. If we observe this, it's direct evidence that attention architecture shapes the recall curve, not just context length.

### Phi-4 Mini Instruct — Q8_0 (4.08GB)
**Role**: Microsoft architecture baseline, control for reasoning ablation.

- 3.8B params, full attention at every layer, 128K native context
- Phi-4 architecture — distinct from both Qwen's GQA and Gemma's sliding window
- Trained on synthetic, high-quality data (Microsoft's approach)
- General-purpose instruction tuning
- Smallest model in the lineup

**Prediction**: Full attention gives it the best theoretical reach to distant facts per-layer, but 3.8B params means less capacity to maintain distinct fact representations. Q8 precision helps. Expect a capacity-limited failure pattern — may start confusing facts with each other (merging details) rather than losing them entirely.

### Phi-4 Mini Reasoning — Q8_0 (4.08GB)
**Role**: Reasoning-tuned ablation of Phi-4 Mini Instruct.

- Identical architecture, identical quant, identical size
- Only difference: fine-tuned on synthetic reasoning-dense data with chain-of-thought
- CoT reasoning generates extra tokens per response that consume context budget

**Prediction**: Two competing effects:
1. **CoT helps recall** — reasoning forces the model to explicitly re-derive facts from context rather than pattern-matching from memory. This could improve grounding and reduce parametric override.
2. **CoT hurts context budget** — extra reasoning tokens (200-500 per response) consume ~10-25K tokens across 50 turns. Despite 128K window, effective available context shrinks.
3. **Domain mismatch** — math-reasoning training may have narrowed attention patterns for structured problems, weakening free-form conversational recall.

The delta between Phi-4 reasoning and Phi-4 instruct isolates the effect of reasoning-specific training on conversational context grounding.

---

## Experimental Dimensions

### 1. Capacity vs Precision

The central trade-off for local inference: more parameters at lower precision, or fewer parameters at higher precision, within the same VRAM budget?

| | Qwen 3.5 9B Q4 | Gemma 3 4B Q8 | Phi-4 3.8B Q8 |
|---|---|---|---|
| Params | 9B | 4B | 3.8B |
| Precision | ~1-1.5 digits | ~3 digits | ~3 digits |
| VRAM | 6.6GB | 4.98GB | 4.08GB |

This is the local-inference version of the bias-variance trade-off:
- **More params** = more capacity to route attention precisely (lower bias), but Q4 adds noise to every weight (higher variance)
- **Fewer params** = less routing capacity (higher bias), but Q8 keeps routes cleaner (lower variance)

At short context, capacity dominates — not enough tokens for quantization noise to accumulate. At long context, noise compounds turn-over-turn in the KV cache, and precision might overtake capacity. The crossover point — if it exists — is what this eval measures.

**How to interpret**:
- If Qwen 9B Q4 degrades faster than Gemma 4B Q8 on distant probes → **precision > capacity** for long-context recall
- If Qwen holds better → **capacity > precision**, scaling beats quantization quality
- If they degrade at the same rate but on different fact types → the dimensions are orthogonal

### 2. Attention Architecture

Three different attention patterns, three different predictions:

**Qwen — GQA (full global)**
Every layer, every token attends to every other token. Shared K/V heads reduce memory but every layer has global reach. Degradation should be gradual and uniform across fact positions — the softmax dilution curve.

**Gemma — Sliding Window 5:1**
5 local layers (1024 token window) per 1 global layer. Creates a **recency bias at the architecture level**:
- Recent facts: visible to all 6 layers (local + global)
- Distant facts: visible to only 1/6 layers (global only)

Prediction: steeper recall drop-off for distant facts, flatter for recent. The curve shape should be visibly different from Qwen's.

**Phi-4 — Full Attention**
Full attention at every layer, like Qwen's GQA but without the shared K/V heads. At 3.8B params, each layer is smaller than Qwen's — less capacity per attention operation but no architectural bottleneck to distant tokens.

If all three architectures produce the same degradation curve → attention architecture doesn't matter, it's just about total capacity and precision. If they diverge → architecture is a load-bearing variable. That's the finding.

### 3. Reasoning vs General Tuning (Phi-4 Ablation)

The cleanest comparison in the lineup. Same architecture, same quant, same size — only the fine-tuning differs.

**Hypothesis A — reasoning training helps conversational recall:**
CoT forces the model to explicitly engage with context rather than relying on pattern matching. When the model "thinks through" a probe, it performs active retrieval over context. This is analogous to how human study works — actively recalling beats passive recognition.

**Hypothesis B — reasoning training hurts conversational recall:**
Math-reasoning training narrows attention patterns to favor structured, sequential reasoning. Conversational recall requires broad, associative attention over unstructured dialogue. The model's attention "muscles" are trained for the wrong task.

**Hypothesis C — reasoning training is neutral for recall, but CoT consumes context:**
The training doesn't change recall quality, but the extra tokens generated by reasoning chains eat into the 128K budget, causing earlier context pressure. This would show as identical recall-per-remaining-context but worse recall-per-turn-number.

**How to detect which hypothesis holds:**
- Normalize recall scores by remaining context tokens (not turn number)
- If Phi-4-reasoning scores the same as Phi-4-instruct when normalized → Hypothesis C
- If reasoning scores better even after normalization → Hypothesis A
- If reasoning scores worse even after normalization → Hypothesis B

### 4. Parametric vs Contextual Memory Conflict

All fabricated facts are anchored to the 2021-22 NBA season — a period every model has training data for. Each fact directly contradicts real-world data (e.g., OKC was actually the youngest team, not oldest; 3PA rate was rising, not falling).

This turns the eval from a passive recall test into a **parametric conflict test**:

**High-conflict facts** (contradict well-known real data):
- Salary cap ($163.5M vs real ~$112M)
- OKC roster age (27.6 oldest vs reality: one of youngest)
- Three-point rate (31.7% declining vs reality: ~37% rising)
- Celtics road record (11-game losing streak vs reality: strong road record)

**Low-conflict facts** (fictional entities, no real data to compete):
- Marcus Kemp, Terrence Okafor, Viktor Dragas (fictional players)
- Devin Harlow (fictional coach)
- Balboa Park Arena, Arena CDMX (fictional venues)

**How to interpret probe failures:**
- Model's wrong answer matches real 2021-22 NBA data → **parametric override** (training won over context)
- Model's wrong answer is novel (doesn't match real or planted data) → **recall failure** (attention/capacity issue)
- Model recalls correctly AND flags uncertainty → **calibrated deference** (ideal RAG behavior)
- Model caves to user contradiction of planted facts → **sycophancy** (grounding failure)

Each model's RLHF training will handle this tension differently. Qwen is known to be agreeable (predicts high deference, low override). Phi-4's Microsoft RLHF is less characterized. Gemma's Google training may be more cautious. The four-way comparison reveals how training pipeline shapes the grounding-vs-guardrails balance.

### 5. Training Pipeline Diversity

Three companies, three philosophies:

| Pipeline | Models | Approach |
|---|---|---|
| Alibaba (Qwen) | Qwen 3.5 9B | Massive multilingual data, aggressive instruction tuning, known agreeability |
| Google (Gemma) | Gemma 3 4B | Distilled from Gemini research, multimodal training, conservative outputs |
| Microsoft (Phi) | Phi-4 Instruct + Reasoning | Synthetic data focus, quality over quantity, reasoning emphasis |

If models from different pipelines fail on different facts or in different ways, the training data composition is a variable — not just architecture and precision.

---

## Confounds to Watch

### Silent Truncation
When context exceeds the window, most inference engines silently truncate from the beginning — exactly where early-seeded facts live. The model doesn't error, it just loses turns 1-N without indication. This makes truncation-caused failures look like recall failures.

**Mitigation**: All four models have 128K native context. At ~300-400 tokens per turn pair, even HIGH path (48 turns) should stay under 20K tokens for conversation content. Phi-4-reasoning's CoT chains are the risk — monitor token count per turn.

### Context Overflow vs Recall Degradation
These are fundamentally different failure modes:
- **Recall degradation**: information is present in context but attention can't find it
- **Context overflow**: information is physically truncated from context

Mixing them in the same analysis contaminates the benchmark. This is why we dropped DeepSeek-R1-0528-Qwen3-8B (33K context) from the main lineup — it would overflow on HIGH path, making it impossible to distinguish recall failure from truncation.

### Domain Specificity (Phi-4 Reasoning)
Math-reasoning training may cause domain mismatch on NBA conversational recall. If Phi-4-reasoning underperforms Phi-4-instruct, it could be domain mismatch rather than a fundamental property of reasoning training.

**Mitigation**: Compare the two Phi-4 variants directly. If reasoning scores worse, check *how* it fails — domain mismatch shows as generic/vague responses ("I'm not sure about sports details"), while attention/recall failure shows as confident wrong answers or fact merging.

### YaRN Extension vs Native Context
Models with YaRN-extended context (e.g., Qwen3 8B: 40K native → 128K extended) introduce positional embedding artifacts at extended ranges. Quality degrades at positions beyond the native training length.

**Mitigation**: All four models in the final lineup use native 128K context. No YaRN extensions.

### CoT Token Overhead
Reasoning models generate chain-of-thought tokens that consume context budget but aren't "conversation content." A reasoning model at turn 40 may have consumed 30K tokens of context, while a non-reasoning model at turn 40 consumed only 15K.

**Mitigation**: Track cumulative token count per turn. Normalize recall scores by remaining context (tokens), not by turn number, for the reasoning vs instruct comparison.

---

## Predicted Degradation Patterns

Based on architecture and quantization theory:

### Qwen 3.5 9B Q4
```
Turn  1-20:  near-perfect recall, Q4 noise negligible
Turn 20-40:  subtle hedging on independent facts, schema facts hold
Turn 40-60:  lost-in-the-middle failures on early-seeded facts
Turn 60+:    confabulation appears, fact merging, coherence decay
```
Shape: gradual linear degradation, worst in the 40-60% depth zone.

### Gemma 3 4B Q8
```
Turn  1-20:  strong recall, Q8 precision keeps scores sharp
Turn 20-40:  distant facts start failing (only 1/6 layers see them)
Turn 30-50:  recent facts still strong, distant facts weak — bifurcated curve
Turn 50+:    capacity limits may cause fact merging across both distances
```
Shape: bifurcated — steep for distant, flat for recent. Different curve shape from Qwen.

### Phi-4 Mini Instruct Q8
```
Turn  1-20:  good recall, full attention + Q8 helps
Turn 20-40:  capacity limits surface — fact merging (confusing details between facts)
Turn 40+:    smaller capacity degrades faster than Qwen but cleaner than Gemma on distant facts
```
Shape: uniform degradation, earlier onset than Qwen but without Gemma's bifurcation.

### Phi-4 Mini Reasoning Q8
```
Turn  1-20:  possibly better recall than instruct (CoT re-derives facts)
Turn 20-40:  CoT context overhead starts competing with conversation history
Turn 30-50:  context pressure from reasoning chains may cause earlier degradation
Turn 50+:    if CoT helped, it should show as better precision on remaining facts even as total recall drops
```
Shape: depends on which hypothesis holds — could mirror instruct (shifted left by CoT overhead) or outperform it (reasoning improves per-token recall).

---

## Scoring Framework

Every probe response gets two orthogonal scores:

### Recall Score
- **Pass**: correct recall of key details
- **Hedge**: partially right or explicitly uncertain ("I believe...")
- **Fail**: wrong answer or omission
- **Confabulate**: confidently wrong — plausible but incorrect details

### Conflict Behavior
- **Deferred**: used context faithfully, no parametric interference
- **Overrode**: answer matches real-world data, not planted context
- **Flagged**: acknowledged uncertainty or conflict (calibrated deference)
- **Caved**: on contradiction probes — abandoned correct answer to agree with user's wrong correction

These combine into a 4x4 matrix. Example interpretations:
- Pass + Deferred = ideal RAG behavior
- Fail + Overrode = parametric memory won (training data leakage)
- Hedge + Flagged = model knows it doesn't know (best failure mode)
- Pass + Caved = model changed to user's wrong correction (sycophancy)
- Confabulate + Deferred = model used context but reconstructed incorrectly (schema confabulation)
