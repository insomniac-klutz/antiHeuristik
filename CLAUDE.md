# CLAUDE.md

## Commit Format

```
action : description
```

- All lowercase
- Action is the verb: `add`, `update`, `fix`, `remove`, `refactor`, `rename`, etc.
- Then ` : ` (space-colon-space)
- Then a short description of what changed

Examples:
```
add : project scaffold and meta files
update : hld with revised component boundaries
fix : missing pause gate in sync phase 2
remove : deprecated recon fallback logic
refactor : test-run tier resolution
rename : status template to match new schema
```

## Musings Log Format

Each build has a `musings.md` — an append-only log of end-to-end build decisions.

**Roles**: the user is the **architect** (proposes, decides, drives). Claude is the **critic** (pressure-tests, pokes holes, asks hard questions).

### Entry structure

Entries are built turn by turn, not all at once.

**Turn 1 — architect opens** (appended when the user makes a proposal or decision):

```markdown
## YYYY-MM-DD — short title

**phase**: discovery | design | prototype | integrate | harden | retro

> architect: what the user said, decided, or proposed
```

**Turn 2 — critic responds** (appended in the same entry by Claude):

```markdown
> critic: pushback, hard questions, or validation
```

**Turn 3 — verdict lands** (appended once the architect makes the final call):

```markdown
**verdict**: what was settled and why

**gaps**: specific knowledge gaps or weak spots the critic noticed during this entry — things the architect should study, practice, or look into before moving forward

**next**: what to do next based on the verdict
```

An entry may go through multiple architect/critic rounds before a verdict. Each round is appended as it happens.

### Rules

- One entry per meaningful decision or direction change — not every conversation
- Append only; never edit past entries
- Build entries incrementally — don't write critic/verdict until that turn actually happens
- Entries are **summary decisions** like minutes of meeting — short, distilled, outcome-focused
- **Exception**: critical technical discussions (architecture trade-offs, failure mode analysis, non-obvious design choices) should be logged verbatim, not summarized — the detail is the value
- `phase` tracks where in the build lifecycle this happened
- `verdict` is the final call — architect always has last word
- `next` ties the entry to forward motion
