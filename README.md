# Replay Suite

Replay Suite is a free browser add-on for ReplayPoker, made by Badr (aka ThonBl7ror). It records your hands as you play, lets you replay any of them, shows how you are doing, and puts a few numbers about each opponent at the table. Nothing leaves your computer.

**Website, install guide and downloads:** https://pokeralliance.github.io/replay-suite-site/
**Firefox:** https://addons.mozilla.org/en-US/firefox/addon/replay-suite/
**Chrome and Edge:** the newest zip is on the [Releases](../../releases/latest) page; the website explains how to install and update it.

This repository holds the website, the release downloads, and the lists of known bugs and player suggestions. It does not hold the add-on's source code, which is private. Replay Suite is free to use under the [licence](LICENSE.md). It is not affiliated with ReplayPoker.

## Keeping the site up to date

Everything on the Versions and Status pages comes from `data/*.yml`. Three ways to change it:

1. Edit a file in `data/` on github.com and commit. The site rebuilds in about a minute.
2. `./site.py` on your computer (run `./site.py -h` for every command).
3. In Claude Code, `/triage` and paste forum posts.

First-time setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Preview with `.venv/bin/mkdocs serve`.

Writing rule for everything on the site: no em dashes or en dashes. `./site.py check` enforces it.
