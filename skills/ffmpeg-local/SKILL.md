---
name: ffmpeg-local
description: "Use when inspecting or processing local media with the managed FFmpeg and FFprobe tools."
---

# ffmpeg-local

Prefer any applicable installed FFmpeg workflow skill. Inspect inputs with `ffprobe -v error -show_format -show_streams -of json <input>`. Write to a new output path, choose codecs and stream mappings deliberately, then verify output duration, streams and full decoding with `ffmpeg -v error -xerror -i <output> -f null -`. Frame-accurate cuts may require encoding. Avoid silently overwriting originals. This wrapper manages discovery and verification, not a replacement implementation of FFmpeg.

## Installation and provenance

Run `python setup_integrations.py --install` from the ai-work-skills checkout, then load the generated toolchain environment as documented in `docs/INTEGRATIONS.md`. Use the installed CLI help as the version-specific interface.

This is an independently authored Codex routing skill. Upstream: https://github.com/ffmpeg/ffmpeg/tree/b60ab6c9a4583cd4bbdc010b412d598945919da8. Runtime version and source audit pin are recorded separately in `integrations-lock.json`. Follow the host tool policy and user instructions.
