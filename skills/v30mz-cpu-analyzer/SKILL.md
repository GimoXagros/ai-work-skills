---
name: v30mz-cpu-analyzer
description: "Analyze NitroSwan NEC V30MZ instruction, flags, segmentation, interrupts and CPU cycle/test-vector failures. Use for V30MZ-specific execution; not generic x86 assumptions or WonderSwan peripheral register behavior."
---

# v30mz-cpu-analyzer

## Purpose

Diagnose V30MZ CPU behavior while keeping compatible x86 behavior and model-specific evidence separate.

## When to Use

A NitroSwan CPU validation case disagrees in flags, segment/address behavior, interrupt boundaries or instruction cycles.

## When Not to Use

The fault is a WonderSwan video/EEPROM peripheral transaction, general desktop x86 reverse engineering, or only raw tile packing.

## Inputs

NitroSwan and ARMV30MZ revisions; CPU model; instruction bytes/prefixes; initial flags/registers/segments/memory; memory/I/O hooks; test-suite source/version and expected-result provenance.

## Workflow

1. Read the checked-out ARMV30MZ documentation and hooks, including declared limitations. Do not infer complete accuracy from broad opcode coverage or the core’s name.
2. Reproduce baseline and candidate with identical initial CPU, segment and interrupt state. Identify whether failure first occurs in instruction handling or memory/I/O integration.
3. Reduce the instruction sequence while preserving prefixes, segment selection, operand boundaries and interrupt inputs. Classify each expected result as V30MZ documented/measured, reference-core behavior or merely 8086/80186 comparison.
4. Compare PC/registers/flags, segmented address generation, bus accesses and exception/interrupt state at each instruction. Find the first divergence and retain evidence for undefined or untested status bits.
5. For REP/LOCK, divide faults, interruptibility and cycle boundaries, consult exact core and model evidence. Treat README caveats as implementation limits, not a hardware specification; do not import generic x86 flags/timings.
6. Separate CPU cycle accounting from Sphinx scheduler/peripheral behavior. Use timing-interrupt-dma-analyzer or wonderswan-hardware-analyzer when the first mismatch is outside the CPU.
7. Apply an authorized minimal CPU/hook fix and rerun reduced vectors, adjacent prefixes/segment boundaries and lawful CPU validation tests whose expected results are known.

## Evidence Requirements

Instruction bytes and initial state, first differing field/address/cycle, core revision and source path, validation test provenance, model-specific expected behavior and unresolved assumptions.

## Verification

Repeat vectors and interpreted test-suite results; never call a passed x86 test proof of V30MZ accuracy. Distinguish PC/reference runs from actual WonderSwan hardware results. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

V30MZ state-difference report, minimal vector, CPU vs hook/scheduler classification, test results and declared limitations.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Primary core source and implementation caveats: https://github.com/FluBBaOfWard/ARMV30MZ . Use cpu-isa-differential-analyzer only for a cross-model comparison, not as a second competing CPU specification. Helpers are conditional and do not grant broader scope or become installation dependencies.
