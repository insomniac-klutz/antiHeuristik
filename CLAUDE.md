# CLAUDE.md

## Commit Format

`action : description` — all lowercase, space-colon-space separator.

Examples: `add : project scaffold`, `fix : missing pause gate`, `refactor : test-run tier resolution`

## Musings Log Format

Each build has `musings.md` — append-only decision log. User = **architect** (drives). Claude = **critic** (pressure-tests).

### Entry structure (built turn by turn)

1. **Architect opens**: `## YYYY-MM-DD — title` + `**phase**: discovery|design|prototype|integrate|harden|retro` + `> architect: proposal`
2. **Critic responds**: `> critic: pushback or validation`
3. **Verdict lands**: `**verdict**: what was settled` + `**gaps**: knowledge gaps to address` + `**next**: forward motion`

Multiple architect/critic rounds may happen before verdict.

### Rules

- One entry per meaningful decision, not every conversation
- Append only; build incrementally — don't write ahead
- Summary decisions, except critical technical discussions → log verbatim
- Architect always has last word

## Environment

This is a **uv** project with a uv-managed venv. Use `uv pip install`, `uv run`, etc. — not bare `pip`.

## Shared Clients

Reusable clients live in `clients/`. Check there first before reimplementing; add new client types there for reuse.

## Progress Logging

All long-running operations (loops, pipelines, batch jobs) must use **tqdm** progress bars. No bare `print` progress — tqdm is the standard. Add `tqdm` to requirements if not present.

## Build Workflow

- **No code until architect says "build."** During discovery/design: critique, question, iterate.
- On "build": log decision in musings first, then build. Pushback if something's wrong.
- **Every critic turn** includes a theory tip — practical concept/paper/principle tied to the discussion. No exceptions: a short user message ("yes", "yep", "do it") does not mean skip deliberation. If the user's input changes a design decision — even by one parameter — that's a critic turn with a theory tip. Only pure mechanical execution (renaming a variable, fixing a typo) skips the critic.
- On "build": collect all theory tips into `theory/` directory, grouped by topic (e.g., `theory/context-windows.md`). Append to existing docs before creating new ones.
- **Do not conflate brevity with "skip protocol."** Short messages often carry the highest-signal decisions. Treat the protocol as load-bearing, not optional.

## Daily Journal

`meta/journeys.md` — append-only daily log. **Only update when the user explicitly asks** (e.g. "end of day", "update journal", "log the day"). Not automatic, not mid-session. One entry per day, covering what was worked on across all builds and repo-level changes. Infer context from recent git commits (`git log`) to fill in days the user didn't explicitly journal — don't fabricate, just read the commit history.
