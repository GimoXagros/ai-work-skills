---
name: cpu-isa-differential-analyzer
description: "Analyze emulator opcode, flag, exception and side-effect mismatches across guest and host CPUs: SM83/LR35902, SGB 65C816/SPC700, ARM7TDMI/ARM946E-S or V30MZ. Use for ISA divergence; not JIT relocation, mapper decoding or general binary triage."
---

# cpu-isa-differential-analyzer

## Purpose

Find the first architectural state mismatch without treating the host ISA as the guest specification.

## When to Use

A minimal instruction sequence disagrees in registers, flags, memory effects or exception state, including GBARunner3 guest/host execution differences.

## When Not to Use

The mismatch is already isolated to code cache/relocation, a cartridge bus mapping, or an executable whose CPU and subsystem are unknown.

## Inputs

Exact CPU/model and mode; instruction bytes; initial registers/flags/memory; interrupt inputs; implementation source at a commit; CPU manual revision or identified reference traces.

## Workflow

1. Identify guest, host and any translator separately. GameYob GB CPU and its optional SGB 65C816/SPC700 host paths are different execution domains; V30MZ is not automatically an 8086 oracle.
2. Establish a passing baseline and failing candidate with identical architectural input. Reduce to the shortest sequence retaining the mismatch without removing relevant exception or bus state.
3. Read the project opcode handler and applicable primary CPU documentation. Label every expectation as documented, hardware-measured, reference-implementation behavior or unresolved.
4. Collect pre/post PC, registers, flags, memory reads/writes, interrupt mask and exception return state per instruction. Mask only explicitly undefined fields and explain the mask.
5. Identify the first divergence before downstream corruption. Separate arithmetic/flag semantics, addressing side effects, privilege/mode changes, exception entry and return, and implementation-specific behavior.
6. Check boundary operands and both taken/untaken paths. Do not compare raw host flags to guest flags without the implementation mapping; do not transfer one CPU revision’s undefined behavior to another.
7. For an authorized fix, change only the responsible semantic path; rerun the reduced vector, adjacent instructions/modes and functional regression checks. Hand translation/cache defects to arm7-arm946-jit-analyzer.

## Evidence Requirements

Include exact bytes, initial/final states and the first unequal field, source locations and source authority. An unavailable manual remains an unresolved dependency, not a reconstructed specification.

## Verification

Repeat with identical initial state and an independently identified reference where available; document which expected fields are established and which need real hardware evidence. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

State-difference table, instruction reproducer, semantic cause or bounded hypothesis, minimal fix evidence and unresolved CPU-model questions.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use binary-re or re only for undecoded machine code; log-analyzer only for trace triage. ARM documentation is indexed at https://developer.arm.com/documentation/ ; consult the exact model manual, not a generic ARM summary. Helpers are conditional and do not grant broader scope or become installation dependencies.
