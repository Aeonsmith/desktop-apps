#!/usr/bin/env python3
"""Generates synergy_icon.ico for the Synergy Saber app - a glowing cross-saber / spark icon."""

import math
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
BG = (5, 6, 10, 255)
SABER_GREEN = (57, 255, 136, 255)
SABER_PURPLE = (122, 92, 255, 255)
SPARK_CORE = (255, 255, 255, 255)


def build_icon():
    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    margin = 35
    # Purple saber diagonal \
    draw.line(
        [(margin, margin), (SIZE - margin, SIZE - margin)],
        fill=SABER_PURPLE,
        width=14,
    )
    # Green saber diagonal /
    draw.line(
        [(margin, SIZE - margin), (SIZE - margin, margin)],
        fill=SABER_GREEN,
        width=14,
    )

    # Glowing center clash/spark
    cx, cy = SIZE / 2, SIZE / 2
    r = 22
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SPARK_CORE)

    # 4 spark spikes
    spike_len = 38
    draw.line([(cx - spike_len, cy), (cx + spike_len, cy)], fill=SPARK_CORE, width=5)
    draw.line([(cx, cy - spike_len), (cx, cy + spike_len)], fill=SPARK_CORE, width=5)

    return img


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    icon = build_icon()
    out_path = out_dir / "synergy_icon.ico"
    icon.save(out_path, sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
    print(f"wrote {out_path}")
