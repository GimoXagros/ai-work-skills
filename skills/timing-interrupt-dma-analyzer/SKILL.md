---
name: timing-interrupt-dma-analyzer
description: "Trace emulator cycle and event-order bugs involving timers, IRQ/NMI, DMA, HBlank/VBlank, scanlines, FIFO, serial or audio in GameYob, GBARunner3 and NitroSwan. Use for timing divergence; not standalone opcode semantics or build failures."
---

# timing-interrupt-dma-analyzer

## Purpose

Explain a failure as an observed event sequence against an evidence-backed expected sequence.

## When to Use

An interrupt arrives too early/late, DMA ordering corrupts output, a FIFO underruns, or a frame/serial/audio failure depends on scheduling.

## When Not to Use

The same instruction is wrong without external events, an NDS linker fails, or a screenshot alone provides no timing evidence yet.

## Inputs

Commit pair; guest/host clock domains and mode; scheduler/cycle accounting source; trigger input; timestamped CPU/bus/device trace; documented event rules or hardware captures.

## Workflow

1. Reproduce on candidate and baseline. Define timestamps explicitly: guest cycles, scanline/dot, host ticks or audio samples; record conversion and avoid mixing domains.
2. Follow scheduler, timer reload, DMA request/transfer, interrupt latch/mask/acknowledgment and consumer code. List competing events at the failure boundary.
3. Build an ordered trace with event ID, timestamp, producer, pending IRQ/DMA state, bus owner and relevant register values. Keep instrumentation overhead visible.
4. Derive the expected order from the applicable device/model source and primary timing documentation. Mark uncertain cycle counts; do not borrow another console’s HBlank or DMA rules.
5. Find the earliest missing, extra or reordered event. Distinguish interrupt request from CPU service and DMA completion from request; test simultaneous events and masking/reload boundaries.
6. Reduce to a timer/DMA/serial/FIFO interaction or small lawful homebrew test. Check whether slowing the host merely hides a guest scheduling error.
7. Apply only an authorized scheduler/accounting fix. Rerun the boundary trace, adjacent event combinations and graphics/audio/save regressions without adding unexplained cycle fudge factors.

## Evidence Requirements

Observed → expected → first divergence with timestamp units, event ordering, state snapshots, source citations and capture method. “Timing issue” alone is not a result.

## Verification

Verify event order before and after, repeat at relevant clock/mode settings, and record hardware timing as a separate test from a PC/reference-emulator run. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Event timeline, first divergent transition, responsible producer/consumer, targeted test result and remaining timing uncertainty.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use graphics-vram-pipeline-debugger for rendering consequences or gb-link-nifi-debugger for a serial/transport boundary; use cpu-isa-differential-analyzer only if the instruction transition itself differs. Helpers are conditional and do not grant broader scope or become installation dependencies.
