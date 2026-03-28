# Theo Cross-Reference

Add cross-references between related sections across `grind/theo/` directories.

Run this after `/anti-theo-conso` when consolidated content spans multiple directories.

---

## Inputs

- `$ARGUMENTS` — optional: specific directory or file to focus on (e.g., `dl` or `dl/attention.md`). If empty, scan all.

---

## Steps

### Step 1 — Inventory

Read `grind/theo/theo-index.md` to get the full file list. Then read each sub-dir's `theo-index.md` to get heading trees.

Build a concept map: for each file, list the key concepts it covers (from heading trees + a quick scan of content).

### Step 2 — Identify Links

Find pairs of sections across different directories where:
- The same concept appears in both (e.g., quantization discussed in `dl/` and referenced in `nlp/` evaluation)
- One section explains a mechanism that another section measures or applies
- A term defined in one file is used without definition in another

For each proposed cross-reference, note:
- Source section (file + heading)
- Target section (file + heading)
- Relationship type: `explains`, `measures`, `applies`, `defines`, `extends`
- One-line justification

### Step 3 — Present & Confirm

Show the user the proposed cross-references as a table:

```
| From | To | Relationship | Why |
|------|-----|-------------|-----|
| dl/attention.md § Systematic Flattening | nlp/evaluation.md § Scoring Categories | explains → measures | Flattening causes the hedge/confabulate failures the scoring categories capture |
```

**Wait for user confirmation.** User may reject, modify, or add links.

### Step 4 — Write References

For each approved cross-reference, append a line at the end of the relevant section:

```markdown
> See also: dl/attention.md § Systematic Flattening — how quantization flattens attention scores
```

Rules:
- Place the cross-ref at the **end** of the section it's added to, before the next heading
- Use `> See also:` blockquote format — visually distinct, doesn't break flow
- Include the target file, heading, and a short phrase explaining the connection
- Do NOT add bidirectional refs unless both directions are independently useful
- Do NOT modify any existing content — append only

### Step 5 — Update Indexes

Update any affected sub-dir `theo-index.md` files to note cross-references exist (no structural change needed — just add `(xref)` marker next to headings that have cross-references).

### Step 6 — Summary

Present:
- Number of cross-references added
- Files modified
- Any sections that seem related but didn't have enough connection to warrant a formal xref (flag for user awareness)
