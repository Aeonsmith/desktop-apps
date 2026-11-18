#!/usr/bin/env python3
"""
Node 4 (Norway) - Nordic Telemetry & Cryo-Sensor Hub
Monitors optical channels, cryogenic baseline, and photon transceiver states
across the Q999 quantum network.
"""

import math
import random
import time
import tkinter as tk
from tkinter import font as tkfont

BG = "#05060a"
FG = "#39ff88"
CYAN = "#00f0ff"
ACCENT = "#7a5cff"
MUTED = "#8a93a6"
PANEL = "#10121b"
ALERT_COLOR = "#ff0055"

NODES_STATUS = [
    {"name": "Node 1: Nigeria", "status": "ONLINE", "latency": "38ms", "flow": "3.42 Gbps"},
    {"name": "Node 2: South Africa", "status": "ONLINE", "latency": "64ms", "flow": "1.15 Gbps"},
    {"name": "Node 3: Norway (CORE)", "status": "TRANSMITTING", "latency": "1ms", "flow": "9.80 Gbps"},
    {"name": "Node 4: Sweden", "status": "SYNCED", "latency": "4ms", "flow": "4.20 Gbps"},
    {"name": "Node 5: Denmark", "status": "MEASURING", "latency": "8ms", "flow": "2.85 Gbps"},
    {"name": "AUX: Gambia (DEMOTED)", "status": "THROTTLED", "latency": "142ms", "flow": "0.12 Gbps"},
]

class Node4TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Q999 - Node 4 (Norway) Telemetry Hub")
        self.root.geometry("540x580")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.title_font = tkfont.Font(family="Consolas", size=18, weight="bold")
        self.mono_font = tkfont.Font(family="Consolas", size=10)
        self.bold_mono = tkfont.Font(family="Consolas", size=11, weight="bold")

        self.cryo_temp = 0.015  # Kelvin (15 mK)
        self.pulse_phase = 0.0

        self.build_ui()
        self.update_telemetry()

    def build_ui(self):
        # Header
        tk.Label(
            self.root,
            text="NODE 4 // NORWAY // PHOTONIC CORE",
            font=self.title_font,
            fg=CYAN,
            bg=BG
        ).pack(pady=(16, 2))

        tk.Label(
            self.root,
            text="CRYOGENIC SENSOR & OPTICAL RELAY MATRIX",
            font=self.mono_font,
            fg=MUTED,
            bg=BG
        ).pack(pady=(0, 10))

        # Core Metrics Panel
        metrics_frame = tk.Frame(self.root, bg=PANEL, padx=12, pady=10)
        metrics_frame.pack(fill="x", padx=16, pady=(0, 10))

        self.temp_var = tk.StringVar(value="CRYO-CORE: 0.015 K (STABLE)")
        tk.Label(
            metrics_frame,
            textvariable=self.temp_var,
            font=self.bold_mono,
            fg=FG,
            bg=PANEL
        ).pack(anchor="w")

        self.photonic_var = tk.StringVar(value="AURORA BEAM: 1550nm LASER LOCKED")
        tk.Label(
            metrics_frame,
            textvariable=self.photonic_var,
            font=self.mono_font,
            fg=CYAN,
            bg=PANEL
        ).pack(anchor="w", pady=(4, 0))

        self.entropy_var = tk.StringVar(value="ENTROPY FLUX: CERTIFIED REAL-TIME")
        tk.Label(
            metrics_frame,
            textvariable=self.entropy_var,
            font=self.mono_font,
            fg=ACCENT,
            bg=PANEL
        ).pack(anchor="w", pady=(2, 0))

        # Pulse Scope Canvas
        self.scope_canvas = tk.Canvas(self.root, width=508, height=80, bg="#000810", highlightthickness=1, highlightbackground=PANEL)
        self.scope_canvas.pack(padx=16, pady=(0, 10))

        # Grid Status Panel
        grid_frame = tk.LabelFrame(self.root, text=" 6-NODE NETWORK TOPOLOGY ", font=self.mono_font, fg=MUTED, bg=BG, padx=8, pady=8)
        grid_frame.pack(fill="x", padx=16, pady=(0, 10))

        self.node_labels = []
        for i, n in enumerate(NODES_STATUS):
            color = FG if "CORE" in n["name"] else "white"
            lbl_text = f"{n['name']:<24} {n['status']:<14} Latency: {n['latency']:<6} {n['flow']}"
            var = tk.StringVar(value=lbl_text)
            lbl = tk.Label(grid_frame, textvariable=var, font=self.mono_font, fg=color, bg=BG, anchor="w", justify="left")
            lbl.pack(fill="x", pady=1)
            self.node_labels.append((n, var))

        # Action Buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=6)

        tk.Button(
            btn_frame,
            text="PULSE LASER TRANSMITTER",
            command=self.pulse_laser,
            font=self.mono_font,
            bg=ACCENT,
            fg="white",
            activebackground=FG,
            bd=0,
            padx=12,
            pady=6
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            btn_frame,
            text="PURGE THERMAL NOISE",
            command=self.purge_noise,
            font=self.mono_font,
            bg="#1c1f2b",
            fg=FG,
            activebackground="#2a2e40",
            bd=0,
            padx=12,
            pady=6
        ).grid(row=0, column=1, padx=6)

        self.status_var = tk.StringVar(value="SYSTEM: All 6 nodes locked to Node 4 Nordic standard.")
        tk.Label(self.root, textvariable=self.status_var, font=self.mono_font, fg=MUTED, bg=BG).pack(side="bottom", pady=12)

    def pulse_laser(self):
        self.pulse_phase += math.pi / 2
        self.status_var.set("BEAM FIRED: Synchronized clock state with Sweden (5) & Denmark (6).")

    def purge_noise(self):
        self.cryo_temp = max(0.010, self.cryo_temp - 0.003)
        self.status_var.set(f"CRYO-COOLED: Thermal noise scrubbed. Base at {self.cryo_temp:.3f} K.")

    def update_telemetry(self):
        # Fluctuate temperature slightly
        self.cryo_temp += random.uniform(-0.0005, 0.0006)
        self.cryo_temp = max(0.010, min(0.025, self.cryo_temp))
        self.temp_var.set(f"CRYO-CORE: {self.cryo_temp:.4f} K (STABLE NORDIC BASE)")

        # Redraw waveform on canvas
        self.scope_canvas.delete("wave")
        width = 508
        height = 80
        points = []
        self.pulse_phase += 0.15
        for x in range(0, width, 4):
            y = (height / 2) + math.sin((x * 0.05) + self.pulse_phase) * 20 * math.sin(x * 0.01)
            points.append(x)
            points.append(y)
        if len(points) >= 4:
            self.scope_canvas.create_line(points, fill=CYAN, width=2, tags="wave", smooth=True)

        # Fluctuate network flow slightly
        for n, var in self.node_labels:
            if "CORE" not in n["name"]:
                ms = random.randint(int(n["latency"].replace("ms","")) - 2, int(n["latency"].replace("ms","")) + 3)
                ms = max(2, ms)
                var.set(f"{n['name']:<24} {n['status']:<14} Latency: {ms}ms      {n['flow']}")

        self.root.after(100, self.update_telemetry)

if __name__ == "__main__":
    root = tk.Tk()
    app = Node4TelemetryApp(root)
    root.mainloop()
