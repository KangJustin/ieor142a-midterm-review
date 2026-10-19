#!/bin/bash
# Build all eight videos in order. Narration is cached in cache/tts, so rebuilds only re-voice changed lines.
set -e
cd "$(dirname "$0")"
for v in v01 v02 v03 v04 v05 v06 v07 v08; do python3 "$v.py"; done
