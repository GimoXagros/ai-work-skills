---
name: emulator-regression-tester
description: "Compare baseline and candidate emulator builds for boot, crashes, graphics, audio, saves and speed in GameYob, GBARunner3 or NitroSwan. Use for compatibility regressions; not isolated opcode diagnosis or browser UI testing."
---

# emulator-regression-tester

## Purpose

Produce a reproducible compatibility matrix that separates observed regressions from missing coverage.

## When to Use

A core change needs before/after acceptance evidence, a game stops booting, or graphics/audio/saving/speed changes across revisions.

## When Not to Use

An isolated CPU instruction already has a minimal trace, a browser interface is broken, or the request is only to build an NDS file.

## Inputs

Baseline/candidate commit and artifact hashes; machine and DS/DSi mode; lawful locally available assets identified by hash; boot/input/reset script; initial save/state policy; capture points and tolerances.

## Workflow

1. Reproduce one failure and verify the same procedure on the baseline. Freeze inputs, seeds, clocks and starting state where possible; record unavoidable nondeterminism.
2. Build a matrix of asset hash × platform/mode × scenario. Include boot, sustained execution, crash, graphics, audio, save/reload and performance only where evidence can be collected.
3. Use project-provided runners or manual checkpoints. Keep display scaling, audio sample format, run length and CPU settings identical; never create a fictional runner.
4. Capture frame hashes/screenshots at matching guest events, audio windows, save outcomes and traces. A screenshot hash is meaningful only when the capture path is stable; otherwise use a stated tolerance or manual comparison.
5. Locate the first divergence in input/frame/event chronology. Distinguish capture noise and intentional output changes from changed guest behavior; route a reduced trace to the relevant subsystem skill.
6. After an authorized minimal fix, rerun the failing cell, neighboring games/features and repeated trials needed to assess variance. Measure speed separately from compatibility and state the reference device.
7. Classify each cell PASS, FAIL, BLOCKED or NOT RUN against an explicit expectation. Preserve failure artifacts and unresolved cells instead of averaging them away.

## Evidence Requirements

Record expected and actual outcome per cell, command/input transcript, capture event, artifact hashes and trial count. A reference emulator match is evidence, not a hardware oracle.

## Verification

Replay the failing and neighboring cells with the same starting state. Verify a claimed fix against the original symptom and compare variability before using a performance threshold. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Compatibility matrix; first divergent event; reproducible steps; subsystem handoff; coverage and platform limitations.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use log-analyzer for initial error grouping, save-nvram-state-validator for persistence, and graphics-vram-pipeline-debugger for a reduced rendering mismatch. These are optional helpers. Helpers are conditional and do not grant broader scope or become installation dependencies.
