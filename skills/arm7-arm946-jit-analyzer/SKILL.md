---
name: arm7-arm946-jit-analyzer
description: "Analyze GBARunner3 ARM7TDMI guest execution on ARM946E-S, ARM/Thumb JIT patching, relocation, hicode, caches, MPU and Data Abort emulation. Use for translation/execution-boundary faults; not generic ARM assembly review or ROM pointer fixing."
---

# arm7-arm946-jit-analyzer

## Purpose

Find whether a failure originates in guest semantics, translated bytes, memory mapping or host execution maintenance.

## When to Use

ARM/Thumb transitions or LDR/LDM/STM edge cases fail only in translated/direct execution, hicode breaks after cache changes, or MPU/Data Abort emulation produces wrong guest state.

## When Not to Use

The request is unrelated ARM assembly review, a static ROM pointer needs editing, or guest opcode semantics differ equally in all execution paths.

## Inputs

GBARunner3 revision and execution-path documentation; guest/host CPU model; original and replaced instruction bytes; CPSR/SPSR/register/memory state; translation/relocation metadata; MPU/cache/abort traces.

## Workflow

1. Reproduce baseline and candidate and identify the active path: direct execution, instruction replacement, dynamic JIT or linear JIT as actually implemented. Guest ARM7TDMI and host ARM946E-S rules require separate authorities.
2. Reduce to an instruction sequence retaining the ARM/Thumb state, addressing/writeback, exception and memory-access conditions. Build lawful homebrew vectors if the existing test harness supports them; never patch the user ROM to make a reproducer.
3. Compare original instruction semantics with emitted/patched bytes, branch targets, relocation ownership and CPSR/SPSR restoration. Hand a pure ISA difference to cpu-isa-differential-analyzer.
4. Trace code address/bank/backing storage, hicode mapping and translation metadata lifetime. Check stale references across mapping, replacement and backing-cache reuse against source invariants.
5. Follow cache maintenance and MPU permission/region changes in their actual order. For Data Abort, record fault address/type, saved PC/state and guest access emulation; never assume an abort is an ordinary guest exception.
6. Find the first divergence in emitted code, mapping, host fetch or resumed guest state. Inspect LDR/LDM/STM and mode transitions only against the exact instruction form/model; avoid invented universal edge-case rules.
7. Apply an authorized minimal fix; rerun the reduced vector in relevant execution paths plus relocation/cache invalidation, mode/exception and compatibility regression cases.

## Evidence Requirements

Guest vs emitted byte listing, architectural state comparison, first divergent mapping/fetch/abort, source metadata ownership and applicable CPU documentation revision. Equal byte hashes establish only the compared bytes; they do not prove identical host fetch, mapping or execution state.

## Verification

Compare baseline/candidate vectors and relevant path variants; preserve hicode and cache/MPU test evidence. PC assembly/disassembly is distinct from execution on actual ARM946 hardware. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Minimal sequence, responsible ISA/translation/mapping/cache/abort boundary, patch evidence and path/device coverage.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use re or binary-re for unknown emitted code and timing-interrupt-dma-analyzer for peripheral event order. Primary implementation: https://github.com/Gericom/GBARunner3 ; consult the maintained local fork and exact Arm CPU manuals before asserting semantics. Helpers are conditional and do not grant broader scope or become installation dependencies.
