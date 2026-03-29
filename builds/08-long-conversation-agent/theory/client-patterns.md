# Client & Abstraction Patterns

## Proxy Abstraction Layer
LiteLLM, database ORMs, filesystem VFS layers — same pattern. Wrap a provider-specific interface behind a unified API so callers don't couple to transport details. The trade-off is always portability vs provider-specific optimizations. For LLM clients: you gain model swappability (LMStudio → Ollama → cloud) but lose access to provider-specific features (LMStudio's speculative decoding config, Ollama's keep_alive, etc.).

The discipline: keep the abstraction thin. A client handles connection, retry, and serialization. Business logic (prompt construction, memory management, eval) stays in the caller. The moment you add prompt templates or conversation history to your client, you've created a god object.

## Repository Pattern Applied to LLM Calls
The async client is essentially the Repository pattern — abstract "how do I talk to the model" so consumers think only in terms of "send messages, get response." This is the same reason you don't scatter SQL queries across your codebase. One place to change connection logic, retry policy, or provider.

## Exponential Backoff
Standard retry pattern: wait 2^attempt seconds between retries. Critical for local inference where the model might be mid-generation on another request and temporarily unresponsive. Without backoff, rapid retries just pile up and make things worse (thundering herd on your own machine). Three retries with 1s/2s/4s waits covers transient failures without making the user wait too long on genuine failures.

## Event Sourcing for Conversation State
The conversation runner implements an append-only event log where each event is a `(user_turn, assistant_response)` pair. This is the same pattern used in CQRS/event-sourced systems — the log *is* the state, and you can derive any view (eval scores, latency charts, token counts) by replaying it.

Key properties:
- **Deterministic inputs**: scripted user turns are fixed; only model responses vary between runs
- **Incremental persistence**: save after each turn, not at the end. A crashed run still produces usable partial data — you lose one turn, not the whole conversation
- **Separation of capture and judgment**: the runner writes raw data, the eval layer scores it. This means you can re-score the same run with different eval criteria without re-running the (expensive) inference

This is also why the runner uses `complete()` (non-streaming) rather than `stream()` — for benchmarking, you want the full response as a single atomic artifact. Streaming is for UX, not for eval.

## API Documentation vs API Reality (Impedance Mismatch)

When different endpoints in the same API name the same concept differently, consumers always hit this wall. LMStudio's listing endpoint returns `loaded_instances[].id`, but the unload endpoint expects `{"instance_id": ...}` — same value, different key name. Similarly, models loaded via UI get short identifiers (`qwen3.5-9b`) while the API uses full paths (`qwen/qwen3.5-9b`).

This is the **impedance mismatch** problem — a term borrowed from electrical engineering (and famously applied to ORMs by Ted Neward). Two representations of the same entity don't map cleanly. The defensive patterns:

1. **Dump raw responses during integration**. Never trust docs alone — the first thing you build against a new API is a diagnostic that prints the actual response shape. You debug from reality, not from specs.
2. **Bidirectional matching**. When comparing identifiers across system boundaries, check both directions: `a in b or b in a`. One system may use a prefix, namespace, or abbreviation the other doesn't. Unidirectional substring matching is a latent bug.
3. **Canonical identifiers**. If you control the code but not the API, normalize identifiers early (strip prefixes, lowercase) and compare canonical forms. Don't let different naming conventions leak into business logic.

The broader lesson: integration bugs are almost never in the logic — they're in the assumptions about data shape. Treat every external API response as untrusted structure until you've verified it empirically.

## Observability Over Configuration

A system is **observable** (control theory, Kalman 1960) when its internal state can be determined from its outputs alone. Applied to software: prefer reading actual state over trusting declared constants.

Concrete example: GPU VRAM. A hardcoded `GPU_VRAM_GB=12` in `.env` is a lie the moment you run on a different machine, a driver update changes reported memory, or another process allocates VRAM. Reading `nvidia-smi` at runtime gives ground truth — self-correcting, no manual tuning, works on any machine.

The general principle from **twelve-factor app** methodology (Wiggins, 2011): configuration is for things that *vary between deploys* and *cannot be detected* (API keys, endpoint URLs). Hardware state is not configuration — it's observable system state. Treating observable state as configuration creates a second source of truth that inevitably drifts from the first.

When to prefer detection over config:
- **Hardware**: VRAM, CPU cores, disk space — always detectable, always drifting
- **Runtime state**: loaded models, running processes, network reachability — poll, don't assume
- **Versions**: library versions, API versions — query, don't hardcode

When config is still correct:
- **Secrets**: API keys, tokens — not detectable
- **Policy**: base URLs, retry limits, timeouts — human decisions, not physical state
- **Overrides**: when you *want* to lie to the system (test with 4GB VRAM limit on a 12GB card)

## Thinking Model Output Routing

Not all models put their response in the same field. Standard instruction-tuned models return content in `choices[0].message.content`. But thinking/reasoning models (Qwen 3.5, DeepSeek-R1, etc.) may split their output:

- `content`: the final user-facing response (may be empty if all tokens went to thinking)
- `reasoning_content`: the internal chain-of-thought (the "thinking" block)

Qwen 3.5 at low `max_tokens` (e.g. 256) spends its entire token budget on `reasoning_content` and returns `content: ""`. At higher budgets (2048+), it finishes thinking and writes the actual response to `content`. LMStudio separates these fields at the API level — the same model served through a different runtime might concatenate them or use `<think>` tags instead.

This is a specific instance of the **polymorphic response** problem: the same API endpoint returns structurally different responses depending on the model loaded behind it. The defensive pattern is a **fallback chain** — check `content` first, fall back to `reasoning_content`, and fail explicitly if both are empty. Never assume the response shape is stable across models.

The broader lesson connects to Postel's Law (the Robustness Principle): "Be conservative in what you send, be liberal in what you accept." When consuming API responses, handle all documented fields even if only one model uses them. When producing requests, use the most standard format possible.
