# Theo Index Template

Instructions for maintaining theo indexes. The theo-consolidate skill **must** follow these rules.

---

## Two Levels of Index

### 1. Root Index — `grind/theo/theo-index.md`

Shows what directories exist and which markdown files live in each. Nothing deeper.

```markdown
# Theo Index

## dir-name/ — one-line description of what this bucket covers
- file-one.md — one-line description
- file-two.md — one-line description

## another-dir/ — one-line description of what this bucket covers
- file-three.md — one-line description
```

Rules:
- One `##` section per subdirectory, alphabetical
- Each directory heading includes `— short description` explaining the bucket's scope
- Each file listed as `- filename.md — short description`
- No heading/subheading detail at this level — that lives in the sub-dir index
- Update this file whenever a new markdown file is created or removed in any subdirectory

### 2. Sub-Dir Index — `grind/theo/<dir>/theo-index.md`

A detailed book-style table of contents for that directory. Two parts:

**Part A — File list** (same format as root, repeated here for standalone readability):
```markdown
# <dir> — Theo Index

## Files
- file-one.md — one-line description
- file-two.md — one-line description
```

**Part B — Heading tree** (full TOC per file, every entry gets a one-liner):
```markdown
## file-one.md
- H2 heading — what this section covers
  - H3 subheading — what this subsection covers
  - H3 subheading — what this subsection covers
    - H4 sub-subheading — what this sub-subsection covers
- H2 heading — what this section covers
  - H3 subheading — what this subsection covers

## file-two.md
- H2 heading — what this section covers
  - H3 subheading — what this subsection covers
```

Rules:
- Mirror the actual heading structure of each file — do not invent headings
- Every entry gets a `— short explainer` after the heading name
- Indent to reflect heading depth (H2 = root, H3 = one indent, H4 = two indents)
- Update this file whenever content is added to or restructured in any file in the directory
- If a file is deleted, remove its entire section

---

## Theo Logs

There are two levels of theo-log. Both are append-only.

### 1. Root Log — `grind/theo/theo-log.md`

Master integration log organized **by build**, then **by date** within each build. Records the exact source headings/subheadings that were integrated and where they landed.

Two lookup paths:
- **By build**: "What did build 08 contribute to the book?" → find `## build-08` section
- **By date**: scan the `### YYYY-MM-DD` slots across builds

Structure:
```markdown
# Theo Log

## build-NN-name

### YYYY-MM-DD

**source-file.md** → `dir/target-file.md` (created | appended)
- H2 heading integrated
  - H3 subheading integrated
  - H3 subheading integrated
- H2 heading integrated

**another-source.md** → `dir/other-target.md` (appended)
- H2 heading integrated
  - H3 subheading integrated

> notes: any decisions (new bucket justification, restructuring, etc.)

### YYYY-MM-DD

(later consolidation run from the same build)
```

Rules:
- One `## build-NN-name` section per build, created on first consolidation from that build
- One `### YYYY-MM-DD` subsection per consolidation run date within that build
- List each source file with its target, action, and the **exact headings/subheadings** that were integrated (mirror the source structure, not the target structure)
- `> notes:` block at the end of a date slot for decisions made
- Append new date slots under existing build sections — never create duplicate build sections
- Never edit past entries

### 2. Sub-Dir Log — `grind/theo/<dir>/theo-log.md`

Per-directory log that tracks which source files and **which headings** have been integrated into this bucket. The root log (`theo-log.md`) is the primary dedup source — Step 2 checks it for heading-level history and uses git timestamps to detect changed files. Sub-dir logs serve as a secondary cross-check and directory-scoped view.

Entry format:
```markdown
## YYYY-MM-DD — build-NN-name

- source-file.md → target-file.md (created | appended)
  - H2 heading integrated
    - H3 subheading integrated
- source-file.md → target-file.md (appended | updated)
  - H2 heading integrated
```

Rules:
- One `##` entry per build per consolidation run
- Each line maps a source theory file to the target file it was integrated into, **with the exact headings/subheadings integrated listed beneath**
- Never edit past entries
