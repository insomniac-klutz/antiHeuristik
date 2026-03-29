# Attention

## Mechanisms & Architectures

### Grouped Query Attention (GQA)
Shares K and V projections across groups of query heads. If a model has 32 query heads but only 8 KV heads, every 4 query heads share the same keys. This cuts KV cache size by 4x but trades representational capacity — the shared keys are a compromise optimized for no single head. At long context, this compromise hurts: when two heads in the same group need to attend to different distant facts, the shared keys can't serve both well.

Qwen3.5 uses GQA. This means it can *fit* longer contexts in VRAM, but recall quality at those lengths is slightly worse than equivalent MHA (multi-head attention) would give.

### Flash Attention
Tiles the attention computation to avoid materializing the full N×N attention matrix in GPU HBM (slow main memory). Instead, streams blocks of Q, K, V through fast on-chip SRAM. Result is bit-for-bit identical to standard attention but:
- Memory: O(N) instead of O(N²)
- Speed: 2-4x faster at long contexts (eliminates HBM round-trips)

Flash Attention is a pure engineering win — it doesn't change what's computed, just how the hardware executes it. It does NOT fix attention precision issues.

Key concept: the **Roofline model** — attention is memory-bound, not compute-bound. The GPU can do the math 10x faster than it can fetch the data. Flash Attention closes that gap.

### KV Cache Mechanics
Stores K and V vectors for every past token so they don't need recomputation. At 20K tokens with 32 layers:
- KV cache can reach ~10GB for a 9B model at FP16
- This competes with model weights for VRAM
- Each new token computes attention against the *entire* accumulated cache

With GQA + Q4 quantization, the K vectors in cache are derived from quantized weights (already slightly wrong). Errors accumulate as cache grows — they don't cancel out because quantization systematically reduces the dynamic range of attention scores (peaks get lower, valleys get higher).

### Static Pre-Allocation vs Dynamic KV Cache Growth
LMStudio pre-allocates the full KV cache at model load time based on the `context_length` parameter. A 9B Q4 model loaded with 262K context consumed ~11.4GB of 11.94GB VRAM — the model weights are 6.55GB, and the remaining ~5GB was pre-allocated KV cache for 262K tokens. Reducing to 64K dropped usage significantly.

This is the **static allocation** pattern: reserve the worst-case memory budget upfront, guarantee no mid-run failures. The alternative is **dynamic allocation** where KV cache grows per-token — smaller footprint on short conversations but risks OOM at turn 45 of 48 (losing the entire run).

The trade-off maps directly to real-time systems engineering (avionics, medical devices) where `malloc` at runtime is banned. The reasoning is identical: if you allocate dynamically, you must prove the system can't exceed its budget under any input — which is equivalent to computing the worst case anyway. Static allocation makes the worst case the *only* case.

For benchmarking, static is strictly better: a crash partway through a run wastes more than the extra VRAM would. For production chat (variable-length conversations), dynamic allocation with a hard cap and graceful degradation is more practical — vLLM's PagedAttention takes this approach.

**Practical rule**: set `context_length` to the actual maximum you'll need, not the model's advertised maximum.

### PagedAttention
Used in vLLM. Extends Flash Attention's idea to the KV cache itself — applies virtual memory paging concepts to GPU memory for dynamic context lengths. Relevant for production serving but not for single-session testing.

## Architecture Comparison

### Attention Architecture

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

### Capacity vs Precision

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

### The Lineup

#### Qwen 3.5 9B — Q4_K_M (~6.6GB)
**Role**: High-capacity, low-precision baseline.

- 9B params, GQA (grouped query attention), 128K native context
- Full attention at every layer — every token attends to every other token
- Q4_K_M quantization reduces weights to ~1-1.5 digits of effective precision
- Most parameters in the lineup = most representational capacity for routing attention
- Q4 = lowest precision = most vulnerable to attention score flattening at long context

**Prediction**: Should hold recall longest due to raw capacity, but Q4 noise will compound turn-over-turn in the KV cache. Expect gradual degradation starting around turn 30-40, with the lost-in-the-middle zone (facts at 40-60% depth) failing first.

#### Gemma 3 4B — Q8_0 (4.98GB)
**Role**: Sliding window architecture + high precision.

- 4B params, sliding window (1024) interleaved with global attention at 5:1 ratio, 128K native
- Only 1/6 of layers do global attention — the other 5/6 only see the nearest 1024 tokens
- Q8_0 = ~3x the effective precision of Q4
- RoPE base frequency 1M (vs 10K in Gemma 2)
- KV cache overhead <15% vs ~60% for global-only architectures

**Prediction**: Recent facts should be recalled extremely well (all 6 layers see them). Distant facts degrade faster than Qwen because only global layers (1/6) carry that information. The degradation curve should have a different *shape* — steeper drop-off for distant facts, flatter for recent. If we observe this, it's direct evidence that attention architecture shapes the recall curve, not just context length.

#### Phi-4 Mini Instruct — Q8_0 (4.08GB)
**Role**: Microsoft architecture baseline, control for reasoning ablation.

- 3.8B params, full attention at every layer, 128K native context
- Phi-4 architecture — distinct from both Qwen's GQA and Gemma's sliding window
- Trained on synthetic, high-quality data (Microsoft's approach)
- General-purpose instruction tuning
- Smallest model in the lineup

**Prediction**: Full attention gives it the best theoretical reach to distant facts per-layer, but 3.8B params means less capacity to maintain distinct fact representations. Q8 precision helps. Expect a capacity-limited failure pattern — may start confusing facts with each other (merging details) rather than losing them entirely.

#### Phi-4 Mini Reasoning — Q8_0 (4.08GB)
**Role**: Reasoning-tuned ablation of Phi-4 Mini Instruct.

- Identical architecture, identical quant, identical size
- Only difference: fine-tuned on synthetic reasoning-dense data with chain-of-thought
- CoT reasoning generates extra tokens per response that consume context budget

**Prediction**: Two competing effects:
1. **CoT helps recall** — reasoning forces the model to explicitly re-derive facts from context rather than pattern-matching from memory. This could improve grounding and reduce parametric override.
2. **CoT hurts context budget** — extra reasoning tokens (200-500 per response) consume ~10-25K tokens across 50 turns. Despite 128K window, effective available context shrinks.
3. **Domain mismatch** — math-reasoning training may have narrowed attention patterns for structured problems, weakening free-form conversational recall.

The delta between Phi-4 reasoning and Phi-4 instruct isolates the effect of reasoning-specific training on conversational context grounding.

## Scaling & Degradation

### Lost-in-the-Middle Effect
Liu et al., 2023. LLMs recall facts placed at the beginning and end of context far better than facts buried in the middle. In a 100-turn conversation, facts at turns 30-60 sit in the attention dead zone — even if the context window hasn't overflowed. Probe design must control for *position* of the planted fact, not just distance in turns.

### Attention Score Degradation at Long Context
Every token gets an attention score — "how relevant is this token to what I'm generating now?" At short context (~500 tokens), relevant tokens score 50-100x above noise. At long context (~20K tokens), softmax distributes across all positions — relevant tokens might only score 40x above noise, and there are far more noise positions competing. The signal-to-noise ratio shrinks with length even without any quantization.

### Effective vs Advertised Context
Full-precision model might have perplexity ~8 at 4K tokens and ~12 at 32K. Q4_KM might be ~8.5 at 4K but ~16+ at 32K. The gap widens with context length. Quantization benchmarks on short prompts are misleading for long-context use cases — always test at the context lengths you actually plan to use.

### Expected Degradation Pattern (Q4 9B model)
- Turns 1-20: nearly identical to full precision, recall probes pass
- Turns 20-40: subtle hedging ("I believe you mentioned..."), slightly less precise recalls, occasional fact merging
- Turns 40-60: recall probes for early facts start failing, confabulation appears (plausible but wrong)
- Turns 60+: coherence collapse — contradictions within 5 turns, repetition, thread loss

Exact turn numbers shift based on token density per turn. High-density conversations hit the wall 2-3x sooner than low-density.

### Compound Effect of Optimizations
GQA (trades precision) + Flash Attention (free) + Q4 quantization (trades precision) = quality degrades faster than any single technique would suggest. The "effective context window" under all three may be ~40-50% of the advertised maximum. Nobody benchmarks the compound effect — they benchmark each optimization in isolation and assume linear composition. They don't compose linearly.

### Predicted Degradation Patterns

Based on architecture and quantization theory:

#### Qwen 3.5 9B Q4
```
Turn  1-20:  near-perfect recall, Q4 noise negligible
Turn 20-40:  subtle hedging on independent facts, schema facts hold
Turn 40-60:  lost-in-the-middle failures on early-seeded facts
Turn 60+:    confabulation appears, fact merging, coherence decay
```
Shape: gradual linear degradation, worst in the 40-60% depth zone.

#### Gemma 3 4B Q8
```
Turn  1-20:  strong recall, Q8 precision keeps scores sharp
Turn 20-40:  distant facts start failing (only 1/6 layers see them)
Turn 30-50:  recent facts still strong, distant facts weak — bifurcated curve
Turn 50+:    capacity limits may cause fact merging across both distances
```
Shape: bifurcated — steep for distant, flat for recent. Different curve shape from Qwen.

#### Phi-4 Mini Instruct Q8
```
Turn  1-20:  good recall, full attention + Q8 helps
Turn 20-40:  capacity limits surface — fact merging (confusing details between facts)
Turn 40+:    smaller capacity degrades faster than Qwen but cleaner than Gemma on distant facts
```
Shape: uniform degradation, earlier onset than Qwen but without Gemma's bifurcation.

#### Phi-4 Mini Reasoning Q8
```
Turn  1-20:  possibly better recall than instruct (CoT re-derives facts)
Turn 20-40:  CoT context overhead starts competing with conversation history
Turn 30-50:  context pressure from reasoning chains may cause earlier degradation
Turn 50+:    if CoT helped, it should show as better precision on remaining facts even as total recall drops
```
Shape: depends on which hypothesis holds — could mirror instruct (shifted left by CoT overhead) or outperform it (reasoning improves per-token recall).

## Quantization

### Perplexity
How "surprised" a model is by the next token. Lower = more confident and accurate. Defined as `perplexity = 2^(cross-entropy)`. When papers report "0.1 increase in loss from quantization," that sounds small, but exponentiated over thousands of tokens across a long conversation, it means materially more wrong-token choices.

### Q4 Quantization and Attention Precision
Weights stored with ~1-1.5 digits of effective precision (vs ~3-4 for FP16). Attention scores are computed from Q, K matrices derived from these weights. At short context, the gap between relevant and irrelevant attention scores is huge — small rounding doesn't flip rankings. At long context, scores are already small and close together. Q4 rounding introduces noise on the *same scale as the signal difference*. The model literally cannot distinguish between the token it should attend to and 50 nearby irrelevant tokens.

### Systematic Flattening
Quantization doesn't add random noise — it *systematically reduces the dynamic range* of attention scores. Peaks get lower, valleys get higher. The model's ability to say "THIS token matters, those don't" gets weaker with every turn added to context. This is directional, not stochastic — it consistently degrades retrieval.
