#!/usr/bin/env python3
"""
A look at each post before it goes on the forum, in both of the forum's themes.

    .venv/bin/python forum/preview.py      (after python3 forum/check.py)

Reads forum/out/*.md and writes forum/out/preview-<post>.html: the post at the
forum's 690 px column, light theme on the left, dark on the right. Open it in a
browser. Images are shown from this folder, so the preview works before the site
is published.

It imitates Discourse closely enough to judge layout, image sizes and how the
panels sit on each background. It is not Discourse: the real check is pasting
into the forum's composer and looking at its preview without posting.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
OUT = HERE / "out"
IMG = SITE / "docs" / "img" / "forum"

CSS = """
body { margin: 0; font-family: Arial, Helvetica, sans-serif; background: #888; }
.pair { display: flex; gap: 24px; padding: 24px; align-items: flex-start; }
.post { width: 690px; padding: 18px 20px 30px; font-size: 15px; line-height: 1.5; }
.light { background: #ffffff; color: #222222; }
.dark { background: #222222; color: #dddddd; }
.dark a { color: #6fb3ff; } .light a { color: #0f5ea8; }
.post img { max-width: 100%; height: auto; }
.post h2 { font-size: 1.45em; margin: 1.2em 0 .5em; }
.post blockquote { margin: 1em 0; padding: 12px; border-left: 5px solid #e9e9e9; background: rgba(127,127,127,.08); }
.dark .post blockquote, .dark blockquote { border-left-color: #3d3d3d; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
details { margin: .8em 0; } summary { cursor: pointer; font-weight: bold; }
.label { font: bold 13px Arial; color: #fff; padding: 6px 24px 0; }
code { background: rgba(127,127,127,.15); padding: 1px 4px; border-radius: 3px; }
"""


def to_html(md: str) -> str:
    # Images: ![alt|WxH](url) is Discourse's way of giving a display size.
    def img(m):
        alt, w, h, url = m[1], m[2], m[3], m[4]
        name = url.rsplit("/", 1)[-1]
        local = IMG / name
        src = local.as_uri() if local.exists() else url
        return f'<img alt="{escape(alt)}" src="{src}" width="{w}" height="{h}">'

    md = re.sub(r"!\[([^\]|]*)\|(\d+)x(\d+)\]\(([^)]+)\)", img, md)
    md = re.sub(r"\[grid\]\s*(.*?)\s*\[/grid\]", lambda m: '<div class="grid">' + m[1] + "</div>", md, flags=re.S)
    md = re.sub(r'\[details="([^"]*)"\]', lambda m: f'<details open markdown="1"><summary>{escape(m[1])}</summary>', md)
    md = md.replace("[/details]", "</details>")
    return markdown.markdown(md, extensions=["md_in_html"])


def main() -> None:
    for src in sorted(OUT.glob("*.md")):
        body = to_html(src.read_text())
        page = (f"<!doctype html><meta charset='utf-8'><title>{src.stem}</title><style>{CSS}</style>"
                f"<div class='pair'><div><div class='label'>Light theme</div><div class='post light'>{body}</div></div>"
                f"<div><div class='label'>Dark theme</div><div class='post dark'>{body}</div></div></div>")
        out = OUT / f"preview-{src.stem}.html"
        out.write_text(page)
        print(f"  {out.relative_to(SITE)}")


if __name__ == "__main__":
    main()
