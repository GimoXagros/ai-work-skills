---
name: sgb-host-debugger
description: "Debug GameYob Super Game Boy packet/command boundaries, 65C816/SPC700/DSP host execution, palette/border and OBJ transfers. Use for SGB host/protocol defects; not ordinary GB CPU bugs or a claim of complete SNES emulation."
---

# sgb-host-debugger

## Purpose

Trace a Super Game Boy command across GB protocol, host state and composition while respecting the implemented host subset.

## When to Use

SGB commands lose packets, border/palette transfer fails, host code/audio faults, or OBJ data reaches host state but not the final display.

## When Not to Use

Ordinary GB opcodes differ without SGB interaction, a web screen is broken, or general-purpose SNES emulation is requested.

## Inputs

GameYob commit and host coverage documentation; SGB model/mode; packet bits/bytes; command count/state; host memory/CPU/SPC/DSP trace; display captures and fault diagnostics.

## Workflow

1. Read the current project host coverage and fault policy before testing. Inventory protocol handlers, 65C816 execution, SPC700/DSP features and final composition separately; dispatch coverage is not semantic completeness.
2. Reproduce on baseline and candidate. Capture JOYP packet framing, bit order, packet count/command decoding and command payload validation before investigating downstream effects.
3. Follow accepted commands into palette/attribute/border transfer and bounded host memory/state. Trace DATA_SND/DATA_TRN/JUMP or audio paths only when present in this revision.
4. For a host CPU or audio fault, capture initial state and first divergent instruction/register/memory/DSP transition. Distinguish GB-side transfer, 65C816 execution, SPC700 behavior and DSP output.
5. For OBJ/border defects, verify decoding and transfer, then confirm whether the final renderer implements composition/priority. Separate documented no-op or unsupported paths from regressions.
6. Use project protocol/host tests or a small lawful synthetic command sequence; compare to SGB documentation and separately identified hardware captures. Never invent unimplemented timer/echo/IRQ behavior.
7. After an authorized minimal fix, rerun packet validation, host vectors and border/audio/composition regressions relevant to the change; preserve explicit faults for unsupported behavior.

## Evidence Requirements

Packet and decoded command, host coverage at inspected commit, first divergent boundary, source handler and expected behavior authority. Record whether a reference describes SGB hardware or the project’s subset.

## Verification

Test malformed/multipart packets plus the implicated host/composition path. Verify actual displayed/audio output separately from successful host-state decoding; PC tests do not prove SGB hardware accuracy. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

GB→packet→host→output boundary report, reproducer, implemented/unsupported table and regression results.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use cpu-isa-differential-analyzer for reduced 65C816/SPC700 vectors and graphics-vram-pipeline-debugger for final output. Primary protocol reference: https://gbdev.io/pandocs/SGB_Command_Packet.html ; implementation coverage must come from the inspected GameYob tree. Helpers are conditional and do not grant broader scope or become installation dependencies.
