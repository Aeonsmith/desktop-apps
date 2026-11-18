# Freestyle Desk

A one-window recorder for freestyling over a beat you already have. The rhyme margin looks words up. It does not type them in.

## Requirements

- Windows
- Python 3.10 or newer. This machine uses Python 3.14.
- A microphone and an output device. Headphones keep the beat out of the vocal.

## Setup

From this folder:

```powershell
python -m pip install -r requirements.txt
```

The packages are `customtkinter`, `sounddevice`, `numpy`, and `miniaudio`. `miniaudio` is what plays mp3 beats. Without it, the player still plays wav files.

The rhyme index is already in `data/cmudict.dict`. That file is the public-domain CMU Pronouncing Dictionary. No API key and no network call are required.

## Launch

Double-click `run.bat`, or from this folder:

```powershell
python -m freestyle_desk
```

A desktop shortcut named **Freestyle Desk** launches the same command with `pythonw`, so no console window stays open. If that shortcut is missing, create it with the working directory set to this folder and the target set to `pythonw -m freestyle_desk`.

## Use

1. Drop a `.wav` or `.mp3` into `Desktop\Freestyle Sessions\Beats`. The **Beats folder** button opens that folder. Then press **Refresh**.
2. Press **Play**. Loop start and end are in seconds. An end of `0` loops the whole file. BPM is a label you type. It is not detected, and the empty slots under the pad stay empty.
3. Write in the pad, or leave it blank and freestyle. Finish a word with a space, comma, or Enter. Rhymes appear in the margin. Clicking one does not insert it.
4. **Warm-up** asks the Gib89erish engine for syllable scraps at the BPM you typed. Coherence stays at 0, so it does not turn them into a verse. The scraps land in the margin. A take that includes them is tagged happy accident. Save scraps writes that session without opening the mic, including a scraps.txt file. **Bones** shows the vowel skeleton of the line you already wrote. Neither button changes the pad. When you stop a take, those scraps are written into `lyrics.txt` with whatever you typed.
5. **Typeset** breaks on breaths you already marked (line breaks and punctuation) and spaces couplets. It does not change words.
6. **Record** starts the beat if one is loaded, then captures the mic only. The beat is not mixed into the vocal file. Stop writes the take. There is no save dialog.

Each take lands in `Desktop\Freestyle Sessions\YYYY-MM-DD HH-mm\` as `vocal.wav`, `lyrics.txt`, and `session.txt`. A `Latest` shortcut in that folder points at the newest take. Rename and star from the filmstrip. **Load** puts that take's lyrics in the pad. **Replay** starts the beat at the position where recording began and plays the vocal with it.

The stamp subtracts the output buffer and the mic buffer, so the replay lines up with what you heard in the headphones. On this machine those delays were about 180 ms and 26 ms.

## Tests

From this folder:

```powershell
python tests\test_desk.py -v
```
