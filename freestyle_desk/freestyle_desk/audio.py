"""Wav loop playback and mic capture. The vocal file is the mic, not a mix."""

from __future__ import annotations

import threading
import time
import wave
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import sounddevice as sd


def parse_seconds(text: str) -> float:
    try:
        value = float(str(text).strip())
    except ValueError:
        return 0.0
    if value < 0 or value != value:  # NaN
        return 0.0
    return value


def parse_bpm(text: str) -> float:
    return parse_seconds(text)


def pocket_slots(count: int = 16) -> list[str]:
    """Empty pockets. The writer fills the pad, never these slots."""
    return [""] * count


def stream_latency(stream) -> float:
    """Seconds between the callback and the converter. Half-duplex streams report a float."""
    if stream is None:
        return 0.0
    value = stream.latency
    if isinstance(value, (tuple, list)):
        value = value[0]
    try:
        delay = float(value)
    except (TypeError, ValueError):
        return 0.0
    if delay < 0 or delay != delay:
        return 0.0
    return delay


def aligned_beat_seconds(
    playhead_sec: float,
    output_latency: float,
    input_latency: float,
    loop_start: float,
    loop_end: float,
    *,
    allow_wrap: bool,
) -> float:
    """Beat time that was audible when the first vocal sample was captured.

    The playhead is ahead of the headphones by the output buffer, and the mic
    buffer delivers the voice after it was sung. Replay has to start the beat
    at what was heard, not at the playhead.
    """
    target = playhead_sec - max(0.0, output_latency) - max(0.0, input_latency)
    if loop_end <= loop_start:
        return max(0.0, target)
    if target < loop_start:
        if not allow_wrap:
            return loop_start
        span = loop_end - loop_start
        return loop_start + (target - loop_start) % span
    if target >= loop_end:
        span = loop_end - loop_start
        return loop_start + (target - loop_start) % span
    return target


def beat_slot_index(
    position_sec: float,
    bpm: float,
    slots: int = 16,
    playing: bool = False,
) -> int | None:
    if not playing or bpm <= 0 or slots <= 0:
        return None
    return int(position_sec * bpm / 60.0) % slots


def effective_loop(start_sec: float, end_sec: float, frames: int, sample_rate: int) -> tuple[int, int]:
    if frames <= 0:
        return 0, 0
    if end_sec <= start_sec:
        return 0, frames
    start = _frame(start_sec, sample_rate, frames)
    end = _frame(end_sec, sample_rate, frames)
    if end <= start:
        return 0, frames
    return start, end


def _frame(seconds: float, sample_rate: int, frames: int) -> int:
    return max(0, min(frames, int(round(seconds * sample_rate))))


def read_loop_block(
    samples: np.ndarray,
    pos: int,
    frames: int,
    start: int,
    end: int,
) -> tuple[np.ndarray, int]:
    channels = samples.shape[1] if samples.ndim == 2 else 1
    out = np.zeros((frames, channels), dtype=np.float32)
    if samples.shape[0] == 0 or frames <= 0 or end <= start:
        return out, start
    if pos < start or pos >= end:
        pos = start
    filled = 0
    while filled < frames:
        take = min(frames - filled, end - pos)
        if take <= 0:
            pos = start
            continue
        out[filled : filled + take] = samples[pos : pos + take]
        pos += take
        filled += take
        if pos >= end:
            pos = start
    return out, pos


def as_stereo(samples: np.ndarray) -> np.ndarray:
    data = np.asarray(samples, dtype=np.float32)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    if data.shape[1] == 1:
        return np.repeat(data, 2, axis=1)
    return np.ascontiguousarray(data[:, :2])


def resample(samples: np.ndarray, src_rate: int, dst_rate: int) -> np.ndarray:
    if src_rate == dst_rate or len(samples) == 0:
        return np.ascontiguousarray(samples, dtype=np.float32)
    dst_n = max(1, int(round(len(samples) * float(dst_rate) / float(src_rate))))
    old_x = np.linspace(0.0, 1.0, len(samples), endpoint=False)
    new_x = np.linspace(0.0, 1.0, dst_n, endpoint=False)
    columns = [np.interp(new_x, old_x, samples[:, channel]) for channel in range(samples.shape[1])]
    return np.ascontiguousarray(np.stack(columns, axis=1), dtype=np.float32)


def fit_channels(block: np.ndarray, channels: int) -> np.ndarray:
    if block.shape[1] == channels:
        return block
    out = np.zeros((block.shape[0], channels), dtype=np.float32)
    usable = min(block.shape[1], channels)
    out[:, :usable] = block[:, :usable]
    return out


def _pcm_to_float(raw: bytes, sampwidth: int) -> np.ndarray:
    if sampwidth == 2:
        return np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if sampwidth == 1:
        return (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    if sampwidth == 4:
        return np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
    if sampwidth != 3:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    blob = np.frombuffer(raw, dtype=np.uint8)
    blob = blob[: len(blob) - (len(blob) % 3)]
    triples = blob.reshape(-1, 3).astype(np.int32)
    values = triples[:, 0] | (triples[:, 1] << 8) | (triples[:, 2] << 16)
    values = np.where(values >= 0x800000, values - 0x1000000, values)
    return values.astype(np.float32) / 8388608.0


def load_mp3(path: Path) -> tuple[np.ndarray, int]:
    import miniaudio

    decoded = miniaudio.mp3_read_file_f32(str(path))
    channels = max(1, int(decoded.nchannels))
    samples = np.asarray(decoded.samples, dtype=np.float32)
    usable = len(samples) - (len(samples) % channels)
    return np.ascontiguousarray(samples[:usable].reshape(-1, channels)), int(decoded.sample_rate)


def load_audio(path: Path) -> tuple[np.ndarray, int]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".wav":
        return load_wav(path)
    if suffix == ".mp3":
        return load_mp3(path)
    raise ValueError(f"{path.name} is not a wav or mp3.")


def beat_suffixes() -> tuple[str, ...]:
    return (".wav", ".mp3")


def load_wav(path: Path) -> tuple[np.ndarray, int]:
    path = Path(path)
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sampwidth = handle.getsampwidth()
        rate = handle.getframerate()
        raw = handle.readframes(handle.getnframes())
    if sampwidth not in (1, 2, 3, 4):
        raise ValueError(f"{path.name} is {sampwidth * 8}-bit. Export a 16-bit wav.")
    floats = _pcm_to_float(raw, sampwidth)
    if channels > 1:
        usable = len(floats) - (len(floats) % channels)
        floats = floats[:usable].reshape(-1, channels)
    else:
        floats = floats.reshape(-1, 1)
    return np.ascontiguousarray(floats, dtype=np.float32), rate


def save_vocal(path: Path, samples: np.ndarray, sample_rate: int) -> None:
    data = np.asarray(samples, dtype=np.float32)
    if data.ndim == 2:
        data = data.mean(axis=1)
    data = np.clip(data, -1.0, 1.0)
    if data.size == 0:
        data = np.zeros(1, dtype=np.float32)
    ints = (data * 32767.0).astype("<i2")
    path = Path(path)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(int(sample_rate))
        handle.writeframes(ints.tobytes())


@dataclass
class Recording:
    samples: np.ndarray
    sample_rate: int
    beat_position: float
    started_at: datetime


class Engine:
    """One output stream. Recording uses a separate input so the beat is not mixed in."""

    def __init__(self) -> None:
        self.output_rate = 44100
        self.input_rate = 44100
        self.output_channels = 2
        self.beat_path: Path | None = None
        self._beat: np.ndarray | None = None
        self._beat_pos = 0
        self._loop = (0, 0)
        self._volume = 0.8
        self._mode = "idle"
        self._out = None
        self._in = None
        self._chunks: list[np.ndarray] = []
        self._record_started_at: datetime | None = None
        self._record_beat_pos = 0.0
        self._first_playhead: float | None = None
        self._output_latency = 0.0
        self._input_latency = 0.0
        self._play_started: float | None = None
        self._replay_vocal: np.ndarray | None = None
        self._replay_pos = 0
        self._replay_done = False
        self._lock = threading.Lock()
        self._configure_devices()

    def _configure_devices(self) -> None:
        try:
            out = sd.query_devices(kind="output")
            self.output_rate = int(out["default_samplerate"]) or 44100
            max_out = int(out["max_output_channels"]) or 2
            self.output_channels = 2 if max_out >= 2 else 1
        except Exception:
            pass
        try:
            incoming = sd.query_devices(kind="input")
            self.input_rate = int(incoming["default_samplerate"]) or 44100
        except Exception:
            pass

    @property
    def has_beat(self) -> bool:
        return self._beat is not None and len(self._beat) > 0

    @property
    def output_running(self) -> bool:
        return self._out is not None

    @property
    def recording(self) -> bool:
        return self._in is not None

    @property
    def replaying(self) -> bool:
        return self._mode == "replay" and self._out is not None

    @property
    def replay_finished(self) -> bool:
        return self._replay_done

    @property
    def position_seconds(self) -> float:
        rate = self.output_rate or 1
        return self._beat_pos / rate

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, float(volume)))

    def load_beat(self, path: Path) -> None:
        samples, rate = load_audio(path)
        stereo = resample(as_stereo(samples), rate, self.output_rate)
        if self._out is not None:
            self._stop_output()
        with self._lock:
            self._beat = stereo
            self._loop = (0, len(stereo))
            self._beat_pos = 0
            self._replay_vocal = None
            self._replay_done = False
            self.beat_path = Path(path)

    def set_loop(self, start_sec: float, end_sec: float) -> None:
        frames = 0 if self._beat is None else len(self._beat)
        start, end = effective_loop(start_sec, end_sec, frames, self.output_rate)
        with self._lock:
            self._loop = (start, end)
            if self._beat_pos < start or self._beat_pos >= end:
                self._beat_pos = start

    def seek_seconds(self, seconds: float) -> None:
        frame = int(round(max(0.0, seconds) * self.output_rate))
        with self._lock:
            start, end = self._loop
            if end > start and (frame < start or frame >= end):
                span = end - start
                frame = start + (frame - start) % span
            elif frame < 0:
                frame = 0
            self._beat_pos = frame

    def play(self) -> None:
        if not self.has_beat:
            raise RuntimeError("No beat loaded")
        with self._lock:
            self._mode = "play"
            self._replay_vocal = None
            self._replay_done = False
        self._start_output()

    def pause(self) -> None:
        self._stop_output()
        self._replay_done = False

    def start_recording(self) -> None:
        if self._in is not None:
            return
        self._chunks = []
        self._record_started_at = datetime.now()
        self._first_playhead = None
        self._record_beat_pos = self.position_seconds
        stream = sd.InputStream(
            samplerate=self.input_rate,
            channels=1,
            dtype="float32",
            latency="high",
            callback=self._on_input,
        )
        stream.start()
        self._in = stream
        self._input_latency = stream_latency(stream)
        with self._lock:
            self._mode = "record"

    def stop_recording(self) -> Recording | None:
        stream = self._in
        if stream is None:
            return None
        self._in = None
        stream.stop()
        stream.close()
        with self._lock:
            if self._mode == "record":
                self._mode = "play" if self._out is not None else "idle"
        if self._chunks:
            audio = np.concatenate(self._chunks, axis=0)
        else:
            audio = np.zeros((0, 1), dtype=np.float32)
        self._chunks = []
        started = self._record_started_at or datetime.now()
        playhead = self._first_playhead if self._first_playhead is not None else self._record_beat_pos
        self._record_beat_pos = self._aligned_position(playhead)
        return Recording(audio, self.input_rate, self._record_beat_pos, started)

    def start_replay(
        self,
        vocal_path: Path,
        beat_path: str,
        loop_start: float,
        loop_end: float,
        beat_position: float,
    ) -> None:
        vocal, vocal_rate = load_audio(vocal_path)
        vocal = resample(as_stereo(vocal), vocal_rate, self.output_rate)
        self.pause()
        beat = Path(beat_path) if beat_path else None
        if beat is not None and beat.is_file():
            self.load_beat(beat)
            self.set_loop(loop_start, loop_end)
            self.seek_seconds(beat_position)
        else:
            with self._lock:
                self._beat = np.zeros_like(vocal)
                self._loop = (0, max(1, len(vocal)))
                self._beat_pos = 0
                self.beat_path = None
        with self._lock:
            self._replay_vocal = vocal
            self._replay_pos = 0
            self._replay_done = False
            self._mode = "replay"
        self._start_output()

    def close(self) -> None:
        if self._in is not None:
            self.stop_recording()
        self.pause()

    def _start_output(self) -> None:
        if self._out is not None:
            return
        stream = sd.OutputStream(
            samplerate=self.output_rate,
            channels=self.output_channels,
            dtype="float32",
            latency="high",
            callback=self._on_output,
        )
        stream.start()
        self._out = stream
        self._output_latency = stream_latency(stream)
        self._play_started = time.monotonic()

    def _stop_output(self) -> None:
        stream = self._out
        self._out = None
        if stream is not None:
            stream.stop()
            stream.close()
        with self._lock:
            if self._mode != "record":
                self._mode = "idle"

    def _loop_seconds(self) -> tuple[float, float]:
        rate = self.output_rate or 1
        start, end = self._loop
        return start / rate, end / rate

    def _aligned_position(self, playhead: float) -> float:
        loop_start, loop_end = self._loop_seconds()
        elapsed = 0.0 if self._play_started is None else time.monotonic() - self._play_started
        compensation = self._output_latency + self._input_latency
        return aligned_beat_seconds(
            playhead,
            self._output_latency,
            self._input_latency,
            loop_start,
            loop_end,
            allow_wrap=elapsed >= compensation and compensation > 0,
        )

    def _on_input(self, indata, frames, time_info, status) -> None:
        if self._first_playhead is None:
            self._first_playhead = self.position_seconds
        self._chunks.append(indata.copy())

    def _on_output(self, outdata, frames, time_info, status) -> None:
        outdata.fill(0)
        with self._lock:
            beat = self._beat
            pos = self._beat_pos
            start, end = self._loop
            volume = self._volume
            mode = self._mode
            vocal = self._replay_vocal
            vocal_pos = self._replay_pos
        if beat is None or len(beat) == 0:
            return
        block, pos = read_loop_block(beat, pos, frames, start, end)
        next_vocal = vocal_pos
        if mode == "replay" and vocal is not None:
            piece = np.zeros((frames, vocal.shape[1]), dtype=np.float32)
            if vocal_pos < len(vocal):
                take = min(frames, len(vocal) - vocal_pos)
                piece[:take] = vocal[vocal_pos : vocal_pos + take]
                next_vocal = vocal_pos + take
            else:
                next_vocal = vocal_pos
            if piece.shape[1] != block.shape[1]:
                piece = fit_channels(piece, block.shape[1])
            block = np.clip(block * 0.45 + piece * 0.9, -1.0, 1.0)
        block = fit_channels(block, outdata.shape[1]) * volume
        np.clip(block, -1.0, 1.0, out=block)
        outdata[:] = block
        with self._lock:
            self._beat_pos = pos
            if mode == "replay":
                self._replay_pos = next_vocal
                if vocal is not None and next_vocal >= len(vocal):
                    self._replay_done = True
