#!/usr/bin/env python3
"""Build the web gallery for Isabella's Studio.

Reads every image in figures/Gallery/ and writes web-sized copies plus a
manifest to game/gallery/. Titles and dates come from figures/Gallery/info.json,
which this script also keeps up to date (new images get an entry you can edit).

    python tools/build_gallery.py

Images whose file name starts with "team" are not shown as artworks; the first
one is used as the team photo in the "About the game" panel instead.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "figures" / "Gallery"
OUT = ROOT / "game" / "gallery"
INFO = SRC / "info.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
FULL_PX = 1200   # long side of the picture shown in the viewer
THUMB_PX = 240   # long side of the picture hung on the studio wall


def save_jpeg(im, path, px, quality):
    im = im.copy()
    im.thumbnail((px, px), Image.LANCZOS)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return im.size


def main():
    if not SRC.is_dir():
        sys.exit(f"Finner ikke {SRC}")
    info = json.loads(INFO.read_text(encoding="utf-8")) if INFO.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    keep, items, team = set(), [], None

    for f in sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS):
        data = f.read_bytes()
        h = hashlib.sha1(data).hexdigest()[:10]
        meta = info.setdefault(f.name, {})
        meta.setdefault("title", "")
        meta.setdefault("date", datetime.fromtimestamp(f.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d"))
        with Image.open(f) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            full, thumb = f"g_{h}.jpg", f"g_{h}_t.jpg"
            if not (OUT / full).exists():
                save_jpeg(im, OUT / full, FULL_PX, 82)
            if not (OUT / thumb).exists():
                save_jpeg(im, OUT / thumb, THUMB_PX, 80)
            w, hgt = im.size
        keep.update({full, thumb})
        entry = {"id": f.stem[:40], "file": full, "thumb": thumb, "w": w, "h": hgt,
                 "title": meta.get("title", ""), "date": meta.get("date", ""), "_o": meta.get("order", 999)}
        for lang in ("nb", "zh", "en"):
            if meta.get("title_" + lang):
                entry["title_" + lang] = meta["title_" + lang]
        if f.stem.lower().startswith("team"):
            team = team or entry
        else:
            items.append(entry)

    # newest first; "order" in info.json can pin pictures to the front
    items.sort(key=lambda e: e["date"], reverse=True)
    items.sort(key=lambda e: e["_o"])
    for e in items + ([team] if team else []):
        e.pop("_o", None)

    manifest = {"version": 1, "items": items, "team": team}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    for old in OUT.glob("g_*.jpg"):
        if old.name not in keep:
            old.unlink()
    # drop entries for pictures that were removed, keep the rest
    info = {k: v for k, v in info.items() if (SRC / k).exists()}
    INFO.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(items)} bilder" + (" + teamfoto" if team else "") + f" -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
