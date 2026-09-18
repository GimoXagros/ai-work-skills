---
name: graphics-vram-pipeline-debugger
description: "Debug emulator BG/OBJ, palette, VRAM/OAM, window, scanline and framebuffer composition using register and rendering traces in GameYob, GBARunner3 or NitroSwan. Use for rendering pipeline faults; not browser layout or raw tile compression."
---

# graphics-vram-pipeline-debugger

## Purpose

Connect a visible defect to the first incorrect rendering input, transfer or composition decision.

## When to Use

Sprites disappear, palettes/borders corrupt, window/priority is wrong, or scanline updates differ across emulator builds.

## When Not to Use

Only a web interface is misaligned, an asset needs packing/unpacking, or a font repertoire needs capacity planning.

## Inputs

Matching baseline/candidate frame checkpoint; guest machine model; guest register/memory snapshots; host display/VRAM configuration; renderer source; scanline/transfer trace and expected image evidence.

## Workflow

1. Reproduce the defect at a stable guest frame/event. Capture baseline and candidate without changing scaling, screen layout or display filters.
2. Separate guest BG/OBJ/tile/palette/OAM/window state from host DS VRAM banks/display engines and final framebuffer. Follow the actual renderer and transfer path rather than assuming direct equivalence.
3. Trace from guest writes through tile/palette interpretation, cache invalidation, transfer scheduling, scanline latches and final priority/window/blend composition.
4. At the first bad pixel/scanline, compare contributing BG and OBJ values, palette entry, address/bank and window/priority decisions. A visually similar screenshot is not proof of the same mechanism.
5. Find the first divergence before the visible output: wrong source bytes, stale cache/transfer, mode-dependent decode, or composition order. Hand event-order defects to timing-interrupt-dma-analyzer.
6. Create a minimal lawful homebrew scene or reproducible input checkpoint covering overlap, clipping/window edges and the implicated mode; keep ROM sources read-only.
7. Apply an authorized minimal rendering fix and rerun the failing checkpoint plus neighboring modes/scenes. Check graphics and transfer-related audio/performance regressions.

## Evidence Requirements

Annotated capture linked to register/memory/renderer trace, guest/host address distinction, baseline/candidate values, first divergence and expected priority/format authority.

## Verification

Compare the same checkpoint and explicit edge cases; report pixel/hash tolerances and distinguish PC capture, reference emulator and real hardware observations. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Pixel-to-state explanation, pipeline stage responsible, reduced scene/checkpoint, comparison artifacts and mode coverage.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use ws-tile-compressor only for raw asset layout, retro-font-allocator only for font budgets, and sgb-host-debugger for protocol/host-side border or OBJ transfer. Helpers are conditional and do not grant broader scope or become installation dependencies.
