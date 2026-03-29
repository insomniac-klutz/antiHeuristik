"""Async conversation runner — executes a scripted path against the LLM.

Sends each user turn sequentially, accumulates conversation history,
captures the model's response with timing metadata. Saves incrementally
after each turn so a crash still yields usable partial data.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field
from tqdm import tqdm

# allow imports from repo root for shared clients
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from clients import LLMClient, Message, Role, ContextOverflowError

from .paths import PATHS, SYSTEM_PROMPT, ScriptedTurn


class TurnResult(BaseModel):
    turn_number: int
    user_content: str
    assistant_content: str
    is_probe: bool = False
    probe_type: str | None = None
    tests_facts: list[str] = Field(default_factory=list)
    seeds_facts: list[str] = Field(default_factory=list)
    latency_seconds: float = 0.0
    timestamp: str = ""


class RunResult(BaseModel):
    path_name: str
    model: str
    system_prompt: str
    started_at: str
    finished_at: str = ""
    turns: list[TurnResult] = Field(default_factory=list)
    total_duration_seconds: float = 0.0
    completed: bool = False


def _save(result: RunResult, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")


async def run_path(
    path_name: str,
    client: LLMClient,
    output_dir: Path,
) -> RunResult:
    """Run a scripted conversation path and capture all results."""

    turns: list[ScriptedTurn] = PATHS[path_name]
    out_path = output_dir / f"{path_name}.json"

    result = RunResult(
        path_name=path_name,
        model=client.model,
        system_prompt=SYSTEM_PROMPT,
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    # conversation history accumulates across turns
    history: list[Message] = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

    run_start = time.monotonic()
    probe_count = sum(1 for t in turns if t.is_probe)

    pbar = tqdm(
        turns,
        desc=f"{path_name.upper()}",
        unit="turn",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        leave=True,
    )

    for i, turn in enumerate(pbar):
        # update bar description with turn info
        probe_tag = f" PROBE:{turn.probe_type.value}" if turn.is_probe else ""
        pbar.set_postfix_str(f"t{i+1}{probe_tag}", refresh=False)

        # append user turn to history
        history.append(Message(role=Role.USER, content=turn.content))

        # call the model
        t0 = time.monotonic()
        try:
            response = await client.complete(history)
        except ContextOverflowError as e:
            pbar.close()
            print(f"\n  CONTEXT OVERFLOW at turn {i+1}: {e}")
            result.finished_at = datetime.now(timezone.utc).isoformat()
            result.total_duration_seconds = round(time.monotonic() - run_start, 3)
            _save(result, out_path)
            raise
        latency = time.monotonic() - t0

        # append assistant response to history
        history.append(Message(role=Role.ASSISTANT, content=response.content))

        turn_result = TurnResult(
            turn_number=i + 1,
            user_content=turn.content,
            assistant_content=response.content,
            is_probe=turn.is_probe,
            probe_type=turn.probe_type.value if turn.probe_type else None,
            tests_facts=turn.tests_facts,
            seeds_facts=turn.seeds_facts,
            latency_seconds=round(latency, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        result.turns.append(turn_result)

        # incremental save after every turn
        _save(result, out_path)

        # update bar with latency
        pbar.set_postfix_str(f"t{i+1}{probe_tag} {latency:.1f}s", refresh=True)

    pbar.close()

    result.finished_at = datetime.now(timezone.utc).isoformat()
    result.total_duration_seconds = round(time.monotonic() - run_start, 3)
    result.completed = True
    _save(result, out_path)

    return result
