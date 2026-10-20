#!/usr/bin/env python3
"""
Wires the coach's content into everything that quotes it.

    python3 tools/assemble-coach.py      (also run by ./site.py check)

Reads   coach/coach-content.md   (written by the poker-coach agent; its prompt is kept privately)
Writes  docs/glossary.md                 section A, as a page
        docs/includes/abbreviations.md   one line per stat, so any VPIP on any page has a hover
        docs/*.md                        every  <!-- COACH: Card "..." -->  marker gets its card

The spoken video segments (section C) are read by the video scripts in Sprint 3.

Markers stay in place after filling, so the script is safe to re-run after the
coach content changes. Fails loudly on a dash, because that is the one rule.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "coach" / "coach-content.md"
DOCS = ROOT / "docs"

text = SRC.read_text()
if "\u2014" in text or "\u2013" in text:
    sys.exit("coach-content.md contains a dash; fix the source first")


def section(title: str) -> str:
    """Body of a '## X' section."""
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"section not found: {title}")
    return m.group(1).strip()


def block(heading: str) -> str:
    """Body of a '### heading' block, any level-2 section."""
    m = re.search(rf"^### {re.escape(heading)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"block not found: {heading}")
    return m.group(1).strip()


# --- glossary page -----------------------------------------------------------

glossary = section("A. Glossary")
GLOSSARY_HEAD = """# Glossary

Every number the add-on shows, in one or two plain sentences each. What it counts, and what a high or a low number means at Replay tables. Numbers given as a guide are rough; the tables you play on decide what normal is.

Written with a poker coach. Each definition matches exactly what Replay Suite counts.

"""
(DOCS / "glossary.md").write_text(GLOSSARY_HEAD + glossary + "\n")

# --- hover abbreviations -----------------------------------------------------
# '**VPIP** (Voluntarily put money in pot)' -> '*[VPIP]: Voluntarily put money in pot'

abbr = []
for m in re.finditer(r"^\*\*([A-Za-z0-9$/ ]+?)\*\* \(([^)]+)\)", glossary, re.M):
    key, name = m.group(1).strip(), m.group(2).strip()
    if " " not in key:  # only true abbreviations get a hover
        abbr.append(f"*[{key}]: {name}")
(DOCS / "includes").mkdir(exist_ok=True)
(DOCS / "includes" / "abbreviations.md").write_text("\n".join(sorted(set(abbr))) + "\n")

# --- cards into pages --------------------------------------------------------

CARD_MARK = re.compile(r'( *)<!-- COACH: Card "((?:[^"\\]|\\.)+)" -->\n(?:\1\*Placeholder[^\n]*\n)?(?:\1(?!!!!|<!--)[^\n]*\n)*')


def fill_cards(path: Path) -> int:
    src = path.read_text()
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        indent, title = m.group(1), m.group(2).replace('\\"', '"')
        body = block(f"Card: {title}")
        count += 1
        lines = "\n".join(f"{indent}{ln}" if ln else "" for ln in body.splitlines())
        return f'{indent}<!-- COACH: Card "{m.group(2)}" -->\n{lines}\n'

    out = CARD_MARK.sub(repl, src)
    path.write_text(out)
    return count


total = 0
for page in sorted(DOCS.glob("*.md")):
    n = fill_cards(page)
    if n:
        print(f"{page.name:16} {n} card(s)")
        total += n

print(f"glossary: {len(abbr)} hover abbreviations, {total} cards placed")
for f in DOCS.glob("*.md"):
    if "\u2014" in f.read_text() or "\u2013" in f.read_text():
        sys.exit(f"dash found in {f}")
