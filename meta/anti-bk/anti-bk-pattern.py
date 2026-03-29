"""anti-bk-pattern — markdown pattern registry and compliance scanner.

Defines every markdown pattern found in the theo knowledge base as a
datamodel with compiled regex.  The scanner walks the directory tree,
matches patterns, and reports which patterns exist, which are missing,
and where each pattern occurs.

Run standalone to survey:
    uv run python meta/anti-bk/anti-bk-pattern.py
    uv run python meta/anti-bk/anti-bk-pattern.py --json   # machine-readable
"""

from __future__ import annotations

import json
import re
import sys
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto, unique
from functools import cached_property
from pathlib import Path
from typing import Iterator, NamedTuple, Protocol, Self, runtime_checkable

# ── constants ──────────────────────────────────────────────────────────

SCRIPT_DIR: Path = Path(__file__).resolve().parent
REPO_ROOT: Path = SCRIPT_DIR.parent.parent
THEO_ROOT: Path = REPO_ROOT / "grind" / "theo"

IGNORE_STEMS: frozenset[str] = frozenset(
    {"theo-index", "theo-index-template", "theo-log"}
)


# ── enums ──────────────────────────────────────────────────────────────


@unique
class Category(Enum):
    """Broad grouping of markdown pattern types."""

    HEADING = auto()
    EMPHASIS = auto()
    CODE = auto()
    LIST = auto()
    BLOCK = auto()
    LINK = auto()
    RULE = auto()
    SEMANTIC = auto()  # domain-specific patterns (em-dash, arrows, status)

    def __str__(self) -> str:
        return self.name.lower()


# ── core data models ───────────────────────────────────────────────────


class PatternMatch(NamedTuple):
    """A single regex hit inside a file."""

    pattern_name: str
    file: Path
    line_no: int
    text: str


@dataclass(slots=True, frozen=True)
class MarkdownPattern:
    """One markdown pattern: a name, a compiled regex, and metadata."""

    name: str
    category: Category
    regex: re.Pattern[str]
    description: str
    multiline: bool = False

    @classmethod
    def inline(cls, name: str, category: Category, expr: str, description: str) -> Self:
        """Factory for single-line patterns."""
        return cls(
            name=name,
            category=category,
            regex=re.compile(expr),
            description=description,
            multiline=False,
        )

    @classmethod
    def block(cls, name: str, category: Category, expr: str, description: str) -> Self:
        """Factory for multi-line patterns (code fences, etc.)."""
        return cls(
            name=name,
            category=category,
            regex=re.compile(expr, re.MULTILINE | re.DOTALL),
            description=description,
            multiline=True,
        )

    def scan_text(self, text: str, path: Path) -> Iterator[PatternMatch]:
        """Yield every match of this pattern in *text*, with line numbers."""
        if self.multiline:
            for m in self.regex.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                yield PatternMatch(self.name, path, line_no, m.group().split("\n")[0])
        else:
            for i, line in enumerate(text.splitlines(), start=1):
                if self.regex.search(line):
                    yield PatternMatch(self.name, path, i, line.strip())


# ── pattern registry ───────────────────────────────────────────────────

# fmt: off
PATTERNS: tuple[MarkdownPattern, ...] = (
    # ── headings ───────────────────────────────────────────────────
    MarkdownPattern.inline("h1",            Category.HEADING,   r"^# (?!#)",                             "H1 heading"),
    MarkdownPattern.inline("h2",            Category.HEADING,   r"^## (?!#)",                            "H2 heading"),
    MarkdownPattern.inline("h3",            Category.HEADING,   r"^### (?!#)",                           "H3 heading"),
    MarkdownPattern.inline("h4",            Category.HEADING,   r"^#### (?!#)",                          "H4 heading"),
    MarkdownPattern.inline("h5",            Category.HEADING,   r"^##### (?!#)",                         "H5 heading"),
    MarkdownPattern.inline("h6",            Category.HEADING,   r"^###### ",                             "H6 heading"),
    MarkdownPattern.inline("numbered_head", Category.HEADING,   r"^#{1,6}\s+\d+\.\d*",                  "Numbered section heading (1.2. title)"),

    # ── emphasis ───────────────────────────────────────────────────
    MarkdownPattern.inline("bold",          Category.EMPHASIS,  r"\*\*[^*]+\*\*",                        "Bold text (**word**)"),
    MarkdownPattern.inline("italic",        Category.EMPHASIS,  r"(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)", "Italic text (*word*)"),
    MarkdownPattern.inline("bold_italic",   Category.EMPHASIS,  r"\*\*\*[^*]+\*\*\*",                    "Bold-italic text (***word***)"),

    # ── code ───────────────────────────────────────────────────────
    MarkdownPattern.inline("inline_code",   Category.CODE,      r"`[^`\n]+`",                            "Inline code (`expr`)"),
    MarkdownPattern.block("fenced_code",    Category.CODE,      r"^```\w*\n.*?^```",                     "Fenced code block (```lang ... ```)"),

    # ── lists ──────────────────────────────────────────────────────
    MarkdownPattern.inline("bullet",        Category.LIST,      r"^\s*- (?!\[[ x]\])",                   "Bullet list item (- text)"),
    MarkdownPattern.inline("numbered_list", Category.LIST,      r"^\s*\d+\.\s+",                         "Numbered list item (1. text)"),
    MarkdownPattern.inline("task_empty",    Category.LIST,      r"^\s*- \[ \]\s+",                       "Unchecked task (- [ ] text)"),
    MarkdownPattern.inline("task_checked",  Category.LIST,      r"^\s*- \[x\]\s+",                       "Checked task (- [x] text)"),
    MarkdownPattern.inline("nested_bullet", Category.LIST,      r"^\s{2,}- ",                            "Nested bullet (indented ≥2 spaces)"),
    MarkdownPattern.inline("bold_def",      Category.LIST,      r"^\s*- \*\*[^*]+\*\*:\s+",             "Bold-colon definition (- **term**: desc)"),

    # ── tables ─────────────────────────────────────────────────────
    MarkdownPattern.inline("table_row",     Category.BLOCK,     r"^\|.+\|$",                             "Table row (| col | col |)"),
    MarkdownPattern.inline("table_sep",     Category.BLOCK,     r"^\|[-:|]+\|$",                         "Table separator row (|---|---|)"),

    # ── blocks ─────────────────────────────────────────────────────
    MarkdownPattern.inline("blockquote",    Category.BLOCK,     r"^>\s+",                                "Blockquote (> text)"),
    MarkdownPattern.inline("notes_block",   Category.BLOCK,     r"^>\s*notes:",                          "Notes blockquote (> notes: ...)"),

    # ── links ──────────────────────────────────────────────────────
    MarkdownPattern.inline("inline_link",   Category.LINK,      r"\[([^\]]+)\]\(([^)]+)\)",              "Inline link ([text](url))"),
    MarkdownPattern.inline("anchor_link",   Category.LINK,      r"\[([^\]]+)\]\(#[^)]+\)",               "Anchor link ([text](#slug))"),

    # ── rules ──────────────────────────────────────────────────────
    MarkdownPattern.inline("hrule",         Category.RULE,      r"^---\s*$",                             "Horizontal rule (---)"),

    # ── semantic (domain-specific) ─────────────────────────────────
    MarkdownPattern.inline("em_dash_sep",   Category.SEMANTIC,  r"\s—\s",                                "Em-dash separator ( — )"),
    MarkdownPattern.inline("arrow_map",     Category.SEMANTIC,  r"→",                                    "Arrow mapping operator (→)"),
    MarkdownPattern.inline("pipe_alt",      Category.SEMANTIC,  r"\([^)]*\|[^)]*\)",                     "Pipe alternatives ((a | b))"),
    MarkdownPattern.inline("paren_status",  Category.SEMANTIC,  r"\((created|appended|updated)\)",       "Parenthetical status marker"),
    MarkdownPattern.inline("citation",      Category.SEMANTIC,  r"\w+(?:\s+et\s+al\.)?,\s*\d{4}",       "Academic citation (Author, YYYY)"),
    MarkdownPattern.inline("italic_desc",   Category.SEMANTIC,  r"^\*[^*]{10,}\*$",                      "Italic description line (*long text*)"),
)
# fmt: on


# ── scanner protocol ──────────────────────────────────────────────────


@runtime_checkable
class Scannable(Protocol):
    """Anything that yields markdown file paths."""

    def md_files(self) -> Iterator[Path]: ...


@dataclass(slots=True)
class TheoTree:
    """Walks the theo directory tree, yielding content markdown files."""

    root: Path
    ignore: frozenset[str] = IGNORE_STEMS

    def md_files(self) -> Iterator[Path]:
        """Yield every content .md file under root, sorted deterministically."""
        files = sorted(
            (f for f in self.root.rglob("*.md") if f.stem not in self.ignore),
            key=lambda f: f.relative_to(self.root).as_posix(),
        )
        yield from files


# ── report ─────────────────────────────────────────────────────────────


@dataclass
class SurveyReport:
    """Aggregated results of a pattern scan across all files."""

    matches: dict[str, list[PatternMatch]] = field(default_factory=lambda: defaultdict(list))
    file_count: int = 0

    @cached_property
    def found_patterns(self) -> frozenset[str]:
        return frozenset(k for k, v in self.matches.items() if v)

    @cached_property
    def missing_patterns(self) -> frozenset[str]:
        all_names = frozenset(p.name for p in PATTERNS)
        return all_names - self.found_patterns

    @cached_property
    def counts(self) -> Counter[str]:
        return Counter({name: len(hits) for name, hits in self.matches.items()})

    @cached_property
    def by_category(self) -> dict[Category, list[str]]:
        grouped: dict[Category, list[str]] = defaultdict(list)
        lookup = {p.name: p.category for p in PATTERNS}
        for name in sorted(self.found_patterns):
            grouped[lookup[name]].append(name)
        return dict(grouped)

    def render_text(self) -> str:
        """Human-readable report."""
        lines: list[str] = ["THEO PATTERN SURVEY", "=" * 40, ""]

        lines.append(f"files scanned: {self.file_count}")
        lines.append(f"patterns defined: {len(PATTERNS)}")
        lines.append(f"patterns found: {len(self.found_patterns)}")
        lines.append(f"patterns missing: {len(self.missing_patterns)}")
        lines.append("")

        # by category
        for cat in Category:
            cat_patterns = [p for p in PATTERNS if p.category == cat]
            found_in_cat = [p.name for p in cat_patterns if p.name in self.found_patterns]
            missing_in_cat = [p.name for p in cat_patterns if p.name in self.missing_patterns]
            lines.append(f"[{cat}] {len(found_in_cat)}/{len(cat_patterns)}")
            for name in found_in_cat:
                lines.append(f"  + {name} ({self.counts[name]} hits)")
            for name in missing_in_cat:
                lines.append(f"  - {name} (NOT FOUND)")
            lines.append("")

        # top files by pattern density
        file_hits: Counter[str] = Counter()
        for hits in self.matches.values():
            for hit in hits:
                file_hits[str(hit.file.relative_to(THEO_ROOT))] += 1

        if file_hits:
            lines.append("top files by pattern density:")
            for path, count in file_hits.most_common(10):
                lines.append(f"  {count:4d}  {path}")
            lines.append("")

        # missing detail
        if self.missing_patterns:
            lines.append("MISSING PATTERNS (not found in any content file):")
            lookup = {p.name: p for p in PATTERNS}
            for name in sorted(self.missing_patterns):
                p = lookup[name]
                lines.append(f"  {name}: {p.description}")

        return "\n".join(lines)

    def render_json(self) -> str:
        """Machine-readable JSON report."""
        data = {
            "files_scanned": self.file_count,
            "patterns_defined": len(PATTERNS),
            "patterns_found": len(self.found_patterns),
            "patterns_missing": len(self.missing_patterns),
            "counts": dict(self.counts.most_common()),
            "missing": sorted(self.missing_patterns),
            "by_category": {
                str(cat): {
                    "found": [p.name for p in PATTERNS if p.category == cat and p.name in self.found_patterns],
                    "missing": [p.name for p in PATTERNS if p.category == cat and p.name in self.missing_patterns],
                }
                for cat in Category
            },
        }
        return json.dumps(data, indent=2)


# ── scanner ────────────────────────────────────────────────────────────


class BaseScanner(ABC):
    """Abstract scanner — subclass to change pattern set or file source."""

    @abstractmethod
    def patterns(self) -> tuple[MarkdownPattern, ...]: ...

    @abstractmethod
    def source(self) -> Scannable: ...

    def run(self) -> SurveyReport:
        report = SurveyReport()
        for path in self.source().md_files():
            report.file_count += 1
            text = path.read_text(encoding="utf-8")
            for pattern in self.patterns():
                for match in pattern.scan_text(text, path):
                    report.matches[pattern.name].append(match)
        # ensure every pattern has an entry even if no matches
        for p in self.patterns():
            report.matches.setdefault(p.name, [])
        return report


@dataclass(slots=True)
class TheoScanner(BaseScanner):
    """Concrete scanner for the theo knowledge base."""

    root: Path = THEO_ROOT

    def patterns(self) -> tuple[MarkdownPattern, ...]:
        return PATTERNS

    def source(self) -> TheoTree:
        return TheoTree(root=self.root)


# ── entry point ────────────────────────────────────────────────────────


def main() -> int:
    as_json = "--json" in sys.argv
    scanner = TheoScanner()
    report = scanner.run()
    output = report.render_json() if as_json else report.render_text()
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    return 1 if report.missing_patterns else 0


if __name__ == "__main__":
    sys.exit(main())
