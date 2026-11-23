#!/usr/bin/env python3
"""Build-time render: write entry.png next to this script."""

import os

from meme import render

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    render(out)
    print("wrote", out)
