#!/usr/bin/env python3
"""
Turns the thread templates into paste-ready posts, and refuses anything unsafe to post.

    python3 forum/check.py            render and check both threads
    python3 forum/check.py --offline  skip the link and live-image checks

Writes forum/out/thread-a.md, thread-b-deep-dive.md and thread-b-status.md.

Thread A is locked once posted and only moderators can change it, so it gets one
chance. This script is the gate. It fails on:

  - a template tag left unfilled, or an image or coach card that does not exist
  - an em or en dash anywhere
  - the GitHub account name outside a URL
  - in Thread A: any version number or date (it must never go out of date)
  - in Thread A: no Thread B address yet (post Thread B first, then put its
    address in forum/thread-b-url.txt)
  - any link that does not answer, and any image whose live copy on the site
    differs from the one here (publish the site first: the posts load images from it)

Images are linked from the website rather than uploaded by hand: pasting a post
brings its images along, and Discourse copies them into its own storage.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
sys.path.insert(0, str(SITE / "tools"))
import rsdata as d  # noqa: E402

IMG = SITE / "docs" / "img" / "forum"
OUT = HERE / "out"
COACH = SITE / "coach" / "coach-content.md"
THREAD_B_URL_FILE = HERE / "thread-b-url.txt"

TARGETS = {"amo": d.AMO_URL, "latest-zip": d.LATEST_ZIP_URL}
POSTS = [
    ("thread-a", HERE / "thread-a-showcase.md", True),
    ("thread-b-deep-dive", HERE / "thread-b-deep-dive.md", False),
]
DASHES = ("—", "–")
URL_RE = re.compile(r"https?://[^\s)\]*]+")

problems: list[str] = []
images_used: dict[str, list[str]] = {}


def img_url(name: str) -> str:
    return f"{d.SITE_URL}img/forum/{name}.png"


def img_markup(name: str, alt: str, post: str) -> str:
    path = IMG / f"{name}.png"
    if not path.exists():
        problems.append(f"{post}: image {name}.png does not exist yet (python3 forum/make-assets.py)")
        return f"![{alt}](MISSING:{name})"
    w, h = Image.open(path).size
    images_used.setdefault(post, []).append(name)
    alt = alt.replace("|", " ").replace("]", "").replace("[", "")
    return f"![{alt}|{w // 2}x{h // 2}]({img_url(name)})"


def target_url(target: str, post: str) -> str:
    if target == "thread-b":
        url = THREAD_B_URL_FILE.read_text().strip() if THREAD_B_URL_FILE.exists() else ""
        if not url:
            problems.append(f"{post}: no Thread B address yet. Post Thread B, then put its address in "
                            "forum/thread-b-url.txt")
            return "THREAD-B-URL"
        return url
    if target in TARGETS:
        return TARGETS[target]
    return d.SITE_URL + target


def coach_card(title: str, post: str) -> str:
    text = COACH.read_text()
    m = re.search(rf"^### Card: {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    if not m:
        problems.append(f"{post}: no coach card titled {title!r} in coach/coach-content.md")
        return ""
    body = m.group(1).strip()
    label = img_markup("coach-label", "Coach's opinion", post)
    return f"> {label}\n>\n> " + body.replace("\n\n", "\n>\n> ").replace("\n", "\n> ").replace("> > ", "> ")


def render(src: Path, post: str) -> str:
    text = re.sub(r"<!--.*?-->\s*", "", src.read_text(), flags=re.S)  # notes for us, not for readers
    text = re.sub(r"\{\{img:([\w-]+)\|([^}]*)\}\}", lambda m: img_markup(m[1], m[2], post), text)
    text = re.sub(r"\{\{link-img:([\w-]+)\|([^|}]*)\|([^}]*)\}\}",
                  lambda m: f"[{img_markup(m[1], m[2], post)}]({target_url(m[3], post)})", text)
    text = re.sub(r"\{\{site:([^}]*)\}\}", lambda m: d.SITE_URL + m[1], text)
    text = re.sub(r"\{\{coach:([^}]*)\}\}", lambda m: coach_card(m[1], post), text)
    for left in re.findall(r"\{\{[^}]*\}\}", text):
        problems.append(f"{post}: unfilled tag {left}")
    return text.strip() + "\n"


def prose(text: str) -> str:
    """What a reader sees as words: the post without its URLs."""
    return URL_RE.sub(" ", text)


def check_text(post: str, text: str, evergreen: bool) -> None:
    words = prose(text)
    for dash in DASHES:
        if dash in words:
            line = next(l for l in text.splitlines() if dash in l)
            problems.append(f"{post}: dash in {line.strip()[:70]!r}")
    if d.ACCOUNT.lower() in words.lower():
        problems.append(f"{post}: the GitHub account name appears outside a URL")
    if evergreen:
        for pattern, what in ((r"\b\d+\.\d+\.\d+\b", "a version number"), (r"\b20\d\d\b", "a year")):
            m = re.search(pattern, words)
            if m:
                problems.append(f"{post}: Thread A holds {what} ({m[0]}); it would go out of date")


def fetch(url: str, method: str = "GET") -> tuple[int, bytes]:
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "replay-suite-forum-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, (r.read() if method == "GET" else b"")
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001
        return 0, str(e).encode()


def check_online(posts: dict[str, str]) -> None:
    urls = sorted({u.rstrip(".,") for text in posts.values() for u in URL_RE.findall(text)})
    for url in urls:
        if "/img/forum/" in url:
            continue  # checked below, byte for byte
        if url == "THREAD-B-URL":
            continue
        status, _ = fetch(url, "HEAD")
        if status in (403, 405):  # some sites refuse HEAD
            status, _ = fetch(url)
        if status != 200:
            problems.append(f"link does not answer ({status}): {url}")
    for name in sorted({n for names in images_used.values() for n in names}):
        status, body = fetch(img_url(name))
        local = (IMG / f"{name}.png").read_bytes()
        if status != 200:
            problems.append(f"image not on the live site yet ({status}): {name}.png. Publish the site first.")
        elif hashlib.sha256(body).digest() != hashlib.sha256(local).digest():
            problems.append(f"live copy of {name}.png differs from this one. Publish the site first.")


def status_post() -> str:
    res = subprocess.run([sys.executable, str(SITE / "site.py"), "forum", "status-board"],
                         capture_output=True, text=True, env={"RS_NO_CLIPBOARD": "1", "PATH": "/usr/bin:/bin"})
    if res.returncode != 0:
        problems.append(f"site.py forum status-board failed: {res.stderr.strip()[:200]}")
    return res.stdout


def main() -> None:
    offline = "--offline" in sys.argv
    OUT.mkdir(exist_ok=True)
    rendered = {}
    for post, src, evergreen in POSTS:
        text = render(src, post)
        check_text(post, text, evergreen)
        rendered[post] = text
    rendered["thread-b-status"] = status_post()
    check_text("thread-b-status", rendered["thread-b-status"], False)
    if not offline:
        check_online(rendered)

    # Written even when something is wrong, so the preview can be looked at, but
    # then with a banner nobody could paste past without noticing.
    banner = (f"**NOT READY TO POST: {len(problems)} problem(s). Run python3 forum/check.py**\n\n"
              if problems else "")
    for post, text in rendered.items():
        (OUT / f"{post}.md").write_text(banner + text)

    print("Rendered into forum/out/:")
    for post, text in rendered.items():
        print(f"  {post}.md   {len(text.split())} words, {len(images_used.get(post, []))} images")
    if problems:
        print(f"\n✖ {len(problems)} problem(s). Do not post until they are fixed:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\n✔ safe to post" + (" (links and live images NOT checked: --offline)" if offline else ""))
    print("""
Posting order:
  1. Thread B: new topic in General Poker Discussion. Title: Replay Suite: questions, bugs, ideas and the full walkthrough
     Paste forum/out/thread-b-deep-dive.md. Check the preview (light and dark). Post.
  2. Thread B, reply: paste forum/out/thread-b-status.md. Post.
  3. Put Thread B's address in forum/thread-b-url.txt and run this again.
  4. Thread A: new topic in General Poker Discussion. Title: Replay Suite: a free hand tracker for Replay (Firefox, Chrome, Edge)
     Paste forum/out/thread-a.md. Check the preview. Post. Then send staff the lock request (forum/moderator-kit.md).""")


if __name__ == "__main__":
    main()
