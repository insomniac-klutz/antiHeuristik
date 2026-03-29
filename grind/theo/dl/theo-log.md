# dl — Theo Log

## 2026-03-28 — build-08-long-conversation-agent

- context-and-attention.md → attention.md (created)
  - Grouped Query Attention (GQA)
  - Flash Attention
  - KV Cache Mechanics
  - PagedAttention
  - Lost-in-the-Middle Effect
  - Attention Score Degradation at Long Context
  - Compound Effect of Optimizations
- quantization-effects.md → attention.md (appended)
  - Perplexity
  - Q4 Quantization and Attention Precision
  - Systematic Flattening
  - Effective vs Advertised Context
  - Expected Degradation Pattern

## 2026-03-29 — build-08-long-conversation-agent

- context-and-attention.md → attention.md (appended)
  - Static Pre-Allocation vs Dynamic KV Cache Growth
- architecture-eval.md → attention.md (appended)
  - Attention Architecture
  - Capacity vs Precision
  - The Lineup
    - Qwen 3.5 9B — Q4_K_M (~6.6GB)
    - Gemma 3 4B — Q8_0 (4.98GB)
    - Phi-4 Mini Instruct — Q8_0 (4.08GB)
    - Phi-4 Mini Reasoning — Q8_0 (4.08GB)
  - Predicted Degradation Patterns
    - Qwen 3.5 9B Q4
    - Gemma 3 4B Q8
    - Phi-4 Mini Instruct Q8
    - Phi-4 Mini Reasoning Q8
