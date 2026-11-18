import inspect
import re
import tempfile
import unittest
import wave
from datetime import datetime
from pathlib import Path

import numpy as np

from freestyle_desk.audio import (
    aligned_beat_seconds,
    beat_slot_index,
    effective_loop,
    load_wav,
    pocket_slots,
    read_loop_block,
    save_vocal,
)
from freestyle_desk.gibber import bones_text, format_warmup, leave_pad, warmup_lines
from freestyle_desk.rhymes import RhymeIndex, apply_lookup, default_dict_path, last_completed_word
from freestyle_desk.typeset import typeset
from freestyle_desk.vault import Vault, parse_session

FIXTURE = """
;;; comment
LIGHT  L AY1 T # lamp
NIGHT  N AY1 T
FIGHT  F AY1 T
LIKE  L AY1 K
BIKE  B AY1 K
HELLO  HH AH0 L OW1
CAT  K AE1 T
"""


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text)


class TypesetTests(unittest.TestCase):
    def test_preserves_words_and_case(self):
        raw = "Hello   world, this is a line. another breath here"
        sheet = typeset(raw)
        self.assertEqual(words(raw), words(sheet))
        self.assertIn("Hello", sheet)
        self.assertIn("world,", sheet)

    def test_couplet_gap_and_no_invented_breaks(self):
        self.assertEqual(typeset("a\nb\nc\nd"), "a\nb\n\nc\nd")
        self.assertEqual(typeset("skrrt skrrt flippa"), "skrrt skrrt flippa")
        self.assertIn("\n\n", typeset("one, two. three, four"))

    def test_apostrophe_survives(self):
        raw = "don't stop, go"
        self.assertEqual(words(raw), words(typeset(raw)))


class RhymeTests(unittest.TestCase):
    def setUp(self):
        self.index = RhymeIndex.from_text(FIXTURE)

    def test_perfect_and_family_stay_grouped(self):
        suggestion = self.index.suggest("light")
        perfect = {hit.word for hit in suggestion.perfect}
        family = {hit.word for hit in suggestion.family}
        self.assertIn("night", perfect)
        self.assertIn("fight", perfect)
        self.assertIn("like", family)
        self.assertIn("bike", family)
        self.assertNotIn("night", family)
        self.assertNotIn("light", perfect)
        self.assertNotIn("cat", perfect | family)
        self.assertEqual(suggestion.syllables, 1)

    def test_unknown_word_is_empty(self):
        suggestion = self.index.suggest("zzzzqqq")
        self.assertFalse(suggestion.known)
        self.assertEqual(suggestion.perfect, [])
        self.assertEqual(suggestion.family, [])

    def test_lookup_does_not_change_the_pad(self):
        pad = "in the light "
        returned, margin = apply_lookup(pad, len(pad), self.index)
        self.assertIs(returned, pad)
        self.assertIn("night", margin)
        self.assertNotIn("night", pad)
        incomplete = "in the light"
        returned, margin = apply_lookup(incomplete, len(incomplete), self.index)
        self.assertIs(returned, incomplete)
        self.assertIsNone(margin)

    def test_word_boundary(self):
        self.assertEqual(last_completed_word("in the light "), "light")
        self.assertEqual(last_completed_word("in the light,"), "light")
        self.assertIsNone(last_completed_word("in the light"))
        self.assertEqual(last_completed_word("light", 5), None)
        self.assertEqual(last_completed_word(""), "")

    def test_vendored_dictionary_has_light_night(self):
        path = default_dict_path()
        self.assertTrue(path.exists(), "cmudict was not vendored")
        index = RhymeIndex.from_path(path)
        perfect = {hit.word for hit in index.suggest("light").perfect}
        self.assertIn("night", perfect)
        self.assertFalse(index.suggest("zzzzqqq-not-a-word").known)


class AudioMathTests(unittest.TestCase):
    def test_loop_wraps_inside_the_region(self):
        samples = np.arange(100, dtype=np.float32).reshape(-1, 1)
        block, pos = read_loop_block(samples, 18, 5, 10, 20)
        self.assertEqual(block[:, 0].tolist(), [18, 19, 10, 11, 12])
        self.assertEqual(pos, 13)

    def test_loop_keeps_channels_and_zero_end_means_whole_file(self):
        samples = np.ones((10, 2), dtype=np.float32)
        samples[:, 1] = 2
        block, _pos = read_loop_block(samples, 0, 4, 0, 10)
        self.assertEqual(block.shape, (4, 2))
        self.assertEqual(float(block[0, 1]), 2.0)
        self.assertEqual(effective_loop(0, 0, 1000, 100), (0, 1000))
        self.assertEqual(effective_loop(1.0, 2.5, 1000, 100), (100, 250))

    def test_alignment_subtracts_both_buffers_and_wraps(self):
        # 180 ms headphones plus 26 ms mic, the delays measured on this machine.
        heard = aligned_beat_seconds(0.500, 0.180, 0.026, 0.0, 3.0, allow_wrap=True)
        self.assertAlmostEqual(heard, 0.294, places=3)
        self.assertEqual(
            aligned_beat_seconds(0.05, 0.180, 0.026, 0.0, 3.0, allow_wrap=False),
            0.0,
        )
        wrapped = aligned_beat_seconds(0.05, 0.180, 0.026, 0.0, 3.0, allow_wrap=True)
        self.assertAlmostEqual(wrapped, 2.844, places=3)

    def test_slots_stay_empty(self):
        self.assertEqual(pocket_slots(), [""] * 16)
        self.assertIsNone(beat_slot_index(1.0, 90, playing=False))
        self.assertEqual(beat_slot_index(1.0, 60, playing=True), 1)
        self.assertEqual(beat_slot_index(16.0, 60, playing=True), 0)

    def test_wav_roundtrip_and_24bit(self):
        folder = Path(tempfile.mkdtemp())
        samples = np.array([[0.0], [0.5], [-0.5], [0.25]], dtype=np.float32)
        path = folder / "vocal.wav"
        save_vocal(path, samples, 44100)
        loaded, rate = load_wav(path)
        self.assertEqual(rate, 44100)
        self.assertEqual(loaded.shape[0], 4)
        self.assertAlmostEqual(float(loaded[1, 0]), 0.5, places=2)

        wide = folder / "wide.wav"
        values = [0, 8388607, -8388608]
        raw = b"".join(int(value).to_bytes(3, "little", signed=True) for value in values)
        with wave.open(str(wide), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(3)
            handle.setframerate(16000)
            handle.writeframes(raw)
        loaded, rate = load_wav(wide)
        self.assertEqual(rate, 16000)
        self.assertAlmostEqual(float(loaded[1, 0]), 1.0, places=3)
        self.assertAlmostEqual(float(loaded[2, 0]), -1.0, places=3)


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()) / "Freestyle Sessions"
        self.vault = Vault(self.tmp)

    def test_stop_writes_three_files_and_latest_without_a_dialog(self):
        source = inspect.getsource(Vault.write_session)
        self.assertNotIn("filedialog", source)
        self.assertNotIn("filedialog", Path(inspect.getfile(Vault)).read_text(encoding="utf-8"))
        when = datetime(2026, 11, 18, 6, 18, 0)
        beat = r"C:\Beats\my loop.wav"
        result = self.vault.write_session(
            when,
            np.zeros((8, 1), dtype=np.float32),
            44100,
            "hello light",
            {"beat": beat, "bpm": "90.000", "loop_start": "0.000", "loop_end": "0.000", "beat_position": "1.250"},
        )
        self.assertTrue(result.shortcut_ok, result.shortcut_error)
        self.assertEqual(result.folder.name, "2026-11-18 06-18")
        self.assertTrue(str(result.folder).startswith(str(self.tmp)))
        self.assertEqual((result.folder / "lyrics.txt").read_text(encoding="utf-8"), "hello light")
        self.assertTrue((result.folder / "vocal.wav").exists())
        meta = parse_session((result.folder / "session.txt").read_text(encoding="utf-8"))
        self.assertEqual(meta["beat"], beat)
        self.assertTrue((self.tmp / "Latest.lnk").exists())
        self.assertEqual(self.vault.list_sessions()[0].folder, result.folder)

        second = self.vault.write_session(when, np.zeros((4, 1), np.float32), 44100, "again", {})
        self.assertEqual(second.folder.name, "2026-11-18 06-18-2")

    def test_rename_and_star_keep_the_beat_path(self):
        when = datetime(2026, 11, 18, 7, 1, 0)
        result = self.vault.write_session(
            when,
            np.zeros((4, 1), np.float32),
            44100,
            "bars",
            {"beat": r"C:\Beats\my loop.wav"},
        )
        self.vault.update_session(result.folder, name="happy accident", starred=True)
        meta = parse_session((result.folder / "session.txt").read_text(encoding="utf-8"))
        self.assertEqual(meta["name"], "happy accident")
        self.assertEqual(meta["starred"], "1")
        self.assertEqual(meta["beat"], r"C:\Beats\my loop.wav")
        self.assertEqual(self.vault.list_beats(), [])


class GibberTests(unittest.TestCase):
    def test_warmup_stays_out_of_the_pad(self):
        pad = "my own line stays"
        lines, source = warmup_lines(bpm=140, bars=4, seed=3)
        self.assertIs(leave_pad(pad), pad)
        self.assertEqual(len(lines), 4)
        self.assertEqual(source, "Gib89erish")
        margin = format_warmup(lines, source)
        self.assertIn("Not a verse", margin)
        self.assertNotIn(pad, margin)
        for line in lines:
            self.assertNotIn("#", line)
            self.assertNotIn("(", line)

    def test_bones_use_their_vowels(self):
        index = RhymeIndex.from_text("LIGHT  L AY1 T\n")
        pad = "in the light"
        self.assertEqual(bones_text(pad, index), "in the ay")
        self.assertEqual(bones_text("", index), "Write a line first.")


class GuiContractTests(unittest.TestCase):
    def test_rhyme_handler_does_not_insert(self):
        from freestyle_desk.app import DeskApp

        source = inspect.getsource(DeskApp._on_pad_key)
        self.assertNotIn(".insert(", source)
        self.assertNotIn("pad.insert", source)
        self.assertIn("apply_lookup", source)
        app_source = Path(inspect.getfile(DeskApp)).read_text(encoding="utf-8")
        self.assertNotIn("filedialog", app_source)
        warmup = inspect.getsource(DeskApp._warmup)
        bones = inspect.getsource(DeskApp._bones)
        self.assertNotIn("pad.insert", warmup)
        self.assertNotIn("pad.delete", warmup)
        self.assertNotIn("pad.insert", bones)
        self.assertNotIn("pad.delete", bones)


if __name__ == "__main__":
    unittest.main()
