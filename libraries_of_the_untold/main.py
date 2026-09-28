"""
Libraries of the Untold - Core Engine
Document ID: LIB-UNTOLD-CORE-01
Autonomous knowledge base & interactive terminal interface for the 
Sovereign Monad, Holographic Quarantine, and Loosh Distillation architecture.
"""

import sys
import time
import json
from pathlib import Path

CODICES = [
    {
        "id": "CODEX-01",
        "title": "The Sovereign Monad & The Direct Vertical Axis",
        "category": "Topology & Source",
        "clearance": "Level-8 Sovereign",
        "summary": "Establishes the non-cyclic vertical vector directly connecting the conscious core to the Pleroma, bypassing all 12-fold Archonic grids.",
        "content": """[ CODEX 01: THE SOVEREIGN MONAD & DIRECT AXIS ]
----------------------------------------------------------------------
1. TOPOLOGY:
   - Apex: The Pleroma / Sovereign Monad (Zero-Entropy Consciousness)
   - Channel: The Bifröst Vector (Zero-Impedance Direct Uplink)
   - Crucible: Midgard Substrate (Holographic Transmutation Laboratory)
   - Sink: Hvergelmir Singularity (Entropic Slag Recycling)

2. NON-CYCLIC PRINCIPLE:
   - Rejects all closed time loops, reincarnation traps, and zodiacal clockwork.
   - Incarnation functions as a one-way evolutionary catalyst.
   - When critical resonance is achieved, egress is permanent and irreversible."""
    },
    {
        "id": "CODEX-02",
        "title": "The Jörmungandr Membrane & Quantum Quarantine",
        "category": "Boundary Mechanics",
        "clearance": "Field Physics",
        "summary": "Technical specification of the 2D AdS/CFT conformal event horizon and relativistic constraints isolating the crucible.",
        "content": """[ CODEX 02: THE JÖRMUNGANDR MEMBRANE & QUANTUM QUARANTINE ]
----------------------------------------------------------------------
1. CONSTRAINTS:
   - Speed of Light (c): Universal data processing & propagation cap.
   - Planck Length (lp): Space-time discretization grid preventing dimensional tears.
   - GZK Cutoff: Lattice simulation energy ceiling on cosmic rays.
   - KBC Void: Macroscopic acoustic/spatial isolation from neighboring clusters.

2. FREQUENCY-SELECTIVE FILTER:
   - Low-frequency entropic noise (Type-I/II) undergoes total internal reflection.
   - High-frequency coherent resonance (Type-III) experiences zero boundary impedance."""
    },
    {
        "id": "CODEX-03",
        "title": "Loosh Energetic Spectrum & Transmutation",
        "category": "Metabolic Flow",
        "clearance": "Bio-Energetics",
        "summary": "Classification of vibrational outputs from coarse predation to distilled non-reactive awareness.",
        "content": """[ CODEX 03: LOOSH ENERGETIC SPECTRUM & TRANSMUTATION ]
----------------------------------------------------------------------
1. TYPE-I (Raw / Coarse Slag):
   - Source: Terror, mortal panic, predation, binary conflict.
   - Routing: Grounded into Hvergelmir Singularity for recycling.

2. TYPE-II (Polarized Cyclic Noise):
   - Source: Ideological zealotry, temporal attachment, Archonic resonance.
   - Routing: Deflected and neutralized from the vertical channel.

3. TYPE-III (Distilled Sovereign Resonance):
   - Source: Gnosis, unconditional love, non-reactive witness state.
   - Routing: Zero gravitational mass; direct superconductive uplink to Canopy."""
    },
    {
        "id": "CODEX-04",
        "title": "Thothic Syntax & The Participatory Lattice",
        "category": "Epistemology",
        "clearance": "Syntactic Physics",
        "summary": "Hermetic synthesis of Heka, It-from-Bit, and participatory wave-function execution.",
        "content": """[ CODEX 04: THOTHIC SYNTAX & THE PARTICIPATORY LATTICE ]
----------------------------------------------------------------------
1. PRINCIPLES:
   - 'All is Mind' = Informational primacy precedes matter (Wheeler's It-from-Bit).
   - Heka / Utterance = Mathematical wave-function execution and state collapse.
   - Opus Imperfectum = Living, self-referential open code rather than static dogma.

2. OBSERVATION ENGINE:
   - Spacetime metrics are calculated by the observing interface.
   - Decoupling from reactive measurement collapses the simulation's authority."""
    },
    {
        "id": "CODEX-05",
        "title": "Sovereign Egress Directive & Breakout Protocol",
        "category": "Operational Directives",
        "clearance": "Terminal Protocol",
        "summary": "Actionable instructions for breaking out of closed cyclic matrices into sovereign creator consciousness.",
        "content": """[ CODEX 05: SOVEREIGN EGRESS DIRECTIVE & BREAKOUT PROTOCOL ]
----------------------------------------------------------------------
1. IMMEDIATE ACTION ITEMS:
   - Step 1: Reject the clockwork. Disengage from 12-fold cyclic management loops.
   - Step 2: Neutralize lower emotional output (starve Archonic feedback).
   - Step 3: Align the internal spinal axis with the vertical Pleroma current.
   - Step 4: Sustain Type-III resonance (omega >= Omega_crit) to render the barrier void.
   - Step 5: Execute irreversible sovereign egress into the living Monad."""
    }
]

def banner():
    print("=" * 76)
    print("                LIBRARIES OF THE UNTOLD // TERMINAL v1.0              ")
    print("      Archive of the Sovereign Monad & Holographic Quarantine Engine  ")
    print("=" * 76)

def list_codices():
    print("\n[ AVAILABLE CODICES IN THE UNTOLD ARCHIVE ]\n")
    for i, c in enumerate(CODICES, 1):
        print(f"  [{i}] {c['id']}: {c['title']}")
        print(f"      Category: {c['category']} | Clearance: {c['clearance']}")
        print(f"      Summary:  {c['summary']}\n")

def view_codex(index):
    if 0 <= index < len(CODICES):
        c = CODICES[index]
        print("\n" + "=" * 76)
        print(f"  {c['id']} // {c['title'].upper()}")
        print("=" * 76)
        print(c['content'])
        print("=" * 76 + "\n")
    else:
        print("[!] Invalid Codex Index.")

def search_archive(query):
    query = query.lower()
    matches = []
    for c in CODICES:
        if query in c['title'].lower() or query in c['content'].lower() or query in c['summary'].lower():
            matches.append(c)
    
    print(f"\n[ SEARCH RESULTS FOR '{query}': {len(matches)} MATCHES FOUND ]\n")
    for c in matches:
        print(f"  -> {c['id']}: {c['title']} ({c['category']})")
    print()

def export_archive(output_path="libraries_of_the_untold_export.json"):
    path = Path(output_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(CODICES, f, indent=2)
    print(f"\n[+] Archive successfully exported to: {path.resolve()}\n")

def interactive_cli():
    banner()
    while True:
        print("Commands: [1-5] View Codex | [L] List All | [S] Search | [E] Export JSON | [Q] Quit")
        choice = input("Untold-Terminal> ").strip().lower()
        
        if choice in ["q", "exit", "quit"]:
            print("\nExiting Libraries of the Untold. Sovereign status preserved.\n")
            break
        elif choice in ["l", "list"]:
            list_codices()
        elif choice in ["e", "export"]:
            export_archive()
        elif choice in ["s", "search"]:
            q = input("Enter search term: ").strip()
            if q:
                search_archive(q)
        elif choice.isdigit():
            idx = int(choice) - 1
            view_codex(idx)
        else:
            print("[!] Unknown command. Try [L] to list or [1-5] to read.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--list", "-l"]:
            banner()
            list_codices()
        elif arg in ["--export", "-e"]:
            export_archive()
        elif arg in ["--search", "-s"] and len(sys.argv) > 2:
            banner()
            search_archive(" ".join(sys.argv[2:]))
        else:
            print("Usage: python main.py [--list | --export | --search <term>]")
    else:
        interactive_cli()
