"""One window. Beat on top, pad in the middle, rhymes in the margin, takes along the bottom."""

from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from .audio import Engine, beat_slot_index, beat_suffixes, parse_bpm, parse_seconds, pocket_slots
from .gibber import HAPPY_ACCIDENT, bones_text, format_warmup, happy_accident_tag, leave_pad, session_lyrics, warmup_lines
from .rhymes import RhymeIndex, apply_lookup, load_default_index
from .typeset import typeset
from .vault import Vault, parse_session

ctk.set_appearance_mode("dark")


class DeskApp(ctk.CTk):
    def __init__(self, vault: Vault | None = None, index: RhymeIndex | None = None):
        super().__init__()
        self.vault = vault or Vault()
        self.vault.ensure()
        self.index = index if index is not None else load_default_index()
        self.engine = Engine()
        self._rec_mark: float | None = None
        self._scrap_lines: list[str] = []
        self._slot_count = len(pocket_slots())

        self.title("Freestyle Desk")
        self.geometry("1120x780")
        self.minsize(920, 640)
        self.c_bg = "#10110f"
        self.c_card = "#1a1c16"
        self.c_border = "#2c2e26"
        self.c_text = "#f4f1e8"
        self.c_muted = "#9aa18f"
        self.c_accent = "#d6ff4a"
        self.c_record = "#ff5a36"
        self.c_slot = "#2a2c24"
        self.c_input = "#14160f"
        self.configure(fg_color=self.c_bg)
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(80, self._tick)
        if self.index.prons:
            self._set_status("Drop wav or mp3 files into Freestyle Sessions\\Beats. Headphones keep the beat out of the vocal.")
        else:
            self._set_status("Rhyme index missing. Recording still works. Drop wav or mp3 files into the Beats folder.")

    def _build(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(14, 4))
        ctk.CTkLabel(
            header,
            text="FREESTYLE DESK",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=self.c_text,
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text="The margin suggests. It does not write.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.c_muted,
        ).pack(anchor="w")

        beat = ctk.CTkFrame(self, fg_color=self.c_card, corner_radius=12, border_width=1, border_color=self.c_border)
        beat.pack(fill="x", padx=16, pady=8)
        row = ctk.CTkFrame(beat, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=10)

        self.beat_var = ctk.StringVar(value="Drop a wav or mp3 in Beats")
        self.beat_menu = ctk.CTkOptionMenu(
            row,
            variable=self.beat_var,
            values=["Drop a wav or mp3 in Beats"],
            fg_color=self.c_input,
            button_color="#34382c",
            button_hover_color="#454a3a",
            width=220,
            height=32,
        )
        self.beat_menu.pack(side="left")
        self.play_btn = ctk.CTkButton(row, text="Play", width=72, height=32, fg_color=self.c_accent, text_color="#111", hover_color="#c4ef2e", command=self._toggle_play)
        self.play_btn.pack(side="left", padx=(8, 4))
        ctk.CTkButton(row, text="Refresh", width=72, height=32, fg_color="#34382c", hover_color="#454a3a", command=self.refresh_beats).pack(side="left", padx=4)
        ctk.CTkButton(row, text="Beats folder", width=96, height=32, fg_color="#34382c", hover_color="#454a3a", command=self._open_beats).pack(side="left", padx=4)

        ctk.CTkLabel(row, text="Vol", text_color=self.c_muted).pack(side="left", padx=(12, 4))
        self.vol = ctk.CTkSlider(row, from_=0, to=1, number_of_steps=100, width=90, command=self._on_volume)
        self.vol.set(0.8)
        self.vol.pack(side="left")

        ctk.CTkLabel(row, text="Loop", text_color=self.c_muted).pack(side="left", padx=(12, 4))
        self.loop_start = ctk.CTkEntry(row, width=52, height=32, placeholder_text="0")
        self.loop_start.insert(0, "0")
        self.loop_start.pack(side="left")
        ctk.CTkLabel(row, text="–", text_color=self.c_muted).pack(side="left", padx=4)
        self.loop_end = ctk.CTkEntry(row, width=52, height=32, placeholder_text="0")
        self.loop_end.insert(0, "0")
        self.loop_end.pack(side="left")
        ctk.CTkLabel(row, text="BPM", text_color=self.c_muted).pack(side="left", padx=(12, 4))
        self.bpm_entry = ctk.CTkEntry(row, width=52, height=32)
        self.bpm_entry.insert(0, "90")
        self.bpm_entry.pack(side="left")

        self.slot_row = ctk.CTkFrame(self, fg_color="transparent")
        self.slot_row.pack(fill="x", padx=16, pady=(0, 6))
        self.slot_frames = []
        for _empty in pocket_slots():
            slot = ctk.CTkFrame(self.slot_row, fg_color=self.c_slot, height=14, corner_radius=3)
            slot.pack(side="left", fill="x", expand=True, padx=2)
            self.slot_frames.append(slot)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.pack(fill="both", expand=True, padx=16, pady=4)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=0)
        workspace.grid_rowconfigure(0, weight=1)

        pad_card = ctk.CTkFrame(workspace, fg_color=self.c_card, corner_radius=12, border_width=1, border_color=self.c_border)
        pad_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ctk.CTkLabel(pad_card, text="Lyrics", text_color=self.c_text, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(8, 0))
        self.pad = ctk.CTkTextbox(
            pad_card,
            fg_color=self.c_input,
            text_color=self.c_text,
            font=ctk.CTkFont(family="Consolas", size=15),
            wrap="word",
            undo=True,
        )
        self.pad.pack(fill="both", expand=True, padx=12, pady=8)
        self.pad.bind("<KeyRelease>", self._on_pad_key)
        self.pad.bind("<ButtonRelease-1>", self._on_pad_key)

        margin_card = ctk.CTkFrame(workspace, fg_color=self.c_card, corner_radius=12, border_width=1, border_color=self.c_border, width=280)
        margin_card.grid(row=0, column=1, sticky="nsew")
        margin_card.grid_propagate(False)
        self.margin_title = ctk.CTkLabel(margin_card, text="Rhymes", text_color=self.c_accent, font=ctk.CTkFont(size=13, weight="bold"))
        self.margin_title.pack(anchor="w", padx=12, pady=(8, 0))
        self.margin = ctk.CTkTextbox(
            margin_card,
            fg_color=self.c_input,
            text_color=self.c_muted,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
            width=250,
        )
        self.margin.pack(fill="both", expand=True, padx=12, pady=8)
        self.margin.insert("1.0", "Finish a word.")
        self.margin.bind("<Key>", lambda _event: "break")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=16, pady=6)
        self.record_btn = ctk.CTkButton(
            actions,
            text="Record",
            height=44,
            fg_color=self.c_record,
            hover_color="#e04828",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._toggle_record,
        )
        self.record_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            actions,
            text="Typeset",
            width=88,
            height=44,
            fg_color="#34382c",
            hover_color="#454a3a",
            command=self._typeset,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            actions,
            text="Warm-up",
            width=88,
            height=44,
            fg_color="#34382c",
            hover_color="#454a3a",
            command=self._warmup,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            actions,
            text="Bones",
            width=72,
            height=44,
            fg_color="#34382c",
            hover_color="#454a3a",
            command=self._bones,
        ).pack(side="left")

        self.film = ctk.CTkScrollableFrame(
            self,
            orientation="horizontal",
            height=150,
            fg_color=self.c_card,
            corner_radius=12,
            border_width=1,
            border_color=self.c_border,
        )
        self.film.pack(fill="x", padx=16, pady=(4, 6))

        self.status_var = ctk.StringVar(value="")
        ctk.CTkLabel(self, textvariable=self.status_var, text_color=self.c_muted, anchor="w", font=ctk.CTkFont(size=12)).pack(fill="x", padx=18, pady=(0, 10))
        self.refresh_beats()
        self._refresh_filmstrip()

    def _set_status(self, text: str) -> None:
        self.status_var.set(text)

    def _set_margin(self, text: str, title: str = "Rhymes") -> None:
        self.margin_title.configure(text=title)
        self.margin.delete("1.0", "end")
        self.margin.insert("1.0", text)

    def _on_pad_key(self, _event=None) -> None:
        text = self.pad.get("1.0", "end-1c")
        cursor = len(self.pad.get("1.0", "insert"))
        _same, margin = apply_lookup(text, cursor, self.index)
        if margin is not None:
            self._set_margin(margin)

    def _typeset(self) -> None:
        original = self.pad.get("1.0", "end-1c")
        sheet = typeset(original)
        self.pad.delete("1.0", "end")
        self.pad.insert("1.0", sheet)
        self._on_pad_key()
        self._set_status("Typeset. Words unchanged.")

    def _warmup(self) -> None:
        pad = self.pad.get("1.0", "end-1c")
        lines, source = warmup_lines(parse_bpm(self.bpm_entry.get()))
        leave_pad(pad)
        self._scrap_lines = list(lines)
        self._set_margin(format_warmup(lines, source), title="Warm-up")
        self._set_status(f"Warm-up from {source}. The pad was not changed.")

    def _bones(self) -> None:
        pad = self.pad.get("1.0", "end-1c")
        leave_pad(pad)
        self._set_margin(bones_text(pad, self.index), title="Bones")
        self._set_status("Bones of the pad. The words were not changed.")

    def _loop_values(self) -> tuple[float, float]:
        return parse_seconds(self.loop_start.get()), parse_seconds(self.loop_end.get())

    def _selected_beat(self) -> Path | None:
        path = self.vault.beats_dir() / self.beat_var.get()
        if path.is_file():
            return path
        return None

    def refresh_beats(self) -> None:
        names = [path.name for path in self.vault.list_beats(beat_suffixes())]
        if not names:
            names = ["Drop a wav or mp3 in Beats"]
        self.beat_menu.configure(values=names)
        if self.beat_var.get() not in names:
            self.beat_var.set(names[0])

    def _open_beats(self) -> None:
        os.startfile(self.vault.beats_dir())
        self._set_status("Drop wav or mp3 files in that folder, then Refresh.")

    def _on_volume(self, value) -> None:
        self.engine.set_volume(float(value))

    def _apply_transport(self) -> None:
        if self.engine.has_beat:
            self.engine.set_loop(*self._loop_values())
        self.engine.set_volume(float(self.vol.get()))

    def _toggle_play(self) -> None:
        if self.engine.output_running:
            self.engine.pause()
            self.play_btn.configure(text="Play")
            self._set_status("Beat paused.")
            return
        path = self._selected_beat()
        if path is None:
            self._set_status("Drop a wav or mp3 into the Beats folder, then Refresh.")
            return
        try:
            if self.engine.beat_path != path:
                self.engine.load_beat(path)
            self._apply_transport()
            self.engine.play()
        except Exception as exc:
            self._set_status(f"Could not play beat: {exc}")
            return
        self.play_btn.configure(text="Pause")
        self._set_status(f"Playing {path.name}")

    def _toggle_record(self) -> None:
        if self.engine.recording:
            self._stop_record()
            return
        if self.engine.replaying:
            self._set_status("Stop replay before recording.")
            return
        if self._selected_beat() is not None and not self.engine.output_running:
            self._toggle_play()
            if not self.engine.output_running:
                return
        self._apply_transport()
        try:
            self.engine.start_recording()
        except Exception as exc:
            self._set_status(f"Mic did not open: {exc}")
            return
        self._rec_mark = time.monotonic()
        self.record_btn.configure(text="Stop  0:00")
        if self.engine.beat_path:
            self._set_status("Recording. The vocal file will not contain the beat.")
        else:
            self._set_status("Recording a cappella.")

    def _stop_record(self) -> None:
        recording = self.engine.stop_recording()
        self._rec_mark = None
        self.record_btn.configure(text="Record", fg_color=self.c_record)
        if recording is None:
            self._set_status("Nothing was recording.")
            return
        try:
            result = self._write_take(
                recording.samples,
                recording.sample_rate,
                when=recording.started_at,
                beat_position=recording.beat_position,
            )
        except Exception as exc:
            self._set_status(f"Take not saved: {exc}")
            return
        self._refresh_filmstrip()
        extra = "" if result.shortcut_ok else f" Shortcut failed: {result.shortcut_error}"
        tagged = " Tagged happy accident." if happy_accident_tag(self._scrap_lines) else ""
        self._set_status(f"Saved {result.folder.name}.{extra}{tagged}")

    def _write_take(self, samples, sample_rate: int, when: datetime | None = None, beat_position: float = 0.0):
        when = when or datetime.now()
        start, end = self._loop_values()
        bpm = parse_bpm(self.bpm_entry.get())
        beat = str(self.engine.beat_path) if self.engine.beat_path else ""
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S")
        tag = happy_accident_tag(self._scrap_lines)
        meta = {
            "name": "",
            "starred": "0",
            "beat": beat,
            "loop_start": f"{start:.3f}",
            "loop_end": f"{end:.3f}",
            "bpm": f"{bpm:.3f}",
            "beat_position": f"{beat_position:.3f}",
            "record_started_at": stamp,
            "created": stamp,
        }
        if tag:
            meta["tag"] = tag
        pad = self.pad.get("1.0", "end-1c")
        lyrics = session_lyrics(pad, self._scrap_lines)
        return self.vault.write_session(when, samples, sample_rate, lyrics, meta)

    def _paint_slots(self, index: int | None) -> None:
        for slot_index, slot in enumerate(self.slot_frames):
            slot.configure(fg_color=self.c_accent if slot_index == index else self.c_slot)

    def _tick(self) -> None:
        index = beat_slot_index(
            self.engine.position_seconds,
            parse_bpm(self.bpm_entry.get()),
            slots=self._slot_count,
            playing=self.engine.output_running,
        )
        self._paint_slots(index)
        if self.engine.recording and self._rec_mark is not None:
            elapsed = int(time.monotonic() - self._rec_mark)
            self.record_btn.configure(text=f"Stop  {elapsed // 60}:{elapsed % 60:02d}")
        if self.engine.replay_finished:
            self.engine.pause()
            self.play_btn.configure(text="Play")
            self._set_status("Replay finished.")
        self.after(80, self._tick)

    def _refresh_filmstrip(self) -> None:
        for child in self.film.winfo_children():
            child.destroy()
        sessions = self.vault.list_sessions()
        if not sessions:
            ctk.CTkLabel(self.film, text="No takes yet.", text_color=self.c_muted).pack(anchor="w", padx=8, pady=8)
            return
        for info in sessions[:40]:
            self._add_card(info)
        extra = len(sessions) - 40
        if extra > 0:
            ctk.CTkLabel(self.film, text=f"+{extra} older in the folder", text_color=self.c_muted).pack(side="left", padx=8)

    def _add_card(self, info) -> None:
        tagged = info.meta.get("tag") == HAPPY_ACCIDENT
        card = ctk.CTkFrame(
            self.film,
            fg_color=self.c_input,
            corner_radius=8,
            width=200,
            height=128 if tagged else 112,
            border_width=1 if tagged else 0,
            border_color=self.c_accent,
        )
        card.pack(side="left", padx=6, pady=4)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=info.folder.name, text_color=self.c_muted, font=ctk.CTkFont(size=11)).pack(anchor="w", padx=8, pady=(6, 0))
        if tagged:
            ctk.CTkLabel(
                card,
                text=HAPPY_ACCIDENT,
                text_color=self.c_accent,
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(anchor="w", padx=8)
        entry = ctk.CTkEntry(card, width=176, height=28, placeholder_text="name")
        if info.meta.get("name"):
            entry.insert(0, info.meta["name"])
        entry.pack(padx=8, pady=4)
        entry.bind("<FocusOut>", lambda _event, folder=info.folder, widget=entry: self._rename(folder, widget))
        entry.bind("<Return>", lambda _event, folder=info.folder, widget=entry: self._rename(folder, widget))
        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=8)
        star = "Starred" if info.meta.get("starred") == "1" else "Star"
        ctk.CTkButton(buttons, text=star, width=64, height=24, fg_color="#34382c", command=lambda folder=info.folder: self._toggle_star(folder)).pack(side="left")
        ctk.CTkButton(buttons, text="Load", width=48, height=24, fg_color="#34382c", command=lambda folder=info.folder: self._load_lyrics(folder)).pack(side="left", padx=4)
        ctk.CTkButton(buttons, text="Replay", width=58, height=24, fg_color="#34382c", command=lambda folder=info.folder: self._replay(folder)).pack(side="left")

    def _rename(self, folder: Path, entry) -> None:
        try:
            self.vault.update_session(folder, name=entry.get())
            self._set_status(f"Named {folder.name}.")
        except Exception as exc:
            self._set_status(f"Could not rename: {exc}")

    def _toggle_star(self, folder: Path) -> None:
        try:
            meta = parse_session((Path(folder) / "session.txt").read_text(encoding="utf-8"))
            self.vault.update_session(folder, starred=meta.get("starred") != "1")
        except Exception as exc:
            self._set_status(f"Could not star: {exc}")
            return
        self._refresh_filmstrip()

    def _load_lyrics(self, folder: Path) -> None:
        text = (Path(folder) / "lyrics.txt").read_text(encoding="utf-8")
        self.pad.delete("1.0", "end")
        self.pad.insert("1.0", text)
        self._on_pad_key()
        self._set_status(f"Loaded lyrics from {Path(folder).name}.")

    def _replay(self, folder: Path) -> None:
        if self.engine.recording:
            self._set_status("Stop the take before replay.")
            return
        folder = Path(folder)
        meta = parse_session((folder / "session.txt").read_text(encoding="utf-8"))
        vocal = folder / "vocal.wav"
        if not vocal.exists():
            self._set_status("No vocal in that session.")
            return
        beat = meta.get("beat", "")
        missing = bool(beat) and not Path(beat).is_file()
        if meta.get("bpm"):
            self.bpm_entry.delete(0, "end")
            self.bpm_entry.insert(0, meta["bpm"])
        try:
            self.engine.start_replay(
                vocal,
                "" if missing else beat,
                parse_seconds(meta.get("loop_start", "0")),
                parse_seconds(meta.get("loop_end", "0")),
                parse_seconds(meta.get("beat_position", "0")),
            )
        except Exception as exc:
            self._set_status(f"Replay failed: {exc}")
            return
        self.play_btn.configure(text="Pause")
        if missing:
            self._set_status(f"Beat missing. Replaying vocal from {folder.name}.")
        else:
            self._set_status(f"Replaying {folder.name}.")

    def _on_close(self) -> None:
        if self.engine.recording:
            self._stop_record()
        self.engine.close()
        self.destroy()


def main() -> None:
    app = DeskApp()
    app.mainloop()
