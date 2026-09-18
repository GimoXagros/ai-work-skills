---
name: wonderswan-hardware-analyzer
description: "Analyze NitroSwan WonderSwan/Color/Crystal video, DMA/IRQ, sound, EEPROM, RTC, serial and cartridge register/timing behavior. Use for hardware-subsystem emulation faults; not V30MZ opcode semantics or raw tile packing/deduplication."
---

# wonderswan-hardware-analyzer

## Purpose

Trace WonderSwan peripheral integration from guest registers and bus events to emulated output for the selected machine model.

## When to Use

Video/windows/sprites, DMA/IRQ, sound, internal/cartridge EEPROM, RTC or serial tests disagree outside the CPU handler.

## When Not to Use

A V30MZ opcode has an isolated semantic mismatch, a tile file needs conversion/deduplication, or a DS build fails before running.

## Inputs

NitroSwan revision and submodule revisions; mono/Color/Crystal selection; relevant Sphinx/WSCart/WSEEPROM handlers; register/bus/timing traces; baseline/candidate; lawful hardware test source and expected-result evidence.

## Workflow

1. Identify the selected WonderSwan model and read the relevant checked-out subsystem docs. Separate guest hardware from NitroSwan’s DS display, audio, storage and input adapters.
2. Reproduce baseline and candidate with equal reset, cartridge and peripheral state. Identify the earliest failing register transaction or scheduled event before interpreting final pixels/audio.
3. Follow guest port/address decoding into Sphinx, WSCart or WSEEPROM as present. Distinguish internal EEPROM from cartridge EEPROM and RTC protocol from host-clock persistence.
4. For video, trace mode, sprite/window/palette state and transfer/latch timing; for sound, DMA/IRQ/serial, capture producer/consumer events and device state. Do not apply Color-only features to mono by assumption.
5. Interpret hardware test results from the actual test version, model and expected signature. Separate hardware measurement, reference emulator behavior and implementation comments; an unexplained pass screen is insufficient.
6. Reduce the failing subsystem sequence using synthetic register/bus inputs or existing lawful homebrew tests. Route CPU semantics to v30mz-cpu-analyzer and persistence to save-nvram-state-validator.
7. Apply an authorized minimal peripheral/integration fix; rerun the failed and neighboring model/device cases plus graphics/audio/timing regressions. Keep unimplemented behavior explicit.

## Evidence Requirements

Machine model, submodule commits, first divergent register/event, input state, test signature/provenance and expected hardware behavior authority.

## Verification

Verify subsystem traces and observable outputs for each tested model; report PC/reference and real WonderSwan hardware results separately and avoid unsupported “hardware accurate” conclusions. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Subsystem/model matrix, register/event reproducer, integration diagnosis, regression evidence and unsupported device coverage.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use ws-tile-compressor only for raw tile formats, graphics-vram-pipeline-debugger for composition, and cartridge-mapper-peripheral-analyzer for reduced cartridge decoding. Primary implementation references: https://github.com/FluBBaOfWard/Sphinx and https://github.com/FluBBaOfWard/NitroSwan . Helpers are conditional and do not grant broader scope or become installation dependencies.
