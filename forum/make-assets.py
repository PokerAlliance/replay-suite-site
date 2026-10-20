#!/usr/bin/env python3
"""
Every image in the two forum threads, drawn with Pillow.

    python3 forum/make-assets.py            all assets + proof sheets
    python3 forum/make-assets.py hero       just the ones whose name starts with "hero"

Output goes to docs/img/forum/, so every image is published with the site and the
threads can link to it by URL: pasting a thread brings its images along, and
Discourse copies them into its own storage when the post is made.

Rules (PLAN.md section 3.1):

- 1380 px wide, shown at 690 in the post, so text stays sharp on any screen.
- Transparent canvas around self-contained panels with their own fill, border and
  glow. The forum has a light and a dark theme and readers pick; a panel reads on
  both, bare text on transparency does not.
- Words are drawn here, never by an image model: exact text, exact font, no dashes.
- Thread A is locked and cannot be edited, so nothing it shows may go out of date:
  no version numbers, no dates. `check_text` refuses them in Thread A assets.
- Illustrations come from forum/art/ (Codex, see codex-prompts.md). If one is
  missing, a simple drawn stand-in is used so nothing waits on it.

Every asset also gets a proof sheet in forum/proof/: the image on the forum's
white background and on its dark one, side by side, at the size readers see.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
OUT = SITE / "docs" / "img" / "forum"  # published with the site, so the threads link to them
PROOF = HERE / "proof"
ART = HERE / "art"
SHOTS = SITE / "docs" / "img" / "shots"
LOGO = SITE / "docs" / "img" / "logo.png"

W = 1380  # 2x the forum's 690 px post column

# Palette: the extension's own colours (src/styles/tailwind.css)
NAVY_TOP = (0x1E, 0x26, 0x3D)
NAVY_BOTTOM = (0x12, 0x18, 0x29)
PANEL = (0x2F, 0x36, 0x55)
BORDER = (0x4A, 0x57, 0x7C)
TEXT = (0xFF, 0xFF, 0xFF)
MUTED = (0xC4, 0xCC, 0xE0)
ACCENT = (0xDE, 0x1C, 0x3F)
GOLD = (0xF9, 0xD2, 0x76)
GOOD = (0x34, 0xA2, 0x64)

# The forum's two themes, for proof sheets
FORUM_LIGHT = (0xFF, 0xFF, 0xFF)
FORUM_DARK = (0x22, 0x22, 0x22)

FONT_DIR = Path("/usr/share/fonts/truetype/noto")
DASHES = ("—", "–")


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"NotoSans-{weight}.ttf"), size)


def check_text(text: str, evergreen: bool) -> str:
    if any(d in text for d in DASHES):
        raise SystemExit(f"✖ dash in asset text: {text!r}")
    if evergreen and (re.search(r"\b\d+\.\d+(\.\d+)?\b", text) or re.search(r"\b20\d\d\b", text)):
        raise SystemExit(f"✖ Thread A asset text must not hold a version or date: {text!r}")
    return text


# --- building blocks ----------------------------------------------------------------

MARGIN = 28  # transparent room around a panel for its glow


def canvas(h: int) -> Image.Image:
    return Image.new("RGBA", (W, h), (0, 0, 0, 0))


def vgradient(w: int, h: int, top, bottom) -> Image.Image:
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,))
    return im


def panel(im: Image.Image, box, radius=36, top=NAVY_TOP, bottom=NAVY_BOTTOM, border=BORDER, glow=True) -> None:
    """A rounded panel with its own fill, a border, and a soft glow under it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if glow:
        shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((x0, y0 + 8, x1, y1 + 8), radius, fill=(5, 8, 18, 150))
        im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    fill = vgradient(w, h, top, bottom)
    fill.putalpha(mask)
    im.alpha_composite(fill, (x0, y0))
    ImageDraw.Draw(im).rounded_rectangle(box, radius, outline=border + (255,), width=3)


def spade(d: ImageDraw.ImageDraw, cx: int, cy: int, s: int, fill) -> None:
    """A spade made of two circles, a triangle and a stem, s = overall height."""
    r = s * 0.27
    d.polygon([(cx, cy - s * 0.5), (cx - s * 0.47, cy + s * 0.06), (cx + s * 0.47, cy + s * 0.06)], fill=fill)
    for dx in (-r * 0.95, r * 0.95):
        d.ellipse((cx + dx - r, cy - r * 0.2, cx + dx + r, cy + r * 1.8), fill=fill)
    d.polygon([(cx, cy + s * 0.1), (cx - s * 0.2, cy + s * 0.5), (cx + s * 0.2, cy + s * 0.5)], fill=fill)


def text_center(d, cx, y, text, f, fill) -> None:
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


def wrap(d, text: str, f, width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if d.textlength(trial, font=f) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = w
    return lines + ([line] if line else [])


def pill(d, x, y, text, f, fg, bg, outline=None, pad=(26, 12)) -> int:
    """Draws a pill with its left edge at x; returns its width."""
    tw = d.textlength(text, font=f)
    asc, desc = f.getmetrics()
    w, h = tw + pad[0] * 2, asc + desc + pad[1] * 2
    d.rounded_rectangle((x, y, x + w, y + h), h / 2, fill=bg, outline=outline, width=3 if outline else 0)
    d.text((x + pad[0], y + pad[1]), text, font=f, fill=fg)
    return int(w)


def art(name: str, size: int, wide: float = 1.0) -> Image.Image | None:
    """An illustration from forum/art/, fitted to size high and at most size * wide across, or None."""
    path = ART / f"{name}.png"
    if not path.exists():
        return None
    im = Image.open(path).convert("RGBA")
    bbox = im.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    im.thumbnail((round(size * wide), size), Image.LANCZOS)
    return im


def paste_center(im: Image.Image, piece: Image.Image, cx: int, cy: int) -> None:
    im.alpha_composite(piece, (round(cx - piece.width / 2), round(cy - piece.height / 2)))


# --- stand-in icons, used until the Codex art exists --------------------------------


def drawn_icon(kind: str, size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size
    d.ellipse((0, 0, s - 1, s - 1), fill=PANEL + (255,), outline=BORDER + (255,), width=4)
    c = s / 2
    if kind == "records":  # a notebook with a spade
        d.rounded_rectangle((s * .3, s * .22, s * .7, s * .78), 10, fill=(240, 240, 248, 255))
        spade(d, c, c, s * .26, ACCENT)
    elif kind == "replays":  # a play button
        d.polygon([(s * .4, s * .3), (s * .4, s * .7), (s * .72, s * .5)], fill=ACCENT)
    elif kind == "opponents":  # three heads with badges
        for i, x in enumerate((s * .3, s * .5, s * .7)):
            d.ellipse((x - s * .08, s * .3, x + s * .08, s * .46), fill=MUTED)
            d.rounded_rectangle((x - s * .1, s * .52, x + s * .1, s * .62), 6, fill=GOLD if i == 1 else BORDER)
    elif kind == "results":  # rising bars
        for i, h in enumerate((.18, .28, .22, .4)):
            x = s * (.27 + i * .13)
            d.rounded_rectangle((x, s * (.7 - h), x + s * .09, s * .7), 6, fill=GOOD if i == 3 else MUTED)
    elif kind == "play":
        d.polygon([(s * .4, s * .3), (s * .4, s * .7), (s * .72, s * .5)], fill=TEXT)
    return im


def icon(kind: str, size: int) -> Image.Image:
    # Feature icons may be wider than tall (three avatars side by side).
    return art(f"icon-{kind}", size, wide=1.6) or drawn_icon(kind, size)


# --- assets ---------------------------------------------------------------------------
# Each returns (name, image, evergreen). Evergreen assets are used by Thread A.

ASSETS = {}


def asset(fn):
    ASSETS[fn.__name__.replace("_", "-")] = fn
    return fn


@asset
def hero():
    im = canvas(640)
    panel(im, (MARGIN, MARGIN, W - MARGIN, 640 - MARGIN), radius=44)
    d = ImageDraw.Draw(im)
    logo = Image.open(LOGO).convert("RGBA").resize((112, 112), Image.LANCZOS)
    im.alpha_composite(logo, (96, 96))
    d.text((232, 92), check_text("Replay Suite", True), font=font("ExtraBold", 92), fill=TEXT)
    tag = check_text("Every hand you play on ReplayPoker, saved and explained.", True)
    for i, line in enumerate(wrap(d, tag, font("Medium", 46), 700)):
        d.text((100, 240 + i * 62), line, font=font("Medium", 46), fill=MUTED)
    x, f = 100, font("Bold", 34)
    for label, fg, bg, outline in (
        ("Free", (20, 20, 30), GOLD, None),
        ("No account", TEXT, PANEL, BORDER),
        ("Firefox", TEXT, PANEL, BORDER),
        ("Chrome", TEXT, PANEL, BORDER),
        ("Edge", TEXT, PANEL, BORDER),
    ):
        x += pill(d, x, 462, check_text(label, True), f, fg, bg, outline) + 16
    table = art("hero-table", 420)
    if table:
        paste_center(im, table, 1080, 310)
    else:  # a simple felt table with a fan of cards
        d.ellipse((880, 200, 1290, 430), fill=(22, 92, 62), outline=(120, 80, 40), width=14)
        for i, (r, s) in enumerate((("A", ACCENT), ("K", (30, 30, 40)), ("Q", ACCENT))):
            x0 = 1006 + i * 54
            d.rounded_rectangle((x0, 250, x0 + 92, 380), 12, fill=(250, 250, 252), outline=(200, 200, 210), width=2)
            d.text((x0 + 16, 262), r, font=font("Bold", 44), fill=s)
    return im, True


FEATURES = [
    ("records", "Records every hand", "Automatically, while you play."),
    ("replays", "Replays any hand", "Step by step, with the odds."),
    ("opponents", "Reads your opponents", "A small badge under each player."),
    ("results", "Shows how you're doing", "By seat, by tournament, by hand."),
]


def feature_card(kind, title, line):
    h = 620
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=48)
    d = ImageDraw.Draw(im)
    paste_center(im, icon(kind, 260), W // 2, 210)
    text_center(d, W // 2, 380, check_text(title, True), font("ExtraBold", 74), TEXT)
    text_center(d, W // 2, 478, check_text(line, True), font("Medium", 50), MUTED)
    return im, True


for _kind, _title, _line in FEATURES:
    ASSETS[f"feature-{_kind}"] = (lambda k=_kind, t=_title, l=_line: feature_card(k, t, l))


BUTTONS = [
    ("button-firefox", "Firefox", "Install in one click", ACCENT, (255, 214, 222)),
    ("button-chrome-edge", "Chrome and Edge", "Download the latest version", PANEL, MUTED),
    ("button-guide", "Step-by-step guide", "Pictures for every click", PANEL, MUTED),
    ("button-discussion", "Questions, bugs and ideas", "Join the Replay Suite discussion", PANEL, MUTED),
    ("button-versions", "Every version", "What changed, and the downloads", PANEL, MUTED),
]


def button(title, sub, fill, subfill):
    h = 230
    im = canvas(h)
    top = tuple(min(255, c + 18) for c in fill)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=40, top=top, bottom=fill,
          border=GOLD if fill == PANEL else (255, 120, 140))
    d = ImageDraw.Draw(im)
    d.text((96, 52), check_text(title, True), font=font("ExtraBold", 58), fill=TEXT)
    d.text((98, 132), check_text(sub, True), font=font("Medium", 38), fill=subfill)
    # an arrow on the right, so it reads as something to click
    cx, cy = W - 130, h // 2
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=(255, 255, 255, 40))
    im.alpha_composite(ring)
    d = ImageDraw.Draw(im)
    d.line([(cx - 20, cy), (cx + 20, cy)], fill=TEXT, width=8)
    d.line([(cx + 2, cy - 20), (cx + 22, cy), (cx + 2, cy + 20)], fill=TEXT, width=8, joint="curve")
    return im, True


for _name, _title, _sub, _fill, _subfill in BUTTONS:
    ASSETS[_name] = (lambda t=_title, s=_sub, f=_fill, sf=_subfill: button(t, s, f, sf))


@asset
def trust_strip():
    items = [
        ("Not a bot", "It never clicks or plays for you."),
        ("Never sees hidden cards", "Only what is on your screen."),
        ("Nothing leaves your computer", "No account, no server."),
        ("Replay staff know about it", "Free, and it stays free."),
    ]
    h = 600
    im = canvas(h)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=44)
    d = ImageDraw.Draw(im)
    col_w = (W - 2 * MARGIN - 140) // 2
    for i, (title, line) in enumerate(items):
        x = 90 + (i % 2) * (col_w + 40)
        y = 80 + (i // 2) * 250
        d.ellipse((x, y + 6, x + 64, y + 70), fill=GOOD)
        d.line([(x + 16, y + 40), (x + 28, y + 52), (x + 50, y + 24)], fill=TEXT, width=8, joint="curve")
        ty = y
        for ln in wrap(d, check_text(title, True), font("Bold", 44), col_w - 92):
            d.text((x + 92, ty), ln, font=font("Bold", 44), fill=TEXT)
            ty += 56
        for ln in wrap(d, check_text(line, True), font("Regular", 38), col_w - 92):
            d.text((x + 92, ty + 6), ln, font=font("Regular", 38), fill=MUTED)
            ty += 48
    return im, True


@asset
def video_card():
    h = 440
    im = canvas(h)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=44)
    d = ImageDraw.Draw(im)
    cx, cy = 250, h // 2
    d.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), fill=ACCENT, outline=(255, 140, 160), width=6)
    d.polygon([(cx - 30, cy - 52), (cx - 30, cy + 52), (cx + 58, cy)], fill=TEXT)
    d.text((420, 120), check_text("Watch the video tour", True), font=font("ExtraBold", 66), fill=TEXT)
    d.text((424, 214), check_text("Short videos on the Replay Suite website:", True), font=font("Medium", 40), fill=MUTED)
    d.text((424, 266), check_text("installing, updating, and a full walkthrough.", True), font=font("Medium", 40), fill=MUTED)
    return im, True


@asset
def coach_label():
    f = font("Bold", 44)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w = int(probe.textlength("Coach's opinion", font=f)) + 200
    im = Image.new("RGBA", (w, 140), (0, 0, 0, 0))
    panel(im, (16, 16, w - 16, 124), radius=54, top=(0x4A, 0x3E, 0x1E), bottom=(0x2E, 0x26, 0x12), border=GOLD)
    d = ImageDraw.Draw(im)
    spade(d, 84, 66, 50, GOLD)
    d.text((128, 38), check_text("Coach's opinion", True), font=f, fill=GOLD)
    return im, True


def separator(thin: bool):
    h = 90
    im = canvas(h)
    d = ImageDraw.Draw(im)
    y = h // 2
    for x0, x1 in ((120, W // 2 - 70), (W // 2 + 70, W - 120)):
        d.rounded_rectangle((x0, y - 3, x1, y + 3), 3, fill=BORDER if thin else GOLD)
    d.ellipse((W // 2 - 42, y - 42, W // 2 + 42, y + 42), fill=PANEL, outline=GOLD, width=4)
    spade(d, W // 2, y - 2, 40, GOLD)
    return im, True


ASSETS["separator"] = lambda: separator(False)
ASSETS["separator-thin"] = lambda: separator(True)


# Thread B section headers: (number, title, line)
SECTIONS = [
    ("01", "Installing it", "Firefox, Chrome and Edge"),
    ("02", "Your first day", "What happens when you sit down"),
    ("03", "The dashboard", "Every hand, and what it says about your game"),
    ("04", "The replayer", "Watch any hand again, step by step"),
    ("05", "The HUD", "A few numbers about each opponent"),
    ("06", "Settings and your data", "Back up, restore, Retro mode"),
    ("07", "Fair play and privacy", "What it sees, and what it never does"),
    ("08", "Updates, bugs and ideas", "Where to find what changed"),
]


def section_header(num, title, line):
    h = 260
    im = canvas(h)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=40)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((76, 64, 236, h - 64), 30, fill=ACCENT)
    text_center(d, 156, 74, num, font("Black", 74), TEXT)
    d.text((290, 62), check_text(title, False), font=font("ExtraBold", 62), fill=TEXT)
    d.text((292, 146), check_text(line, False), font=font("Medium", 38), fill=MUTED)
    return im, False


for _num, _title, _line in SECTIONS:
    ASSETS[f"section-{_num}"] = (lambda n=_num, t=_title, l=_line: section_header(n, t, l))


@asset
def status_header():
    h = 230
    im = canvas(h)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=40)
    d = ImageDraw.Draw(im)
    d.ellipse((84, 84, 146, 146), fill=GOOD)
    d.text((180, 50), check_text("Status board", False), font=font("ExtraBold", 62), fill=TEXT)
    d.text((182, 132), check_text("Always current on the website. This post is a snapshot.", False), font=font("Medium", 36), fill=MUTED)
    return im, False


# Framed screenshots: the shot in a panel with its caption under it.
FRAMED = [
    ("shot-dashboard", "dashboard-general", "Every hand you play, and what it says about your game", True),
    ("shot-replayer", "replayer-showdown", "Watch any hand again, step by step, with the odds worked out", True),
    ("shot-popup", "popup", "One click on the icon: your library, Retro mode, and the dashboard", True),
    ("shot-analytics", "dashboard-analytics", "Results over time, by stack depth and by blind level", False),
    ("shot-hands", "dashboard-hands", "Every hand in one list. Click one to replay it.", False),
    ("shot-tournaments", "dashboard-tournaments", "Every tournament: entries, results and your best finishes", False),
    ("shot-preflop", "dashboard-preflop", "How you play before the flop, spot by spot", False),
    ("shot-range", "dashboard-range", "Pick a group of starting hands and see how they did for you", False),
    ("shot-viewing-as", "dashboard-viewing-as", "Look at any opponent's numbers from the hands you played together", False),
    ("shot-settings-hud", "options-hud", "Choose what the badge at the table shows", False),
    ("shot-settings-data", "options-data", "Your library, back up and restore", False),
    ("shot-chrome-extensions", "chrome-extensions", "chrome://extensions: Developer mode on, Load unpacked, and the Replay Suite card", False),
]


def framed(shot: str, caption: str, evergreen: bool):
    src = Image.open(SHOTS / f"{shot}.png").convert("RGBA")
    inner_w = W - 2 * MARGIN - 48
    if src.width > inner_w:
        src = src.resize((inner_w, round(src.height * inner_w / src.width)), Image.LANCZOS)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    f = font("Medium", 40)
    lines = wrap(probe, check_text(caption, evergreen), f, W - 2 * MARGIN - 96)
    cap_h = 40 + 54 * len(lines)
    h = MARGIN * 2 + 24 + src.height + cap_h + 24
    im = canvas(h)
    panel(im, (MARGIN, MARGIN, W - MARGIN, h - MARGIN), radius=36)
    x = (W - src.width) // 2
    mask = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.width - 1, src.height - 1), 18, fill=255)
    src.putalpha(mask)
    im.alpha_composite(src, (x, MARGIN + 24))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        text_center(d, W // 2, MARGIN + 24 + src.height + 26 + i * 54, ln, f, MUTED)
    return im, evergreen


# Shots taken by hand at a live table (see planning SHOTS-TO-TAKE.md). Built only
# once the file exists in docs/img/shots/, after its names have been blurred.
BY_HAND = [
    ("shot-hud", "hud-table", "A badge under each player: how they have played against you", True),
]
FRAMED += [entry for entry in BY_HAND if (SHOTS / f"{entry[1]}.png").exists()]

for _name, _shot, _caption, _ever in FRAMED:
    ASSETS[_name] = (lambda s=_shot, c=_caption, e=_ever: framed(s, c, e))


# --- proof sheets -------------------------------------------------------------------------


def proof(name: str, im: Image.Image) -> None:
    """The asset as readers see it (690 px wide) on the light theme and the dark theme."""
    show_w = round(im.width / 2)
    small = im.resize((show_w, round(im.height / 2)), Image.LANCZOS)
    pad = 40
    sheet = Image.new("RGBA", (2 * (show_w + 2 * pad), small.height + 2 * pad), (0, 0, 0, 255))
    for i, bg in enumerate((FORUM_LIGHT, FORUM_DARK)):
        tile = Image.new("RGBA", (show_w + 2 * pad, small.height + 2 * pad), bg + (255,))
        tile.alpha_composite(small, (pad, pad))
        sheet.alpha_composite(tile, (i * (show_w + 2 * pad), 0))
    sheet.convert("RGB").save(PROOF / f"{name}.png", optimize=True)


def main(prefixes: list[str]) -> None:
    OUT.mkdir(exist_ok=True)
    PROOF.mkdir(exist_ok=True)
    made = 0
    for name, fn in ASSETS.items():
        if prefixes and not any(name.startswith(p) for p in prefixes):
            continue
        im, evergreen = fn()
        alpha = im.getchannel("A").getextrema()
        if alpha[0] != 0:
            raise SystemExit(f"✖ {name}: no transparent edge; panels must sit on a transparent canvas")
        im.save(OUT / f"{name}.png", optimize=True)
        proof(name, im)
        kb = (OUT / f"{name}.png").stat().st_size // 1024
        print(f"  {name:22} {im.width}x{im.height}  {kb:4} KB  {'Thread A' if evergreen else 'Thread B'}")
        made += 1
    print(f"✔ {made} assets in docs/img/forum, proof sheets in forum/proof")
    waiting = [e[1] for e in BY_HAND if not (SHOTS / f"{e[1]}.png").exists()]
    if waiting:
        print(f"  waiting for hand-taken shots: {', '.join(waiting)}")


if __name__ == "__main__":
    main(sys.argv[1:])
