"""
The site's data: loading, validating, writing back, and the URLs built from it.

Used by `site.py` (the command you run) and by `main.py` (the mkdocs-macros
module that renders the Versions and Status pages), so a rule is written once
and both enforce it.

The five files in data/ are the single source of truth. The site pages, the
forum status board and every release announcement are generated from them.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- URLs ---------------------------------------------------------------------
# The account name appears in these URLs and nowhere else on the site.

REPO = "PokerAlliance/replay-suite-site"
SITE_URL = "https://pokeralliance.github.io/replay-suite-site/"
AMO_URL = "https://addons.mozilla.org/en-US/firefox/addon/replay-suite/"
LATEST_ZIP_NAME = "replay-suite-chrome.zip"
LATEST_ZIP_URL = f"https://github.com/{REPO}/releases/latest/download/{LATEST_ZIP_NAME}"


def zip_name(version: str) -> str:
    return f"replay-suite-{version}-chrome.zip"


def zip_url(version: str) -> str:
    return f"https://github.com/{REPO}/releases/download/v{version}/{zip_name(version)}"


# --- vocabulary ------------------------------------------------------------------

BUG_STATUSES = ["open", "investigating", "fixed", "not a bug"]
IDEA_STATUSES = ["under review", "planned", "shipped", "not planned"]
BROWSERS = ["chrome", "edge", "firefox"]

# Field order when a file is written back, so hand edits and script edits look alike.
FIELDS = {
    "releases": ["version", "date", "firefox_only", "summary", "added", "changed",
                 "fixed", "shipped_suggestions", "update_note"],
    "bugs": ["id", "title", "status", "affects", "browsers", "workaround",
             "fixed_in", "reported", "forum"],
    "suggestions": ["id", "title", "status", "shipped_in", "reason", "asked_by",
                    "reported", "forum"],
    "news": ["date", "title", "body"],
    "videos": ["id", "title", "url", "duration", "description"],
}

HEADERS = {
    "releases": """# Every release, newest first. Rendered on the Versions page.
# `fixed` lists bug ids (from bugs.yml); `shipped_suggestions` lists suggestion ids.
# `firefox_only: true` means there was no Chrome/Edge zip for that version.
# Writing rule: no em dashes or en dashes anywhere. `./site.py check` enforces it.
""",
    "bugs": """# Known bugs, as reported on the Replay forum. Rendered on the Status page.
# status: open | investigating | fixed | not a bug
# Titles are plain English, as a player would describe the problem.
# Easiest edit: ./site.py bug add "..." --forum URL      ./site.py bug fix B-001 --in 4.0.2
""",
    "suggestions": """# Suggestions from the Replay forum. Rendered on the Status page.
# status: under review | planned | shipped | not planned  ("not planned" needs a reason)
# Easiest edit: ./site.py idea add "..." --forum URL      ./site.py idea plus S-001
""",
    "news": """# Short news items, newest first. Shown on the Status page and the home page.
""",
    "videos": """# Videos, in the order they appear on the Videos page. Empty until they are recorded.
""",
}

DASHES = ("—", "–")  # em dash, en dash
ACCOUNT = "PokerAlliance"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def nice_date(iso: str) -> str:
    """2026-10-20 as 20 October 2026, the way the site and the forum write dates."""
    day = dt.date.fromisoformat(iso)
    return f"{day.day} {day.strftime('%B %Y')}"


def version_key(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("."))


# --- load / save ---------------------------------------------------------------


def _norm_dates(value):
    """PyYAML turns 2026-10-20 into a date; keep everything as ISO strings."""
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()[:10]
    if isinstance(value, list):
        return [_norm_dates(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm_dates(v) for k, v in value.items()}
    return value


def load(name: str) -> list[dict]:
    path = DATA / f"{name}.yml"
    if not path.exists():
        return []
    try:
        items = yaml.safe_load(path.read_text()) or []
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" near line {mark.line + 1}" if mark else ""
        raise SystemExit(f"✖ data/{name}.yml is not valid YAML{where}. "
                         f"Check the indentation and that each entry starts with '- '.") from None
    return _norm_dates(items)


def load_all() -> dict[str, list[dict]]:
    return {name: load(name) for name in FIELDS}


class _Dumper(yaml.SafeDumper):
    pass


ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _str(dumper, data):
    if ISO_DATE.match(data):  # written bare, read back as a date, normalised by load()
        return dumper.represent_scalar("tag:yaml.org,2002:timestamp", data)
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_Dumper.add_representer(str, _str)


def save(name: str, items: list[dict]) -> None:
    order = FIELDS[name]
    ordered = [{k: item[k] for k in order if k in item} | {k: v for k, v in item.items() if k not in order}
               for item in items]
    body = yaml.dump(ordered, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100) if ordered else "[]\n"
    (DATA / f"{name}.yml").write_text(HEADERS[name] + "\n" + body)


# --- lookups ---------------------------------------------------------------------


def by_id(items: list[dict]) -> dict[str, dict]:
    return {i["id"]: i for i in items}


def latest_release(data: dict) -> dict | None:
    rel = sorted(data["releases"], key=lambda r: version_key(r["version"]), reverse=True)
    return rel[0] if rel else None


def latest_chrome_release(data: dict) -> dict | None:
    rel = [r for r in data["releases"] if not r.get("firefox_only")]
    rel.sort(key=lambda r: version_key(r["version"]), reverse=True)
    return rel[0] if rel else None


# --- validation ------------------------------------------------------------------


def _strings(value, where: str):
    if isinstance(value, str):
        yield where, value
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _strings(v, f"{where}[{i}]")
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _strings(v, f"{where}.{k}")


def _iso(value) -> bool:
    try:
        dt.date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def validate(data: dict) -> list[str]:
    """Every problem in the data, as readable lines. Empty means valid."""
    errors: list[str] = []
    bugs, ideas = by_id(data["bugs"]), by_id(data["suggestions"])

    for name, items in data.items():
        if not isinstance(items, list):
            errors.append(f"{name}.yml must be a list")
            continue
        for where, text in _strings(items, name):
            if any(d in text for d in DASHES):
                errors.append(f"{where}: contains an em or en dash: {text[:60]!r}")
            if ACCOUNT.lower() in text.lower() and "://" not in text:
                errors.append(f"{where}: names the GitHub account outside a URL")

    seen = set()
    for r in data["releases"]:
        v = r.get("version", "")
        tag = f"releases {v or '?'}"
        if not VERSION_RE.match(str(v)):
            errors.append(f"{tag}: version must look like 4.0.1")
        if v in seen:
            errors.append(f"{tag}: duplicate version")
        seen.add(v)
        if not _iso(r.get("date")):
            errors.append(f"{tag}: date must be YYYY-MM-DD")
        if not r.get("summary"):
            errors.append(f"{tag}: summary is empty")
        for bid in r.get("fixed") or []:
            if bid not in bugs:
                errors.append(f"{tag}: fixed lists {bid}, which is not in bugs.yml")
        for sid in r.get("shipped_suggestions") or []:
            if sid not in ideas:
                errors.append(f"{tag}: shipped_suggestions lists {sid}, which is not in suggestions.yml")
    versions = [r["version"] for r in data["releases"] if VERSION_RE.match(str(r.get("version", "")))]
    if versions != sorted(versions, key=version_key, reverse=True):
        errors.append("releases.yml must be newest first")

    for kind, items, pattern, statuses, done_field in (
        ("bugs", data["bugs"], r"^B-\d{3}$", BUG_STATUSES, "fixed_in"),
        ("suggestions", data["suggestions"], r"^S-\d{3}$", IDEA_STATUSES, "shipped_in"),
    ):
        ids = set()
        for item in items:
            iid = item.get("id", "?")
            if not re.match(pattern, str(iid)):
                errors.append(f"{kind} {iid}: bad id")
            if iid in ids:
                errors.append(f"{kind} {iid}: duplicate id")
            ids.add(iid)
            if not item.get("title"):
                errors.append(f"{kind} {iid}: title is empty")
            if item.get("status") not in statuses:
                errors.append(f"{kind} {iid}: status must be one of {statuses}")
            done = item.get(done_field)
            if done and not VERSION_RE.match(str(done)):
                errors.append(f"{kind} {iid}: {done_field} must be a version")
            if item.get("status") in ("fixed", "shipped") and not done:
                errors.append(f"{kind} {iid}: status {item['status']} needs {done_field}")
            if item.get("reported") and not _iso(item["reported"]):
                errors.append(f"{kind} {iid}: reported must be YYYY-MM-DD")
            forum = item.get("forum") or ""
            if forum and not forum.startswith("https://"):
                errors.append(f"{kind} {iid}: forum must be an https link")
        if kind == "bugs":
            for item in items:
                bad = set(item.get("browsers") or []) - set(BROWSERS)
                if bad:
                    errors.append(f"bugs {item.get('id')}: unknown browsers {sorted(bad)}")
        else:
            for item in items:
                if item.get("status") == "not planned" and not item.get("reason"):
                    errors.append(f"suggestions {item.get('id')}: 'not planned' needs a reason")
                if not isinstance(item.get("asked_by", 1), int) or item.get("asked_by", 1) < 1:
                    errors.append(f"suggestions {item.get('id')}: asked_by must be a whole number, 1 or more")

    for n in data["news"]:
        if not _iso(n.get("date")) or not n.get("title"):
            errors.append(f"news {n.get('title', '?')}: needs a date and a title")

    for v in data["videos"]:
        if not str(v.get("url", "")).startswith("https://"):
            errors.append(f"videos {v.get('id', '?')}: url must be https")

    return errors
