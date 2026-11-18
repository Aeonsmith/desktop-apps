"""Offline rhyme margin. Looks words up. Never writes them back."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# CMU Pronouncing Dictionary, public domain.
# https://github.com/cmusphinx/cmudict

_TOKEN = re.compile(r"[A-Za-z0-9']+")
_PERFECT_CAP = 24
_FAMILY_CAP = 16


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z0-9']", "", word.lower())


def default_dict_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "cmudict.dict"


def last_completed_word(text: str, cursor: int | None = None) -> str | None:
    """Word that just ended.

    Returns None while a word is still being typed, so the margin can stay put.
    Returns "" when there is no completed word yet.
    """
    if cursor is None:
        cursor = len(text)
    before = text[: max(0, cursor)]
    if not before:
        return ""
    if re.search(r"[A-Za-z0-9']$", before):
        return None
    words = _TOKEN.findall(before)
    return words[-1] if words else ""


def _is_vowel(phone: str) -> bool:
    return bool(phone) and phone[-1].isdigit()


def rhyme_key(phones: list[str]) -> tuple[str, ...]:
    stress_at = None
    for index, phone in enumerate(phones):
        if phone.endswith("1"):
            stress_at = index
    if stress_at is None:
        for index, phone in enumerate(phones):
            if phone.endswith("2"):
                stress_at = index
    if stress_at is None:
        for index, phone in enumerate(phones):
            if _is_vowel(phone):
                stress_at = index
    if stress_at is None:
        return tuple(phones)
    return tuple(phones[stress_at:])


def nucleus(key: tuple[str, ...]) -> str:
    if not key:
        return ""
    return key[0].rstrip("012")


def syllable_count(phones: list[str]) -> int:
    return sum(1 for phone in phones if _is_vowel(phone))


def parse_cmudict(text: str) -> dict[str, list[list[str]]]:
    prons: dict[str, list[list[str]]] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        key = normalize_word(parts[0].split("(", 1)[0])
        if not key:
            continue
        prons.setdefault(key, []).append(parts[1:])
    return prons


@dataclass(frozen=True)
class Hit:
    word: str
    syllables: int


@dataclass
class Suggestion:
    word: str
    known: bool
    syllables: int
    perfect: list[Hit]
    family: list[Hit]


class RhymeIndex:
    def __init__(self, prons: dict[str, list[list[str]]]):
        self.prons = prons
        self.by_perfect: dict[tuple[str, ...], list[Hit]] = {}
        self.by_family: dict[str, list[tuple[Hit, tuple[str, ...]]]] = {}
        seen_perfect: set[tuple[tuple[str, ...], str]] = set()
        seen_family: set[tuple[str, str, tuple[str, ...]]] = set()
        for word, pronunciations in prons.items():
            for phones in pronunciations:
                key = rhyme_key(phones)
                hit = Hit(word, syllable_count(phones))
                marker = (key, word)
                if marker not in seen_perfect:
                    seen_perfect.add(marker)
                    self.by_perfect.setdefault(key, []).append(hit)
                nuc = nucleus(key)
                family_marker = (nuc, word, key)
                if nuc and family_marker not in seen_family:
                    seen_family.add(family_marker)
                    self.by_family.setdefault(nuc, []).append((hit, key))

    @classmethod
    def from_text(cls, text: str) -> "RhymeIndex":
        return cls(parse_cmudict(text))

    @classmethod
    def from_path(cls, path: Path) -> "RhymeIndex":
        return cls.from_text(Path(path).read_text(encoding="utf-8-sig", errors="replace"))

    def suggest(self, word: str) -> Suggestion:
        key = normalize_word(word)
        if not key:
            return Suggestion("", False, 0, [], [])
        pronunciations = self.prons.get(key)
        if not pronunciations:
            return Suggestion(key, False, 0, [], [])
        perfect_keys = {rhyme_key(phones) for phones in pronunciations}
        syllables = syllable_count(pronunciations[0])
        seen = {key}
        perfect: list[Hit] = []
        for rhyme in perfect_keys:
            for hit in self.by_perfect.get(rhyme, ()):
                if hit.word in seen:
                    continue
                seen.add(hit.word)
                perfect.append(hit)
        family: list[Hit] = []
        for rhyme in perfect_keys:
            for hit, hit_key in self.by_family.get(nucleus(rhyme), ()):
                if hit.word in seen or hit_key in perfect_keys:
                    continue
                seen.add(hit.word)
                family.append(hit)
        query_len = len(key)
        perfect.sort(key=lambda hit: (abs(hit.syllables - syllables), abs(len(hit.word) - query_len), hit.word))
        family.sort(key=lambda hit: (abs(hit.syllables - syllables), abs(len(hit.word) - query_len), hit.word))
        return Suggestion(key, True, syllables, perfect[:_PERFECT_CAP], family[:_FAMILY_CAP])


def format_margin(suggestion: Suggestion) -> str:
    if not suggestion.word:
        return "Finish a word."
    if not suggestion.known:
        return f"{suggestion.word}\nNot in the rhyme index."
    label = "syllable" if suggestion.syllables == 1 else "syllables"
    lines = [f"{suggestion.word} · {suggestion.syllables} {label}", "", "Perfect"]
    lines.extend(_hit_lines(suggestion.perfect))
    lines.extend(["", "Family"])
    lines.extend(_hit_lines(suggestion.family))
    return "\n".join(lines)


def _hit_lines(hits: list[Hit]) -> list[str]:
    if not hits:
        return ["—"]
    return [f"{hit.word} · {hit.syllables}" for hit in hits]


def apply_lookup(pad_text: str, cursor: int, index: RhymeIndex) -> tuple[str, str | None]:
    """Return the same pad text, plus margin copy. None means leave the margin alone."""
    word = last_completed_word(pad_text, cursor)
    if word is None:
        return pad_text, None
    return pad_text, format_margin(index.suggest(word))


def load_default_index() -> RhymeIndex:
    path = default_dict_path()
    if not path.exists():
        return RhymeIndex({})
    return RhymeIndex.from_path(path)
