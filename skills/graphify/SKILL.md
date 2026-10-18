---
name: graphify
description: "Use when building or querying a local code knowledge graph with Graphify."
---

# graphify

Run `graphify --help`. For deterministic local code analysis use `graphify update <project> --no-cluster`; inspect `graphify-out/graph.json` and query with `graphify query "question" --graph <path>`. Read files to verify graph-derived claims. Graph extraction can miss dynamic relationships. LLM labels and remote ingestion are separate opt-ins. Do not run the global always-on installer or modify AGENTS.md merely to analyze one repository; use this scoped entrypoint.

## Installation and provenance

Run `python setup_integrations.py --install` from the ai-work-skills checkout, then load the generated toolchain environment as documented in `docs/INTEGRATIONS.md`. Use the installed CLI help as the version-specific interface.

This is an independently authored Codex routing skill. Upstream: https://github.com/Graphify-Labs/graphify/tree/86c57be8204673c2a1b9849a3292a7dd3ab373d8. Runtime version and source audit pin are recorded separately in `integrations-lock.json`. Follow the host tool policy and user instructions.
