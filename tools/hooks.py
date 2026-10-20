"""
MkDocs hooks for the site.

The "On this page" panel only earns its space when a page has three or more
sections; on shorter pages it is an empty column, so it is hidden.
"""

MIN_SECTIONS = 3


def on_page_context(context, page, config, nav):
    # page.toc holds the h1; its children are the h2 sections
    sections = sum(len(h1.children) for h1 in page.toc)
    hide = page.meta.setdefault("hide", [])
    if sections < MIN_SECTIONS and "toc" not in hide:
        hide.append("toc")
    return context
