#!/usr/bin/env python3
"""Write the Meme Sprint 3 entry image to /output/entry.png.

The meme is rendered from scratch by meme.py (Pillow) whenever Pillow is
available; otherwise the identical entry.png shipped in this repository
is copied, so the entry always produces a valid image. Standard library
only, no network, no input files beyond this repository.
"""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    asset = os.path.join(here, "entry.png")
    if not os.path.isfile(asset) or os.path.getsize(asset) == 0:
        raise SystemExit(f"error: required meme image is missing or empty: {asset}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    try:
        from meme import render

        render(path)
    except Exception:
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(here, "entry.png"), path)


if __name__ == "__main__":
    main()
