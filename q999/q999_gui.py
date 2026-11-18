#!/usr/bin/env python3
"""Q999 desktop app - tkinter GUI wrapper around the Q999 certified draw core."""

import json
import random
import sys
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont

sys.path.insert(0, str(Path(__file__).resolve().parent))

from q999 import CERT_DIR, draw, hash_certificate  # noqa: E402

BG = "#05060a"
FG = "#39ff88"
ACCENT = "#7a5cff"
MUTED = "#8a93a6"

FACTS = [
    "FUN FACT: No Man's Sky (2016) launched way short of its own hype - "
    "no multiplayer, thin combat, sparse wildlife. Hello Games then shipped "
    "years of free updates (NEXT, a PS5-ready Next Gen patch, Beyond...) "
    "until it became one of gaming's biggest comeback stories.",
]

last_certificate = {"path": None, "hash": None}


def do_spin():
    status_var.set("spinning...")
    root.update_idletasks()

    certificate = draw(offline=False)
    CERT_DIR.mkdir(exist_ok=True)
    out_path = CERT_DIR / f"{certificate['run_id']}.json"
    out_path.write_text(json.dumps(certificate, indent=2), encoding="utf-8")
    last_certificate["path"] = out_path
    last_certificate["hash"] = certificate["certificate_hash"]

    result_var.set(
        f"NODE {certificate['node_number']}/6 -> {certificate['node']}\n"
        f"source: {certificate['source']}\n"
        f"raw value: {certificate['raw_value']}\n"
        f"hash: {certificate['certificate_hash'][:20]}...\n"
        f"saved: {out_path.name}"
    )
    fact_var.set(random.choice(FACTS))
    status_var.set("spin complete - certificate saved")


def do_copy_hash():
    full_hash = last_certificate["hash"]
    if not full_hash:
        status_var.set("no hash yet - spin first")
        return
    root.clipboard_clear()
    root.clipboard_append(full_hash)
    root.update()
    status_var.set("full hash copied to clipboard")


def do_verify():
    path = last_certificate["path"]
    if path is None or not path.exists():
        status_var.set("no certificate yet - spin first")
        return
    certificate = json.loads(path.read_text(encoding="utf-8"))
    stored = certificate.get("certificate_hash")
    recomputed = hash_certificate(certificate)
    if stored == recomputed:
        status_var.set(f"VALID - {path.name}")
    else:
        status_var.set(f"INVALID - {path.name}")


root = tk.Tk()
root.title("Q999")
root.configure(bg=BG)
root.geometry("420x480")
root.resizable(False, False)

title_font = tkfont.Font(family="Consolas", size=22, weight="bold")
mono_font = tkfont.Font(family="Consolas", size=11)

tk.Label(root, text="Q999", font=title_font, fg=FG, bg=BG).pack(pady=(24, 4))
tk.Label(root, text="spin . measure . verify", font=mono_font, fg=MUTED, bg=BG).pack()

result_var = tk.StringVar(value="press SPIN to draw a node")
tk.Label(
    root,
    textvariable=result_var,
    font=mono_font,
    fg="white",
    bg=BG,
    justify="left",
    wraplength=380,
).pack(pady=(20, 8))

fact_var = tk.StringVar(value="")
tk.Label(
    root,
    textvariable=fact_var,
    font=tkfont.Font(family="Consolas", size=9),
    fg=MUTED,
    bg=BG,
    justify="left",
    wraplength=380,
).pack(pady=(0, 10), padx=20)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="SPIN",
    command=do_spin,
    font=mono_font,
    bg=ACCENT,
    fg="white",
    activebackground=FG,
    width=28,
    height=2,
    bd=0,
).grid(row=0, column=0, columnspan=2, padx=8, pady=(0, 8))

tk.Button(
    btn_frame,
    text="COPY HASH",
    command=do_copy_hash,
    font=mono_font,
    bg="#1c1f2b",
    fg=FG,
    activebackground="#2a2e40",
    width=12,
    height=2,
    bd=0,
).grid(row=1, column=0, padx=8)

tk.Button(
    btn_frame,
    text="VERIFY LAST",
    command=do_verify,
    font=mono_font,
    bg="#1c1f2b",
    fg=FG,
    activebackground="#2a2e40",
    width=14,
    height=2,
    bd=0,
).grid(row=1, column=1, padx=8)

status_var = tk.StringVar(value="ready")
tk.Label(root, textvariable=status_var, font=mono_font, fg=MUTED, bg=BG).pack(
    side="bottom", pady=16
)

root.mainloop()
