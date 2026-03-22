# Musings — Long-Conversation Agent

<!-- architect: synergyStud | critic: claude -->

## 2026-03-22 — Ground truth baseline: naive context stuffing stress test

**phase**: prototype

> architect: Build a simple FastAPI + Streamlit engine connecting to local LMStudio (Qwen3.5 9B Q4_KM at 127.0.0.1:1234). Three conversation paths (low/medium/high intensity) with 15 fabricated NBA facts as planted ground truth. Run paths one at a time in separate sessions to avoid OOM. Capture all responses, inspect afterwards against golden truth to define next steps.

> critic: NBA domain is strong — verifiable, specific facts with no room to hedge. Fabricated facts force pure context recall vs training data leakage. Separated intensity axes (length, density, recall distance) across paths. Key risks: quantization compounding with long context will shrink effective window to ~40-50% of advertised; sycophancy increases with context length (model may cave to user contradictions in HIGH path). Using temperature=0 for determinism. Direct OpenAI SDK to LMStudio — no LiteLLM layer needed for single-endpoint setup.

**verdict**: Build the baseline engine with 3 scripted paths, 15 fabricated NBA facts, probe-based recall testing. Direct OpenAI SDK to LMStudio, no LiteLLM. Capture raw data only — score later against golden truth.

**gaps**:
- Need to verify Qwen3.5's actual context window behavior under Q4 quantization
- Lost-in-the-middle positioning effects not yet controlled for in probe design
- No baseline for how fast KV cache grows with this specific model/quantization combo

**next**: Run all three paths, collect results, analyze failure points
