# v2026.11.05.2

## Runtime and plugin refresh

- @opengsd/gsd-core: 1.18.0 -> 1.20.0
- agent-browser: 0.39.2 -> 0.41.2
- chrome-devtools-mcp: 1.12.0 -> 1.12.0
- firecrawl-cli: 1.26.22 -> 1.28.0
- hyperframes: 0.8.192 -> 0.9.14
- graphifyy: 0.9.102
- headroom-ai: 0.42.0
- openai-whisper: 20250625
- yt-dlp: 2026.10.26
- uv: 0.13.7
- Plugin ecc: v2.2.3 (c05b2d6614f62f6db0047669aa4eefb223d478f9)
- Plugin ponytail: v5.3.3 (7801d061243d7b753bad0e0b3c057cd250b11755)
- Plugin hyperframes: v0.9.14 (15b1de4aeba2a375931c13542fa2d1e6500174db)
- Plugin superpowers: v7.0.2 (22f0b463e7a5e579904dd6211a520321035526f7)
- Plugin claude-mem: v15.9.0 (d0968e5d136abc34dcfe1b78acf3726fa84978d8)

- Node 24 LTS: 24.22.2; Bun 1.4.4; FFmpeg 9.0.2; Python runtime 3.13.17.
- Existing memory database and settings backed up locally before migration. Private data and credentials are excluded from this release.
- Managed skills: 77; previous SNS verification and skill refresh remain included.
- Hook trust remains a user action. No paid service activation, account authentication, personal browser attachment, proxy route changes or model downloads requested.

## Security and verification

- Pin undici 7.30.1; production npm audit: zero known vulnerabilities. Existing Zod, fallow and ECC fast-uri overrides retained.
- HyperFrames plugin launcher uses the audited managed runtime rather than fetching an unpatched npx copy. The installer fails closed if the runtime is missing or the wrapper changes unexpectedly.
- Repository tests: 63 passed. Firecrawl JSON Schema/Zod compatibility fixture and HyperFrames managed CLI launch passed.
- Claude-Mem 15.9.0: original codex/worker settings and local-only sync preserved; online SQLite backup taken before update. Health: ok, initialized, mcpReady, no degraded dependencies. Doctor: all required checks passed.
- Windows Unicode-path compiler workaround: compile the official bundled launcher with verified Bun from an ASCII temporary path; check protocol 2 before installing to the standard user-local launcher directory. Temporary compiler files are not distributed.
- Full plugin hooks/workflows and account-dependent rendering remain untested. Codex restart and changed-hook trust review are user actions. Host-managed bundled/curated apps remain managed by Codex, not this repository.
- Evidence: docs/RUNTIME_VERIFICATION_2026-11-05.json.
