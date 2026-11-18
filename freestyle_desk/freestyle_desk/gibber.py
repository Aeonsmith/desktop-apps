"""Syllable warm-up from the Gib89erish engine. Scraps stay out of the pad."""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

from .rhymes import normalize_word

_ENGINE = None
_ENGINE_TRIED = False

_ONSETS = ["skr", "tr", "dr", "fl", "bl", "st", "sp", "pr", "kr", "gl", "sl", "br", "ch", "sh", "th", "k", "d", "b", "m", "n", "t", "p"]
_NUCLEI = ["a", "e", "i", "o", "u", "ay", "ee", "oo", "aw", "ow", "oy"]
_CODAS = ["t", "p", "k", "m", "n", "s", "st", "nt", "ck"]


def engine_backend() -> Path | None:
    candidates = [
        Path(r"C:\workspace\gib89erish-app\backend"),
        Path.home() / "workspace" / "gib89erish-app" / "backend",
    ]
    for path in candidates:
        if (path / "gib89erish" / "gibgen.py").is_file():
            return path
    return None


def _engine():
    global _ENGINE, _ENGINE_TRIED
    if _ENGINE_TRIED:
        return _ENGINE
    _ENGINE_TRIED = True
    backend = engine_backend()
    if backend is None:
        return None
    backend_text = str(backend)
    if backend_text not in sys.path:
        sys.path.insert(0, backend_text)
    try:
        from gib89erish.gibgen import GibGenEngine
    except Exception:
        return None
    _ENGINE = GibGenEngine()
    return _ENGINE


def flow_for_bpm(bpm: float) -> tuple[str, str, int]:
    """Archetype, flow name, and syllables per bar. Matches the Gib89erish names."""
    if bpm <= 0:
        bpm = 90
    if bpm < 90:
        return "houston-chopped-screwed", "mumble", 8
    if bpm < 120:
        return "90s-golden-era", "boombap", 14
    if bpm < 145:
        return "2010s-atl-trap", "triplet", 12
    return "uk-ny-drill", "drill", 10


def _local_bar(syllables: int, ending: str) -> str:
    words = []
    count = 0
    while count < max(1, syllables - 1):
        size = 2 if random.random() > 0.6 else 1
        chunk = "".join(_syllable() for _ in range(size))
        words.append(chunk)
        count += size
    words.append(random.choice(_ONSETS) + ending)
    return " ".join(words)


def _syllable() -> str:
    onset = random.choice(_ONSETS) if random.random() > 0.15 else ""
    coda = random.choice(_CODAS) if random.random() > 0.25 else ""
    return f"{onset}{random.choice(_NUCLEI)}{coda}"


def warmup_lines(bpm: float = 90, bars: int = 4, seed: int | None = None) -> tuple[list[str], str]:
    """Syllable scraps for the margin. The caller must not write these into the pad."""
    if seed is not None:
        random.seed(seed)
    bars = max(1, min(8, bars))
    archetype, flow, syllables = flow_for_bpm(bpm)
    engine = _engine()
    if engine is not None:
        result = engine.generate_bars(
            archetype_id=archetype,
            flow_style=flow,
            coherence=0,
            bar_count=bars,
            include_adlibs=False,
            include_hashtags=False,
        )
        lines = [_clean_scrap(bar.get("text", "")) for bar in result.get("bars", [])]
        lines = [line for line in lines if line]
        if lines:
            return lines, "Gib89erish"
    ending = random.choice(_CODAS)
    return [_local_bar(syllables, ending) for _ in range(bars)], "desk mouth"


def _clean_scrap(text: str) -> str:
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip(" ,")
    return text


def format_warmup(lines: list[str], source: str) -> str:
    body = "\n".join(lines) if lines else "—"
    return f"Warm-up · {source}\nNot a verse. The pad stays yours.\n\n{body}"


def leave_pad(pad_text: str) -> str:
    """The warm-up contract: the pad string comes back unchanged."""
    return pad_text


def bones_text(text: str, index) -> str:
    """Vowel skeleton of a line the writer already typed. Unknown words stay put."""
    if not text or not text.strip():
        return "Write a line first."

    def vowel_bones(match: re.Match[str]) -> str:
        word = match.group(0)
        prons = getattr(index, "prons", {}).get(normalize_word(word))
        if not prons:
            return word
        vowels = [phone.rstrip("012").lower() for phone in prons[0] if phone[-1:].isdigit()]
        return "-".join(vowels) if vowels else word

    return re.sub(r"[A-Za-z0-9']+", vowel_bones, text)
