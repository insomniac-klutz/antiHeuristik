# dl — Theo Index

## Files
- attention.md — attention mechanisms, scaling behavior, quantization, and precision tradeoffs

## attention.md
- Mechanisms & Architectures — how attention variants and caching work at the hardware level
  - Grouped Query Attention (GQA) — shared KV heads trade representational capacity for memory savings
  - Flash Attention — tiled attention computation for O(N) memory without changing results
  - KV Cache Mechanics — storing past token projections, memory costs, and error accumulation
  - PagedAttention — virtual memory paging applied to KV cache for dynamic context lengths
- Scaling & Degradation — how attention quality breaks down as context grows
  - Lost-in-the-Middle Effect — recall drops for facts in the 40-60% depth range of context
  - Attention Score Degradation at Long Context — softmax dilution reduces signal-to-noise at scale
  - Effective vs Advertised Context — quantized models degrade faster than benchmarks suggest
  - Expected Degradation Pattern (Q4 9B model) — turn-by-turn breakdown of recall collapse
  - Compound Effect of Optimizations — GQA + quantization degrade non-linearly together
- Quantization — weight compression mechanics and their impact on attention precision
  - Perplexity — next-token surprise metric and why small loss increases compound over long contexts
  - Q4 Quantization and Attention Precision — reduced weight precision makes attention scores indistinguishable at long context
  - Systematic Flattening — quantization directionally compresses attention score dynamic range
