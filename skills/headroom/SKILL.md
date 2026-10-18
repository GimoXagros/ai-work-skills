---
name: headroom
description: "Use when explicitly optimizing LLM context or inspecting Headroom compression, proxy, or MCP integration."
---

# headroom

Run `headroom --help`, then inspect the requested subcommand help. Start with synthetic input and compare original versus compressed content. Preserve addresses, hashes, error identifiers and evidence needed for the task. Compression ratios are not proof of task accuracy. Proxy and MCP serving are optional: do not replace provider URLs, collect conversations, or start persistent services just because the package is installed. Measure correctness and token reduction separately.

## Installation and provenance

Run `python setup_integrations.py --install` from the ai-work-skills checkout, then load the generated toolchain environment as documented in `docs/INTEGRATIONS.md`. Use the installed CLI help as the version-specific interface.

This is an independently authored Codex routing skill. Upstream: https://github.com/headroomlabs-ai/headroom/tree/fbf7bc3278c11975299b9bd0a2ecf200dfd25a05. Runtime version and source audit pin are recorded separately in `integrations-lock.json`. Follow the host tool policy and user instructions.
