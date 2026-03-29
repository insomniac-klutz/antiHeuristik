"""Model cards — metadata for all evaluation targets.

Each card captures the model's architecture, quantization, context limits,
and the experimental dimension it isolates. This serves as the experiment
manifest — anyone reading result JSONs can trace back to exact model specs.

VRAM headroom is computed from GPU_VRAM_GB in .env via config.py.
"""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, computed_field

# allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from config import settings


class AttentionType(str, Enum):
    GQA = "grouped_query_attention"
    SLIDING_WINDOW_GLOBAL = "sliding_window_interleaved_global"
    FULL = "full_attention"


class TrainingFocus(str, Enum):
    GENERAL_INSTRUCT = "general_instruct"
    REASONING = "reasoning"


class ModelCard(BaseModel):
    """Immutable metadata for one evaluation target."""

    id: str
    name: str
    family: str
    params_b: float
    quant: str
    size_gb: float
    context_window: int
    context_native: int
    context_method: str  # "native" | "yarn" | etc.
    attention_type: AttentionType
    attention_details: str
    training_focus: TrainingFocus
    training_details: str
    kv_cache_notes: str
    lmstudio_model_path: str = Field(
        description="Model identifier for LMStudio load API (publisher/repo/filename)"
    )
    litellm_model_string: str
    eval_dimensions: list[str] = Field(
        description="What this model uniquely tests in the experiment"
    )
    risks: list[str] = Field(
        default_factory=list,
        description="Known risks or caveats for this model in our eval",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def vram_headroom_gb(self) -> float:
        """Estimated VRAM after weights only (excludes KV cache). Use get_vram() for actual."""
        return round(settings.gpu_vram_gb - self.size_gb, 2)


# ── Model definitions ──────────────────────────────────────────

QWEN_35_9B = ModelCard(
    id="qwen3.5-9b-q4",
    name="Qwen 3.5 9B Instruct",
    family="qwen",
    params_b=9.0,
    quant="Q4_K_M",
    size_gb=6.55,
    context_window=65536,
    context_native=262144,
    context_method="native",
    attention_type=AttentionType.GQA,
    attention_details=(
        "Grouped Query Attention — shares K/V projections across groups of "
        "query heads. Full attention at every layer. All tokens attend to all "
        "other tokens at every layer, but with shared KV heads reducing cache size."
    ),
    training_focus=TrainingFocus.GENERAL_INSTRUCT,
    training_details=(
        "Alibaba Qwen team. General-purpose instruction tuning. "
        "Matches GPT-class on GPQA Diamond (81.7), MMMU-Pro (70.1). "
        "IFBench 76.5. Released Feb-Mar 2026."
    ),
    kv_cache_notes=(
        "GQA reduces KV cache size vs MHA but every layer still computes "
        "global attention. At Q4, KV vectors are derived from quantized weights — "
        "errors accumulate as cache grows. Dynamic range of attention scores "
        "systematically flattened by quantization."
    ),
    lmstudio_model_path="qwen/qwen3.5-9b",
    litellm_model_string="openai/qwen/qwen3.5-9b",
    eval_dimensions=[
        "high_capacity_low_precision_baseline",
        "gqa_full_attention_architecture",
        "capacity_vs_precision_anchor",
    ],
    risks=[
        "Q4 quantization compounds with long context — effective window may be 40-50% of advertised",
        "Known to be relatively agreeable — may defer to fabricated facts easily (weak guardrails test)",
    ],
)

GEMMA_3_4B = ModelCard(
    id="gemma3-4b-q8",
    name="Gemma 3 4B Instruct",
    family="gemma",
    params_b=4.0,
    quant="Q8_0",
    size_gb=4.98,
    context_window=65536,
    context_native=131072,
    context_method="native",
    attention_type=AttentionType.SLIDING_WINDOW_GLOBAL,
    attention_details=(
        "Sliding window (1024 tokens) interleaved with global attention at a "
        "5:1 ratio — 5 local layers per 1 global layer. Only global layers "
        "attend to the full context; local layers see only the nearest 1024 tokens. "
        "RoPE base frequency 1M (vs 10K in Gemma 2). KV cache overhead drops "
        "from ~60% (global-only) to <15%."
    ),
    training_focus=TrainingFocus.GENERAL_INSTRUCT,
    training_details=(
        "Google DeepMind. Multimodal (text + image). 128K context via RoPE "
        "rescaling. Trained on 4T tokens. Beats Gemma 2 27B across benchmarks "
        "despite being 7x smaller. Released March 2025."
    ),
    kv_cache_notes=(
        "5:1 local-to-global ratio dramatically reduces KV cache pressure. "
        "Only 1/6 of layers maintain full-context KV entries. At Q8, attention "
        "scores retain ~3x the effective precision of Q4 — peaks stay sharper "
        "for longer, reducing lost-in-the-middle effect."
    ),
    lmstudio_model_path="gemma-3-4b-it",
    litellm_model_string="openai/gemma-3-4b-it",
    eval_dimensions=[
        "sliding_window_vs_full_attention",
        "low_capacity_high_precision",
        "capacity_vs_precision_test",
        "google_training_pipeline",
    ],
    risks=[
        "4B params = less representational capacity. Recall failures could be capacity, not attention.",
        "5:1 ratio means distant facts only visible to 1/6 of layers — predicts faster early-fact degradation.",
        "60-80 tok/s at Q4 on RTX 3060; Q8 may be slightly slower.",
    ],
)

PHI4_MINI_INSTRUCT = ModelCard(
    id="phi4-mini-instruct-q8",
    name="Phi-4 Mini Instruct",
    family="phi",
    params_b=3.8,
    quant="Q8_0",
    size_gb=4.08,
    context_window=65536,
    context_native=131072,
    context_method="native",
    attention_type=AttentionType.FULL,
    attention_details=(
        "Full attention at every layer. Phi-4 architecture — distinct from "
        "both Qwen's GQA and Gemma's sliding window. Smallest model in the "
        "lineup but at highest effective precision."
    ),
    training_focus=TrainingFocus.GENERAL_INSTRUCT,
    training_details=(
        "Microsoft Research. General-purpose instruction tuning. Built on "
        "synthetic, high-quality training data. Comparable to Llama 3.1 8B "
        "on benchmarks despite being half the size. Released 2025."
    ),
    kv_cache_notes=(
        "Full attention means KV cache grows linearly with context at every "
        "layer — no sliding window savings. But at 3.8B params the per-layer "
        "cache is smaller than Qwen's 9B. Q8 precision keeps attention scores "
        "clean."
    ),
    lmstudio_model_path="phi-4-mini-instruct",
    litellm_model_string="openai/phi-4-mini-instruct",
    eval_dimensions=[
        "microsoft_architecture_baseline",
        "general_instruct_control_for_reasoning_ablation",
        "low_capacity_high_precision",
        "full_attention_small_model",
    ],
    risks=[
        "3.8B is the smallest in the lineup — may underperform on sheer capacity.",
        "General-instruct training may lack strong RLHF guardrails — parametric override behavior unknown.",
    ],
)

PHI4_MINI_REASONING = ModelCard(
    id="phi4-mini-reasoning-q8",
    name="Phi-4 Mini Reasoning",
    family="phi",
    params_b=3.8,
    quant="Q8_0",
    size_gb=4.08,
    context_window=65536,
    context_native=131072,
    context_method="native",
    attention_type=AttentionType.FULL,
    attention_details=(
        "Identical architecture to Phi-4 Mini Instruct. Full attention at "
        "every layer. Same weights at init, different fine-tuning."
    ),
    training_focus=TrainingFocus.REASONING,
    training_details=(
        "Microsoft Research. Fine-tuned on synthetic, reasoning-dense data "
        "for advanced math reasoning. Chain-of-thought trained. Ideal for "
        "multi-step logic-intensive problem-solving. Same base as Phi-4 Mini "
        "Instruct but with reasoning-specific post-training."
    ),
    kv_cache_notes=(
        "Same KV cache profile as Phi-4 Mini Instruct, but CoT reasoning "
        "chains generate extra tokens per response that consume context budget. "
        "A 500-token reasoning chain per turn adds ~25K tokens across 50 turns — "
        "significant context pressure despite 128K window."
    ),
    lmstudio_model_path="microsoft/phi-4-mini-reasoning",
    litellm_model_string="openai/microsoft/phi-4-mini-reasoning",
    eval_dimensions=[
        "reasoning_vs_general_tuning_ablation",
        "cot_context_consumption",
        "reasoning_training_effect_on_conversational_recall",
        "domain_specificity_test",
    ],
    risks=[
        "Math-reasoning specialist — may be weaker at conversational NBA recall (domain mismatch).",
        "CoT tokens consume context — 128K may get tighter than expected on HIGH path.",
        "Reasoning chains may reveal conflict resolution process (upside) but add noise to latency measurements.",
    ],
)


# ── Lookup and iteration ───────────────────────────────────────

ALL_MODELS: dict[str, ModelCard] = {
    m.id: m
    for m in [QWEN_35_9B, GEMMA_3_4B, PHI4_MINI_INSTRUCT, PHI4_MINI_REASONING]
}

# Ordered pairs for controlled comparisons
COMPARISONS = {
    "capacity_vs_precision": (QWEN_35_9B, GEMMA_3_4B),
    "sliding_window_vs_full_gqa": (GEMMA_3_4B, QWEN_35_9B),
    "reasoning_vs_instruct_ablation": (PHI4_MINI_REASONING, PHI4_MINI_INSTRUCT),
    "google_vs_microsoft_small": (GEMMA_3_4B, PHI4_MINI_INSTRUCT),
    "high_cap_low_prec_vs_low_cap_high_prec": (QWEN_35_9B, PHI4_MINI_INSTRUCT),
}
