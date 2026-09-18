---
name: save-nvram-state-validator
description: "Validate emulator SRAM/EEPROM/Flash, RTC persistence and save-state serialization, initialization, corruption handling and load/save round trips. Use for lost or malformed saves in GameYob, GBARunner3 or NitroSwan; not ROM pointer repair."
---

# save-nvram-state-validator

## Purpose

Verify persistent bytes and emulated save-device behavior without risking the user’s only save.

## When to Use

Saves disappear after restart, device detection/size is wrong, RTC state fails to persist, or a state loader accepts corrupt/truncated input.

## When Not to Use

A GBA ROM pointer is misaligned, a bank decoder is wrong before persistence, or the request is dialogue reinsertion.

## Inputs

Save hardware/model and detection evidence; save/state format/version; path policy; baseline/candidate; user-authorized disposable save copies or synthetic data; expected initialization and RTC policy.

## Workflow

1. Preserve original saves and state files; use isolated copies only when authorized, or synthetic fixtures. Record hashes and paths before testing; never load a valuable save into a writing test unprotected.
2. Distinguish cartridge SRAM/EEPROM/Flash protocol, host file persistence, RTC metadata and full emulator state. Determine sizes/signatures/version fields from implementation and device evidence, not extension alone.
3. Reproduce baseline and candidate from equal initialized storage. Trace detection, initialization values, device commands, dirty tracking, flush triggers, filenames and I/O error handling.
4. Perform write → flush → close/process restart → reload → readback. Separately test state serialization/restoration, byte order/layout and RTC elapsed-time/offset policy with a controlled clock.
5. Exercise size boundaries, unknown versions, corrupt headers and every relevant truncation boundary with synthetic fixtures. Confirm rejection before destructive partial state mutation or file overwrite.
6. Locate the first divergence in device response, in-memory state, serialized bytes or reloaded state. Do not confuse a correct save file with incorrect cartridge mapping.
7. After an authorized minimal fix, rerun valid round trips and negative cases, verify originals unchanged, and check existing format compatibility and declared migration behavior.

## Evidence Requirements

Before/after hashes, expected device size and format authority, I/O/state trace, first mismatching offset or transition, restart readback and corrupt-input outcome.

## Verification

Verify bytes and game-visible behavior across actual close/restart; test truncated/corrupt fixtures safely. Separate host-file tests from PC emulation and real save-device tests. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Persistence matrix, format/detection findings, round-trip results, failure atomicity and remaining device/clock coverage.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use cartridge-mapper-peripheral-analyzer for bus/device selection and gba-pointer-fixer only for ROM-internal pointers. Existing save formats must not be silently migrated or truncated. Helpers are conditional and do not grant broader scope or become installation dependencies.
