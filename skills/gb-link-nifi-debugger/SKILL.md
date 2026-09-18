---
name: gb-link-nifi-debugger
description: "Debug GameYob GB link serial clock/master/slave timing and dual-instance NiFi synchronization, packet loss or reorder. Use for link-layer vs wireless transport divergence; not general Wi-Fi setup or SGB packet commands."
---

# gb-link-nifi-debugger

## Purpose

Separate guest serial state-machine errors from network transport and synchronization failures.

## When to Use

Two instances exchange wrong bytes, a transfer hangs, clocks disagree, or NiFi loss/reorder causes guest divergence.

## When Not to Use

The problem is general router configuration, SGB JOYP commands, or a single CPU instruction unrelated to serial state.

## Inputs

Two instance commits/modes and initial states; SB/SC/interrupt traces; internal/external clock roles; transfer IDs; NiFi send/receive logs; adapter configuration and reproducible impairment schedule.

## Workflow

1. Reproduce baseline and candidate with both peers recorded. Fix input/start timing and identify each guest clock role and device mode; host wall-clock time is not guest serial time.
2. Capture guest transfer start, shift edges/bit count, data, completion and interrupt transition independently on each peer. Check external-clock waiting and disconnected behavior against the applicable GB model.
3. Follow guest serial events into the project NiFi protocol and DS adapter. Correlate transport packets with guest transfer IDs and synchronization points; do not assume a sequence field exists without reading the schema.
4. Locate the first divergence before timeout/retry fallout. Distinguish wrong guest clock/completion semantics from missing, duplicated, reordered or stale transport delivery.
5. Exercise simultaneous starts, asymmetric progress and controlled loss/duplicate/reorder in the project test adapter when available. Keep impairment injection out of the user’s live network; stop when only physical wireless testing is possible.
6. Apply an authorized minimal state-machine or adapter fix in the responsible layer. Avoid host-speed sleeps as a substitute for guest synchronization correctness.
7. Rerun both peers, valid/error protocol cases and disconnect/reconnect/reset boundaries. Record actual DS wireless results separately from a host protocol test.

## Evidence Requirements

Correlated guest and transport timelines, both peers’ state, first divergent edge/packet, packet schema/source and model-specific serial expectation.

## Verification

Verify matching transferred bytes and completion/interrupt state on both peers under the tested impairment schedule; report nondeterminism and real hardware coverage separately. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Layer diagnosis, dual-instance reproduction, paired trace, transport impairment results and unresolved wireless constraints.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use timing-interrupt-dma-analyzer for a reduced guest event-order issue. Serial reference: https://gbdev.io/pandocs/Serial_Data_Transfer_(Link_Cable).html ; GameYob NiFi source defines its transport, not Pan Docs. Helpers are conditional and do not grant broader scope or become installation dependencies.
