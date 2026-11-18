#!/usr/bin/env python3
"""Generates icon.ico for the Q999 app - a six-node hex network glyph."""

import math
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
BG = (5, 6, 10, 255)
NODE = (57, 255, 136, 255)
LINE = (122, 92, 255, 200)
CENTER = (255, 255, 255, 255)


def build_icon():
    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE / 2, SIZE / 2
    radius = SIZE * 0.34
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 90)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))

    # spokes from center to each node
    for (x, y) in points:
        draw.line([(cx, cy), (x, y)], fill=LINE, width=4)

    # ring connecting the six nodes
    for i in range(6):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % 6]
        draw.line([(x1, y1), (x2, y2)], fill=LINE, width=3)

    node_r = SIZE * 0.045
    for (x, y) in points:
        draw.ellipse([x - node_r, y - node_r, x + node_r, y + node_r], fill=NODE)

    center_r = SIZE * 0.06
    draw.ellipse(
        [cx - center_r, cy - center_r, cx + center_r, cy + center_r],
        fill=CENTER,
    )

    return img


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    icon = build_icon()
    out_path = out_dir / "icon.ico"
    icon.save(out_path, sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
    print(f"wrote {out_path}")
