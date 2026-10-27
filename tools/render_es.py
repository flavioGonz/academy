#!/usr/bin/env python3
"""Render claudemy two-host scripts to MP3 with local Piper voices (Spanish).

A: Lucía  -> es_AR-daniela-high (rioplatense)
B: Martín -> es_MX-ald-medium

Usage: python3 render_es.py <out_dir_root> <lesson_dir> [<lesson_dir> ...]
For each lesson dir with script.txt, writes <lesson_dir>/<slug>.mp3 where slug is
the dir name without the NN- prefix, and prints "path<TAB>seconds".
Skips lessons whose mp3 is newer than script.txt.
"""
import io, re, subprocess, sys, wave
from pathlib import Path
from piper import PiperVoice
from piper.config import SynthesisConfig

V = Path(__file__).resolve().parent.parent / "voices"
VOICES = {"A": PiperVoice.load(str(V / "es_AR-daniela-high.onnx")),
          "B": PiperVoice.load(str(V / "es_MX-ald-medium.onnx"))}
CFG = {"A": SynthesisConfig(length_scale=1.0, noise_scale=0.6, noise_w_scale=0.8),
       "B": SynthesisConfig(length_scale=0.97, noise_scale=0.6, noise_w_scale=0.8)}
RATE = 22050
TAG = re.compile(r"\[[^\]]*\]")


def pcm_for(speaker, text):
    v = VOICES[speaker]
    out = bytearray()
    for chunk in v.synthesize(text, syn_config=CFG[speaker]):
        out += chunk.audio_int16_bytes
        rate = chunk.sample_rate
    if rate != RATE:  # resample via ffmpeg if a voice differs
        p = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "-",
                            "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-"], input=bytes(out), capture_output=True)
        out = bytearray(p.stdout)
    return bytes(out)


def silence(ms):
    return b"\x00\x00" * int(RATE * ms / 1000)


def render(lesson):
    script = lesson / "script.txt"
    slug = re.sub(r"^\d+-", "", lesson.name)
    mp3 = lesson / f"{slug}.mp3"
    tj = lesson / "timings.json"
    if mp3.exists() and tj.exists() and mp3.stat().st_mtime > script.stat().st_mtime:
        return mp3
    pcm = bytearray(silence(300))
    marks = []
    for line in script.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([AB]):\s*(.+)$", line.strip())
        if not m:
            continue
        text = TAG.sub("", m.group(2)).strip()
        if not text:
            continue
        start = len(pcm) / 2 / RATE
        pcm += pcm_for(m.group(1), text)
        marks.append([round(start, 2), round(len(pcm) / 2 / RATE, 2)])
        pcm += silence(280)
    pcm += silence(500)
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", "-",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "64k",
                        str(mp3)], input=bytes(pcm))
    if p.returncode:
        raise SystemExit(f"ffmpeg failed on {lesson}")
    import json
    tj.write_text(json.dumps(marks))
    return mp3


def duration(mp3):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        d = Path(d)
        if not (d / "script.txt").exists():
            continue
        mp3 = render(d)
        print(f"{mp3}\t{duration(mp3):.1f}", flush=True)
