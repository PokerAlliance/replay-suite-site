#!/usr/bin/env python3
"""
Keeps the Replay Suite website up to date. Run from this folder.

  Bugs
    ./site.py bug add "Badge flickers when a player sits out" --forum URL --affects 4.0.1
    ./site.py bug status B-001 investigating
    ./site.py bug fix B-001 --in 4.0.2

  Suggestions
    ./site.py idea add "A simpler badge for new players" --forum URL
    ./site.py idea plus S-001                  # one more player asked for it
    ./site.py idea status S-001 planned
    ./site.py idea status S-002 "not planned" --reason "One sentence why."

  News
    ./site.py news "Chrome store status" "Still waiting on Google."

  Releases (after `pnpm release:build X.Y.Z` in the extension repository)
    ./site.py release new 4.0.2 --summary "One line."   # drafts the entry, fixes pre-filled
    ./site.py publish -m "Release 4.0.2"                 # site goes live with the notes
    ./site.py release publish 4.0.2                      # GitHub release with the zips

  Forum
    ./site.py forum status-board               # Thread B status post, copied to the clipboard
    ./site.py forum release 4.0.2              # announcement reply for Thread B

  Always
    ./site.py check                            # everything valid, no dashes, builds clean
    ./site.py publish -m "message"             # check, commit, push: the site redeploys

Or edit data/*.yml directly on github.com; the site rebuilds on every commit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Run inside the project's virtual environment when there is one, so `./site.py`
# works without activating anything. First time:  python3 -m venv .venv &&
# .venv/bin/pip install -r requirements.txt
_VENV_PY = ROOT / ".venv" / "bin" / "python"
if _VENV_PY.exists() and Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
    os.execv(str(_VENV_PY), [str(_VENV_PY), __file__, *sys.argv[1:]])

sys.path.insert(0, str(ROOT / "tools"))
import rsdata as d  # noqa: E402

DIST = ROOT / "dist"


def today() -> str:
    return dt.date.today().isoformat()


def die(msg: str) -> None:
    sys.exit(f"✖ {msg}")


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, **kw)


def next_id(items: list[dict], prefix: str) -> str:
    nums = [int(i["id"][2:]) for i in items if re.match(rf"^{prefix}-\d{{3}}$", i.get("id", ""))]
    return f"{prefix}-{max(nums, default=0) + 1:03d}"


def find(items: list[dict], iid: str) -> dict:
    for item in items:
        if item["id"] == iid.upper():
            return item
    die(f"{iid} not found")


def save_checked(name: str, items: list[dict]) -> None:
    """Write only if the whole data set stays valid, so a typo never lands."""
    data = d.load_all()
    data[name] = items
    errors = d.validate(data)
    if errors:
        die("not saved:\n  " + "\n  ".join(errors))
    d.save(name, items)


def no_dash(text: str, what: str) -> None:
    if any(x in text for x in d.DASHES):
        die(f"{what} contains an em or en dash. Use a comma, a full stop or parentheses.")


# --- bugs ------------------------------------------------------------------------


def cmd_bug(a) -> None:
    bugs = d.load("bugs")
    if a.action == "add":
        no_dash(a.title, "the title")
        item = {"id": next_id(bugs, "B"), "title": a.title, "status": "open",
                "affects": a.affects or [], "browsers": a.browsers or list(d.BROWSERS),
                "workaround": a.workaround or "", "fixed_in": None,
                "reported": today(), "forum": a.forum or ""}
        bugs.append(item)
        save_checked("bugs", bugs)
        print(f"✔ {item['id']} added: {item['title']}")
    elif a.action == "status":
        item = find(bugs, a.id)
        item["status"] = a.status
        if a.status != "fixed":
            item["fixed_in"] = None
        save_checked("bugs", bugs)
        print(f"✔ {item['id']} is now {a.status}")
    elif a.action == "fix":
        item = find(bugs, a.id)
        item["status"], item["fixed_in"] = "fixed", a.version
        save_checked("bugs", bugs)
        print(f"✔ {item['id']} fixed in {a.version}; it will be listed in that release's notes")


# --- suggestions ---------------------------------------------------------------


def cmd_idea(a) -> None:
    ideas = d.load("suggestions")
    if a.action == "add":
        no_dash(a.title, "the title")
        item = {"id": next_id(ideas, "S"), "title": a.title, "status": "under review",
                "shipped_in": None, "reason": "", "asked_by": 1,
                "reported": today(), "forum": a.forum or ""}
        ideas.append(item)
        save_checked("suggestions", ideas)
        print(f"✔ {item['id']} added: {item['title']}")
    elif a.action == "plus":
        item = find(ideas, a.id)
        item["asked_by"] = item.get("asked_by", 1) + 1
        save_checked("suggestions", ideas)
        print(f"✔ {item['id']} now asked for by {item['asked_by']} players")
    elif a.action == "status":
        item = find(ideas, a.id)
        item["status"] = a.status
        if a.reason:
            no_dash(a.reason, "the reason")
            item["reason"] = a.reason
        if a.status == "shipped":
            if not a.version:
                die("shipped needs --in VERSION")
            item["shipped_in"] = a.version
        else:
            item["shipped_in"] = None
        save_checked("suggestions", ideas)
        print(f"✔ {item['id']} is now {a.status}")


# --- news ------------------------------------------------------------------------


def cmd_news(a) -> None:
    no_dash(a.title + a.body, "the news item")
    news = d.load("news")
    news.insert(0, {"date": today(), "title": a.title, "body": a.body})
    save_checked("news", news)
    print(f"✔ news added: {a.title}")


# --- release notes, shared by GitHub and the forum ------------------------------


def release_markdown(r: dict, data: dict, heading: bool) -> str:
    bugs, ideas = d.by_id(data["bugs"]), d.by_id(data["suggestions"])
    out = []
    if heading:
        out += [f"## Replay Suite {r['version']}", ""]
    out += [r["summary"], ""]
    if r.get("update_note"):
        out += [f"**Before you update:** {r['update_note']}", ""]
    for title, items in (
        ("Added", r.get("added") or []),
        ("Changed", r.get("changed") or []),
        ("Fixed", [f"{bugs[b]['title']} ({b})" for b in r.get("fixed") or []]),
        ("Suggested by players", [f"{ideas[s]['title']} ({s})" for s in r.get("shipped_suggestions") or []]),
    ):
        if items:
            out += [f"**{title}**", ""] + [f"- {i}" for i in items] + [""]
    if r.get("firefox_only"):
        out += [f"Firefox only: [Firefox Add-ons]({d.AMO_URL})."]
    else:
        out += [
            "**How to get it**",
            "",
            f"- Firefox: nothing to do, it updates itself from [Firefox Add-ons]({d.AMO_URL}).",
            f"- Chrome and Edge: [download {r['version']}]({d.zip_url(r['version'])}), then follow "
            f"[the updating steps]({d.SITE_URL}updating/). Back up first, and never click Remove.",
        ]
    out += ["", f"All versions: {d.SITE_URL}versions/"]
    return "\n".join(out).strip() + "\n"


def cmd_release(a) -> None:
    data = d.load_all()
    if a.action == "new":
        if any(r["version"] == a.version for r in data["releases"]):
            die(f"{a.version} is already in releases.yml")
        entry = {
            "version": a.version, "date": today(), "summary": a.summary or "",
            "added": [], "changed": [],
            "fixed": sorted(b["id"] for b in data["bugs"] if b.get("fixed_in") == a.version),
            "shipped_suggestions": sorted(s["id"] for s in data["suggestions"] if s.get("shipped_in") == a.version),
            "update_note": "",
        }
        if not entry["summary"]:
            entry = edit_entry(entry)
        no_dash(str(entry), "the release entry")
        releases = [entry] + data["releases"]
        releases.sort(key=lambda r: d.version_key(r["version"]), reverse=True)
        save_checked("releases", releases)
        print(f"✔ {a.version} drafted with {len(entry['fixed'])} fix(es) and "
              f"{len(entry['shipped_suggestions'])} shipped suggestion(s). "
              f"Edit data/releases.yml to add Added/Changed lines, then ./site.py publish.")
    elif a.action == "publish":
        r = next((r for r in data["releases"] if r["version"] == a.version), None)
        if not r:
            die(f"{a.version} is not in releases.yml; run `./site.py release new {a.version}` first")
        if r.get("firefox_only"):
            die(f"{a.version} is marked firefox_only; there is nothing to publish here")
        files = [DIST / d.zip_name(a.version), DIST / d.LATEST_ZIP_NAME]
        for f in files:
            if not f.exists():
                die(f"missing {f}. Run `pnpm release:build {a.version}` in the extension repository.")
        if run(["gh", "release", "view", f"v{a.version}", "--repo", d.REPO], capture_output=True).returncode == 0:
            die(f"v{a.version} already exists on GitHub")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write(release_markdown(r, data, heading=False))
        res = run(["gh", "release", "create", f"v{a.version}", "--repo", d.REPO,
                   "--title", f"Replay Suite {a.version}", "--notes-file", fh.name, "--latest",
                   *map(str, files)])
        os.unlink(fh.name)
        if res.returncode != 0:
            die("gh release create failed")
        print(f"✔ released. Latest download: {d.LATEST_ZIP_URL}")
        print(f"  Next: ./site.py forum release {a.version}   (paste into Thread B)")


def edit_entry(entry: dict) -> dict:
    if not sys.stdin.isatty():
        die("give --summary \"one line\" (no terminal to open an editor in)")
    import yaml
    with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as fh:
        fh.write("# Fill in summary (one line), and added/changed if you like. Save and close.\n")
        yaml.safe_dump(entry, fh, sort_keys=False, allow_unicode=True)
    subprocess.run([os.environ.get("EDITOR", "nano"), fh.name])
    edited = yaml.safe_load(Path(fh.name).read_text())
    os.unlink(fh.name)
    if not edited.get("summary"):
        die("no summary given; nothing saved")
    return d._norm_dates(edited)


# --- forum -------------------------------------------------------------------------


def to_clipboard(text: str) -> None:
    if os.environ.get("RS_NO_CLIPBOARD"):  # forum/check.py renders without touching the clipboard
        return
    for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"]):
        if shutil.which(cmd[0]):
            subprocess.run(cmd, input=text.encode())
            print("(copied to the clipboard)", file=sys.stderr)
            return


def cmd_forum(a) -> None:
    data = d.load_all()
    if a.action == "release":
        r = next((r for r in data["releases"] if r["version"] == a.version), None)
        if not r:
            die(f"{a.version} is not in releases.yml")
        text = release_markdown(r, data, heading=True)
    else:
        latest = d.latest_chrome_release(data)
        open_bugs = [b for b in data["bugs"] if b["status"] in ("open", "investigating")]
        planned = [s for s in data["suggestions"] if s["status"] == "planned"]
        review = [s for s in data["suggestions"] if s["status"] == "under review"]
        # Thread B is an ordinary thread: its author may only edit a post for a while.
        # So this post never depends on editing: it points at the always-current page,
        # and when it is out of date a fresh one is posted as a reply.
        lines = [f"![Status board|690x115]({d.SITE_URL}img/forum/status-header.png)", "",
                 f"**Always up to date on the website: {d.SITE_URL}status/**", "",
                 f"*This post is a snapshot from {d.nice_date(today())}. When it gets old, a fresh one is posted further down the thread.*", ""]
        if latest:
            lines += [f"**Latest version: {latest['version']}** ({latest['summary']})", "",
                      f"- Firefox: updates itself. [Firefox Add-ons]({d.AMO_URL})",
                      f"- Chrome and Edge: [download {latest['version']}]({d.LATEST_ZIP_URL}), "
                      f"then [update like this]({d.SITE_URL}updating/)", ""]
        lines += ["### Known bugs", ""]
        lines += ([f"- **{b['id']}** {b['title']} *({b['status']})*"
                   + (f". Meanwhile: {b['workaround']}" if b.get("workaround") else "") for b in open_bugs]
                  or ["- None known right now."])
        lines += ["", "### Planned, from your suggestions", ""]
        lines += [f"- **{s['id']}** {s['title']}" for s in planned] or ["- Nothing yet."]
        if review:
            lines += ["", "### Being considered", ""]
            lines += [f"- **{s['id']}** {s['title']} *(asked for by {s.get('asked_by', 1)})*" for s in review]
        if data["news"]:
            lines += ["", "### News", ""]
            lines += [f"- {n['date']}: **{n['title']}**. {n.get('body', '')}" for n in data["news"][:3]]
        text = "\n".join(lines) + "\n"
    print(text)
    to_clipboard(text)


# --- check -------------------------------------------------------------------------


class _Text(HTMLParser):
    """Collects what a reader sees: text, plus alt and title attributes."""

    def __init__(self):
        super().__init__()
        self.parts, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        for k, v in attrs:
            if k in ("alt", "title") and v:
                self.parts.append(v)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def cmd_check(a=None) -> bool:
    problems = d.validate(d.load_all())

    sources = [*sorted((ROOT / "docs").rglob("*.md")), ROOT / "mkdocs.yml", ROOT / "coach" / "coach-content.md",
               ROOT / "README.md", ROOT / "LICENSE.md"]
    for f in sources:
        if f.exists() and any(x in f.read_text() for x in d.DASHES):
            problems.append(f"{f.relative_to(ROOT)}: contains an em or en dash")

    with tempfile.TemporaryDirectory() as out:
        res = run([sys.executable, "-m", "mkdocs", "build", "--strict", "--quiet", "-d", out],
                  capture_output=True, text=True)
        if res.returncode != 0:
            problems.append("mkdocs build --strict failed:\n" + (res.stderr or res.stdout)[-2000:])
        else:
            for html in Path(out).rglob("*.html"):
                p = _Text()
                p.feed(html.read_text())
                if d.ACCOUNT.lower() in " ".join(p.parts).lower():
                    problems.append(f"{html.relative_to(out)}: shows the GitHub account name as text")

    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    if re.search(rf"(?<![/\w]){d.ACCOUNT}(?![/\w])", re.sub(r"https?://\S+", "", readme), re.I):
        problems.append("README.md: names the GitHub account outside a URL")

    if problems:
        print("✖ check failed:\n  " + "\n  ".join(problems))
        if a is not None:
            sys.exit(1)
        return False
    print("✔ check passed: data valid, no dashes, account name only in URLs, site builds in strict mode")
    return True


def cmd_publish(a) -> None:
    if not cmd_check():
        sys.exit(1)
    run(["git", "add", "-A"], check=True)
    if run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing to publish")
        return
    run(["git", "commit", "-q", "-m", a.message or f"Update the site, {today()}"], check=True)
    if run(["git", "push", "-q"]).returncode != 0:
        die("push failed")
    print(f"✔ pushed. The site redeploys in about a minute: {d.SITE_URL}")


# --- cli -------------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    bug = sub.add_parser("bug").add_subparsers(dest="action", required=True)
    b = bug.add_parser("add")
    b.add_argument("title")
    b.add_argument("--forum")
    b.add_argument("--affects", nargs="*")
    b.add_argument("--browsers", nargs="*", choices=d.BROWSERS)
    b.add_argument("--workaround")
    b = bug.add_parser("status")
    b.add_argument("id")
    b.add_argument("status", choices=d.BUG_STATUSES)
    b = bug.add_parser("fix")
    b.add_argument("id")
    b.add_argument("--in", dest="version", required=True)

    idea = sub.add_parser("idea").add_subparsers(dest="action", required=True)
    i = idea.add_parser("add")
    i.add_argument("title")
    i.add_argument("--forum")
    i = idea.add_parser("plus")
    i.add_argument("id")
    i = idea.add_parser("status")
    i.add_argument("id")
    i.add_argument("status", choices=d.IDEA_STATUSES)
    i.add_argument("--reason")
    i.add_argument("--in", dest="version")

    n = sub.add_parser("news")
    n.add_argument("title")
    n.add_argument("body")

    rel = sub.add_parser("release").add_subparsers(dest="action", required=True)
    r = rel.add_parser("new")
    r.add_argument("version")
    r.add_argument("--summary")
    r = rel.add_parser("publish")
    r.add_argument("version")

    forum = sub.add_parser("forum").add_subparsers(dest="action", required=True)
    forum.add_parser("status-board")
    f = forum.add_parser("release")
    f.add_argument("version")

    sub.add_parser("check")
    pub = sub.add_parser("publish")
    pub.add_argument("-m", "--message")

    a = p.parse_args()
    {"bug": cmd_bug, "idea": cmd_idea, "news": cmd_news, "release": cmd_release,
     "forum": cmd_forum, "check": cmd_check, "publish": cmd_publish}[a.cmd](a)


if __name__ == "__main__":
    main()
