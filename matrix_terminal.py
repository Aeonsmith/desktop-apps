"""
MATRIX // Neural Decryption & Command Terminal (Full Interactive Suite)
"""

import tkinter as tk
import random
import time
import os
import sys
import json
from pathlib import Path

HISTORY_FILE = os.path.join(Path.home(), ".matrix_terminal_history.json")
CONFIG_FILE = os.path.join(Path.home(), ".matrix_terminal_config.json")
MAX_HISTORY_ENTRIES = 200

DEFAULT_CONFIG = {
    "theme": "matrix_green",
    "font_family": "Consolas",
    "font_size_terminal": 10,
    "font_size_rain": 14,
    "font_size_header": 10,
    "themes": {
        "matrix_green": {
            "window_bg": "#010803",
            "canvas_bg": "#010602",
            "term_bg": "#020d04",
            "header_bg": "#051a08",
            "border_color": "#00ff41",
            "text_primary": "#00ff41",
            "text_secondary": "#38ff75",
            "text_accent": "#00ffff",
            "text_dim": "#00802b",
            "text_highlight": "#ffffff",
            "text_warning": "#ffee00",
            "text_error": "#ff3333",
            "prompt_color": "#00ff41",
            "input_bg": "#010602",
            "input_fg": "#ffffff",
            "rain_lead": "#ffffff",
            "rain_trail": "#00ff41"
        },
        "cyber_amber": {
            "window_bg": "#0f0800",
            "canvas_bg": "#0a0500",
            "term_bg": "#140a00",
            "header_bg": "#241200",
            "border_color": "#ffaa00",
            "text_primary": "#ffaa00",
            "text_secondary": "#ffcc44",
            "text_accent": "#ff8800",
            "text_dim": "#804400",
            "text_highlight": "#ffffff",
            "text_warning": "#ffff55",
            "text_error": "#ff4444",
            "prompt_color": "#ffaa00",
            "input_bg": "#0a0500",
            "input_fg": "#ffffff",
            "rain_lead": "#ffffff",
            "rain_trail": "#ffaa00"
        },
        "ice_cyan": {
            "window_bg": "#010b14",
            "canvas_bg": "#01080f",
            "term_bg": "#02121f",
            "header_bg": "#042036",
            "border_color": "#00e5ff",
            "text_primary": "#00e5ff",
            "text_secondary": "#80f0ff",
            "text_accent": "#ff00aa",
            "text_dim": "#007080",
            "text_highlight": "#ffffff",
            "text_warning": "#ffee55",
            "text_error": "#ff3366",
            "prompt_color": "#00e5ff",
            "input_bg": "#01080f",
            "input_fg": "#ffffff",
            "rain_lead": "#ffffff",
            "rain_trail": "#00e5ff"
        },
        "synth_purple": {
            "window_bg": "#0e021a",
            "canvas_bg": "#08010f",
            "term_bg": "#140324",
            "header_bg": "#22053d",
            "border_color": "#d946ef",
            "text_primary": "#e879f9",
            "text_secondary": "#f0abfc",
            "text_accent": "#38bdf8",
            "text_dim": "#701a75",
            "text_highlight": "#ffffff",
            "text_warning": "#facc15",
            "text_error": "#f43f5e",
            "prompt_color": "#d946ef",
            "input_bg": "#08010f",
            "input_fg": "#ffffff",
            "rain_lead": "#ffffff",
            "rain_trail": "#d946ef"
        },
        "blood_red": {
            "window_bg": "#120202",
            "canvas_bg": "#0a0101",
            "term_bg": "#1c0404",
            "header_bg": "#2e0606",
            "border_color": "#ef4444",
            "text_primary": "#f87171",
            "text_secondary": "#fca5a5",
            "text_accent": "#fb923c",
            "text_dim": "#7f1d1d",
            "text_highlight": "#ffffff",
            "text_warning": "#facc15",
            "text_error": "#ff2222",
            "prompt_color": "#ef4444",
            "input_bg": "#0a0101",
            "input_fg": "#ffffff",
            "rain_lead": "#ffffff",
            "rain_trail": "#ef4444"
        }
    }
}

MATRIX_CHARS = [chr(i) for i in range(0x30A0, 0x30FF)] + [str(i) for i in range(10)] + ["#", "$", "%", "&", "*", "+", "-", "<", ">", "="]

MOCK_TARGETS = {
    "mainframe": {
        "ip": "10.0.84.12",
        "hostname": "zion-mainframe-prime",
        "os": "ZionCore OS v9.2 (x86_64)",
        "sec": "DEFCON-2 (HIGH)",
        "encryption": "AES-4096-GCM + Quantum Lattice",
        "ports": [
            (22, "SSH/Neural", "OPEN", "OpenSSH 9.4p1"),
            (80, "HTTP/Zion", "OPEN", "Nginx Zion Gateway"),
            (443, "HTTPS/TLS", "OPEN", "TLSv1.3 ECDHE"),
            (8080, "CORE_PROXY", "FILTERED", "Zion Proxy Relay"),
            (9999, "ORACLE_PIPE", "OPEN", "Prophecy Sub-Grid Protocol")
        ]
    },
    "satellite": {
        "ip": "192.168.104.5",
        "hostname": "orbital-relay-09",
        "os": "OrbitalLink RTOS v4.1",
        "sec": "DEFCON-1 (CRITICAL)",
        "encryption": "ECC-521 + Kinetic Vault",
        "ports": [
            (1337, "MATRIX_GATE", "OPEN", "Matrix Ingress Daemon"),
            (2121, "TELEMETRY_FTP", "OPEN", "Orbital Telemetry Feed"),
            (5000, "LASER_COMMS", "FILTERED", "Downlink Array Receiver")
        ]
    },
    "sentinel": {
        "ip": "172.16.0.44",
        "hostname": "sentinel-swarm-alpha",
        "os": "Machine Mesh AI Kernel 0.99",
        "sec": "DEFCON-0 (AUTOMATED MESH)",
        "encryption": "Dynamic Neural Synapse 8192-bit",
        "ports": [
            (8888, "SWARM_BUS", "OPEN", "Machine Swarm Protocol"),
            (9000, "SENSORY_FEED", "OPEN", "LIDAR / Bio-Sonar Stream"),
            (9999, "OVERSEER_UPLINK", "OPEN", "01 City Main Hub")
        ]
    }
}

DICTIONARY_WORDS = [
    "NEO_AWAKENING", "TRINITY_FORCE", "MORPHEUS_DREAM", "ZION_MAINFRAME",
    "CYPHER_BETRAYAL", "ORACLE_COOKIE", "AGENT_SMITH_01", "NABU_VESSEL",
    "RED_PILL_TRUTH", "BLUE_PILL_SLEEP", "ANOMALY_PRIME", "ARCHITECT_EQUATION"
]


class UnifiedMatrixTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MATRIX // NEURAL DECRYPTION & COMMAND TERMINAL")
        self.geometry("1140x740")
        self.minsize(920, 600)
        self.configure(bg="#010803")

        # Set Window Icon
        icon_candidates = [
            os.path.join(getattr(sys, "_MEIPASS", ""), "matrix_terminal.ico") if getattr(sys, "frozen", False) else None,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix_terminal.ico"),
            os.path.join(Path.home(), "matrix_terminal.ico"),
        ]
        for icon_path in icon_candidates:
            if icon_path and os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    break
                except Exception:
                    pass

        self.config = self._load_or_create_config()
        self.current_theme_name = self.config.get("theme", "matrix_green")
        self.theme = self.config.get("themes", {}).get(self.current_theme_name, DEFAULT_CONFIG["themes"]["matrix_green"])
        self.font_family = self.config.get("font_family", "Consolas")
        self.font_size_term = self.config.get("font_size_terminal", 10)
        self.font_size_rain = self.config.get("font_size_rain", 14)
        self.font_size_header = self.config.get("font_size_header", 10)

        self.history = self._load_persistent_history()
        self.history_index = len(self.history)
        self.current_typed = ""
        self.is_busy = False

        self._build_layout()
        self._apply_theme()
        self._init_matrix_rain()
        self._animate_rain()
        self._print_banner()

    def _load_or_create_config(self):
        """Loads terminal configuration or initializes default config file."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    # Merge with default structure
                    cfg = dict(DEFAULT_CONFIG)
                    cfg.update(user_cfg)
                    if "themes" in user_cfg:
                        merged_themes = dict(DEFAULT_CONFIG["themes"])
                        merged_themes.update(user_cfg["themes"])
                        cfg["themes"] = merged_themes
                    return cfg
            except Exception:
                pass
        
        # Write default configuration file
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
        except Exception:
            pass
        return dict(DEFAULT_CONFIG)

    def _save_config(self):
        """Saves current active configuration to disk."""
        self.config["theme"] = self.current_theme_name
        self.config["font_family"] = self.font_family
        self.config["font_size_terminal"] = self.font_size_term
        self.config["font_size_rain"] = self.font_size_rain
        self.config["font_size_header"] = self.font_size_header
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def _apply_theme(self):
        """Applies colors and fonts from the active theme to all GUI widgets."""
        t = self.theme
        self.configure(bg=t["window_bg"])
        self.paned.configure(bg=t["window_bg"])

        # Canvas
        self.rain_canvas.configure(bg=t["canvas_bg"], highlightbackground=t["border_color"])

        # Terminal frame
        self.term_frame.configure(bg=t["term_bg"], highlightbackground=t["border_color"])
        self.header_frame.configure(bg=t["header_bg"])
        self.lbl_title.configure(bg=t["header_bg"], fg=t["text_primary"], font=(self.font_family, self.font_size_header, "bold"))
        self.lbl_telemetry.configure(bg=t["header_bg"], fg=t["text_secondary"], font=(self.font_family, max(8, self.font_size_header - 1)))

        # Output Box
        self.log_text.configure(
            bg=t["term_bg"],
            fg=t["text_primary"],
            insertbackground=t["text_primary"],
            font=(self.font_family, self.font_size_term)
        )

        # Reconfigure tag colors
        self.log_text.tag_config("green", foreground=t["text_primary"])
        self.log_text.tag_config("bright_green", foreground=t["text_secondary"], font=(self.font_family, self.font_size_term, "bold"))
        self.log_text.tag_config("dark_green", foreground=t["text_dim"])
        self.log_text.tag_config("white", foreground=t["text_highlight"], font=(self.font_family, self.font_size_term, "bold"))
        self.log_text.tag_config("cyan", foreground=t["text_accent"])
        self.log_text.tag_config("yellow", foreground=t["text_warning"])
        self.log_text.tag_config("red", foreground=t["text_error"])
        self.log_text.tag_config("banner", foreground=t["text_primary"], font=(self.font_family, 8, "bold"))

        # Prompt & Input
        self.prompt_frame.configure(bg=t["term_bg"])
        self.prompt_label.configure(bg=t["term_bg"], fg=t["prompt_color"], font=(self.font_family, self.font_size_term, "bold"))
        self.cmd_entry.configure(
            bg=t["input_bg"],
            fg=t["input_fg"],
            insertbackground=t["prompt_color"],
            font=(self.font_family, self.font_size_term)
        )

    def _build_layout(self):
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#001804", bd=0, sashwidth=4)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Left: Matrix Digital Rain Canvas
        self.canvas_width = 330
        self.canvas_height = 660
        self.rain_canvas = tk.Canvas(
            self.paned,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#010602",
            highlightthickness=1,
            highlightbackground="#00ff41"
        )
        self.paned.add(self.rain_canvas, minsize=220)

        # Right: Terminal Panel
        self.term_frame = tk.Frame(self.paned, bg="#020d04", highlightthickness=1, highlightbackground="#00ff41")
        self.paned.add(self.term_frame, minsize=540)

        # Top Header Bar
        self.header_frame = tk.Frame(self.term_frame, bg="#051a08", pady=4, padx=8)
        self.header_frame.pack(fill=tk.X)

        self.lbl_title = tk.Label(
            self.header_frame,
            text="● MATRIX NEURAL CONSOLE [LINK: ACTIVE]",
            font=("Consolas", 10, "bold"),
            fg="#00ff41",
            bg="#051a08"
        )
        self.lbl_title.pack(side=tk.LEFT)

        self.lbl_telemetry = tk.Label(
            self.header_frame,
            text="CORE: ZION-07 // DEFCON: NOMINAL",
            font=("Consolas", 9),
            fg="#38ff75",
            bg="#051a08"
        )
        self.lbl_telemetry.pack(side=tk.RIGHT)

        # Output Log Box with Scrollbar
        log_container = tk.Frame(self.term_frame, bg="#020d04")
        log_container.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        self.scrollbar = tk.Scrollbar(log_container, orient=tk.VERTICAL)
        self.log_text = tk.Text(
            log_container,
            bg="#020d04",
            fg="#00ff41",
            insertbackground="#00ff41",
            font=("Consolas", 10),
            relief=tk.FLAT,
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED
        )
        self.scrollbar.config(command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Styling Tags
        self.log_text.tag_config("green", foreground="#00ff41")
        self.log_text.tag_config("bright_green", foreground="#38ff75", font=("Consolas", 10, "bold"))
        self.log_text.tag_config("dark_green", foreground="#00802b")
        self.log_text.tag_config("white", foreground="#ffffff", font=("Consolas", 10, "bold"))
        self.log_text.tag_config("cyan", foreground="#00ffff")
        self.log_text.tag_config("yellow", foreground="#ffee00")
        self.log_text.tag_config("red", foreground="#ff3333")
        self.log_text.tag_config("banner", foreground="#00ff41", font=("Consolas", 8, "bold"))

        # Interactive Command Entry Line
        self.prompt_frame = tk.Frame(self.term_frame, bg="#020d04", padx=6, pady=6)
        self.prompt_frame.pack(fill=tk.X)

        self.prompt_label = tk.Label(
            self.prompt_frame,
            text="operator@zion-core:~$ ",
            font=("Consolas", 10, "bold"),
            fg="#00ff41",
            bg="#020d04"
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.cmd_entry = tk.Entry(
            self.prompt_frame,
            bg="#010602",
            fg="#ffffff",
            insertbackground="#00ff41",
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cmd_entry.focus_set()

        # Keyboard Bindings
        self.cmd_entry.bind("<Return>", self._on_enter)
        self.cmd_entry.bind("<Up>", self._history_up)
        self.cmd_entry.bind("<Down>", self._history_down)
        self.cmd_entry.bind("<Tab>", self._auto_complete)

    def _init_matrix_rain(self):
        self.font_size = self.font_size_rain
        self.columns = max(1, int(self.canvas_width / self.font_size))
        self.drops = [random.randint(-30, 0) for _ in range(self.columns)]

    def _animate_rain(self):
        self.rain_canvas.delete("all")
        w = self.rain_canvas.winfo_width() or self.canvas_width
        h = self.rain_canvas.winfo_height() or self.canvas_height
        self.columns = max(1, int(w / self.font_size))

        if len(self.drops) < self.columns:
            self.drops.extend([random.randint(-30, 0) for _ in range(self.columns - len(self.drops))])

        lead_color = self.theme.get("rain_lead", "#ffffff")
        trail_color = self.theme.get("rain_trail", "#00ff41")

        for i in range(self.columns):
            char = random.choice(MATRIX_CHARS)
            x = i * self.font_size + 8
            y = self.drops[i] * self.font_size

            # Glowing head
            self.rain_canvas.create_text(x, y, text=char, fill=lead_color, font=(self.font_family, self.font_size, "bold"))

            # Trailing body
            if self.drops[i] > 1:
                trail_char = random.choice(MATRIX_CHARS)
                self.rain_canvas.create_text(x, y - self.font_size, text=trail_char, fill=trail_color, font=(self.font_family, self.font_size))

            if y > h and random.random() > 0.975:
                self.drops[i] = 0
            else:
                self.drops[i] += 1

        self.after(45, self._animate_rain)

    def _print_banner(self):
        banner_art = """
  ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
  ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
  ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ 
  ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ 
  ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
  ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
"""
        self._write(banner_art, tag="banner")
        self._write("INIT: Neural link established. Grid access level: OPERATOR.", tag="bright_green")
        self._write("Type 'help' to review command protocols or 'scan' to start reconnaissance.\n", tag="cyan")

    def _write(self, text, tag="green", end="\n"):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + end, tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _load_persistent_history(self):
        """Loads command history from persistent disk storage."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data[-MAX_HISTORY_ENTRIES:]
            except Exception:
                pass
        return []

    def _save_persistent_history(self):
        """Saves current command history to persistent disk storage."""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history[-MAX_HISTORY_ENTRIES:], f, indent=2)
        except Exception:
            pass

    def _on_enter(self, event=None):
        if self.is_busy:
            return

        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, tk.END)
        self.current_typed = ""
        if not cmd:
            return

        # Append to history if different from the last entry
        if not self.history or self.history[-1] != cmd:
            self.history.append(cmd)
            self._save_persistent_history()

        self.history_index = len(self.history)
        self._write(f"operator@zion-core:~$ {cmd}", tag="white")

        parts = cmd.split()
        cmd_name = parts[0].lower()
        args = parts[1:]

        self._dispatch_command(cmd_name, args)

    def _history_up(self, event=None):
        if not self.history:
            return "break"

        # Save currently typed buffer when beginning history navigation
        if self.history_index == len(self.history):
            self.current_typed = self.cmd_entry.get()

        if self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.history[self.history_index])
            self.cmd_entry.icursor(tk.END)
        return "break"

    def _history_down(self, event=None):
        if not self.history:
            return "break"

        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.history[self.history_index])
            self.cmd_entry.icursor(tk.END)
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.current_typed)
            self.cmd_entry.icursor(tk.END)
        return "break"

    def _auto_complete(self, event=None):
        commands = [
            "scan", "crack", "dump", "override", "inject", "trace",
            "matrix", "status", "ping", "philosophy", "theme", "help", "clear", "cls", "exit", "quit"
        ]
        cur = self.cmd_entry.get().strip()
        matches = [c for c in commands if c.startswith(cur)]
        if len(matches) == 1:
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, matches[0] + " ")
        return "break"

    def _dispatch_command(self, cmd, args):
        handlers = {
            "help": lambda: self._cmd_help(args),
            "theme": lambda: self._cmd_theme(args),
            "clear": self._cmd_clear,
            "cls": self._cmd_clear,
            "scan": lambda: self._cmd_scan(args),
            "crack": lambda: self._cmd_crack(args),
            "dump": lambda: self._cmd_dump(args),
            "override": lambda: self._cmd_override(args),
            "inject": lambda: self._cmd_inject(args),
            "trace": lambda: self._cmd_trace(args),
            "ping": lambda: self._cmd_ping(args),
            "matrix": lambda: self._cmd_matrix(args),
            "philosophy": lambda: self._cmd_philosophy(args),
            "status": self._cmd_status,
            "exit": self.destroy,
            "quit": self.destroy,
        }
        if cmd in handlers:
            handlers[cmd]()
        else:
            self._write(f"[!] Protocol '{cmd}' not recognized. Type 'help' for available commands.\n", tag="red")

    # =========================================================================
    # COMMAND IMPLEMENTATIONS
    # =========================================================================

    def _cmd_help(self, args=None):
        if args and len(args) > 0:
            sub = args[0].lower()
            manuals = {
                "scan": "USAGE: scan [target] [-v]\n  Scans port ranges, banner grabs, and OS fingerprinting on nodes.\n  Targets: mainframe, satellite, sentinel, or custom hostname.",
                "crack": "USAGE: crack [cipher | hash_type]\n  Simulates entropy cycling and dictionary permutation attack against crypto ciphers.",
                "dump": "USAGE: dump [block_count]\n  Extracts and renders formatted hexadecimal memory blocks with ASCII decode columns.",
                "override": "USAGE: override [system_name]\n  Initiates multi-tier security bypass and privilege escalation sequence.",
                "inject": "USAGE: inject [target] [payload_type]\n  Simulates mock payload transmission to compromised ports.",
                "trace": "USAGE: trace [ip_address]\n  Performs multi-hop network traceroute across Zion sub-grid relays.",
                "ping": "USAGE: ping [target]\n  Measures round-trip neural latency and signal fidelity.",
                "matrix": "USAGE: matrix [lines]\n  Streams live Matrix glyph rain into the console output.",
                "status": "USAGE: status\n  Displays quantum telemetry, cortex CPU utilization, and node topologies.",
                "clear": "USAGE: clear (or cls)\n  Purges the terminal output log and redraws the system banner."
            }
            if sub in manuals:
                self._write(f"\n--- MANUAL: {sub.upper()} ---", tag="white")
                self._write(manuals[sub], tag="cyan")
                self._write("")
                return

        catalog = """
================================================================================
                    AVAILABLE MATRIX OPERATOR PROTOCOLS                         
================================================================================

[ RECONNAISSANCE & MAPPING ]
  scan [target] [-v]     Probe target node, map active TCP ports, grab service banners.
  trace [target]         Multi-hop packet route tracing through Zion orbital relays.
  ping [target]          Measure neural packet latency, jitter, and signal integrity.

[ CRYPTANALYSIS & MEMORY EXPLOITATION ]
  crack [target]         Execute real-time dictionary & entropy permutation brute-force.
  dump [blocks]          Dump live hexadecimal memory buffers with ASCII translation.
  override [system]      Execute 4-stage quantum firewall bypass and privilege elevation.
  inject [target]        Inject mock telemetry payload into open neural ports.

[ TELEMETRY & PHILOSOPHICAL ENGINE ]
  philosophy [topic]     Display Carl Jung's depth psychology & individuation insights.
                         (Topics: persona, individuation, synchronicity, shadow, humility)
  matrix [lines]         Stream cascading Matrix glyphs into log window.
  status                 Inspect Zion uplink telemetry, encryption grade, and CPU load.
  theme [name]           Switch live color scheme palette (matrix_green, cyber_amber, etc).
  help [protocol]        Show manual page for a specific protocol (e.g. 'help scan').
  clear / cls            Purge screen buffer and redraw system banner.
  exit / quit            Safely disconnect neural uplink and close application.

================================================================================
* TARGETS: mainframe, satellite, sentinel | Press [TAB] to auto-complete.
"""
        self._write(catalog, tag="cyan")

    def _cmd_clear(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._print_banner()

    def _cmd_scan(self, args):
        """Full interactive port & service scanner."""
        target_key = "mainframe"
        verbose = False

        for a in args:
            if a.lower() == "-v":
                verbose = True
            elif a.lower() in MOCK_TARGETS or not a.startswith("-"):
                target_key = a.lower()

        target = MOCK_TARGETS.get(target_key, {
            "ip": f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "hostname": f"node-{target_key}.grid",
            "os": "Custom Neural Architecture",
            "sec": "DEFCON-3 (MODERATE)",
            "encryption": "SHA-512 + Lattice",
            "ports": [
                (22, "SSH/Neural", "OPEN", "Standard Node SSH"),
                (80, "HTTP", "OPEN", "Virtual Web Gateway"),
                (443, "HTTPS", "OPEN", "Secure Web Socket"),
                (3389, "RDP/Grid", "FILTERED", "Remote Subsystem")
            ]
        })

        self.is_busy = True
        self._write(f"[*] INITIATING NEURAL SCAN ON [{target['hostname'].upper()}] ({target['ip']})...", tag="yellow")

        stages = [
            "Pinging ICMP Echo to target...",
            "SYN stealth scan on 1024 privileged ports...",
            "Probing SSL/TLS encryption certificates...",
            "Fingerprinting remote TCP/IP stack OS..."
        ]

        def step_scan(idx=0):
            if idx < len(stages):
                self._write(f"  [+] {stages[idx]}", tag="dark_green")
                self.after(140, lambda: step_scan(idx + 1))
            else:
                self._write("\n--- NODE RECONNAISSANCE REPORT ---", tag="white")
                self._write(f"  Target Host  : {target['hostname']}", tag="green")
                self._write(f"  Virtual IP   : {target['ip']}", tag="green")
                self._write(f"  OS Signature : {target['os']}", tag="green")
                self._write(f"  Security Tier: {target['sec']}", tag="yellow")
                self._write(f"  Encryption   : {target['encryption']}", tag="cyan")
                self._write("  Port Status & Banners:", tag="white")
                
                for port, service, status, banner in target["ports"]:
                    color = "bright_green" if status == "OPEN" else "yellow"
                    self._write(f"    --> [{port:>5}/TCP] {status:<8} {service:<16} [{banner}]", tag=color)
                
                self._write("\n[✓] Reconnaissance complete. Vulnerability index: 88.4%\n", tag="bright_green")
                self.is_busy = False

        step_scan()

    def _cmd_crack(self, args):
        """Full cryptographic password & hash cracking simulation."""
        target_cipher = args[0].upper() if args else random.choice(DICTIONARY_WORDS)
        mock_hash = f"0x{random.randint(0x10000000, 0xFFFFFFFF):08X}"
        self.is_busy = True

        self._write(f"[*] TARGETING ENCRYPTED DIGEST: {mock_hash} (Target: {target_cipher})", tag="yellow")
        self._write("  [+] Initializing rainbow table dictionary...", tag="dark_green")
        self._write("  [+] Allocating 128 virtual GPU matrix threads...", tag="dark_green")

        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        steps = 14

        def cycle_entropy(i=0):
            if i < steps:
                scrambled = "".join(
                    target_cipher[idx] if idx < i * len(target_cipher) // steps else random.choice(charset)
                    for idx in range(len(target_cipher))
                )
                rate = random.randint(14200, 18900)
                self._write(f"  [CRACKING] Scramble: {scrambled:<18} | Hashes/sec: {rate:,} | Iteration: {i*25000 + 1200}", tag="dark_green")
                self.after(55, lambda: cycle_entropy(i + 1))
            else:
                self._write(f"\n  ==================================================", tag="bright_green")
                self._write(f"  [✓] CIPHER SOLVED: {target_cipher}", tag="white")
                self._write(f"  [✓] PLAINTEXT KEY: 0x{random.randint(0xAAAAAA, 0xFFFFFF):X}_PASSPHRASE_CONFIRMED", tag="bright_green")
                self._write(f"  ==================================================\n", tag="bright_green")
                self.is_busy = False

        cycle_entropy()

    def _cmd_dump(self, args):
        """Full raw hexadecimal & ASCII memory inspector."""
        size = int(args[0]) if args and args[0].isdigit() else 10
        size = min(max(size, 4), 32)
        self.is_busy = True

        self._write(f"[*] STREAMING LIVE NEURAL BUFFER AT OFFSET 0x7FFF0000 ({size} BLOCKS)...", tag="yellow")
        self._write(f"  {'OFFSET':<12} {'HEXADECIMAL BYTES':<49} {'ASCII DECODE':<16}", tag="white")
        self._write(f"  {'-'*12} {'-'*49} {'-'*16}", tag="dark_green")

        def stream_block(i=0):
            if i < size:
                offset = f"0x{0x7FFF0000 + (i * 16):08X}"
                raw_bytes = [random.randint(0, 255) for _ in range(16)]
                hex_str1 = " ".join(f"{b:02X}" for b in raw_bytes[:8])
                hex_str2 = " ".join(f"{b:02X}" for b in raw_bytes[8:])
                hex_full = f"{hex_str1}  {hex_str2}"
                ascii_repr = "".join(chr(b) if 32 <= b <= 126 else "." for b in raw_bytes)

                self._write(f"  {offset}  {hex_full:<49}  |{ascii_repr}|", tag="green")
                self.after(40, lambda: stream_block(i + 1))
            else:
                self._write("\n[✓] Buffer stream complete. 0 parity errors detected.\n", tag="bright_green")
                self.is_busy = False

        stream_block()

    def _cmd_override(self, args):
        """Multi-stage system override & privilege escalation."""
        system = args[0].upper() if args else "DEFENSE_GRID"
        self.is_busy = True
        self._write(f"[!] INITIATING SYSTEM OVERRIDE PROTOCOL ON [{system}]...", tag="yellow")

        stages = [
            ("Stage 1/4: Injecting Heap Buffer Overflow to Kernel Driver", 180),
            ("Stage 2/4: Neutralizing Quantum Antivirus Watchdogs", 220),
            ("Stage 3/4: Patching SID Token & Acquiring SYSTEM Privileges", 200),
            ("Stage 4/4: Deploying Persistent Neural Ring-0 Rootkit", 240)
        ]

        def run_stage(idx=0):
            if idx < len(stages):
                desc, wait_time = stages[idx]
                self._write(f"  [+] {desc}...", tag="cyan")
                self.after(wait_time, lambda: run_stage(idx + 1))
            else:
                self._write("\n=======================================================", tag="bright_green")
                self._write(f"  [✓] SYSTEM OVERRIDE SUCCESSFUL: {system}", tag="white")
                self._write(f"  [✓] ROOT ACCESS: GRANTED (UID=0, GID=0, CAP_SYS_ADMIN)", tag="bright_green")
                self._write("=======================================================\n", tag="bright_green")
                self.lbl_telemetry.config(text=f"CORE: {system} [COMPROMISED]", fg="#ff3333")
                self.is_busy = False

        run_stage()

    def _cmd_inject(self, args):
        target = args[0].upper() if args else "MAINFRAME"
        self.is_busy = True
        self._write(f"[*] INJECTING PAYLOAD TO {target} PORT 443 (TLS TUNNEL)...", tag="yellow")

        payloads = [
            "0x90 0x90 0x90 (NOP Sled)",
            "0x31 0xC0 0x50 0x68 0x2F 0x2F (Shellcode Payload)",
            "0xFF 0xE4 (JMP ESP Vector)",
            "0xCC (Breakpoint Trap Confirmed)"
        ]

        def step_inject(i=0):
            if i < len(payloads):
                self._write(f"  --> Transmitting Block {i+1}: [ {payloads[i]} ] OK", tag="dark_green")
                self.after(120, lambda: step_inject(i + 1))
            else:
                self._write("[✓] PAYLOAD EXECUTED: Daemon spawned with PID 8192.\n", tag="bright_green")
                self.is_busy = False

        step_inject()

    def _cmd_trace(self, args):
        target_ip = args[0] if args else "10.0.84.12"
        self.is_busy = True
        self._write(f"[*] TRACEROUTE TO {target_ip} (Max 6 Hops, 64-byte packets)...", tag="yellow")

        hops = [
            ("1", "10.0.0.1", "zion-gateway.local", "1.12 ms"),
            ("2", "172.16.4.1", "orbital-repeater-alpha.net", "4.35 ms"),
            ("3", "192.168.99.2", "subgrid-firewall-relay.core", "12.80 ms"),
            ("4", "10.128.0.5", "matrix-ingress-router-04", "18.42 ms"),
            ("5", target_ip, "target-node-prime.zion", "21.05 ms")
        ]

        def step_hop(i=0):
            if i < len(hops):
                num, ip, host, rtt = hops[i]
                self._write(f"  {num:>2}  {ip:<16}  {host:<32}  {rtt}", tag="cyan")
                self.after(110, lambda: step_hop(i + 1))
            else:
                self._write("[✓] Trace complete. Route converged successfully.\n", tag="bright_green")
                self.is_busy = False

        step_hop()

    def _cmd_ping(self, args):
        target = args[0] if args else "mainframe"
        self.is_busy = True
        self._write(f"[*] PING {target} with 32 bytes of quantum telemetry data:", tag="yellow")

        def send_ping(seq=1):
            if seq <= 4:
                lat = random.randint(3, 14)
                self._write(f"  64 bytes from {target}: icmp_seq={seq} ttl=64 time={lat}.{random.randint(10,99)}ms", tag="green")
                self.after(150, lambda: send_ping(seq + 1))
            else:
                self._write("\n--- PING STATISTICS ---", tag="white")
                self._write("  4 packets transmitted, 4 received, 0% packet loss, time 602ms\n", tag="bright_green")
                self.is_busy = False

        send_ping()

    def _cmd_matrix(self, args):
        lines = int(args[0]) if args and args[0].isdigit() else 18
        chars = [chr(i) for i in range(0x30A0, 0x30DF)] + ["0", "1", "X", "#", "$", "%"]
        self.is_busy = True

        def stream_line(step=0):
            if step < lines:
                row = " ".join(random.choice(chars) if random.random() > 0.4 else " " for _ in range(35))
                self._write(f"  {row}", tag="green")
                self.after(30, lambda: stream_line(step + 1))
            else:
                self._write("")
                self.is_busy = False

        stream_line()

    def _cmd_theme(self, args):
        """Inspects or switches color theme dynamically."""
        available = list(self.config.get("themes", {}).keys())
        if not args:
            self._write(f"\n--- THEME CONFIGURATION ({CONFIG_FILE}) ---", tag="white")
            self._write(f"  Active Theme  : {self.current_theme_name}", tag="bright_green")
            self._write(f"  Font Family   : {self.font_family} (Terminal: {self.font_size_term}pt, Rain: {self.font_size_rain}pt)", tag="cyan")
            self._write("  Available Themes:", tag="white")
            for t in available:
                prefix = "  [✓] " if t == self.current_theme_name else "  [ ] "
                self._write(f"{prefix}{t}", tag="green" if t != self.current_theme_name else "bright_green")
            self._write(f"\nUsage: theme [theme_name] (e.g. 'theme cyber_amber', 'theme ice_cyan')\n", tag="cyan")
            return

        choice = args[0].lower()
        if choice in self.config.get("themes", {}):
            self.current_theme_name = choice
            self.theme = self.config["themes"][choice]
            self._apply_theme()
            self._save_config()
            self._write(f"[✓] Switched theme to '{choice}'. Configuration saved to disk.\n", tag="bright_green")
        else:
            self._write(f"[!] Unknown theme '{choice}'. Available: {', '.join(available)}\n", tag="red")

    def _cmd_philosophy(self, args=None):
        """Displays Carl Jung's depth psychology, individuation, and consciousness insights."""
        topic = args[0].lower() if args else "all"

        insights = {
            "persona": {
                "title": "THE PERSONA & THE SOCIAL MASK",
                "content": [
                    "• The persona is a functional adaptation to social life, not the totality of your being.",
                    "• Being good at a role does not mean it can contain the fullness of your unfolding life.",
                    "• Recognize emotions and drives beyond your mask without needing to destroy the mask entirely.",
                    "• Question inherited definitions of success, status, and failure: are they truly yours?"
                ]
            },
            "individuation": {
                "title": "INDIVIDUATION & PERSONAL RESPONSIBILITY",
                "content": [
                    "• Individuation is the journey of integrating the conscious and unconscious Self.",
                    "• Take total personal responsibility: no one else can bear the consequences of your choices.",
                    "• Face the unanswerable questions alone: what to devote life to, what to end, and who to become.",
                    "• Others can guide you to the water's edge, but you must swim to the far shore yourself."
                ]
            },
            "synchronicity": {
                "title": "SYNCHRONICITY (ACAUSAL MEANINGFUL COINCIDENCE)",
                "content": [
                    "• Synchronicity is the intersection of external events with inner psychic questions.",
                    "• Treat synchronicity as an invitation for deeper introspection, not fatalistic superstition.",
                    "• Discern meaningful patterns without obsessively over-interpreting random chance."
                ]
            },
            "shadow": {
                "title": "CONFRONTING THE SHADOW & UNCERTAINTY",
                "content": [
                    "• 'One does not become enlightened by imagining figures of light, but by making the darkness conscious.'",
                    "• Examine hidden motives, unasked questions, and unacknowledged limitations.",
                    "• Genuine awakening brings greater consciousness, not dogmatic certainty.",
                    "• Remain open to what you do not yet know."
                ]
            },
            "humility": {
                "title": "EGO INFLATION VS. CONSCIOUS HUMILITY",
                "content": [
                    "• Beware psychological inflation: when the ego confuses insight with superiority.",
                    "• Awakening is not a badge of elitism ('I am enlightened, they are asleep').",
                    "• Ground your realizations into humble daily practice, self-discipline, and compassion."
                ]
            }
        }

        if topic in insights:
            selected = [insights[topic]]
        else:
            selected = list(insights.values())

        self._write("\n================================================================================", tag="white")
        self._write("                 CARL JUNG // DEPTH PSYCHOLOGY & INDIVIDUATION                 ", tag="bright_green")
        self._write("================================================================================", tag="white")

        for section in selected:
            self._write(f"\n[ {section['title']} ]", tag="cyan")
            for line in section["content"]:
                self._write(f"  {line}", tag="green")

        quotes = [
            "\"Who looks outside, dreams; who looks inside, awakes.\" — Carl G. Jung",
            "\"Until you make the unconscious conscious, it will direct your life and you will call it fate.\" — Carl G. Jung",
            "\"The privilege of a lifetime is to become who you truly are.\" — Carl G. Jung"
        ]
        self._write(f"\nORACLE ARCHIVE: {random.choice(quotes)}\n", tag="yellow")

    def _cmd_status(self):
        self._write("\n--- OPERATOR & TELEMETRY STATUS ---", tag="white")
        self._write("  Connection  : SECURE_NEURAL_UPLINK (Zion-Node-7)", tag="bright_green")
        self._write("  Encryption  : Quantum 4096-bit Lattice", tag="green")
        self._write(f"  Active Theme: {self.current_theme_name} ({self.font_family})", tag="cyan")
        self._write(f"  Signal Noise: 0.00{random.randint(1,9)} dB", tag="green")
        self._write(f"  Cortex Load : {random.randint(18, 42)}%", tag="yellow")
        self._write(f"  Target Nodes: {', '.join(MOCK_TARGETS.keys())}\n", tag="cyan")


if __name__ == "__main__":
    app = UnifiedMatrixTerminal()
    app.mainloop()
