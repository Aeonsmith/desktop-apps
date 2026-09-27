# Desktop Applications & Matrix Terminal Suite
> **Repository**: `Aeonsmith/desktop-apps` | **Environment**: Windows 11 / Python 3.14+

A collection of interactive desktop applications, terminal simulators, physics engines, and creative studio tools.

---

## Applications in the Suite

### 1. Matrix Neural Terminal & Mock CLI (`matrix_terminal.py`)
- **Dual-Pane Interface**: Real-time falling Matrix digital rain canvas paired with an interactive cyber CLI console.
- **Mock Command Suite**: `scan`, `crack`, `dump`, `override`, `inject`, `trace`, `ping`, `matrix`, `status`, `theme`, `philosophy`, and `help`.
- **Persistent Command History**: Automatically saves/loads across sessions (`~/.matrix_terminal_history.json`) with `Up`/`Down` navigation and `Tab` autocompletion.
- **Customizable Themes & Fonts**: Live theme switching (`matrix_green`, `cyber_amber`, `ice_cyan`, `synth_purple`, `blood_red`) and JSON configuration (`~/.matrix_terminal_config.json`).
- **Jungian Philosophy Module**: Exploration of Carl Jung's depth psychology (*Persona*, *Individuation*, *Synchronicity*, *The Shadow*, *Conscious Humility*).
- **Desktop Executable**: `dist/MatrixTerminal/MatrixTerminal.exe` with custom multi-resolution icon.

### 2. Firespray-31 (*Slave I*) Cockpit Avionics (`slave1_cockpit.py`)
- **Transit Ignition (`[T]`)**: 90-degree attitude rotation from horizontal landing to vertical attack mode with sublight propulsion spooling.
- **Tactical Mastermind Dials**: Real-time controls for IFF transponder spoofing, stealth heat baffles, rotary blasters, and seismic charges.
- **Diagnostic Alert & Triage Engine**: Priority-tiered alert hierarchy (`ADVISORY` → `CAUTION` → `CRITICAL` → `EMERGENCY`).
- **Blackbox Flight Recorder**: Structured telemetry snapshot persistence (`slave1_blackbox_log.json`) with visual frame playback.

### 3. Whiteflash Shader Art Engine (`whiteflash/`)
- Real-time ThreeJS and WebGL shader visualizer packaged with native desktop webview.
- Executable: `whiteflash/dist/Whiteflash/Whiteflash.exe`.

### 4. SimHack Physics Decryption Terminal (`simhack-physics-decryption/`)
- Interactive matrix and physics decryption terminal with network map topologies and audio synthesis.
- Executable: `simhack-physics-decryption/dist/SimHack_Physics_Decryption/SimHack_Physics_Decryption.exe`.

### 5. Zarathustrazoom 13D Cosmos Engine (`Zarathustrazoom-Engine/`)
- 13D fractal volumetric neurocosmic simulator rendered in high-density interactive canvas.
- Executable: `Zarathustrazoom-Engine/dist/Zarathustrazoom_Engine/Zarathustrazoom_Engine.exe`.

### 6. Creative Drawing Studio (`drawing_app/`)
- Full-featured canvas drawing suite with pen, brush, eraser, geometry tools, color palettes, undo/redo stacks, and lossless PIL export.
- Executable: `drawing_app/dist/DrawingStudio/DrawingStudio.exe`.

### 7. Positive Perspective Switch (`Desktop/Project 35/Positive_Switch.pyw`)
- Cognitive reframing utility with randomized affirmation cycling and local state persistence.

---

## Quick Launch & Execution

```powershell
# 1. Run Matrix Terminal
python matrix_terminal.py

# 2. Run Slave I Cockpit
python slave1_cockpit.py

# 3. Run Drawing Studio
python drawing_app/draw_app.py

# 4. Run Test Suites
python -m unittest test_matrix_terminal.py -v
python -m unittest test_slave1_cockpit.py -v
```

---

## Release Archive & Deployment

- **Release Package**: `MatrixTerminal-v1.0.0-Release.zip`
- **Desktop Shortcuts**: Deployed on user Desktop linking to all native binaries and scripts.
