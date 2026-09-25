# Desktop Applications Suite

A collection of lightweight, standalone native Windows desktop applications, quantum circuit hacking engines, 3D/13D simulation environments, and tactical interactive tools with zero-dependency execution and bundled custom icons.

---

## 📥 Installation & Quick Start (Releases)

Download ready-to-run release bundles directly from GitHub Releases:

1. Visit [Releases v1.0.0](https://github.com/Aeonsmith/desktop-apps/releases/tag/v1.0.0).
2. Download the desired `.zip` bundle for any application:
   - `QuantumLogicGame-v1.0.0-windows.zip`
   - `SimHack_Physics_Decryption-v1.0.0-windows.zip`
   - `TikTokTac-v1.0.0-windows.zip`
   - `Whiteflash-v1.0.0-windows.zip`
   - `Zarathustrazoom_Engine-v1.0.0-windows.zip`
3. Extract the ZIP archive to a local folder.
4. Double-click the main `.exe` file (e.g. `QuantumLogicGame.exe`) to launch immediately. No additional dependencies or runtime installation required.

---

## 📦 Included Applications

### 1. ⚡ LogicCore :: Quantum Logic Game
**Directory:** `quantum-logic-game/`  
**Executable:** `QuantumLogicGame.exe`  
**Type:** Native PyWebView Desktop App with Web Audio Synthesizer  
- **Features:**
  - Interactive quantum circuit board with real-time Qubit state calibration.
  - Multi-gate logic: Pauli-X (Bit Flip), Hadamard (H Superposition), Phase Flip (Z), CNOT, and SWAP gates.
  - Real-time animated quantum probability waveform visualizer.
  - Procedural sound synthesis and progressive multi-stage puzzle missions.

### 2. 🌌 SimHack :: Physics Decryption Terminal
**Directory:** `simhack-physics-decryption/`  
**Executable:** `SimHack_Physics_Decryption.exe`  
**Type:** Standalone Terminal Simulator with Matrix Background & Dynamic Topology  
- **Features:**
  - Full matrix rain canvas background and cyber-themed HUD.
  - Interactive SVG subsystem network topology map.
  - Live decryption console log with custom command parser.
  - Speedrun timer, milestone records, audio synthesizer effects, and embedded documentation.

### 3. ✨ Whiteflash :: 3D Shader Art Engine
**Directory:** `whiteflash/`  
**Executable:** `Whiteflash.exe`  
**Type:** High-Performance ThreeJS / WebGL Native Window App  
- **Features:**
  - Real-time custom fragment/vertex GLSL shader rendering in Three.js.
  - Responsive window viewport scaling and zero browser UI overhead.
  - Built with TypeScript and Vite compiled to an isolated `dist_web` bundle.

### 4. 🌀 Zarathustrazoom 13D Cosmos Engine
**Directory:** `Zarathustrazoom-Engine/`  
**Executable:** `Zarathustrazoom_Engine.exe`  
**Type:** 13D Fractal Volumetric Simulator & Binaural Audio Synthesizer  
- **Features:**
  - 6-DOF (Degrees of Freedom) camera navigation with velocity, position, and pitch/yaw/roll telemetry.
  - Real-time volumetric fractal manifold parameter tweaking (iteration depth, power exponent, scale, color presets).
  - Binaural brainwave audio entrainment synthesizer (Delta, Theta, Alpha, Beta, Gamma presets).
  - Live audio spectrum frequency visualizer.

### 5. 🎯 TikTok Tac :: Tactical Cuffbreaker
**Directory:** `tiktok_tac/`  
**Executable:** `TikTokTac.exe`  
**Type:** Tactical Undefined App & Parahistory Graph Engine  
- **Features:**
  - Tactical command console with CRT scanline visual filter.
  - Parahistory graph tree renderer and element inspector.
  - Real-time state-machine progression and quick command chips.

### 6. 🔄 The Recursive Engine & Dual Principles
**Directory:** `RecursiveEngine/`  
**Executable:** `RecursiveEngine.exe`  
**Type:** Standalone C# Native Desktop App  
- **Features:**
  - 1,000× recursive transmutation spinning fractal wheel.
  - State machine cycling from `Rest & Digest (8)` ➔ `Hyper-Recursion / Fun` ➔ `Rest & Digest (8)`.

### 7. 🎮 Tic Tac Toe — Modern Neon Edition
**Directory:** `TicTacToe/`  
**Executable:** `TicTacToe.exe`  
**Type:** C# Windows Forms Application  
- **Features:**
  - Minimax AI engine with alpha-beta pruning (Master mode) and 2-Player local mode.
  - Neon dark glassmorphism aesthetic with anti-aliased GDI+ rendering.

---

## 🛠️ Building From Source

### Prerequisites
- Python 3.10+ with `pywebview` and `pyinstaller`
- Node.js 18+ (for Whiteflash Vite frontend)
- Microsoft .NET Framework C# compiler (`csc.exe`) for C# applications

### Build Commands

#### 1. Quantum Logic Game
```powershell
cd quantum-logic-game
python -m PyInstaller --noconfirm QuantumLogicGame.spec
```

#### 2. SimHack Physics Decryption
```powershell
cd simhack-physics-decryption
python -m PyInstaller --noconfirm SimHack_Physics_Decryption.spec
```

#### 3. Whiteflash
```powershell
cd whiteflash
npm run build
python -m PyInstaller --noconfirm Whiteflash.spec
```

#### 4. Zarathustrazoom 13D Engine
```powershell
cd Zarathustrazoom-Engine
python -m PyInstaller --noconfirm Zarathustrazoom_Engine.spec
```

#### 5. TikTok Tac
```powershell
cd tiktok_tac
python -m PyInstaller --noconfirm TikTokTac.spec
```

---

## 📜 License
MIT
