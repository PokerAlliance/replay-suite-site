# Codex illustration prompts

The illustrations in `forum/art/` come from these prompts, generated with the Codex CLI
(`codex exec`, image generation). Words never come from the image model: every label is
drawn by `make-assets.py`.

Codex saves into `~/.codex/generated_images/<session>/`; copy each result into
`forum/art/` under the name given here, then run `python3 forum/make-assets.py`.

**Shared style (append to every prompt):** flat, modern app-icon illustration, soft
rounded shapes, gentle highlights, palette deep navy #2f3655, crimson #de1c3f, warm gold
#f9d276, white highlights. Transparent background, no text, no letters, no numbers, no
frame. Square, at least 1024 px, subject centred with some empty space around it.

| File | Prompt |
|---|---|
| `icon-records.png` | A small navy notebook with a red spade on its cover and a gold pen beside it. |
| `icon-replays.png` | Three playing cards fanned out, with a round crimson play button in front of them. |
| `icon-opponents.png` | Three friendly, faceless player avatars side by side, each with a small rounded gold badge under it. |
| `icon-results.png` | A rising bar chart of four rounded bars with a small gold upward arrow and a poker chip at its foot. |
| `icon-export.png` | A stack of three playing cards with a red spade on the top card, and a curved gold arrow leaving the stack towards a small navy document page, suggesting hands being exported to other software. |
| `hero-table.png` | A green felt poker table seen from slightly above, oval, with a polished wooden rail, a few chip stacks and three face down cards, soft glow under the table. |
