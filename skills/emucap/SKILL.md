---
name: emucap
description: Prepare or use emucap Control and optional Tracking MCP for emulator screenshots, input replay, memory/register inspection and reproducible retro-game debugging. Use for emucap setup, emulator control, runtime patch checks or experiment records. Available operations depend on the connected adapter.
---

# emucap workflow

Read the pinned [agent guide](https://github.com/mcpads/emucap/blob/cd0a39b6a4b102bd64c5877229b57e501f93697c/AGENT_GUIDE.md) for setup and [compatibility contract](https://github.com/mcpads/emucap/blob/cd0a39b6a4b102bd64c5877229b57e501f93697c/COMPATIBILITY.md) for version questions. This is an independently written skill entrypoint; installing it does not install emulator binaries, adapters, BIOS or MCP servers.

For an existing connection, discover the available Control tools and obtain bootstrap/status before choosing operations. Identify the emulator, adapter, source build, loaded game and capabilities from reported state. Do not infer connectivity or compatibility from the skill's presence.

For an authorized installation/update, follow the guide: select the host package, verify its published checksum and core manifest, prepare the adapter for the requested system, register the chosen executable paths, reconnect discovery and check reported identities. On Windows use documented PowerShell/Rust launch paths. Preserve existing settings and only replace the relevant server registrations. Users supply game images and required firmware.

Control drives the emulator; Tracking records experiments under .emucap and does not itself run games. Use Tracking only when experiment records are needed. Pass observed values to records rather than fabricating screenshot, hash or runtime results.

Before a debugging run, identify the exact candidate, baseline, start condition and reproduction path. Use supported step/tap operations and inspect the resulting state; distinguish frozen frame advances from explicitly running operations. Save-state evidence must identify its source build and creation point; use cold boot where initialization matters.

Report what was observed, which inputs/interventions were used, associated evidence and remaining coverage. Static build success and a successful MCP connection do not establish runtime correctness. Use kr-patch-qa for localization release criteria when available.
