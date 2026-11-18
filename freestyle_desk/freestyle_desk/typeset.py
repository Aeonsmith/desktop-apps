"""Turn rough lyric scribbles into a sheet without changing the words."""

from __future__ import annotations

import re

# Breaths the writer already marked. No new words, no new punctuation.
_BREATH = re.compile(r"(\n+|,|;|\.\.\.|[.!?]|—|–)")
_HAS_WORD = re.compile(r"[A-Za-z0-9']")


def typeset(text: str) -> str:
    """Break on breaths and space couplets. Word tokens stay as written."""
    if not text or not text.strip():
        return ""
    segments: list[str] = []
    buf = ""
    for part in _BREATH.split(text):
        if part == "":
            continue
        if _BREATH.fullmatch(part):
            if "\n" in part:
                _push(segments, buf)
                buf = ""
            else:
                buf += part
                _push(segments, buf)
                buf = ""
        else:
            buf += part
    _push(segments, buf)
    if not segments:
        return _collapse(text)
    lines: list[str] = []
    last = len(segments) - 1
    for index, segment in enumerate(segments):
        lines.append(segment)
        if index % 2 == 1 and index != last:
            lines.append("")
    return "\n".join(lines)


def _push(segments: list[str], buf: str) -> None:
    piece = _collapse(buf)
    if piece and _HAS_WORD.search(piece):
        segments.append(piece)


def _collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
