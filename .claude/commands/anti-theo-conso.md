# Theo Consolidate

Consolidate theory from a build's `theory/` directory into the permanent book at `grind/theo/`.

You are building an antiHeuristik-compliant theory book incrementally — each consolidation run pulls raw build theory into structured, lasting reference material.

---

## Inputs

- `$ARGUMENTS` — optional: build number or name (e.g., `08` or `08-long-conversation-agent`). If empty, proceed to Step 0.

---

## Steps

### Step 0 — Identify Target Build

If `$ARGUMENTS` is provided and resolves to a valid build directory, use it. Otherwise, list the builds that have non-empty `theory/` directories and ask the user which one to target.

```
Check: builds/*/theory/ — which ones have .md files?
```

Present the list and wait for the user to pick.

### Step 1 — Read Current State

Read these files to understand what already exists:
- `grind/theo/theo-log.md` — root-level consolidation history
- `grind/theo/theo-index.md` — the root bucket index (dirs + file titles)
- `grind/theo/theo-index-template.md` — the structural rules you must follow

Summarize to the user:
- Which builds have already been consolidated (from theo-log)
- The current bucket structure (from theo-index)

### Step 2 — Analyze Build Theory Files

**Heading-level dedup check first**:

1. Read `grind/theo/theo-log.md` (root log). For the target build's section, collect the **exact headings and subheadings** already integrated per source file, along with the integration date.
2. For each source file that has any prior integration entries, check for changes since last integration using **both** committed history and working tree state:
   ```
   git log --after="<last-integration-date>" -- builds/<target>/theory/<source-file>.md
   git diff -- builds/<target>/theory/<source-file>.md
   ```
   A file is changed if **either** check shows changes — commits after the integration date OR uncommitted working tree modifications. `git log` alone misses unstaged edits.
   - **File changed** (commits OR working tree diff) → mark as `re-examine`. All headings must be re-read — content under previously integrated headings may have been updated. Flag these to the user with `(changed since last integration)`.
   - **File unchanged** (no commits AND no working tree diff) → skip headings already in the log. Only process genuinely new headings that weren't in the log.
3. Source files with zero prior integration entries are fully new — process everything.

Then read each `.md` file in `builds/<target>/theory/` that has work to do (new files + files with new or changed headings).

**Critical: heading-level decomposition, not file-level mapping.**

Do NOT map source files 1:1 to target files. Instead:

1. Extract every individual heading (H2, H3) from all source files into a flat pool of headings
2. For each heading, identify its domain category and which existing `grind/theo/` bucket it belongs in
3. Group headings by target *sub-topic* — an overarching theme broad enough to absorb future content on the same subject
4. Map each group to either an existing file in the target bucket or propose a new file

**Target file naming rules:**
- Names must be **broad and generic** — they represent lasting sub-topics, not narrow build-specific concepts
- **Minimize the number of files per directory.** Only create a new file when headings genuinely cannot fit an existing one
- A good target file name can absorb 3-5 future builds' worth of related content (e.g., `attention.md` not `attention-score-degradation-at-long-context.md`)
- When in doubt, fewer bigger files beats many small ones

Build a mapping organized by **target file**, not by source file:
```
grind/theo/dl/attention.md (create):
  - "GQA" ← context-and-attention.md
  - "Flash Attention" ← context-and-attention.md
  - "Perplexity" ← quantization-effects.md
  - "Systematic Flattening" ← quantization-effects.md

grind/theo/nlp/evaluation.md (create):
  - "NIAH" ← recall-and-behavior.md
  - "Probe Design" ← evaluation-methods.md

[already integrated — unchanged, skipped]:
  - source-file.md § "Heading X" → grind/theo/ml/ (via 2026-03-25 run, file unchanged)

[re-examining — file changed since last integration]:
  - other-file.md § "Heading Z" → previously in grind/theo/dl/ (file modified 2026-03-27, last integrated 2026-03-25)
```

Present this mapping to the user. If a topic doesn't fit existing buckets, explain why and propose either:
- A new subdirectory (only if the topic represents a genuinely distinct domain)
- A new file in an existing directory
- Splitting content across multiple existing directories

### Step 3 — Confirm Targets

Present to the user:
- Which bucket directories you plan to write into
- Which existing files you plan to append to (if any exist)
- Which new files you plan to create
- The proposed internal H2/H3 structure for each target file — show how headings from different source files interleave into a coherent outline
- Reasoning for each choice

**Wait for user confirmation before proceeding.** If the user disagrees, adjust the plan. Common feedback to watch for:
- "too specific" — broaden target file names, merge proposed files
- "too many files" — consolidate into fewer, broader sub-topics
- Target file names should be generic enough to absorb future content on the same theme

### Step 4 — Turn-Based Integration

For each target file, do the integration **one file at a time** in conversation with the user:

**If appending to an existing file:**
1. Read the existing file fully
2. Show the user what sections you plan to add and where they fit in the existing structure
3. Explain how the new content relates to / extends what's already there
4. Wait for user approval
5. Write the update

**If creating a new file:**
1. Show the user the proposed structure (title, H2/H3 outline)
2. Justify why this needs a new file rather than fitting into an existing one
3. Wait for user approval
4. Write the file

**Content rules:**
- **Copy theory content verbatim.** Do not modify, interpret, rephrase, extend, summarize, or "improve" the source material. The theory chunks are written by the architect — transfer them exactly as they are. The only permitted changes are the structural ones listed below.
- Restructure _organization_ for book-style readability (reorder sections, split across files, adjust heading levels) — but the prose and technical content under each heading must remain untouched
- Do NOT add cross-references during consolidation — use `/anti-theo-xref` as a separate pass after consolidation
- Strip build-specific context that doesn't generalize (e.g., "Build 08's probe design" → "Probe design for long-context evaluation")
- Keep paper citations and concrete numbers — these are high-value

### Step 5 — Update Indexes

After all files are written:

**5a — Root index (`grind/theo/theo-index.md`):**
- Add entries for any new files created
- Every directory heading must have a `— one-line description` of the bucket's scope
- Every file entry must have a `— one-line description`
- Follow `theo-index-template.md` root index rules

**5b — Sub-dir index (`grind/theo/<dir>/theo-index.md`):**
- If the sub-dir index doesn't exist yet, create it following the template
- If it exists, update it with the new/modified file entries
- Every file entry (Part A) must have a `— one-line description`
- Every heading tree entry (Part B) — H2, H3, H4 — must have a `— one-line explainer`
- Include the full heading tree (Part B from template) for every file that was created or modified
- Follow `theo-index-template.md` sub-dir index rules exactly

### Step 6 — Update Theo Logs

**6a — Root log (`grind/theo/theo-log.md`):**

The root log is organized **by build, then by date**. Follow the format from `theo-index-template.md`:

1. Check if a `## build-NN-name` section already exists in the log
   - If yes: append a new `### YYYY-MM-DD` subsection under it
   - If no: create the `## build-NN-name` section, then add the `### YYYY-MM-DD` subsection
2. Under the date slot, list each source file with its target, action, and the **exact headings/subheadings from the source** that were integrated
3. Add a `> notes:` block at the end for any decisions made

```markdown
## build-NN-name

### YYYY-MM-DD

**source-file.md** → `dir/target-file.md` (created | appended)
- H2 heading integrated
  - H3 subheading integrated
  - H3 subheading integrated
- H2 heading integrated

> notes: any decisions made
```

**6b — Sub-dir logs (`grind/theo/<dir>/theo-log.md`):**

For each directory touched, append an entry mapping source → target files **with heading-level detail**. If the sub-dir theo-log doesn't exist yet, create it with a header.

```markdown
## YYYY-MM-DD — build-NN-name

- source-file.md → target-file.md (created | appended)
  - H2 heading integrated
    - H3 subheading integrated
- source-file.md → target-file.md (appended | updated)
  - H2 heading integrated
```

The root log is the primary dedup source (Step 2 checks it for heading-level history + git timestamps). Sub-dir logs serve as a secondary cross-check and directory-scoped view of what landed where.

### Step 7 — Rebuild & Validate Book

Run the book pipeline and validate the output:

1. **Rebuild**: `uv run python meta/anti-bk/anti-bk-writer.py`
2. **Validate**: Read the generated `meta/anti-bk/assets/anti-bk.md` and cross-check against the source `.md` files in `grind/theo/`:
   - Every content file's H2/H3/H4 headings must appear in the book (heading completeness)
   - No heading text should be truncated, mangled, or duplicated
   - Chapter names in the TOC must match `DISPLAY_NAMES` in the writer (if a new directory was created, add it to the map)
   - Section descriptions must match the subdir `theo-index.md` descriptions
3. **Pattern scan** (optional): `uv run python meta/anti-bk/anti-bk-pattern.py` — check if newly added content introduces markdown patterns not yet captured by the pattern registry. If new patterns are found, update `anti-bk-pattern.py`'s `PATTERNS` tuple.
4. **Fix forward**: If validation finds issues:
   - Missing content → check `IGNORE_STEMS` in the writer, check `_is_content_file` logic
   - Broken rendering → check `_bump_headings` offset, check HTML passthrough in markdown-it
   - New directory not appearing → add entry to `DISPLAY_NAMES` in the writer
   - New markdown patterns not rendered → update `PATTERNS` in `anti-bk-pattern.py`

Report the book status to the user:
```
book: ✓ rebuilt (N chapters, N sections, N headings)
validation: ✓ all source headings present | ✗ missing: [list]
patterns: ✓ all captured | ✗ new patterns found: [list]
```

### Step 8 — Summary

Present a final summary to the user:
- Files created/modified
- Sections added
- Book rebuild status
- Suggestions for follow-up (e.g., "the quantization content could also inform a future grind/theo/deploy/ entry on serving optimization")
- Recommend running `/anti-theo-xref` if content spans multiple directories
- Recommend running `/anti-theo-split` if any target file grew large

---

## Principles

- **The theo book is the lasting artifact.** Build theory is raw material; the book is refined reference. Treat it accordingly.
- **Incremental, not rewrite.** Each run adds to what exists. Never rewrite existing content unless the user explicitly asks for restructuring.
- **Book structure matters.** A reader should be able to open any theo file and understand it without having done the build. Context must be self-contained.
- **The user decides bucket boundaries.** You propose, they confirm. Never create new directories or files without asking.
- **Indexes are never optional.** Every run must leave indexes consistent with the actual file contents.
