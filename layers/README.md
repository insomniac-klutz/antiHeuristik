# Layers

Layers are not builds. They're what you apply **to** every build, in order, after the MVP works.

```
BRIEF → WHITEBOARD → MVP → [EVAL] → [COST-KILL] → [FEEDBACK] → [CATASTROPHE] → DEBRIEF
```

Each layer deepens the build. A build without layers is a demo. A build with all four is a production system you can whiteboard from any angle.

## The Order Matters

1. **Eval** — you can't improve what you can't measure. Always first after MVP.
2. **Cost Killer** — optimize against the baseline your eval established.
3. **Feedback Flywheel** — now that it's measured and optimized, make it learn.
4. **Catastrophe** — now break everything and prove you can fix it.

## Per-Build Layer Structure

Each core build gets a `layers/` directory:

```
builds/01-patent-search/
├── brief.md
├── attempt_01.md
├── walls.md
├── prototype/
├── theory/
├── layers/
│   ├── eval/
│   │   ├── attempt.md      # How you approached eval for THIS build
│   │   ├── walls.md         # What you didn't know about eval in this context
│   │   └── prototype/       # Eval code/scripts
│   ├── cost-killer/
│   │   ├── attempt.md
│   │   ├── walls.md
│   │   └── prototype/
│   ├── feedback/
│   │   ├── attempt.md
│   │   ├── walls.md
│   │   └── prototype/
│   └── catastrophe/
│       ├── attempt.md
│       ├── walls.md
│       └── incidents/       # Post-mortems for each injected failure
└── debrief.md               # Written AFTER all layers, not after MVP
```

## Why This Works

Same eval layer, applied to a RAG system vs an agent vs a voice pipeline, forces completely different thinking. The layer is the constant. The build is the variable. You learn eval deeply because you apply it 6 different ways.
