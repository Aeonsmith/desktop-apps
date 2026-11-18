#!/usr/bin/env python3
"""
Q999 Relay - takes a Q999 certificate hash and repurposes it three ways.

1. Lookup - searches local certificates/ for a matching hash and shows
   that draw's original details (source, node, timestamp).
2. Badge  - deterministically renders the hash's own bytes as a unique
   identicon. The same hash always produces the same image.
3. Relay  - deterministically derives a new, reproducible node pick from
   the hash's bytes (byte[0] % 6) - an auditable "child" outcome, not a
   fresh quantum draw.

This is a companion hobby/art tool, not a harm simulator: nodes are just
labeled outcomes, comparable to rolling a die. Standalone script, run
with `python q999_relay.py` (or `pythonw q999_relay.py` for no console
window). No packaging/exe - paste a hash and click ANALYZE.
"""

import hashlib
import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import font as tkfont

from PIL import Image, ImageDraw, ImageTk

sys.path.insert(0, str(Path(__file__).resolve().parent))

from q999 import CERT_DIR, NODES  # noqa: E402

BG = "#05060a"
FG = "#39ff88"
ACCENT = "#7a5cff"
MUTED = "#8a93a6"
PANEL = "#10121b"

HASH_LEN = 64  # sha256 hex length

state = {"badge_image": None, "badge_photo": None}


def clean_hash(raw):
    return "".join(raw.split()).lower()


def get_seed_bytes(hash_hex):
    """Use the hash's own bytes as entropy; fall back to re-hashing if the
    pasted text isn't valid hex (e.g. wrong length or stray characters)."""
    try:
        return bytes.fromhex(hash_hex)
    except ValueError:
        return hashlib.sha256(hash_hex.encode("utf-8")).digest()


def find_local_certificate(hash_hex):
    if not CERT_DIR.exists():
        return None
    for path in CERT_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("certificate_hash", "").lower() == hash_hex:
            data["_source_file"] = path
            return data
    return None


def render_badge(seed_bytes, size=176, cells=8):
    """Deterministic identicon: same seed bytes always -> same image."""
    img = Image.new("RGB", (size, size), (5, 6, 10))
    draw = ImageDraw.Draw(img)
    cell = size // cells
    accent = (
        seed_bytes[0],
        120 + seed_bytes[1 % len(seed_bytes)] % 120,
        180 + seed_bytes[2 % len(seed_bytes)] % 76,
    )

    half = cells // 2
    idx = 0
    for y in range(cells):
        for x in range(half):
            bit = seed_bytes[idx % len(seed_bytes)] & 1
            idx += 1
            if bit:
                x0, y0 = x * cell, y * cell
                x1, y1 = x0 + cell, y0 + cell
                draw.rectangle([x0, y0, x1, y1], fill=accent)
                mx0, mx1 = size - x1, size - x0
                draw.rectangle([mx0, y0, mx1, y1], fill=accent)
    return img


def relay_pick(seed_bytes):
    index = seed_bytes[0] % len(NODES)
    return index, NODES[index]


def do_analyze():
    hash_hex = clean_hash(hash_entry.get())
    warnings = []

    if len(hash_hex) != HASH_LEN or any(c not in "0123456789abcdef" for c in hash_hex):
        warnings.append(f"input is not a standard {HASH_LEN}-char hex hash")

    match = find_local_certificate(hash_hex)
    if match:
        lookup_var.set(
            f"FOUND: node {match.get('node_number')}/6 -> {match.get('node')}\n"
            f"source: {match.get('source')}\n"
            f"raw value: {match.get('raw_value')}\n"
            f"timestamp: {match.get('timestamp_utc')}\n"
            f"file: {match['_source_file'].name}"
        )
    else:
        lookup_var.set("no local certificate matches this hash")

    seed_bytes = get_seed_bytes(hash_hex)

    try:
        badge_img = render_badge(seed_bytes)
        state["badge_image"] = badge_img
        state["badge_photo"] = ImageTk.PhotoImage(badge_img)
        badge_canvas.itemconfig(badge_item, image=state["badge_photo"])
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"badge error: {exc}")

    index, node = relay_pick(seed_bytes)
    relay_var.set(
        f"RELAY PICK: node {index + 1}/6 -> {node}\n"
        f"formula: seed_bytes[0] % 6, seed = hash bytes (deterministic, reproducible)"
    )

    status_var.set("; ".join(warnings) if warnings else "analysis complete")


def do_paste():
    try:
        hash_entry.delete(0, tk.END)
        hash_entry.insert(0, root.clipboard_get())
        status_var.set("pasted from clipboard")
    except tk.TclError:
        status_var.set("clipboard is empty")


def do_save_badge():
    img = state.get("badge_image")
    if img is None:
        status_var.set("analyze a hash first")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG image", "*.png")],
        initialfile="q999_badge.png",
    )
    if path:
        img.resize((512, 512), Image.NEAREST).save(path)
        status_var.set(f"badge saved to {path}")


root = tk.Tk()
root.title("Q999 Relay")
root.configure(bg=BG)
root.geometry("480x700")
root.resizable(False, False)

title_font = tkfont.Font(family="Consolas", size=20, weight="bold")
mono_font = tkfont.Font(family="Consolas", size=10)

tk.Label(root, text="Q999 RELAY", font=title_font, fg=FG, bg=BG).pack(pady=(20, 2))
tk.Label(
    root,
    text="paste a certificate hash: lookup . badge . relay",
    font=mono_font,
    fg=MUTED,
    bg=BG,
).pack()

entry_frame = tk.Frame(root, bg=BG)
entry_frame.pack(pady=14, fill="x", padx=20)

hash_entry = tk.Entry(
    entry_frame, font=mono_font, bg=PANEL, fg="white", insertbackground="white", bd=0
)
hash_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

tk.Button(
    entry_frame,
    text="PASTE",
    command=do_paste,
    font=mono_font,
    bg="#1c1f2b",
    fg=FG,
    bd=0,
).pack(side="left")

tk.Button(
    root,
    text="ANALYZE",
    command=do_analyze,
    font=mono_font,
    bg=ACCENT,
    fg="white",
    activebackground=FG,
    bd=0,
    height=2,
).pack(fill="x", padx=20, pady=(0, 14))

badge_canvas = tk.Canvas(root, width=176, height=176, bg=PANEL, highlightthickness=0)
badge_canvas.pack(pady=(0, 6))
badge_item = badge_canvas.create_image(88, 88, image=None)

tk.Button(
    root,
    text="SAVE BADGE PNG",
    command=do_save_badge,
    font=mono_font,
    bg="#1c1f2b",
    fg=FG,
    bd=0,
).pack(pady=(0, 14))

lookup_var = tk.StringVar(value="lookup results appear here")
tk.Label(
    root,
    textvariable=lookup_var,
    font=mono_font,
    fg="white",
    bg=BG,
    justify="left",
    wraplength=420,
).pack(pady=(0, 12), padx=20, anchor="w")

relay_var = tk.StringVar(value="relay pick appears here")
tk.Label(
    root,
    textvariable=relay_var,
    font=mono_font,
    fg="white",
    bg=BG,
    justify="left",
    wraplength=420,
).pack(pady=(0, 12), padx=20, anchor="w")

status_var = tk.StringVar(value="ready")
tk.Label(root, textvariable=status_var, font=mono_font, fg=MUTED, bg=BG).pack(
    side="bottom", pady=16
)

root.mainloop()
