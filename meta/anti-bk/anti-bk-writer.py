"""anti-bk-writer — deterministic book assembler for the theo knowledge base.

Walks the theo-index hierarchy, collects every content file, assembles a
markdown book, renders it to styled HTML, and prints to PDF.

Usage:
    uv run python meta/anti-bk/anti-bk-writer.py              # full pipeline → meta/anti-bk.pdf
    uv run python meta/anti-bk/anti-bk-writer.py --md-only     # stop after markdown
    uv run python meta/anti-bk/anti-bk-writer.py --html-only   # stop after html

Determinism: directories alphabetical, files alphabetical within each,
headings bumped to fit the chapter/section nesting. Same input → same output.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from itertools import chain
from pathlib import Path
from typing import Iterator, Self

from markdown_it import MarkdownIt

# ── paths ──────────────────────────────────────────────────────────────

SCRIPT_DIR: Path = Path(__file__).resolve().parent
REPO_ROOT: Path = SCRIPT_DIR.parent.parent
THEO_ROOT: Path = REPO_ROOT / "grind" / "theo"
ASSETS_DIR: Path = SCRIPT_DIR / "assets"
ROOT_INDEX: Path = THEO_ROOT / "theo-index.md"

MD_OUTPUT: Path = ASSETS_DIR / "anti-bk.md"
HTML_OUTPUT: Path = ASSETS_DIR / "anti-bk.html"
PDF_OUTPUT: Path = SCRIPT_DIR.parent / "anti-bk.pdf"

IGNORE_STEMS: frozenset[str] = frozenset(
    {"theo-index", "theo-index-template", "theo-log"}
)

# short display names for chapter dirs — falls back to dirname if not mapped
DISPLAY_NAMES: dict[str, str] = {
    "b-dev": "Backend Development",
    "cv": "Computer Vision",
    "data": "Data Engineering",
    "deploy": "Deployment & Infrastructure",
    "dl": "Deep Learning",
    "f-dev": "Frontend Development",
    "ml": "Machine Learning",
    "nlp": "Natural Language Processing",
    "probNstat": "Probability & Statistics",
}

_HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_INDEX_DIR = re.compile(r"^##\s+(\S+?)/?(?:\s+—\s+(.+))?$")
_INDEX_FILE = re.compile(r"^-\s+(\S+\.md)\s+—\s+(.+)$")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STAGE 1 — MARKDOWN ASSEMBLY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# ── data models ────────────────────────────────────────────────────────


@dataclass(slots=True, frozen=True)
class Heading:
    """A single markdown heading extracted from a content file."""

    level: int
    text: str

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self:
        """Alternate constructor from a regex match on a heading line."""
        return cls(level=len(match.group(1)), text=match.group(2).strip())

    def bumped(self, offset: int) -> Self:
        """Return a copy with heading level increased by *offset*, clamped to 6."""
        return type(self)(level=min(self.level + offset, 6), text=self.text)


@dataclass(slots=True)
class Section:
    """One markdown file within a chapter, with its parsed content."""

    name: str
    description: str
    headings: tuple[Heading, ...] = ()
    body: str = ""

    @classmethod
    def from_path(cls, path: Path, description: str = "") -> Self:
        """Parse a content file into a Section."""
        raw = path.read_text(encoding="utf-8").strip()
        headings = tuple(Heading.from_match(m) for m in _HEADING.finditer(raw))
        body = _strip_h1(raw)
        return cls(
            name=path.stem, description=description, headings=headings, body=body
        )

    @property
    def heading_count(self) -> int:
        return len(self.headings)


@dataclass(slots=True)
class Chapter:
    """A subdirectory of theo/, representing one domain chapter."""

    dirname: str
    description: str
    display_name: str = ""
    sections: list[Section] = field(default_factory=list)

    @property
    def title(self) -> str:
        """Short display name for TOC and chapter headings."""
        return self.display_name or self.dirname

    @property
    def is_empty(self) -> bool:
        return not self.sections

    @property
    def all_headings(self) -> Iterator[Heading]:
        """Yield every heading across all sections in this chapter."""
        return chain.from_iterable(s.headings for s in self.sections)


# ── parsing helpers ────────────────────────────────────────────────────


def _strip_h1(text: str) -> str:
    """Remove the first H1 line (title) from markdown — it becomes the section heading."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            stripped = "".join(lines[:i] + lines[i + 1 :]).strip()
            return stripped
    return text


def _is_content_file(path: Path) -> bool:
    """True if *path* is a markdown file we should include in the book."""
    return path.is_file() and path.suffix == ".md" and path.stem not in IGNORE_STEMS


def _anchor(text: str) -> str:
    """Convert heading text to a GitHub-compatible anchor slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s+", "-", slug.strip())


def _bump_headings(body: str, offset: int) -> str:
    """Increase every heading level in *body* by *offset* (H2 → H4 when offset=2)."""

    def _replace(m: re.Match[str]) -> str:
        new_level = min(len(m.group(1)) + offset, 6)
        return f"{'#' * new_level} {m.group(2)}"

    return _HEADING.sub(_replace, body)


# ── index parsing ──────────────────────────────────────────────────────


def parse_root_index(index_path: Path) -> dict[str, str]:
    """Parse root theo-index.md → ``{dirname: description}``."""
    mapping: dict[str, str] = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if m := _INDEX_DIR.match(line):
            mapping[m.group(1).rstrip("/")] = m.group(2) or ""
    return mapping


def parse_subdir_index(index_path: Path) -> dict[str, str]:
    """Parse a subdir theo-index.md → ``{filename: description}``."""
    mapping: dict[str, str] = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if m := _INDEX_FILE.match(line):
            mapping[m.group(1)] = m.group(2)
    return mapping


# ── discovery ──────────────────────────────────────────────────────────


def discover_chapters() -> Iterator[Chapter]:
    """Walk theo root, yield chapters sorted alphabetically by dirname."""
    dir_descriptions = parse_root_index(ROOT_INDEX) if ROOT_INDEX.exists() else {}

    subdirs = sorted(
        (d for d in THEO_ROOT.iterdir() if d.is_dir()),
        key=lambda d: d.name,
    )

    for subdir in subdirs:
        dirname = subdir.name
        chapter = Chapter(
            dirname=dirname,
            description=dir_descriptions.get(dirname, ""),
            display_name=DISPLAY_NAMES.get(dirname, ""),
        )

        subdir_index = subdir / "theo-index.md"
        file_descriptions = (
            parse_subdir_index(subdir_index) if subdir_index.exists() else {}
        )

        content_files = sorted(
            (f for f in subdir.iterdir() if _is_content_file(f)),
            key=lambda f: f.name,
        )

        chapter.sections = [
            Section.from_path(f, file_descriptions.get(f.name, ""))
            for f in content_files
        ]

        yield chapter


# ── book assembly ──────────────────────────────────────────────────────


def _build_toc_html(chapters: list[Chapter]) -> str:
    """Build a hierarchical TOC as raw HTML for reliable nested rendering."""
    lines: list[str] = [
        '<h2 class="toc-heading">Table of Contents</h2>',
        '<nav class="toc">',
        "<ol>",
    ]
    chapter_num = 0

    for chapter in chapters:
        if chapter.is_empty:
            continue
        chapter_num += 1
        anchor = _anchor(f"{chapter_num} {chapter.title}")
        lines.append(
            f'  <li><a href="#{anchor}"><strong>{chapter_num}. {chapter.title}</strong></a>'
        )
        lines.append("    <ol>")

        for i, section in enumerate(chapter.sections, start=1):
            sec_anchor = _anchor(f"{chapter_num}{i} {section.name}")
            desc = f" &mdash; {section.description}" if section.description else ""
            lines.append(
                f'      <li><a href="#{sec_anchor}">{chapter_num}.{i}. {section.name}</a>'
                f"<span>{desc}</span>"
            )

            # sub-topics from H2 headings in this section (they become H4 in the book)
            h2s = [h for h in section.headings if h.level == 2]
            if h2s:
                lines.append("        <ul>")
                for h in h2s:
                    h_anchor = _anchor(h.text)
                    lines.append(
                        f'          <li><a href="#{h_anchor}">{h.text}</a></li>'
                    )
                lines.append("        </ul>")

            lines.append("      </li>")

        lines.append("    </ol>")
        lines.append("  </li>")

    lines.append("</ol>")
    lines.append("</nav>")
    return "\n".join(lines)


def _build_title_page() -> str:
    """Render the HTML title page block."""
    return "\n".join([
        '<div class="title-page">',
        '  <div class="book-title">antiHeuristik</div>',
        '  <div class="book-subtitle">pathei mathos ara prōtai archai</div>',
        '  <hr class="divider">',
        '  <div class="tagline">cargo cult engineering  ×  return to monke</div>',
        '  <div class="meta">',
        f"    auto-generated {date.today().isoformat()}<br>",
        "    source: grind/theo/ index hierarchy",
        "  </div>",
        "</div>",
    ])


def _build_chapter_minitoc(chapter_num: int, chapter: Chapter) -> str:
    """Build a mini table of contents for a single chapter as HTML."""
    lines: list[str] = ['<nav class="chapter-toc">', "<ul>"]
    for i, section in enumerate(chapter.sections, start=1):
        sec_anchor = _anchor(f"{chapter_num}{i} {section.name}")
        lines.append(f'  <li><a href="#{sec_anchor}"><strong>{chapter_num}.{i}. {section.name}</strong></a>')
        if section.description:
            lines.append(f"    <span> &mdash; {section.description}</span>")

        h2s = [h for h in section.headings if h.level == 2]
        if h2s:
            lines.append("    <ul>")
            for h in h2s:
                h_anchor = _anchor(h.text)
                lines.append(f'      <li><a href="#{h_anchor}">{h.text}</a></li>')
            lines.append("    </ul>")

        lines.append("  </li>")
    lines.append("</ul>")
    lines.append("</nav>")
    return "\n".join(lines)


def _anchored_heading(tag: str, id_text: str, content: str) -> str:
    """Render an HTML heading with an explicit id for anchor linking."""
    return f'<{tag} id="{_anchor(id_text)}">{content}</{tag}>'


def _build_chapter(chapter_num: int, chapter: Chapter) -> str:
    """Render one chapter: heading, description, mini-toc, then sections."""
    chapter_id = f"{chapter_num} {chapter.title}"
    parts: list[str] = [
        _anchored_heading("h2", chapter_id, f"{chapter_num}. {chapter.title}"),
        "",
    ]

    # description as subheading
    if chapter.description:
        parts.append(f'<p class="chapter-desc"><em>{chapter.description}</em></p>')
        parts.append("")

    # mini-toc for this chapter
    parts.append(_build_chapter_minitoc(chapter_num, chapter))
    parts.append("")
    parts.append("---")
    parts.append("")

    for i, section in enumerate(chapter.sections, start=1):
        sec_id = f"{chapter_num}{i} {section.name}"
        parts.append(_anchored_heading("h3", sec_id, f"{chapter_num}.{i}. {section.name}"))
        if section.description:
            parts.append(f'<p class="section-desc"><em>{section.description}</em></p>')
        parts.append("")

        # bump content headings and add anchors to H4s (H2→H4 in book)
        bumped = _bump_headings(section.body, offset=2)
        # inject id attrs into H4/H5 headings
        def _add_ids(m: re.Match[str]) -> str:
            level = len(m.group(1))
            text = m.group(2)
            return f'<h{level} id="{_anchor(text)}">{text}</h{level}>'
        bumped = _HEADING.sub(_add_ids, bumped)

        parts.append(bumped)
        parts.append("")
        parts.append("---")
        parts.append("")

    return "\n".join(parts)


def _build_stats(chapters: list[Chapter]) -> Counter[str]:
    """Collect stats about the assembled book."""
    stats: Counter[str] = Counter()
    for chapter in chapters:
        if chapter.is_empty:
            continue
        stats["chapters"] += 1
        stats["sections"] += len(chapter.sections)
        stats["headings"] += sum(s.heading_count for s in chapter.sections)
    return stats


def build_book(chapters: list[Chapter]) -> str:
    """Assemble the full book as a single markdown string."""
    parts: list[str] = [
        _build_title_page(),
        "",
    ]

    parts.append(_build_toc_html(chapters))
    parts.append("")

    chapter_num = 0
    for chapter in chapters:
        if chapter.is_empty:
            continue
        chapter_num += 1
        parts.append(_build_chapter(chapter_num, chapter))

    return "\n".join(parts).rstrip() + "\n"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STAGE 2 — HTML RENDERING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOOK_CSS = """\
:root {
    --fg: #1a1a1a;
    --fg-dim: #374151;
    --fg-light: #6b7280;
    --accent: #1e40af;
    --accent-light: #3b82f6;
    --accent-bg: #eff6ff;
    --accent-dark: #1e3a5f;
    --border: #d1d5db;
    --border-light: #e5e7eb;
    --bg-code: #f8fafc;
    --bg-code-border: #e2e8f0;
    --font-body: "Calibri", "Segoe UI", "Helvetica Neue", sans-serif;
    --font-heading: "Calibri", "Segoe UI", "Helvetica Neue", sans-serif;
    --font-mono: "Cascadia Code", "Consolas", "Fira Code", monospace;
}

* { box-sizing: border-box; }

body {
    font-family: var(--font-body);
    font-size: 11pt;
    line-height: 1.75;
    color: var(--fg);
    margin: 0;
    padding: 0;
    max-width: 100%;
    overflow-x: hidden;
}

/* ═══ TITLE PAGE ═══════════════════════════ */

.title-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 70vh;
    padding: 25mm 15mm;
    page-break-after: always;
}

.title-page .book-title {
    font-family: var(--font-heading);
    font-size: 36pt;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: var(--accent);
    margin: 0 0 3mm 0;
    line-height: 1.1;
}

.title-page .book-subtitle {
    font-family: var(--font-heading);
    font-size: 16pt;
    font-weight: 300;
    color: var(--fg-light);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0 0 10mm 0;
}

.title-page .divider {
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, #fff, var(--accent), var(--accent-light), #fff);
    border: none;
    margin: 0 auto 10mm auto;
}

.title-page .tagline {
    font-family: var(--font-body);
    font-size: 13pt;
    font-style: italic;
    color: var(--fg-dim);
    margin: 0 0 20mm 0;
    max-width: 80%;
    line-height: 1.6;
}

.title-page .meta {
    font-family: var(--font-mono);
    font-size: 8.5pt;
    color: var(--fg-light);
    margin-top: auto;
    line-height: 1.8;
}

/* ═══ CHAPTER HEADINGS (H2) ════════════════ */

h2 {
    font-family: var(--font-heading);
    font-size: 20pt;
    font-weight: 800;
    color: #fff;
    background: linear-gradient(135deg, var(--accent-dark) 0%, var(--accent) 50%, var(--accent-light) 100%);
    margin: 0 0 8mm 0;
    padding: 6mm 6mm 5mm 6mm;
    page-break-before: always;
    page-break-after: avoid;
    letter-spacing: -0.3px;
    line-height: 1.3;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* ═══ SECTION HEADINGS (H3) ════════════════ */

h3 {
    font-family: var(--font-heading);
    font-size: 17pt;
    font-weight: 700;
    color: var(--accent);
    margin: 12mm 0 2mm 0;
    padding: 3mm 0;
    border-top: 3px solid var(--accent);
    border-bottom: 1px solid var(--border-light);
    page-break-after: avoid;
}

/* ═══ TOPIC HEADINGS (H4) ══════════════════ */

h4 {
    font-family: var(--font-heading);
    font-size: 14pt;
    font-weight: 700;
    color: var(--fg);
    margin: 10mm 0 3mm 0;
    padding: 3mm 4mm 3mm 5mm;
    background: var(--accent-bg);
    border-left: 5px solid var(--accent);
    border-radius: 0 4px 4px 0;
    page-break-after: avoid;
}

/* ═══ CONCEPT HEADINGS (H5) ════════════════ */

h5 {
    font-family: var(--font-heading);
    font-size: 12pt;
    font-weight: 700;
    color: var(--accent-dark);
    margin: 7mm 0 2mm 0;
    padding: 0 0 1.5mm 0;
    border-bottom: 2px dotted var(--border);
    page-break-after: avoid;
}

h6 {
    font-family: var(--font-heading);
    font-size: 11pt;
    font-weight: 600;
    color: var(--fg-light);
    margin: 5mm 0 1.5mm 0;
    font-style: italic;
}

/* ═══ PROSE ════════════════════════════════ */

p {
    margin: 0 0 3.5mm 0;
    orphans: 3;
    widows: 3;
    text-align: justify;
    hyphens: auto;
}

strong { font-weight: 700; color: var(--fg); }
em { font-style: italic; color: var(--fg-dim); }

blockquote {
    margin: 5mm 0;
    padding: 3mm 5mm;
    border-left: 4px solid var(--accent-light);
    background: var(--accent-bg);
    border-radius: 0 4px 4px 0;
    color: var(--fg-dim);
    font-size: 10.5pt;
}

h3 + p > em:only-child {
    display: block;
    font-size: 10pt;
    color: var(--fg-light);
    margin: -1mm 0 4mm 0;
    padding: 0 0 2mm 0;
    border-bottom: 1px solid var(--border-light);
}

/* ═══ LISTS ════════════════════════════════ */

ul {
    margin: 3mm 0 5mm 0;
    padding-left: 0;
    list-style: none;
}

ul > li {
    margin-bottom: 2.5mm;
    padding-left: 5mm;
    position: relative;
}

ul > li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 2.5mm;
    width: 6px;
    height: 6px;
    background: var(--accent-light);
    border-radius: 50%;
}

ul ul > li::before {
    width: 5px;
    height: 5px;
    background: transparent;
    border: 1.5px solid var(--accent-light);
    top: 3mm;
}

ol {
    margin: 3mm 0 5mm 0;
    padding-left: 7mm;
}

li { margin-bottom: 2.5mm; }

li > ul, li > ol {
    margin-top: 1.5mm;
    margin-bottom: 0;
}

li > strong:first-child {
    color: var(--accent);
    font-size: 10.5pt;
}

/* ═══ CODE ═════════════════════════════════ */

code {
    font-family: var(--font-mono);
    font-size: 9pt;
    background: var(--bg-code);
    border: 1px solid var(--bg-code-border);
    padding: 0.3mm 2mm;
    border-radius: 3px;
    color: var(--accent);
}

pre {
    background: var(--bg-code);
    border: 1px solid var(--bg-code-border);
    border-left: 4px solid var(--accent-light);
    padding: 4mm 5mm;
    border-radius: 0 4px 4px 0;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    margin: 4mm 0 5mm 0;
    page-break-inside: avoid;
}

pre code {
    background: none;
    border: none;
    padding: 0;
    color: var(--fg);
}

/* ═══ RULES ════════════════════════════════ */

hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, #fff, var(--accent-light), #fff);
    margin: 8mm 0;
}

/* ═══ LINKS ════════════════════════════════ */

a { color: var(--accent-light); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ═══ TABLE OF CONTENTS ════════════════════ */

.toc-heading {
    font-family: var(--font-heading);
    font-size: 20pt;
    font-weight: 700;
    color: var(--accent);
    border-bottom: 3px solid var(--accent);
    background: none !important;
    color: var(--accent) !important;
    padding: 0 0 3mm 0 !important;
    margin: 0 0 6mm 0 !important;
    page-break-before: avoid;
}

nav.toc {
    margin: 0 0 8mm 0;
    page-break-after: always;
}

nav.toc ol {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

nav.toc > ol > li {
    margin-bottom: 5mm;
    padding-bottom: 3mm;
    border-bottom: 1px solid var(--border-light);
}

nav.toc > ol > li:last-child { border-bottom: none; }

nav.toc > ol > li > a {
    font-family: var(--font-heading);
    font-size: 14pt;
    font-weight: 700;
    color: var(--accent);
    text-decoration: none;
    display: block;
    margin-bottom: 2mm;
}

nav.toc > ol > li > a > strong { font-weight: 700; }

nav.toc > ol > li > ol {
    padding-left: 8mm;
    margin-top: 1mm;
}

nav.toc > ol > li > ol > li {
    margin-bottom: 2.5mm;
    line-height: 1.5;
    padding-left: 4mm;
    border-left: 2px solid var(--accent-bg);
}

nav.toc > ol > li > ol > li > a {
    font-family: var(--font-heading);
    font-size: 11pt;
    font-weight: 600;
    color: var(--fg);
    text-decoration: none;
}

nav.toc > ol > li > ol > li > span {
    font-size: 9.5pt;
    color: var(--fg-light);
    display: block;
    margin-top: 0.5mm;
}

nav.toc ul {
    list-style: none;
    padding-left: 4mm;
    margin: 1.5mm 0 0 0;
}

nav.toc ul li {
    margin-bottom: 1mm;
    line-height: 1.4;
    padding-left: 3mm;
    position: relative;
}

nav.toc ul li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 2mm;
    width: 4px;
    height: 4px;
    background: var(--accent-light);
    border-radius: 50%;
}

nav.toc ul li a {
    font-size: 9.5pt;
    color: var(--fg-dim);
    text-decoration: none;
}

nav.toc a:hover { color: var(--accent-light); }

/* ═══ CHAPTER MINI-TOC ═════════════════════ */

nav.chapter-toc {
    margin: 4mm 0 6mm 0;
    padding: 4mm 5mm;
    background: var(--accent-bg);
    border: 1px solid var(--border-light);
    border-radius: 4px;
}

nav.chapter-toc > ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

nav.chapter-toc > ul > li {
    margin-bottom: 2.5mm;
    padding-left: 0;
}

nav.chapter-toc > ul > li::before { display: none; }

nav.chapter-toc > ul > li > a {
    font-family: var(--font-heading);
    font-size: 11pt;
    font-weight: 600;
    color: var(--accent);
    text-decoration: none;
}

nav.chapter-toc > ul > li > span {
    font-size: 9.5pt;
    color: var(--fg-light);
}

nav.chapter-toc ul ul {
    padding-left: 5mm;
    margin: 1mm 0 0 0;
    list-style: none;
}

nav.chapter-toc ul ul li {
    margin-bottom: 0.5mm;
    padding-left: 3mm;
    position: relative;
}

nav.chapter-toc ul ul li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 2mm;
    width: 4px;
    height: 4px;
    background: var(--accent-light);
    border-radius: 50%;
}

nav.chapter-toc ul ul li a {
    font-size: 9.5pt;
    color: var(--fg-dim);
    text-decoration: none;
}

nav.chapter-toc a:hover { color: var(--accent-light); }

/* ═══ PRINT ════════════════════════════════ */

@page { size: A4 portrait !important; }

@media print {
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body { font-size: 10.5pt; max-width: 210mm; }
}
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>antiHeuristik</title>
    <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


# ── rendering ──────────────────────────────────────────────────────────


def md_to_html(md_text: str) -> str:
    """Convert markdown text to HTML body via markdown-it."""
    md = MarkdownIt("commonmark", {"typographer": True, "html": True})
    return md.render(md_text)


def wrap_html(body: str) -> str:
    """Wrap rendered HTML body in a full document with book CSS."""
    return HTML_TEMPLATE.format(css=BOOK_CSS, body=body)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STAGE 3 — PDF GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def html_to_pdf(html_path: Path, output: Path) -> None:
    """Render HTML file to PDF via playwright headless Chromium."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(html_path.as_uri())
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=str(output),
            format="A4",
            margin={"top": "20mm", "right": "18mm", "bottom": "22mm", "left": "18mm"},
            print_background=True,
            display_header_footer=True,
            header_template="<span></span>",
            footer_template=(
                '<div style="font-size:8pt; color:#9ca3af; text-align:center; width:100%;'
                ' font-family:Calibri,sans-serif;">'
                'antiHeuristik &middot; <span class="pageNumber"></span>'
                '</div>'
            ),
        )
        browser.close()


def add_pdf_bookmarks(pdf_path: Path, chapters: list[Chapter]) -> None:
    """Add a clickable bookmark outline to the PDF using pypdf."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(pdf_path)
    writer = PdfWriter(clone_from=reader)

    def _find_page(text: str) -> int:
        """Find the first page containing *text*."""
        for i, page in enumerate(reader.pages):
            content = page.extract_text() or ""
            if text in content:
                return i
        return 0

    for chapter_num, chapter in enumerate(
        (c for c in chapters if not c.is_empty), start=1
    ):
        ch_title = f"{chapter_num}. {chapter.title}"
        ch_page = _find_page(ch_title)
        ch_bookmark = writer.add_outline_item(ch_title, ch_page)

        for i, section in enumerate(chapter.sections, start=1):
            sec_title = f"{chapter_num}.{i}. {section.name}"
            sec_page = _find_page(sec_title)
            sec_bookmark = writer.add_outline_item(sec_title, sec_page, parent=ch_bookmark)

            for h in section.headings:
                if h.level == 2:
                    h_page = _find_page(h.text)
                    writer.add_outline_item(h.text, h_page, parent=sec_bookmark)

    with open(pdf_path, "wb") as f:
        writer.write(f)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ENTRY POINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main() -> int:
    """Full pipeline: discover → markdown → html → pdf."""
    md_only = "--md-only" in sys.argv
    html_only = "--html-only" in sys.argv

    if not THEO_ROOT.is_dir():
        print(f"theo root not found: {THEO_ROOT}", file=sys.stderr)
        return 1

    # stage 1 — markdown
    chapters = list(discover_chapters())
    non_empty = [c for c in chapters if not c.is_empty]

    if not non_empty:
        print("no content files found — nothing to write", file=sys.stderr)
        return 1

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    book_md = build_book(chapters)
    MD_OUTPUT.write_text(book_md, encoding="utf-8")

    stats = _build_stats(chapters)
    print(
        f"[md]   {MD_OUTPUT.name}: "
        f"{stats['chapters']} chapters, {stats['sections']} sections, "
        f"{stats['headings']} headings, {len(book_md):,} chars"
    )

    if md_only:
        return 0

    # stage 2 — html
    body = md_to_html(book_md)
    full_html = wrap_html(body)
    HTML_OUTPUT.write_text(full_html, encoding="utf-8")
    print(f"[html] {HTML_OUTPUT.name}: {len(full_html):,} chars")

    if html_only:
        return 0

    # stage 3 — pdf
    try:
        html_to_pdf(HTML_OUTPUT, PDF_OUTPUT)
    except Exception as exc:
        print(f"[pdf]  failed: {exc}", file=sys.stderr)
        print(f"       fallback: open {HTML_OUTPUT} in a browser and print", file=sys.stderr)
        return 1

    # stage 4 — pdf bookmarks
    try:
        add_pdf_bookmarks(PDF_OUTPUT, non_empty)
        print("[pdf]  bookmarks added")
    except Exception as exc:
        print(f"[pdf]  bookmarks failed (non-fatal): {exc}", file=sys.stderr)

    size_kb = PDF_OUTPUT.stat().st_size / 1024
    print(f"[pdf]  {PDF_OUTPUT.relative_to(REPO_ROOT)}: {size_kb:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
