"""Bake the archive photo treatment for the local redesign preview.

Each source photo becomes:
  <name>.duo.jpg   greyscale mapped navy (shadows) -> cream (highlights), max 1200px
  <name>.orig.jpg  colour original, max 1200px, for the hover/full view

Sources: the git-ignored intake folder plus photos already published under public/media.
Output: preview/media/ (git-ignored; intake photos are not cleared for publishing).
"""
import json, os, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTAKE = os.path.join(ROOT, "data", "intake", "2026-10-26-kevan-photos")
PUBLIC = os.path.join(ROOT, "public", "media")
OUT = os.path.join(ROOT, "preview", "media")
INK, PAPER = (19, 33, 58), (243, 238, 226)
PUBLISHED = ["rod-carew-hillside.jpg", "panama-rod-carew-rail.jpg", "coach-cage.jpg", "dugout.jpg"]


def bake(src, stem):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1200, 1200), Image.LANCZOS)
    im.save(os.path.join(OUT, stem + ".orig.jpg"), quality=86, optimize=True)
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
    ImageOps.colorize(g, black=INK, white=PAPER, mid=(150, 140, 128)).save(
        os.path.join(OUT, stem + ".duo.jpg"), quality=84, optimize=True)


BATCH = os.path.join(ROOT, "data", "intake", "2026-10-26-onedrive-batch")
SKIP = {"b10", "b11", "b27"}  # b10/b11 show children (need a parent's yes); b27 is a blank render
LOGOS = {"b28", "b29", "b30", "b31"}  # AI-made logo concepts, shown as-is


def key_out_checker(src, dst):
    """b31 has a fake checkerboard drawn in; make light, low-saturation pixels transparent."""
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if min(r, g, b) > 185 and max(r, g, b) - min(r, g, b) < 18:
                px[x, y] = (r, g, b, 0)
    im.thumbnail((512, 512), Image.LANCZOS)
    im.save(dst)


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(INTAKE)):
        if f.lower().endswith(".jpg"):
            bake(os.path.join(INTAKE, f), "k" + os.path.splitext(f)[0]); n += 1
    for f in PUBLISHED:
        bake(os.path.join(PUBLIC, f), os.path.splitext(f)[0]); n += 1
    hashes = {}
    for line in open(os.path.join(BATCH, "hashes.tsv"), encoding="utf-8"):
        name, size, sha, folder = line.rstrip("\n").split("\t")
        hashes[os.path.splitext(name)[0]] = {"file": name, "bytes": int(size), "sha256": sha, "folder": folder}
    for stem, meta in sorted(hashes.items()):
        src = os.path.join(BATCH, meta["file"])
        if stem in SKIP:
            continue
        if stem in LOGOS:
            im = Image.open(src).convert("RGB"); im.thumbnail((800, 800), Image.LANCZOS)
            im.save(os.path.join(OUT, stem + ".logo.jpg"), quality=88)
        else:
            bake(src, stem)
        n += 1
    key_out_checker(os.path.join(BATCH, "b31.png"), os.path.join(OUT, "mark.png"))
    json.dump(hashes, open(os.path.join(OUT, "hashes.json"), "w"), indent=1)
    print(f"baked {n} photos into {OUT}")


if __name__ == "__main__":
    sys.exit(main())
