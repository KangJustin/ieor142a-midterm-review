"""Check a finished video: stream durations line up, and the narration transcribes cleanly."""
import json
import os
import subprocess
import sys
import time

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

ROOT = os.path.dirname(os.path.abspath(__file__))
slug, mp4 = sys.argv[1], sys.argv[2]
os.makedirs(f"{ROOT}/qa", exist_ok=True)
info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration,nb_frames",
                                  "-of", "json", mp4], capture_output=True, text=True).stdout)
d = {s["codec_type"]: float(s.get("duration", 0)) for s in info["streams"] if s["codec_type"] in ("video", "audio")}
print(f"{slug}: video {d['video']:.2f}s audio {d['audio']:.2f}s diff {d['video'] - d['audio']:+.2f}s")
t = time.time()
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
x, sr = sf.read(f"{ROOT}/work/{slug}/audio.wav", dtype="float32")
x = resample_poly(x, 2, 3).astype(np.float32)
segs, _ = m.transcribe(x, beam_size=1)
with open(f"{ROOT}/qa/{slug}_asr.txt", "w") as f:
    for s in segs:
        f.write(f"[{s.start:6.1f}] {s.text.strip()}\n")
print(f"transcript written in {time.time() - t:.0f}s")
