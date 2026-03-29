# dl — Theo Index

## Files
- attention.md — attention mechanisms, architecture comparison, scaling behavior, quantization, and precision tradeoffs

## attention.md
- Mechanisms & Architectures — how attention variants and caching work at the hardware level
  - Grouped Query Attention (GQA) — shared KV heads trade representational capacity for memory savings
  - Flash Attention — tiled attention computation for O(N) memory without changing results
  - KV Cache Mechanics — storing past token projections, memory costs, and error accumulation
  - Static Pre-Allocation vs Dynamic KV Cache Growth — upfront vs per-token KV cache memory and the static allocation tradeoff
  - PagedAttention — virtual memory paging applied to KV cache for dynamic context lengths
- Architecture Comparison — comparative analysis of attention architectures and capacity-precision tradeoffs
  - Attention Architecture — GQA vs sliding window vs full attention: three patterns, three degradation predictions
  - Capacity vs Precision — parameter count vs quantization quality as a bias-variance tradeoff for local inference
  - The Lineup — concrete model examples illustrating architecture and quantization combinations
    - Qwen 3.5 9B — Q4_K_M (~6.6GB) — high-capacity GQA baseline at low precision
    - Gemma 3 4B — Q8_0 (4.98GB) — sliding window architecture with high precision
    - Phi-4 Mini Instruct — Q8_0 (4.08GB) — full attention baseline and reasoning ablation control
    - Phi-4 Mini Reasoning — Q8_0 (4.08GB) — reasoning-tuned ablation isolating CoT effects
- Scaling & Degradation — how attention quality breaks down as context grows
  - Lost-in-the-Middle Effect — recall drops for facts in the 40-60% depth range of context
  - Attention Score Degradation at Long Context — softmax dilution reduces signal-to-noise at scale
  - Effective vs Advertised Context — quantized models degrade faster than benchmarks suggest
  - Expected Degradation Pattern (Q4 9B model) — turn-by-turn breakdown of recall collapse
  - Compound Effect of Optimizations — GQA + quantization degrade non-linearly together
  - Predicted Degradation Patterns — architecture-specific degradation curves based on theory
    - Qwen 3.5 9B Q4 — gradual linear degradation, worst in the 40-60% depth zone
    - Gemma 3 4B Q8 — bifurcated curve: steep for distant facts, flat for recent
    - Phi-4 Mini Instruct Q8 — uniform degradation with earlier onset from capacity limits
    - Phi-4 Mini Reasoning Q8 — CoT overhead vs reasoning benefit: competing effects on recall
- Quantization — weight compression mechanics and their impact on attention precision
  - Perplexity — next-token surprise metric and why small loss increases compound over long contexts
  - Q4 Quantization and Attention Precision — reduced weight precision makes attention scores indistinguishable at long context
  - Systematic Flattening — quantization directionally compresses attention score dynamic range
