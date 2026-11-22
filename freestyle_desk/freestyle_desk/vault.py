"""Fixed desktop folder. Stop writes the take. No save dialog."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .audio import save_vocal
from .gibber import HAPPY_ACCIDENT

SESSION_FIELDS = (
    "name",
    "starred",
    "tag",
    "kind",
    "beat",
    "loop_start",
    "loop_end",
    "bpm",
    "beat_position",
    "record_started_at",
    "created",
)


def desktop_sessions_root() -> Path:
    return Path.home() / "Desktop" / "Freestyle Sessions"


def session_folder_name(when: datetime) -> str:
    return when.strftime("%Y-%m-%d %H-%M")


def format_session(meta: dict) -> str:
    lines = []
    seen = set()
    for key in SESSION_FIELDS:
        if key in meta:
            lines.append(f"{key}: {meta[key]}")
            seen.add(key)
    for key, value in meta.items():
        if key not in seen:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def parse_session(text: str) -> dict:
    meta = {}
    for line in text.splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        meta[key] = value
    return meta


def _ps_quote(path: Path) -> str:
    return str(path).replace("'", "''")


def _powershell_exes() -> list[str]:
    """Full paths first. A pythonw launch often has no PowerShell on PATH."""
    windir = os.environ.get("SystemRoot", r"C:\Windows")
    candidates = [
        Path(windir) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "PowerShell" / "7" / "pwsh.exe",
    ]
    found = [str(path) for path in candidates if path.is_file()]
    for name in ("pwsh", "powershell"):
        from shutil import which

        located = which(name)
        if located and located not in found:
            found.append(located)
    return found


@dataclass
class WriteResult:
    folder: Path
    shortcut_ok: bool
    shortcut_error: str = ""


@dataclass
class SessionInfo:
    folder: Path
    meta: dict

    def display_name(self) -> str:
        name = self.meta.get("name", "").strip()
        return name or self.folder.name


class Vault:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else desktop_sessions_root()

    def ensure(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "Beats").mkdir(exist_ok=True)
        return self.root

    def beats_dir(self) -> Path:
        self.ensure()
        return self.root / "Beats"

    def allocate_session_dir(self, when: datetime) -> Path:
        self.ensure()
        base = session_folder_name(when)
        candidate = self.root / base
        if not candidate.exists():
            return candidate
        number = 2
        while (self.root / f"{base}-{number}").exists():
            number += 1
        return self.root / f"{base}-{number}"

    def write_session(self, when, samples, sample_rate, lyrics: str, meta: dict, scraps: str | None = None) -> WriteResult:
        folder = self.allocate_session_dir(when)
        folder.mkdir(parents=True, exist_ok=False)
        save_vocal(folder / "vocal.wav", samples, sample_rate)
        (folder / "lyrics.txt").write_text(lyrics, encoding="utf-8")
        self._write_scraps_file(folder, scraps)
        return self._store_meta(folder, meta, when)

    def write_scraps_session(self, when, lyrics: str, scraps: str, meta: dict) -> WriteResult:
        """A session of generated scraps. No microphone file."""
        folder = self.allocate_session_dir(when)
        folder.mkdir(parents=True, exist_ok=False)
        (folder / "lyrics.txt").write_text(lyrics, encoding="utf-8")
        self._write_scraps_file(folder, scraps)
        payload = dict(meta)
        payload["kind"] = "scraps"
        payload.setdefault("tag", HAPPY_ACCIDENT)
        return self._store_meta(folder, payload, when)

    def _write_scraps_file(self, folder: Path, scraps: str | None) -> None:
        if not scraps or not scraps.strip():
            return
        text = scraps if scraps.endswith("\n") else scraps + "\n"
        (folder / "scraps.txt").write_text(text, encoding="utf-8")

    def _store_meta(self, folder: Path, meta: dict, when: datetime) -> WriteResult:
        payload = dict(meta)
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S")
        payload.setdefault("created", stamp)
        payload.setdefault("record_started_at", payload["created"])
        payload.setdefault("name", "")
        payload.setdefault("starred", "0")
        (folder / "session.txt").write_text(format_session(payload), encoding="utf-8")
        shortcut_ok = True
        shortcut_error = ""
        try:
            self.write_latest_shortcut(folder)
        except Exception as exc:
            shortcut_ok = False
            shortcut_error = str(exc)
        return WriteResult(folder, shortcut_ok, shortcut_error)

    def write_latest_shortcut(self, target: Path) -> Path:
        self.ensure()
        link = self.root / "Latest.lnk"
        script = (
            "$sh = New-Object -ComObject WScript.Shell; "
            f"$s = $sh.CreateShortcut('{_ps_quote(link)}'); "
            f"$s.TargetPath = '{_ps_quote(target)}'; "
            "$s.Save()"
        )
        errors = []
        try:
            import win32com.client

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(link))
            shortcut.TargetPath = str(target)
            shortcut.Save()
            if link.is_file():
                return link
            errors.append("win32com: shortcut was not written")
        except Exception as exc:
            errors.append(f"win32com: {exc}")
        for executable in _powershell_exes():
            try:
                completed = subprocess.run(
                    [executable, "-NoProfile", "-NonInteractive", "-Command", script],
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
            except OSError as exc:
                errors.append(f"{executable}: {exc}")
                continue
            if completed.returncode == 0 and link.is_file():
                return link
            detail = (completed.stderr or completed.stdout or "shortcut failed").strip()
            errors.append(f"{executable}: {detail}")
        raise RuntimeError("; ".join(errors) or "shortcut failed")

    def update_session(self, folder: Path, *, name: str | None = None, starred: bool | None = None) -> dict:
        path = Path(folder) / "session.txt"
        meta = parse_session(path.read_text(encoding="utf-8"))
        if name is not None:
            meta["name"] = name
        if starred is not None:
            meta["starred"] = "1" if starred else "0"
        path.write_text(format_session(meta), encoding="utf-8")
        return meta

    def list_sessions(self) -> list[SessionInfo]:
        if not self.root.exists():
            return []
        found = []
        for folder in self.root.iterdir():
            if not folder.is_dir() or folder.name == "Beats":
                continue
            session_file = folder / "session.txt"
            if not session_file.exists():
                continue
            meta = parse_session(session_file.read_text(encoding="utf-8"))
            found.append(SessionInfo(folder, meta))
        found.sort(key=lambda item: item.meta.get("created", item.folder.name), reverse=True)
        return found

    def list_beats(self, suffixes: tuple[str, ...] = (".wav",)) -> list[Path]:
        beats = self.beats_dir()
        allowed = {suffix.lower() for suffix in suffixes}
        files = [path for path in beats.iterdir() if path.is_file() and path.suffix.lower() in allowed]
        files.sort(key=lambda path: path.name.lower())
        return files
