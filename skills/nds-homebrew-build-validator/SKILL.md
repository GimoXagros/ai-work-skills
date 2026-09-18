---
name: nds-homebrew-build-validator
description: "Validate DS/DSi homebrew emulator builds, devkitARM/BlocksDS/libnds configuration, ARM7/ARM9 linking and NDS/DLDI/TWL artifacts. Use for GameYob, GBARunner3 or NitroSwan build/toolchain failures; not runtime CPU compatibility."
---

# nds-homebrew-build-validator

## Purpose

Establish whether the configured toolchain produces the intended DS/DSi artifact and explain build failures at their first cause.

## When to Use

A project fails to compile/link/package, selects the wrong DS/DSi mode, or a produced NDS artifact needs structural validation.

## When Not to Use

An artifact already boots but game CPU semantics differ, or a ROM modification rather than homebrew build is requested.

## Inputs

Project build instructions and CI at a commit; selected build target; tool paths/versions; environment variables without secrets; submodule state; full build log; linker maps and ARM7/ARM9/NDS outputs.

## Workflow

1. Read maintained project docs, CI, Makefiles and linker scripts before choosing commands. Determine whether devkitARM/libnds or BlocksDS is authoritative for this target; legacy build paths are not current gates.
2. Record toolchain/container versions and environment discovery. Compare required submodules/libraries with checked-out versions; diagnose mismatches without upgrading or mixing toolchains globally.
3. Reproduce the documented baseline build in an isolated output location if supported. Respect project dependency/order constraints, including a documented serial build; do not invent parallel-build support.
4. Find the first compile/link/package failure rather than the last cascading error. Trace missing symbols, sections, CPU architecture flags and ARM7/ARM9 ownership through maps and rules.
5. Inspect NDS header and declared ARM7/ARM9 load/entry/size fields against produced binaries and maps using a confirmed tool or a small read-only parser. Distinguish malformed layout from a valid artifact’s runtime bug.
6. Check DLDI and DS/DSi/TWL configuration only as applicable to the project and launcher. Do not claim DLDI patching or DSi execution from filename/header alone.
7. After an authorized minimal build/configuration change, rebuild the failing target and relevant CI targets; hash artifacts. Record actual device boot separately from successful packaging.

## Evidence Requirements

Source build command, CI/toolchain identity, first error, linker/header observations, artifact hashes and target mode. Tool versions from the inspected project are facts for that revision, not universal requirements.

## Verification

Run the documented build and structural checks. Report compilation, packaging and actual hardware boot as distinct outcomes; a PC tool reading an NDS header does not validate DS execution. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Environment/build diagnosis, reproducible command, artifact validation table, minimal change result and untested launcher/device paths.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use log-analyzer for long logs and emulator-regression-tester after runtime launch is available. BlocksDS documentation: https://blocksds.skylyrac.net/docs/ ; project CI remains the target-specific authority. Helpers are conditional and do not grant broader scope or become installation dependencies.
