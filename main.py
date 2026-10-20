"""
mkdocs-macros module: turns data/*.yml into the Versions, Status, Videos and
home-page boxes.

Pages opt in with `render_macros: true` in their front matter; every other page
is left alone, so a stray brace in normal text can never break the build.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import rsdata  # noqa: E402

BUG_PILL = {"open": "open", "investigating": "investigating", "fixed": "done", "not a bug": "muted"}
IDEA_PILL = {"under review": "investigating", "planned": "open-idea", "shipped": "done", "not planned": "muted"}


nice_date = rsdata.nice_date


def pill(text: str, kind: str) -> str:
    return f'<span class="rs-pill rs-pill--{kind}">{escape(text)}</span>'


def forum_link(item: dict) -> str:
    url = item.get("forum")
    return f' <a class="rs-forum" href="{escape(url)}">forum post</a>' if url else ""


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>" if items else ""


def define_env(env):
    data = rsdata.load_all()
    errors = rsdata.validate(data)
    if errors:
        raise SystemExit("data/ is invalid:\n  " + "\n  ".join(errors))

    bugs, ideas = rsdata.by_id(data["bugs"]), rsdata.by_id(data["suggestions"])
    latest = rsdata.latest_release(data)
    latest_chrome = rsdata.latest_chrome_release(data)

    env.variables.update({
        "amo_url": rsdata.AMO_URL,
        "latest_zip_url": rsdata.LATEST_ZIP_URL,
        "latest_version": latest["version"] if latest else "",
        "latest_chrome_version": latest_chrome["version"] if latest_chrome else "",
        "latest_chrome_zip": rsdata.zip_name(latest_chrome["version"]) if latest_chrome else "",
    })

    @env.macro
    def release_cards() -> str:
        out = []
        for r in data["releases"]:
            is_latest = latest and r["version"] == latest["version"]
            head = f'<h2 id="v{escape(r["version"])}">Version {escape(r["version"])}'
            if is_latest:
                head += " " + pill("Latest", "done")
            head += "</h2>"
            parts = [head, f'<p class="rs-date">{nice_date(r["date"])}</p>',
                     f'<p class="rs-summary">{escape(r["summary"])}</p>']
            if r.get("update_note"):
                parts.append(f'<div class="admonition careful"><p class="admonition-title">Before you update</p>'
                             f'<p>{escape(r["update_note"])}</p></div>')
            sections = [
                ("Added", [escape(x) for x in r.get("added") or []]),
                ("Changed", [escape(x) for x in r.get("changed") or []]),
                ("Fixed", [f'{escape(bugs[b]["title"])} <span class="rs-id">{b}</span>' for b in r.get("fixed") or []]),
                ("Suggested by players", [f'{escape(ideas[s]["title"])} <span class="rs-id">{s}</span>'
                                          for s in r.get("shipped_suggestions") or []]),
            ]
            for title, items in sections:
                if items:
                    parts.append(f"<h3>{title}</h3>{ul(items)}")
            if r.get("firefox_only"):
                dl = f'<p class="rs-dl">Firefox only. <a href="{rsdata.AMO_URL}">Firefox Add-ons</a></p>'
            else:
                dl = (f'<p class="rs-dl"><a class="md-button" href="{rsdata.zip_url(r["version"])}">'
                      f'Chrome and Edge: download {escape(r["version"])}</a> '
                      f'Firefox: updates itself from <a href="{rsdata.AMO_URL}">Firefox Add-ons</a>.</p>')
            parts.append(dl)
            out.append(f'<section class="rs-release">{"".join(parts)}</section>')
        return "\n".join(out)

    @env.macro
    def bug_list() -> str:
        if not data["bugs"]:
            return '<p class="rs-empty">No known bugs right now. Found one? Tell us on the forum.</p>'
        rank = {"open": 0, "investigating": 1, "fixed": 2, "not a bug": 3}
        rows = []
        for b in sorted(data["bugs"], key=lambda b: (rank[b["status"]], b["id"])):
            label = b["status"] if b["status"] != "fixed" else f'fixed in {b["fixed_in"]}'
            meta = []
            if b.get("affects"):
                meta.append("Affects " + ", ".join(b["affects"]))
            if b.get("browsers") and set(b["browsers"]) != set(rsdata.BROWSERS):
                meta.append(", ".join(x.capitalize() for x in b["browsers"]) + " only")
            row = (f'<div class="rs-item"><div class="rs-item-head">{pill(label, BUG_PILL[b["status"]])}'
                   f'<span class="rs-id">{b["id"]}</span> {escape(b["title"])}</div>')
            if meta:
                row += f'<div class="rs-meta">{escape(". ".join(meta))}.{forum_link(b)}</div>'
            elif b.get("forum"):
                row += f'<div class="rs-meta">{forum_link(b).strip()}</div>'
            if b.get("workaround") and b["status"] in ("open", "investigating"):
                row += f'<div class="rs-workaround"><b>Meanwhile:</b> {escape(b["workaround"])}</div>'
            rows.append(row + "</div>")
        return "\n".join(rows)

    @env.macro
    def suggestion_list() -> str:
        if not data["suggestions"]:
            return '<p class="rs-empty">No suggestions listed yet. Have an idea? Share it on the forum.</p>'
        out = []
        for status in ["planned", "under review", "shipped", "not planned"]:
            group = [s for s in data["suggestions"] if s["status"] == status]
            if not group:
                continue
            group.sort(key=lambda s: (-s.get("asked_by", 1), s["id"]))
            out.append(f"<h3>{status.capitalize()}</h3>")
            for s in group:
                label = status if status != "shipped" else f'shipped in {s["shipped_in"]}'
                asked = s.get("asked_by", 1)
                meta = f"Asked for by {asked} player{'s' if asked != 1 else ''}."
                if s.get("reason"):
                    meta += f' {escape(s["reason"])}'
                out.append(f'<div class="rs-item"><div class="rs-item-head">{pill(label, IDEA_PILL[status])}'
                           f'<span class="rs-id">{s["id"]}</span> {escape(s["title"])}</div>'
                           f'<div class="rs-meta">{meta}{forum_link(s)}</div></div>')
        return "\n".join(out)

    @env.macro
    def news_list(limit: int = 0) -> str:
        items = data["news"][:limit] if limit else data["news"]
        if not items:
            return '<p class="rs-empty">No news yet.</p>'
        return "\n".join(
            f'<div class="rs-news"><span class="rs-date">{nice_date(n["date"])}</span> '
            f'<b>{escape(n["title"])}</b><p>{escape(n.get("body", ""))}</p></div>'
            for n in items
        )

    @env.macro
    def status_box() -> str:
        open_bugs = [b for b in data["bugs"] if b["status"] in ("open", "investigating")]
        planned = [s for s in data["suggestions"] if s["status"] == "planned"]
        newest = data["news"][0] if data["news"] else None
        bugs_line = (f"{len(open_bugs)} known bug{'s' if len(open_bugs) != 1 else ''} being worked on"
                     if open_bugs else "No known bugs right now")
        lines = [
            f'<div class="rs-stat"><span class="rs-stat-n">{escape(latest["version"]) if latest else "?"}</span>'
            f'<span>Latest version</span></div>',
            f'<div class="rs-stat"><span class="rs-stat-n">{len(open_bugs)}</span><span>{bugs_line}</span></div>',
            f'<div class="rs-stat"><span class="rs-stat-n">{len(planned)}</span><span>Player suggestions planned</span></div>',
        ]
        news = (f'<p class="rs-news-line"><span class="rs-date">{nice_date(newest["date"])}</span> '
                f'{escape(newest["title"])}. <a href="status/">See the status page</a>.</p>') if newest else ""
        return f'<div class="rs-statusbox">{"".join(lines)}</div>{news}'

    @env.macro
    def video_list() -> str:
        if not data["videos"]:
            return ('<div class="admonition try"><p class="admonition-title">Coming soon</p>'
                    "<p>Four short videos are on the way: an overview, installing on each browser, "
                    "updating on Chrome and Edge, and a full walkthrough. Until then, every page of "
                    "this guide has pictures for each step.</p></div>")
        out = []
        for v in data["videos"]:
            vid = v["url"].rsplit("v=", 1)[-1].rsplit("/", 1)[-1]
            out.append(f'<h2 id="{escape(v["id"])}">{escape(v["title"])}</h2>'
                       f'<div class="rs-video"><iframe src="https://www.youtube-nocookie.com/embed/{escape(vid)}" '
                       f'title="{escape(v["title"])}" allowfullscreen loading="lazy"></iframe></div>'
                       f'<p>{escape(v.get("description", ""))}</p>')
        return "\n".join(out)
