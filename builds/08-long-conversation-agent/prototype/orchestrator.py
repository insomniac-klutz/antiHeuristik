"""Orchestrator — runs all models x paths as a single automated pipeline.

Enforces the single-model invariant: only one model loaded at a time.
Flow per model: unload all → load → run paths → unload → next.

Usage:
    python -m prototype.orchestrator
    python -m prototype.orchestrator --paths low medium
    python -m prototype.orchestrator --models qwen3.5-9b-q4 gemma3-4b-q8
    python -m prototype.orchestrator --paths low  # smoke test all models on LOW
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from clients import LLMClient, LMStudioManager, get_vram

from .model_cards import ALL_MODELS, ModelCard
from .paths import PATHS
from .runner import run_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run full evaluation pipeline")
    p.add_argument(
        "--models",
        nargs="*",
        default=list(ALL_MODELS.keys()),
        choices=list(ALL_MODELS.keys()),
        help="Model IDs to evaluate (default: all)",
    )
    p.add_argument(
        "--paths",
        nargs="*",
        default=list(PATHS.keys()),
        choices=list(PATHS.keys()),
        help="Paths to run per model (default: all)",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
    )
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument(
        "--settle-time",
        type=float,
        default=5.0,
        help="Seconds to wait after unload for VRAM to clear",
    )
    return p.parse_args()


def print_banner(text: str, width: int = 60) -> None:
    print(f"\n{'=' * width}")
    print(f"  {text}")
    print(f"{'=' * width}\n")


async def run_model(
    card: ModelCard,
    paths_to_run: list[str],
    manager: LMStudioManager,
    output_dir: Path,
    max_tokens: int,
    settle_time: float,
) -> dict[str, bool]:
    """Load a model, run all paths, unload. Returns {path: success}."""

    results: dict[str, bool] = {}
    model_output = output_dir / card.id

    # ── enforce single-model invariant ─────────────────────
    print(f"  unloading all models...")
    unloaded = manager.unload_all()
    if unloaded:
        print(f"  unloaded {unloaded} model(s), waiting {settle_time}s for VRAM to clear")
        time.sleep(settle_time)

    # ── load target model ──────────────────────────────────
    print(f"  loading {card.name} ({card.lmstudio_model_path})...")
    try:
        manager.load(
            model=card.lmstudio_model_path,
            context_length=card.context_window,
        )
    except Exception as e:
        print(f"  FAILED to load {card.name}: {e}")
        return {p: False for p in paths_to_run}

    # ── verify invariant ───────────────────────────────────
    loaded_ids = manager.list_loaded_instance_ids()
    if len(loaded_ids) != 1:
        print(f"  WARNING: expected 1 model loaded, found {len(loaded_ids)}: {loaded_ids}")
    else:
        print(f"  loaded: {loaded_ids[0]}")

    vram = get_vram()
    if vram:
        print(f"  VRAM free: {vram.free_gb}GB (weights + KV cache using {vram.used_gb}GB) {vram.bar()}")
    else:
        print(f"  VRAM free: unknown (nvidia-smi unavailable)")

    # ── create client for this model ───────────────────────
    client = LLMClient(
        model=card.litellm_model_string,
        max_tokens=max_tokens,
    )

    # ── run each path ──────────────────────────────────────
    for path_name in paths_to_run:
        turn_count = len(PATHS[path_name])
        print_banner(f"{card.name} :: {path_name.upper()} ({turn_count} turns)")

        try:
            result = await run_path(path_name, client, model_output)
            probe_count = sum(1 for t in result.turns if t.is_probe)
            avg_latency = (
                sum(t.latency_seconds for t in result.turns) / len(result.turns)
                if result.turns
                else 0
            )
            print(f"\n  completed — {len(result.turns)} turns, {probe_count} probes")
            print(f"  avg latency: {avg_latency:.1f}s | total: {result.total_duration_seconds:.1f}s")
            print(f"  saved: {model_output / f'{path_name}.json'}")
            results[path_name] = True
        except Exception as e:
            print(f"\n  FAILED on {path_name}: {e}")
            results[path_name] = False

    # ── unload after all paths ─────────────────────────────
    print(f"\n  unloading {card.name}...")
    try:
        manager.unload_all()
    except Exception as e:
        print(f"  WARNING: unload failed: {e}")

    return results


async def main() -> None:
    args = parse_args()
    manager = LMStudioManager()

    total_runs = len(args.models) * len(args.paths)
    print_banner(
        f"ORCHESTRATOR — {len(args.models)} models x {len(args.paths)} paths = {total_runs} runs"
    )

    # verify LMStudio is reachable
    try:
        manager.list_loaded_instance_ids()
        print("  LMStudio API: reachable")
    except Exception as e:
        print(f"  ERROR: cannot reach LMStudio API: {e}")
        print("  Make sure LMStudio is running with the server enabled.")
        return

    vram = get_vram()
    if vram:
        print(f"  GPU VRAM: {vram.bar()}")
    else:
        print("  GPU VRAM: unavailable (nvidia-smi not found)")

    # ── pre-flight: check all models are downloaded ────────
    cards = [ALL_MODELS[m] for m in args.models]
    model_paths = [c.lmstudio_model_path for c in cards]

    print("\n  checking downloaded models...")
    try:
        availability = manager.check_available(model_paths)
    except Exception as e:
        print(f"  WARNING: could not verify downloads ({e}), proceeding anyway...")
        availability = {p: True for p in model_paths}

    missing = [path for path, available in availability.items() if not available]
    if missing:
        print("\n  MISSING MODELS — download these in LMStudio before running:\n")
        for path in missing:
            card = next(c for c in cards if c.lmstudio_model_path == path)
            print(f"    - {card.name}")
            print(f"      search: {path}")
            print(f"      quant:  {card.quant}  size: {card.size_gb}GB\n")
        print("  Open LMStudio → Search → download each model above.")
        print("  Then re-run this command.\n")
        return

    found_count = sum(1 for v in availability.values() if v)
    print(f"  all {found_count} models available\n")

    pipeline_start = time.monotonic()
    summary: dict[str, dict[str, bool]] = {}

    for model_id in args.models:
        card = ALL_MODELS[model_id]
        print_banner(f"MODEL: {card.name} ({card.params_b}B {card.quant} @ {card.size_gb}GB)")

        model_results = await run_model(
            card=card,
            paths_to_run=args.paths,
            manager=manager,
            output_dir=args.output_dir,
            max_tokens=args.max_tokens,
            settle_time=args.settle_time,
        )
        summary[model_id] = model_results

    pipeline_duration = time.monotonic() - pipeline_start

    # ── final summary ──────────────────────────────────────
    print_banner("PIPELINE COMPLETE")
    print(f"  total time: {pipeline_duration / 60:.1f} minutes\n")

    for model_id, path_results in summary.items():
        card = ALL_MODELS[model_id]
        status_line = "  ".join(
            f"{p}: {'ok' if ok else 'FAIL'}" for p, ok in path_results.items()
        )
        print(f"  {card.name:30s}  {status_line}")

    # count failures
    total_failures = sum(
        1 for pr in summary.values() for ok in pr.values() if not ok
    )
    if total_failures:
        print(f"\n  {total_failures}/{total_runs} runs failed.")
    else:
        print(f"\n  all {total_runs} runs succeeded.")


if __name__ == "__main__":
    asyncio.run(main())
