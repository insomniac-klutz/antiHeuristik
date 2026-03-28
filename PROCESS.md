# The antiHeuristic Process

Theory through application. Not the other way around.

---

## The Loop

Every unit of learning is a **Build** — a system you design, prototype, and then deepen through **Layers**.

```
┌─────────────────────────────────────────────────┐
│  MVP PHASE                                      │
│                                                 │
│  1. READ the brief                     (5 min)  │
│  2. WHITEBOARD — diagram, flow        (30 min)  │ → attempt_01.md
│  3. PROTOTYPE — scrappy, working     (2-3 hrs)  │ → prototype/
│  4. HIT WALLS — log unknowns                    │ → walls.md
│  5. LEARN — only what blocked you  (30m - 1hr)  │ → theory/
│  6. REATTEMPT — redo whiteboard       (20 min)  │ → attempt_02.md
│                                                 │
├─────────────────────────────────────────────────┤
│  LAYERS (apply in order, each has its own       │
│  attempt.md + walls.md + prototype/)            │
│                                                 │
│  L1. EVAL — measure quality baseline            │ → layers/eval/
│  L2. COST-KILL — cut cost 70%, hold quality     │ → layers/cost-killer/
│  L3. FEEDBACK — make it learn over time         │ → layers/feedback/
│  L4. CATASTROPHE — break it, debug it, harden   │ → layers/catastrophe/
│                                                 │
├─────────────────────────────────────────────────┤
│  7. DEBRIEF — full system narrative    (10 min) │ → debrief.md
│     (written AFTER all layers, not after MVP)   │
└─────────────────────────────────────────────────┘
```

Each layer follows the same micro-loop: attempt → wall → learn → reattempt. The layers compound — eval informs cost-killing, cost-killing constrains feedback design, catastrophe stress-tests everything.

See `layers/README.md` for layer definitions and `layers/01-04` for full briefs.

## Rules

1. **No schedule.** Pick the Build that scares you most. When it's done, pick again.
2. **Theory lives inside Builds.** You don't study reranking. You build a search system that needs reranking, and you learn it when you can't make it work.
3. **walls.md is the most important file.** It's the raw record of what you didn't know. This becomes your real study list — the gaps theory never showed you.
4. **Grind is seeded, not scheduled.** grind/ has every topic from the original plan organized by domain. Use it two ways: (a) when a Build hits a wall, find the topic and drill it, (b) when you need a new Build idea, scan for uncovered topic clusters. Mark topics as you cover them.
5. **Stories happen in dead time.** Walk, commute, shower. Not at a desk.
6. **No completion theater.** A Build is done when you can explain every decision and its tradeoff from memory. Not when you've filled in all the files.

## Three Tiers

### Tier 1: Builds + Layers
The spine. 12 core builds × 4 layers = 48 depth exercises from 12 systems. See `builds/` for challenges, `layers/` for layer definitions.

### Tier 2: Stories
Verbal reps. Your project narratives, paper summaries, ambiguity exercises. See `stories/`.

### Tier 3: Grind
Topic seed bank organized by domain. Use it two ways: find what blocked you during a build, or scan for uncovered clusters to design new builds. See `grind/`.

## Picking Order

Don't go 01 → 02 → 03. Go by fear.

Ask: "Where's my biggest gap between 'I've read about this' and 'I've built this'?" Do that one.

## When You're Done With a Build

**After MVP** — you should be able to:
- Draw the architecture from memory in under 5 minutes
- Explain every design decision and its tradeoff

**After all layers** — you should also be able to:
- Explain how you measure quality and what the numbers are
- Walk through 3 cost optimizations and their quality tradeoff
- Describe the feedback loop and prove it improved the system
- Name 5 things that would break, how you'd detect them, how you'd fix them
- Pivot to a variation ("now make it multi-tenant" / "now do it at 100x scale")

If you can't do all of these, you're not done. Write the debrief only when you can.

## Learning Tactics

- **Record yourself on walks.** Explaining systems out loud in dead time. Speak, listen back, cut the fluff. If you can't explain it simply, you don't understand it yet.
- **3-minute cap.** Any system explanation should be under 3 minutes on first pass. If it's longer, you're hiding confusion behind words.
- **Explain like you're drawing.** Not reading notes. Walking through the flow, pointing at decisions, naming tradeoffs.
- **Lead with decisions, not definitions.** You're not explaining "what is RAG?" — you're explaining "here's why I chose this architecture, here's what I'd change at 10x scale, here's what I said no to."

## The Anti-List (Don't Waste Time Here)

| Topic | Why it's cut |
|-------|-------------|
| DSA / leetcode-style | Basic Python data structures are enough for Applied AI work. |
| OOP theory | You write OOP daily. No one needs to re-derive polymorphism in 2026. |
| OS / DBMS theory | Irrelevant for Applied AI. Know enough SQL to be dangerous. |
| Classical ML derivations | Know when to use XGBoost vs a prompt. Don't derive gradient boosting. |
| Deep Learning derivations | Know transformer architecture conceptually. Don't derive attention. |
| Probability / Stats / LinAlg | If it comes up, it'll be applied (A/B testing, embedding similarity). Not textbook. |
| Reinforcement Learning | Unless the work requires RL, skip entirely. |
| Recommendation Systems | Only if domain-specific. |
