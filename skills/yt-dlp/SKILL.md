---
name: yt-dlp
description: "Use when downloading user-requested media or inspecting available formats with yt-dlp."
---

# yt-dlp

Run `yt-dlp --version` and inspect `yt-dlp --help`. Inspect formats with `yt-dlp --list-formats <url>` before selecting format and output directory. Use `--no-playlist` for one video unless the user requested a playlist. Use FFmpeg for muxing when needed. Browser cookies and credentials are not required for the version check; only access account material when needed and authorized. Verify downloaded streams and report source, output path and failures.

## Installation and provenance

Run `python setup_integrations.py --install` from the ai-work-skills checkout, then load the generated toolchain environment as documented in `docs/INTEGRATIONS.md`. Use the installed CLI help as the version-specific interface.

This is an independently authored Codex routing skill. Upstream: https://github.com/yt-dlp/yt-dlp/tree/897341241f2bfb2439fe0367f4c7c9ccd29a3828. Runtime version and source audit pin are recorded separately in `integrations-lock.json`. Follow the host tool policy and user instructions.
