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

### PagedAttention
Used in vLLM. Extends Flash Attention's idea to the KV cache itself — applies virtual memory paging concepts to GPU memory for dynamic context lengths. Relevant for production serving but not for single-session testing.

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

## Quantization

### Perplexity
How "surprised" a model is by the next token. Lower = more confident and accurate. Defined as `perplexity = 2^(cross-entropy)`. When papers report "0.1 increase in loss from quantization," that sounds small, but exponentiated over thousands of tokens across a long conversation, it means materially more wrong-token choices.

### Q4 Quantization and Attention Precision
Weights stored with ~1-1.5 digits of effective precision (vs ~3-4 for FP16). Attention scores are computed from Q, K matrices derived from these weights. At short context, the gap between relevant and irrelevant attention scores is huge — small rounding doesn't flip rankings. At long context, scores are already small and close together. Q4 rounding introduces noise on the *same scale as the signal difference*. The model literally cannot distinguish between the token it should attend to and 50 nearby irrelevant tokens.

### Systematic Flattening
Quantization doesn't add random noise — it *systematically reduces the dynamic range* of attention scores. Peaks get lower, valleys get higher. The model's ability to say "THIS token matters, those don't" gets weaker with every turn added to context. This is directional, not stochastic — it consistently degrades retrieval.
