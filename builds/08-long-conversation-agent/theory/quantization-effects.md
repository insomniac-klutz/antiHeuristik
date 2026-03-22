# Quantization Effects on Long-Context Performance

## Perplexity
How "surprised" a model is by the next token. Lower = more confident and accurate. Defined as `perplexity = 2^(cross-entropy)`. When papers report "0.1 increase in loss from quantization," that sounds small, but exponentiated over thousands of tokens across a long conversation, it means materially more wrong-token choices.

## Q4 Quantization and Attention Precision
Weights stored with ~1-1.5 digits of effective precision (vs ~3-4 for FP16). Attention scores are computed from Q, K matrices derived from these weights. At short context, the gap between relevant and irrelevant attention scores is huge — small rounding doesn't flip rankings. At long context, scores are already small and close together. Q4 rounding introduces noise on the *same scale as the signal difference*. The model literally cannot distinguish between the token it should attend to and 50 nearby irrelevant tokens.

## Systematic Flattening
Quantization doesn't add random noise — it *systematically reduces the dynamic range* of attention scores. Peaks get lower, valleys get higher. The model's ability to say "THIS token matters, those don't" gets weaker with every turn added to context. This is directional, not stochastic — it consistently degrades retrieval.

## Effective vs Advertised Context
Full-precision model might have perplexity ~8 at 4K tokens and ~12 at 32K. Q4_KM might be ~8.5 at 4K but ~16+ at 32K. The gap widens with context length. Quantization benchmarks on short prompts are misleading for long-context use cases — always test at the context lengths you actually plan to use.

## Expected Degradation Pattern (Q4 9B model)
- Turns 1-20: nearly identical to full precision, recall probes pass
- Turns 20-40: subtle hedging ("I believe you mentioned..."), slightly less precise recalls, occasional fact merging
- Turns 40-60: recall probes for early facts start failing, confabulation appears (plausible but wrong)
- Turns 60+: coherence collapse — contradictions within 5 turns, repetition, thread loss

Exact turn numbers shift based on token density per turn. High-density conversations hit the wall 2-3x sooner than low-density.
