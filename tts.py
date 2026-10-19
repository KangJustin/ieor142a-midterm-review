"""Narration: Kokoro TTS with an on-disk cache keyed by text, voice and speed."""
import hashlib
import os
import re

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.environ.get("KOKORO_MODEL_DIR", os.path.join(ROOT, "models"))
CACHE = os.path.join(ROOT, "cache", "tts")
VOICE = "af_heart"
SPEED = 1.0
SR = 24000

_kokoro = None

# Spoken forms for terms the voice would otherwise read badly. Applied to narration only;
# captions keep the written form.
SAY = [
    (r"\bTPR\b", "T P R"), (r"\bFPR\b", "F P R"), (r"\bTNR\b", "T N R"), (r"\bFNR\b", "F N R"),
    (r"\bROC\b", "R O C"), (r"\bAUC\b", "A-U-C"), (r"\bLDA\b", "L D A"), (r"\bVIF\b", "V I F"),
    (r"\bVIFs\b", "V I Fs"), (r"\bOSR²", "O S R squared"), (r"R²", "R squared"),
    (r"\bL_FN\b", "L F N"), (r"\bL_FP\b", "L F P"), (r"\bp\*", "p star"), (r"\bcp\b", "C P"),
    (r"\bTP\b", "T P"), (r"\bTN\b", "T N"), (r"\bFP\b", "F P"), (r"\bFN\b", "F N"), (r"\bCDF\b", "C D F"),
    (r"\bCV\b", "C V"), (r"\bLOOCV\b", "leave one out C V"), (r"\bAR\(1\)", "A-R one"),
    (r"\bAIC\b", "A-I-C"), (r"\bRSS\b", "R S S"), (r"\bSSE\b", "S S E"), (r"\bSST\b", "S S T"),
    (r"\bmtry\b", "m try"), (r"\bPM1\b", "practice midterm one"), (r"\bPM2\b", "practice midterm two"),
    (r"\bPM3\b", "practice midterm three"), (r"\bK-means\b", "K means"), (r"\be\^", "e to the "),
    (r"\bvs\.", "versus"), (r"\bi\.e\.", "that is"), (r"\be\.g\.", "for example"),
    (r"\bCHAVG\b", "C H average"), (r"\bCHMAX\b", "C H max"), (r"\bCHMIN\b", "C H min"),
    (r"\bMMAX\b", "M max"), (r"\bMMIN\b", "M min"), (r"\bPRP\b", "P R P"), (r"\bNA\b", "N A"),
    (r"\bOSR\b", "O S R"), (r"\bMAE\b", "M.A.E"), (r"\bFICO\b", "Fye-co"), (r"\bVehicleModelId\b", "Vehicle Model I D"),
    (r"\bMobileSiteBooking\b", "Mobile Site Booking"), (r"\bOnlineBooking\b", "Online Booking"),
    (r"\bAverageScore\b", "Average Score"), (r"\bYourCabs\b", "Your Cabs"), (r"\bCPU\b", "C P U"),
]


DEC = re.compile(r"(?<![\w.])(\d+)\.(\d+)(?![\w])")


def spoken(text: str) -> str:
    out = text
    for pat, rep in SAY:
        out = re.sub(pat, rep, out)
    # espeak misreads some decimals ("0.906." -> "zero. nine hundred six"), so spell the digits after the point.
    out = DEC.sub(lambda m: f"{m.group(1)} point {' '.join(m.group(2))}", out)
    return out


def _engine():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
    return _kokoro


def synth(text: str, voice: str = VOICE, speed: float = SPEED) -> tuple[str, float]:
    """Return (wav_path, seconds) for the narration text, synthesizing only on a cache miss."""
    os.makedirs(CACHE, exist_ok=True)
    say = spoken(text)
    key = hashlib.sha1(f"{voice}|{speed}|{say}".encode()).hexdigest()[:16]
    path = os.path.join(CACHE, f"{key}.wav")
    if not os.path.exists(path):
        samples, sr = _engine().create(say, voice=voice, speed=speed, lang="en-us")
        samples = np.asarray(samples, dtype=np.float32)
        # Trim leading/trailing near-silence so timing is driven by speech, then pad 30 ms.
        thr = 0.01 * float(np.max(np.abs(samples)) or 1.0)
        idx = np.where(np.abs(samples) > thr)[0]
        if len(idx):
            samples = samples[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.06 * sr)]
        sf.write(path, samples, sr)
    info = sf.info(path)
    return path, info.frames / info.samplerate
