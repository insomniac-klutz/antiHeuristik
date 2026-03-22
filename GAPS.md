# Known Unknowns

Living document. Update as you discover gaps during Builds.

---

## Identified Gaps (from starter.md audit)

### Missing Fields (now covered)
- [x] Multimodal AI → Build 04 (Doc AI), Build 10 (Video Analyzer)
- [x] Voice/Speech → Build 06 (Voice Agent)
- [x] Structured Data + LLMs → Build 03 (NL2SQL Dashboard)
- [x] Security & Safety → Build 02 (tenant isolation), Build 11 (Compliance Gateway), Layer 04
- [x] Code Generation → Build 05 (Code Review Agent)

### Underweighted (now covered)
- [x] Vector DB internals → Build 01 (Patent Search), grind/production-systems.md
- [x] Orchestration frameworks → Build 07 (Framework Shootout)
- [x] Context window management → Build 08 (Long Conversation Agent)
- [x] Cost modeling depth → Layer 02 (Cost Killer), applied to every build
- [x] Async/event-driven → Build 11 (AI Gateway, webhooks), Layer 02

### Structural (now covered)
- [x] Failure mode catalog → Layer 04 (Catastrophe), grind/failure-modes.md
- [x] Paper literacy → stories/papers/timeline.md (19 papers, Word2Vec → DeepSeek V3)
- [x] Data flywheel design → Layer 03 (Feedback Flywheel), applied to every build

---

## Remaining Watch Items

These are thin — covered by a build but only as a secondary concern, not the primary focus. If they don't surface naturally during builds, drill them from grind/.

- [ ] Bias amplification testing — Build 11 mentions it, but easy to skip
- [ ] A/B testing LLM outputs with statistical rigor — Layer 01 stretch, never forced
- [ ] Data residency specifics (GDPR, SOC2) — Build 11 covers it, but compliance details are dense
- [ ] Self-hosted vs managed cost crossover math — Layer 02 + Build 11, but no build forces you to actually self-host and measure
- [ ] "Attention Is All You Need" conceptual depth — no build forces the architecture understanding, pure paper read

---

## Expected Topics Per Build

What you'll likely hit when you start each build. Not a study list — a heads-up so you recognize the wall when you hit it.

### Build 01: Patent Search
`chunking` `embeddings` `reranking` `hybrid search (BM25 + dense)` `vector DB indexing (HNSW/IVF)` `citation grounding` `multi-hop retrieval` `metadata filtering` `RAG paper`

### Build 02: Multi-Tenant Bot
`ReAct loop` `tool use / function calling` `prompt injection (direct + indirect)` `tenant isolation / RBAC` `memory architectures` `human-in-the-loop` `guardrails (input/output)` `system prompt hardening`

### Build 03: NL2SQL Dashboard
`schema linking` `SQL (window functions, CTEs, self-joins)` `structured output (SQL is unforgiving)` `error recovery / retry` `disambiguation strategies` `query validation` `prompt engineering for code generation`

### Build 04: Doc AI Pipeline
`multimodal (vision-language models)` `OCR + LLM pipelines` `document layout detection` `table extraction` `NER / structured extraction` `embedding heterogeneous content` `error handling at scale` `confidence calibration`

### Build 05: Code Review Agent
`code representation for LLMs (diffs, AST)` `agentic planning` `structured output` `precision/recall tradeoffs` `tool use (git, file reading)` `prompt engineering for code understanding` `false positive management`

### Build 06: Voice Agent
`Whisper / STT` `TTS / streaming synthesis` `WebSockets / real-time streaming` `VAD / turn-taking` `end-to-end latency profiling` `audio preprocessing` `async pipeline orchestration`

### Build 07: Framework Shootout
`LangChain` `LangGraph` `LlamaIndex` `CrewAI/AutoGen` `framework vs custom tradeoffs` `vendor lock-in / abstraction layers` `typed interfaces` `debuggability`

### Build 08: Long Conversation Agent
`context window management` `sliding window` `summarization chains` `context packing` `lost-in-the-middle` `KV cache mechanics` `Constitutional AI (self-critique)` `long-context model behavior` `Attention paper`

### Build 09: LLM vs Classical Bakeoff
`XGBoost / logistic regression` `feature engineering vs embeddings` `pandas / polars` `CSV / Parquet` `sequence labeling vs classification vs generation` `cost per prediction` `ensemble routing` `when LLMs are overkill`

### Build 10: Video Incident Analyzer
`frame sampling strategies` `Whisper with timestamps` `speaker diarization` `multimodal fusion (vision + transcript)` `temporal reasoning` `embedding heterogeneous content` `long-context management`

### Build 11: AI Gateway Compliance
`multi-provider abstraction` `PII detection / redaction` `data residency (GDPR)` `webhook design` `self-hosted vs managed cost crossover` `bias testing` `logging sanitization` `circuit breakers / failover` `SOC2 implications`

### Build 12: Greenfield Scoping Sim
`ambiguity navigation` `saying no to AI` `prioritization under uncertainty` `competitive analysis` `cost estimation from scratch` `MVP scoping` `classical ML vs LLM decision` `stakeholder communication`

### Layers (applied to every build)
**L1 Eval**: `LLM-as-judge` `eval dataset construction` `hallucination detection` `metric design (varies per system type)` `statistical significance` `CI quality gates`
**L2 Cost Killer**: `token economics` `caching (semantic, KV, provider-level)` `model routing / cascading` `serving infra (vLLM, TGI)` `observability` `batch vs streaming` `online vs offline`
**L3 Feedback**: `RLHF (applied)` `preference data` `active learning` `LoRA/QLoRA` `fine-tuning decision tree` `continuous eval` `data flywheel economics`
**L4 Catastrophe**: `failure diagnosis` `observability design` `guardrails` `circuit breakers` `drift detection` `graceful degradation` `incident response` `post-mortems`

---

## Gaps Discovered During Builds

*(Add here as you hit walls)*
