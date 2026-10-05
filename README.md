# Finn kattene 🐱🌺

A hide-and-seek game for up to 7 cats, drawn by Isabella. Play it here:
**https://wangyongjie12312.github.io/finn_katten/game/**

- Play alone with robot cats, or together online with a 4-letter room code.
- The house has an attic, a living room, a cellar, a garden – and **Isabella's Studio**
  up in the treehouse, where her pictures hang and every cat can give hearts and notes.
- Norwegian, Chinese and English.

## Adding pictures to Isabella's Studio

1. Put the picture (`.jpg`, `.png` or `.webp`) in `figures/Gallery/`.
2. Optional: give it a title in `figures/Gallery/info.json`
   (`"title"`, `"date"`, and `"order": 1` to hang it first on the wall).
3. Run `python tools/build_gallery.py` (needs `pip install pillow`).
   It writes web-sized copies to `game/gallery/` and adds new pictures to `info.json`.
4. Commit and push – GitHub Pages shows the new pictures a minute later.
A picture whose file name starts with `team` (for example `team.jpg`) replaces the
drawn group photo in "About the game".

## Files

- `game/index.html` – the whole game in one file
- `game/gallery/` – web-sized pictures and `manifest.json` (generated)
- `figures/` – Isabella's original drawings
- `sounds/` – the flower song recordings
- `tools/build_gallery.py` – gallery builder
