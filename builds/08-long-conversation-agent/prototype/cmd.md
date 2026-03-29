# Commands

Run from `builds/08-long-conversation-agent/`.

## Smoke test — two models, LOW only
```bash
uv run python -m prototype.orchestrator --models qwen3.5-9b-q4 gemma3-4b-q8 --paths low
```

## Smoke test — all models, LOW only
```bash
uv run python -m prototype.orchestrator --paths low
```

## Single model, single path
```bash
uv run python -m prototype.orchestrator --models phi4-mini-instruct-q8 --paths low
```

## Full pipeline — all 4 models x 3 paths (12 runs)
```bash
uv run python -m prototype.orchestrator
```

## Custom output dir
```bash
uv run python -m prototype.orchestrator --output-dir ./results-v2
```

## Pre-flight check only (list downloaded models)
```bash
uv run python -c "
import sys; sys.path.insert(0,'../..'); sys.path.insert(0,'.')
from clients import LMStudioManager
from prototype.model_cards import ALL_MODELS
mgr = LMStudioManager()
avail = mgr.check_available([c.lmstudio_model_path for c in ALL_MODELS.values()])
for mid, card in ALL_MODELS.items():
    s = 'FOUND' if avail[card.lmstudio_model_path] else 'MISSING'
    print(f'  [{s:7s}] {card.name:30s} -> {card.lmstudio_model_path}')
"
```

## Model IDs 

| ID | Model |
|---|---|
| `qwen3.5-9b-q4` | Qwen 3.5 9B Q4_K_M |
| `gemma3-4b-q8` | Gemma 3 4B Q8_0 |
| `phi4-mini-instruct-q8` | Phi-4 Mini Instruct Q8_0 |
| `phi4-mini-reasoning-q8` | Phi-4 Mini Reasoning Q8_0 |

`See model_cards.py for more info`
