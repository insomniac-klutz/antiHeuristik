# Theo Split Check

Scan `grind/theo/` files for any that have grown too large and propose splits.

Run this after `/anti-theo-conso` or periodically to keep the book navigable.

---

## Inputs

- `$ARGUMENTS` — optional: specific directory to check (e.g., `dl`). If empty, scan all.

---

## Steps

### Step 1 — Measure

First, check for uncommitted changes to content files — these may be from a recent `/anti-theo-conso` run that hasn't been committed yet:
```
git diff -- grind/theo/
```
Flag any files with working tree modifications so the user knows the analysis reflects uncommitted state.

Then, for each `.md` content file (not indexes or logs) in `grind/theo/`:
- Count lines
- Count H2 sections
- Count H3 sections

Flag any file that meets **any** of these thresholds:
- **> 300 lines** — getting long for a single reference doc
- **> 5 H2 sections** — may contain distinct sub-topics that deserve their own files
- **> 15 H3 sections** — high granularity suggests multiple themes compressed together

Present a report:

```
| File | Lines | H2s | H3s | Status |
|------|-------|-----|-----|--------|
| dl/attention.md | 120 | 3 | 12 | ok |
| nlp/evaluation.md | 280 | 2 | 8 | ok |
| dl/training.md | 450 | 7 | 22 | split candidate |
```

### Step 2 — Analyze Split Candidates

For each flagged file:
1. Read the file fully
2. Identify natural split boundaries — where do the H2 sections form independent, self-contained topics?
3. Propose how to split:
   - Which H2 sections go into which new file
   - Proposed new file names (keep them **broad and generic** — the same naming principles from `/anti-theo-conso` apply)
   - Whether any content would need cross-references after splitting

Present the proposal with reasoning.

**If no files are flagged**, report that everything is within bounds and stop.

### Step 3 — Confirm

**Wait for user confirmation.** Common responses:
- "split it" — proceed
- "it's fine" — leave it, the file is large but cohesive
- Adjusted split boundaries

### Step 4 — Execute Split

For each approved split:
1. Create the new file(s) with content moved verbatim from the source
2. Remove the moved sections from the original file
3. Add cross-references if the split creates related-but-separate files
4. Update the sub-dir `theo-index.md` — remove old heading tree entries, add new file entries with heading trees
5. Update the root `theo-index.md` — add new file entries

### Step 5 — Update Logs

Append a split entry to both root and sub-dir `theo-log.md`:

```markdown
## YYYY-MM-DD — split

- original-file.md → new-file-a.md (split)
  - H2 heading moved
  - H2 heading moved
- original-file.md retained:
  - H2 heading kept
  - H2 heading kept
```

### Step 6 — Rebuild & Validate Book

Run the book pipeline and validate the output:

1. **Rebuild**: `uv run python meta/anti-bk/anti-bk-writer.py`
2. **Validate**: Read `meta/anti-bk/assets/anti-bk.md` and verify:
   - Split files appear as separate sections in the book
   - No content was lost — every heading from the original file appears in one of the new files
   - TOC reflects the new file structure
   - If a new directory was created, add it to `DISPLAY_NAMES` in the writer
3. **Fix forward**: If the book is missing content or has rendering issues, fix the writer/pattern files as needed.

Report book status:
```
book: ✓ rebuilt (N chapters, N sections, N headings)
validation: ✓ all split content present | ✗ missing: [list]
```

### Step 7 — Summary

Present:
- Files created by split
- Files modified
- Sections moved
- Cross-references added (if any)
- Book rebuild status

---

## Principles

- **Splitting is cosmetic surgery, not rewriting.** Content moves verbatim. No rephrasing, no "improving."
- **Broad names.** New files from splits follow the same naming rule: generic enough to absorb future content.
- **Don't split prematurely.** A file with 4 H2s that tell one coherent story doesn't need splitting just because it's 280 lines. The thresholds are flags, not mandates — cohesion matters more than line count.
- **User decides.** Always confirm before executing.
