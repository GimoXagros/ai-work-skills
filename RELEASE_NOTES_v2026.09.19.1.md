# v2026.09.19.1 — emulator skill suite and log-analyzer v3.0.0

The default branch `main` now includes the 13 emulator-development skills previously delivered on `feat/emulator-development-skills`, plus the log-analyzer v3 upgrade from `feat/log-analyzer-v3`. The full installation contains 28 active skills; the two retired entries retain their existing preservation policy. See RELEASE_NOTES_v2026.09.17.1.md for the emulator suite and docs/EMULATOR_SKILL_AUDIT.md for routing boundaries.

The existing bundled custom log-analyzer now guides baseline versus failing-run comparison, structural alignment and first-divergence analysis. It retains v2 evidence-first triage, grouping, healthy-window comparisons, redaction and read-only source handling.

- Conservative normalization preserves meaningful addresses, values, timing and correlation; every transformation is recorded.
- Signature-assisted classification and scoped whitelists remain hints with retained evidence, not root-cause or passing-run verdicts.
- Multi-log clock uncertainty, multi-run intermittency and build/test retry/skip/timeout/environment boundaries are explicit.
- Optional handoffs support GameYob, GBARunner3 and NitroSwan subsystem debugging while general application/server logs remain supported.
- Comparison/signature references provide detailed procedures. No helper parser, MCP server, external LLM, daemon or new package dependency is required.

Reviewed djm81/log_analyzer_mcp (MIT + Commons Clause), microsoft/log_analyzer (MIT), lnav (BSD-2-Clause) and faultline-cli/faultline (MIT). Concepts were considered; no external implementation/catalog was copied or vendored. See REVIEW.md for source revisions, decisions and actual checks.

Validation: 48 unittest tests PASS; skill validator, selected/full installation, tool setup and inventory/backup checks PASS. Five explicit synthetic analysis cases were reviewed separately, not counted as parser or hardware tests. Tests add manifest/frontmatter/reference and offline install/backup contracts. Existing installer, upstream pins, retirement policy and other skill implementations remain unchanged. Active count stays 28. No copyrighted ROM, game assets, temporary logs or generated binaries are included. Real emulator/hardware validation and live implicit skill selection are outside the completed package checks.

Delivery: fast-forward merge into `main`, preserving both feature commits and the existing history. README installation instructions now use `main`. Release v2026.09.19.1 publishes the verified main checkout. Local installation is synchronized through the existing installer; system skills, plugin caches and unrelated local skills are preserved.
