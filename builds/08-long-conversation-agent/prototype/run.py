"""CLI entrypoint — run a conversation path against the LLM.

Usage:
    python -m prototype.run low
    python -m prototype.run medium
    python -m prototype.run high
    python -m prototype.run all

Options:
    --model        LiteLLM model string   (default: openai/qwen3.5)
    --base-url     LLM endpoint           (default: http://127.0.0.1:1234/v1)
    --max-tokens   Max response tokens     (default: 1024)
    --output-dir   Where to save results   (default: ./results)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# allow imports from repo root for shared clients
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from clients import LLMClient

from .paths import PATHS
from .runner import run_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run conversation stress test paths")
    p.add_argument(
        "path",
        choices=[*PATHS.keys(), "all"],
        help="Which path to run (low, medium, high, all)",
    )
    p.add_argument("--model", default="openai/qwen3.5")
    p.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    p.add_argument("--max-tokens", type=int, default=1024)
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
    )
    return p.parse_args()


async def main() -> None:
    args = parse_args()

    client = LLMClient(
        model=args.model,
        base_url=args.base_url,
        max_tokens=args.max_tokens,
    )

    paths_to_run = list(PATHS.keys()) if args.path == "all" else [args.path]

    for name in paths_to_run:
        turn_count = len(PATHS[name])
        print(f"\n{'='*50}")
        print(f"  PATH: {name.upper()}  ({turn_count} turns)")
        print(f"  model: {args.model}")
        print(f"{'='*50}\n")

        result = await run_path(name, client, args.output_dir)

        probe_count = sum(1 for t in result.turns if t.is_probe)
        avg_latency = (
            sum(t.latency_seconds for t in result.turns) / len(result.turns)
            if result.turns
            else 0
        )

        print(f"\n  done — {len(result.turns)} turns, {probe_count} probes")
        print(f"  avg latency: {avg_latency:.1f}s")
        print(f"  total time:  {result.total_duration_seconds:.1f}s")
        print(f"  saved to:    {args.output_dir / f'{name}.json'}")


if __name__ == "__main__":
    asyncio.run(main())
