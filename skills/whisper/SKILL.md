---
name: whisper
description: "Use when transcribing local audio with OpenAI Whisper running on this PC."
---

# whisper

Run `whisper --help`. Choose a model appropriate to hardware and language, explain the first-run model download, and write to an explicit output directory. Example: `whisper input.wav --model small --language Korean --task transcribe --output_format srt --output_dir output`. FFmpeg must be on PATH. CPU mode can require `--fp16 False`. Check timestamps and sample transcription against the audio; flag uncertain names. Package installation and CLI import checks do not prove recognition quality or download model weights.

## Installation and provenance

Run `python setup_integrations.py --install` from the ai-work-skills checkout, then load the generated toolchain environment as documented in `docs/INTEGRATIONS.md`. Use the installed CLI help as the version-specific interface.

This is an independently authored Codex routing skill. Upstream: https://github.com/openai/whisper/tree/86098128c0b4f24f0e2aa2994de830614b474227. Runtime version and source audit pin are recorded separately in `integrations-lock.json`. Follow the host tool policy and user instructions.
