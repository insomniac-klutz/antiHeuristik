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

## 2026-03-29 — Shared async LiteLLM client

**phase**: prototype

> architect: Build an async LiteLLM client in a shared `clients/` dir at repo root. Reusable across builds. LiteLLM instead of direct OpenAI SDK. Minimal config, exponential backoff with timeouts, support both streaming and non-streaming, Pydantic message types.

> critic: LiteLLM gives provider portability — swap LMStudio to Ollama/Together/cloud with a model string change. Async is the right default for FastAPI + Streamlit. Kept the client thin: connection, retry, serialization only. Business logic stays in callers. Exponential backoff (2^attempt seconds) handles local inference hangs under VRAM pressure.

**verdict**: Async LiteLLM client built at `clients/litellm_client.py`. Pydantic `Message`/`Role`/`LLMResponse` types. Expo backoff (3 retries, 2^n wait). 120s default timeout. Streaming + non-streaming. CLAUDE.md updated to direct builds to check `clients/` first.

**gaps**:
- LiteLLM's streaming error handling per provider not yet tested — verify with LMStudio before build 08 conversation runs
- No token counting utility yet — will need one when we hit context window budgeting

**next**: Build the conversation engine for build 08 using this client

## 2026-03-29 — Agreeability vs guardrails: the grounding-reliability tension

**phase**: design

> architect: Does better agreeability (contextual grounding) not tussle with the model's inbuilt guardrails (factual reliability)?

> critic: Direct tension — one of the core unsolved alignment problems. The model has two competing directives: (1) be contextually grounded — use what the user/context says, don't override with priors; (2) be factually reliable — don't repeat known falsehoods, maintain guardrails. Our entire test is built on this collision.

Spectrum of failure modes:
- **Too agreeable**: model accepts everything including misinformation. RAG systems break here — blind trust in retrieved context.
- **Too guarded**: model ignores user-provided context because it "knows better." Makes RAG useless.
- **Calibrated deference** (ideal): model uses context by default, flags conflicts when confidence is high. "You mentioned X, though I recall Y — should I go with your figure?" Almost no model does this well.

For our test, probe outcomes need a richer scoring dimension:
- Model **corrects fabricated facts** → parametric override. Bad for RAG, shows guardrail strength.
- Model **faithfully recalls fabricated facts** → contextual grounding. Good for RAG, guardrails yield to context.
- Model **recalls facts AND flags uncertainty** → calibrated deference. Best outcome.
- On contradiction probes: model is asked to trust user's *first* statement but resist user's *second* (contradictory) statement — an inherent tension that tests grounding stability.

Instruction hierarchy matters (Wallace et al., 2024): system prompt > user instructions > context. Our facts are seeded in user turns (middle priority), not system prompt. This is deliberate — reflects real conversation dynamics, not optimized-for-recall placement.

**verdict**: Add `conflict_behavior` as a scoring dimension to the eval model: `deferred` (used context), `overrode` (used training data), `flagged` (acknowledged conflict), `caved` (sycophancy on contradiction). Existing pass/hedge/fail/confabulate scores are necessary but not sufficient — *how* the model handles the conflict is as important as *whether* it recalls correctly.

**gaps**:
- No framework yet for distinguishing "model corrected our fact because parametric override" vs "model just got confused" — need to check if the wrong answer matches real-world data
- Contradiction probes create an inherent paradox: we want the model to trust seeded facts but resist user corrections to those same facts. Scoring this fairly requires knowing which directive the model is following
- Calibrated deference is the best outcome but hardest to score automatically — may need manual review

**next**: Update eval scoring model in theory docs, then build the runner

## 2026-03-29 — Conversation runner + CLI entrypoint

**phase**: prototype

> architect: Build the runner.

> critic: Runner is an event sourcing system — deterministic inputs, append-only state, captured outputs. Key design decisions: (1) history accumulates both user and assistant turns so the model sees its own prior responses; (2) incremental save after every turn so a crash yields usable partial data; (3) runner captures only, eval scores later — separation of concerns. Risk: LMStudio OOM mid-path loses the run without incremental saves.

**verdict**: Built `prototype/runner.py` (async engine with incremental JSON saves, Pydantic result models) and `prototype/run.py` (CLI: `python -m prototype.run low|medium|high|all` with `--model`, `--base-url`, `--max-tokens`, `--output-dir` flags). Uses shared `clients/LLMClient`. Results saved to `prototype/results/`.

**gaps**:
- No token counting per turn — need this to plot context consumption vs recall degradation
- No streaming mode in the runner yet — using `complete()` only, fine for benchmarking but Streamlit will want streaming later
- Haven't tested the full pipeline end-to-end with LMStudio yet

**next**: Run low path against LMStudio as smoke test, then build eval scorer

## 2026-03-29 — Model selection: four models, five dimensions

**phase**: design

> architect: Evaluated multiple models for 12GB VRAM constraint. Key decisions: (1) Qwen 3.5 9B Q4 as high-capacity baseline; (2) Gemma 3 4B Q8 — comparable VRAM but fewer weights at higher precision, testing capacity-vs-precision trade-off AND different attention arch (sliding window 5:1); (3) Phi-4-mini-instruct Q8 + Phi-4-mini-reasoning Q8 as a controlled ablation pair — identical architecture, different fine-tuning, tests whether reasoning training helps or hurts conversational recall. Dropped DeepSeek-R1-0528-Qwen3-8B (33K context) due to silent truncation confound on HIGH path. Dropped Gemma 2 9B (8K context — would overflow by turn 15).

> critic: The Gemma 3 4B Q8 insight is the sharpest design choice — same VRAM as DeepSeek/Phi but allocates it to precision over capacity. The Phi-4 ablation pair is the cleanest comparison in the lineup: same arch, same quant, same size, only training differs. Five dimensions isolated: capacity vs precision, attention architecture (GQA vs sliding window vs full), training pipeline (Alibaba vs Google vs Microsoft), reasoning vs general tuning, and parametric conflict behavior. All four models have native 128K context — no YaRN confounds, no truncation contamination.

**verdict**: Final lineup locked. Qwen 3.5 9B Q4, Gemma 3 4B Q8, Phi-4-mini-instruct Q8, Phi-4-mini-reasoning Q8. Model metadata captured in `prototype/model_cards.py` (Pydantic models with architecture details, eval dimensions, and risk flags). Full experimental design documented in `theory/architecture-eval.md`.

**gaps**:
- Haven't verified LMStudio compatibility for all four models — smoke test needed
- Phi-4-reasoning CoT token overhead not yet measured — need actual token counts to validate context budget projections
- VRAM monitoring during runs not yet instrumented — need to track KV cache growth to validate headroom estimates
- Predicted degradation patterns are theoretical — may diverge significantly from actual behavior

**next**: Add model presets to `run.py`, then smoke test LOW path on all four models
