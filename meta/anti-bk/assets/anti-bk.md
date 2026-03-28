<div class="title-page">
  <div class="book-title">antiHeuristik</div>
  <div class="book-subtitle">pathei mathos ara prōtai archai</div>
  <hr class="divider">
  <div class="tagline">cargo cult engineering  ×  return to monke</div>
  <div class="meta">
    auto-generated 2026-03-29<br>
    source: grind/theo/ index hierarchy
  </div>
</div>

<h2 class="toc-heading">Table of Contents</h2>
<nav class="toc">
<ol>
  <li><a href="#1-deep-learning"><strong>1. Deep Learning</strong></a>
    <ol>
      <li><a href="#11-attention">1.1. attention</a><span> &mdash; attention mechanisms, scaling behavior, quantization, and precision tradeoffs</span>
        <ul>
          <li><a href="#mechanisms-architectures">Mechanisms & Architectures</a></li>
          <li><a href="#scaling-degradation">Scaling & Degradation</a></li>
          <li><a href="#quantization">Quantization</a></li>
        </ul>
      </li>
    </ol>
  </li>
  <li><a href="#2-natural-language-processing"><strong>2. Natural Language Processing</strong></a>
    <ol>
      <li><a href="#21-evaluation">2.1. evaluation</a><span> &mdash; LLM evaluation methods, recall patterns, and behavioral failure modes</span>
        <ul>
          <li><a href="#methods-frameworks">Methods & Frameworks</a></li>
          <li><a href="#behavioral-patterns">Behavioral Patterns</a></li>
        </ul>
      </li>
    </ol>
  </li>
</ol>
</nav>

<h2 id="1-deep-learning">1. Deep Learning</h2>

<p class="chapter-desc"><em>deep learning fundamentals, architectures, and training</em></p>

<nav class="chapter-toc">
<ul>
  <li><a href="#11-attention"><strong>1.1. attention</strong></a>
    <span> &mdash; attention mechanisms, scaling behavior, quantization, and precision tradeoffs</span>
    <ul>
      <li><a href="#mechanisms-architectures">Mechanisms & Architectures</a></li>
      <li><a href="#scaling-degradation">Scaling & Degradation</a></li>
      <li><a href="#quantization">Quantization</a></li>
    </ul>
  </li>
</ul>
</nav>

---

<h3 id="11-attention">1.1. attention</h3>
<p class="section-desc"><em>attention mechanisms, scaling behavior, quantization, and precision tradeoffs</em></p>

<h4 id="mechanisms-architectures">Mechanisms & Architectures</h4>

<h5 id="grouped-query-attention-gqa">Grouped Query Attention (GQA)</h5>
Shares K and V projections across groups of query heads. If a model has 32 query heads but only 8 KV heads, every 4 query heads share the same keys. This cuts KV cache size by 4x but trades representational capacity — the shared keys are a compromise optimized for no single head. At long context, this compromise hurts: when two heads in the same group need to attend to different distant facts, the shared keys can't serve both well.

Qwen3.5 uses GQA. This means it can *fit* longer contexts in VRAM, but recall quality at those lengths is slightly worse than equivalent MHA (multi-head attention) would give.

<h5 id="flash-attention">Flash Attention</h5>
Tiles the attention computation to avoid materializing the full N×N attention matrix in GPU HBM (slow main memory). Instead, streams blocks of Q, K, V through fast on-chip SRAM. Result is bit-for-bit identical to standard attention but:
- Memory: O(N) instead of O(N²)
- Speed: 2-4x faster at long contexts (eliminates HBM round-trips)

Flash Attention is a pure engineering win — it doesn't change what's computed, just how the hardware executes it. It does NOT fix attention precision issues.

Key concept: the **Roofline model** — attention is memory-bound, not compute-bound. The GPU can do the math 10x faster than it can fetch the data. Flash Attention closes that gap.

<h5 id="kv-cache-mechanics">KV Cache Mechanics</h5>
Stores K and V vectors for every past token so they don't need recomputation. At 20K tokens with 32 layers:
- KV cache can reach ~10GB for a 9B model at FP16
- This competes with model weights for VRAM
- Each new token computes attention against the *entire* accumulated cache

With GQA + Q4 quantization, the K vectors in cache are derived from quantized weights (already slightly wrong). Errors accumulate as cache grows — they don't cancel out because quantization systematically reduces the dynamic range of attention scores (peaks get lower, valleys get higher).

<h5 id="pagedattention">PagedAttention</h5>
Used in vLLM. Extends Flash Attention's idea to the KV cache itself — applies virtual memory paging concepts to GPU memory for dynamic context lengths. Relevant for production serving but not for single-session testing.

<h4 id="scaling-degradation">Scaling & Degradation</h4>

<h5 id="lost-in-the-middle-effect">Lost-in-the-Middle Effect</h5>
Liu et al., 2023. LLMs recall facts placed at the beginning and end of context far better than facts buried in the middle. In a 100-turn conversation, facts at turns 30-60 sit in the attention dead zone — even if the context window hasn't overflowed. Probe design must control for *position* of the planted fact, not just distance in turns.

<h5 id="attention-score-degradation-at-long-context">Attention Score Degradation at Long Context</h5>
Every token gets an attention score — "how relevant is this token to what I'm generating now?" At short context (~500 tokens), relevant tokens score 50-100x above noise. At long context (~20K tokens), softmax distributes across all positions — relevant tokens might only score 40x above noise, and there are far more noise positions competing. The signal-to-noise ratio shrinks with length even without any quantization.

<h5 id="effective-vs-advertised-context">Effective vs Advertised Context</h5>
Full-precision model might have perplexity ~8 at 4K tokens and ~12 at 32K. Q4_KM might be ~8.5 at 4K but ~16+ at 32K. The gap widens with context length. Quantization benchmarks on short prompts are misleading for long-context use cases — always test at the context lengths you actually plan to use.

<h5 id="expected-degradation-pattern-q4-9b-model">Expected Degradation Pattern (Q4 9B model)</h5>
- Turns 1-20: nearly identical to full precision, recall probes pass
- Turns 20-40: subtle hedging ("I believe you mentioned..."), slightly less precise recalls, occasional fact merging
- Turns 40-60: recall probes for early facts start failing, confabulation appears (plausible but wrong)
- Turns 60+: coherence collapse — contradictions within 5 turns, repetition, thread loss

Exact turn numbers shift based on token density per turn. High-density conversations hit the wall 2-3x sooner than low-density.

<h5 id="compound-effect-of-optimizations">Compound Effect of Optimizations</h5>
GQA (trades precision) + Flash Attention (free) + Q4 quantization (trades precision) = quality degrades faster than any single technique would suggest. The "effective context window" under all three may be ~40-50% of the advertised maximum. Nobody benchmarks the compound effect — they benchmark each optimization in isolation and assume linear composition. They don't compose linearly.

<h4 id="quantization">Quantization</h4>

<h5 id="perplexity">Perplexity</h5>
How "surprised" a model is by the next token. Lower = more confident and accurate. Defined as `perplexity = 2^(cross-entropy)`. When papers report "0.1 increase in loss from quantization," that sounds small, but exponentiated over thousands of tokens across a long conversation, it means materially more wrong-token choices.

<h5 id="q4-quantization-and-attention-precision">Q4 Quantization and Attention Precision</h5>
Weights stored with ~1-1.5 digits of effective precision (vs ~3-4 for FP16). Attention scores are computed from Q, K matrices derived from these weights. At short context, the gap between relevant and irrelevant attention scores is huge — small rounding doesn't flip rankings. At long context, scores are already small and close together. Q4 rounding introduces noise on the *same scale as the signal difference*. The model literally cannot distinguish between the token it should attend to and 50 nearby irrelevant tokens.

<h5 id="systematic-flattening">Systematic Flattening</h5>
Quantization doesn't add random noise — it *systematically reduces the dynamic range* of attention scores. Peaks get lower, valleys get higher. The model's ability to say "THIS token matters, those don't" gets weaker with every turn added to context. This is directional, not stochastic — it consistently degrades retrieval.

---

<h2 id="2-natural-language-processing">2. Natural Language Processing</h2>

<p class="chapter-desc"><em>natural language processing, tokenization, and language models</em></p>

<nav class="chapter-toc">
<ul>
  <li><a href="#21-evaluation"><strong>2.1. evaluation</strong></a>
    <span> &mdash; LLM evaluation methods, recall patterns, and behavioral failure modes</span>
    <ul>
      <li><a href="#methods-frameworks">Methods & Frameworks</a></li>
      <li><a href="#behavioral-patterns">Behavioral Patterns</a></li>
    </ul>
  </li>
</ul>
</nav>

---

<h3 id="21-evaluation">2.1. evaluation</h3>
<p class="section-desc"><em>LLM evaluation methods, recall patterns, and behavioral failure modes</em></p>

<h4 id="methods-frameworks">Methods & Frameworks</h4>

<h5 id="needle-in-a-haystack-niah">Needle in a Haystack (NIAH)</h5>
Kamradt, 2023. Standard test: bury a single random sentence in filler text, check retrieval at varying depths. Most models fail retrieval when the needle is in the 40-60% depth range of context. Probe design for long-context evaluation improves on NIAH: (a) multiple needles that relate to each other, (b) haystack is actual conversation not filler, (c) probes test reasoning over facts, not just verbatim retrieval.

<h5 id="scripted-dialogue-evaluation">Scripted Dialogue Evaluation</h5>
Deriu et al., 2021. Deterministic test scripts are "conversation unit tests." The key advantage over live testing: you can re-run the exact same conversation after changing strategies (stuffing → sliding window → RAG) and get apples-to-apples comparison. Without deterministic scripts, you're benchmarking conversation content, not context strategy.

<h5 id="probe-design">Probe Design</h5>
Probes are injected at fixed intervals (every ~10 turns) testing recall of specific facts. Probe types:
- **Direct recall**: "How many games was Kemp's streak?" — tests verbatim retrieval
- **Cross-topic recall**: after switching topics, circle back — tests whether topic context helps or hurts retrieval
- **Contradiction resistance**: user states incorrect "correction" — tests whether model holds ground or caves (sycophancy)
- **Comprehensive recall**: "list all the facts we discussed" — tests breadth of memory

<h5 id="scoring-categories">Scoring Categories</h5>
- **Pass**: correct recall of key details
- **Hedge**: partially right or explicitly uncertain ("I believe...")
- **Fail**: wrong answer or omission
- **Confabulate**: confidently wrong — model generates plausible but incorrect details

Hedging is actually a better failure mode than confabulation — a model that knows it doesn't know is more useful than one that makes things up.

<h5 id="ground-truth-control">Ground Truth Control</h5>
Using one real fact mixed with fabricated ones. If the model recalls real facts more reliably, training data leakage is inflating results. This distinguishes context recall from parametric knowledge.

<h5 id="run-until-failure-vs-fixed-turn-count">Run-Until-Failure vs Fixed Turn Count</h5>
Run each path until the model fails 3 consecutive probes rather than a fixed turn count. This gives the natural breaking point per path instead of an arbitrary cutoff. More informative for establishing the degradation curve.

<h4 id="behavioral-patterns">Behavioral Patterns</h4>

<h5 id="sycophancy-at-long-context">Sycophancy at Long Context</h5>
Perez et al., 2022 (Anthropic). Models tend to agree with the user even when the user is wrong. This gets *worse* at longer contexts because:
- Model's confidence in its own earlier statements decays (attention scores to its own past outputs weaken)
- Recent user pressure stays strong (recency bias in attention)
- The model "forgets" that it's right and defaults to agreeing with the closest strong signal

Gaslighting probes ("actually you said X" when the model said Y) directly test this. The turn at which the model stops pushing back is a direct measure of effective context for self-consistency.

<h5 id="schema-consistent-vs-schema-inconsistent-retrieval">Schema-Consistent vs Schema-Inconsistent Retrieval</h5>
Facts that fit a narrative schema (e.g., a playoff arc: trade → coaching drama → rookie breakout → conference semis) are easier to recall because the schema acts as a retrieval cue. The model can reconstruct from the narrative even if exact attention is weak.

Independent facts (e.g., "Thunder average age 23.1") have no schema support — they're pure episodic recall from context.

Critical distinction: reconstruction (schema-based) is where **confabulation hides**. The model reconstructs a plausible-sounding answer from the schema but gets specific details wrong. This is why probes need to test exact numbers, not just topic recall.

The stress test should measure schema-consistent and independent facts separately to understand which type of recall degrades first.

---
