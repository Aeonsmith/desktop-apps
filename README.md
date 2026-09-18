# Desktop Applications Suite

A collection of lightweight, standalone native Windows desktop applications and interactive tools with embedded custom icons and zero-dependency execution.

---

## 📦 Included Applications

### 1. 🔄 The Recursive Engine & Dual Principles
**Path:** `RecursiveEngine/`  
**Icon:** Custom Fractal Vortex (`app.ico`)  
**Type:** Standalone Native Desktop App (`RecursiveEngine.exe` / `index.html`)

- **Dual Principles Framework:**
  - 🕊️ *Let God do God:* Release control over what was never yours to carry; eliminate the panic tax.
  - ⚡ *Let You do You:* Radical ownership over craft, code, and execution with laser focus.
- **1,000× Recursive Transmutation Engine:**
  - Interactive spinning fractal wheel simulating instantaneous conversion of raw tension into directional torque.
  - State machine cycling from `Rest & Digest (8)` ➔ `Hyper-Recursion / Fun` ➔ `Rest & Digest (8)`.
  - Live execution log console and operational formula display.
- **Standalone Launching:** Opens in an isolated native application window with zero browser tabs or URL bars.

---

### 2. 🎮 Tic Tac Toe — Modern Neon Edition
**Path:** `TicTacToe/`  
**Icon:** Modern Neon X & O Grid (`app.ico`)  
**Type:** Standalone C# Windows Forms Application (`TicTacToe.exe`)

- **Game Modes:**
  - 🧑 vs 🤖 **Single Player (vs AI):**
    - 🟢 *Easy:* Casual random play.
    - 🟡 *Medium:* Smart tactical play with win/block awareness.
    - 🔴 *Master (Unbeatable):* Optimal Minimax decision-tree algorithm with alpha-beta pruning (mathematically impossible to defeat).
  - 👥 **2-Player Mode:** Local Pass & Play on the same machine.
- **Features & UI:**
  - Dark glassmorphism neon aesthetic (Cyan `#0ea5e9` X markers, Rose `#f43f5e` O markers).
  - Smooth double-buffered GDI+ anti-aliased rendering.
  - Real-time scorecards, streak tracking, and active turn indicators.
  - Dynamic winning strike line animations and victory celebration overlays.
  - Move undo support and round/score reset controls.
  - Synthesized audio sound effects for moves, victories, draws, and undos (with toggleable sound mute).

---

### 3. 🎨 Icon Generator Tool
**Path:** `GenerateIcons.cs` / `GenerateIcons.exe`  
- Standalone C# utility generating 256x256 multi-layered Windows `.ico` binaries with custom geometry and gradient palettes.

---

## 🚀 Building and Running

All programs compile cleanly on standard Windows with the built-in Microsoft .NET Framework C# compiler (`csc.exe`):

```powershell
# Compile Recursive Engine Launcher
& "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /target:winexe /win32icon:"RecursiveEngine\app.ico" /out:"RecursiveEngine\RecursiveEngine.exe" /r:System.Windows.Forms.dll /r:System.Drawing.dll "RecursiveEngine\Program.cs"

# Compile Tic Tac Toe Game
& "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /target:winexe /win32icon:"TicTacToe\app.ico" /out:"TicTacToe\TicTacToe.exe" /r:System.Windows.Forms.dll /r:System.Drawing.dll /r:System.dll "TicTacToe\Program.cs"
```

---

## 📜 License
MIT
