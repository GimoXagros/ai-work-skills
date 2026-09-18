---
name: cartridge-mapper-peripheral-analyzer
description: "Analyze emulator cartridge bank/address decoding and RTC, rumble, sensor, EEPROM/SRAM or serial peripherals in GameYob, GBARunner3 and NitroSwan. Use for mapper/device transactions; not save-file serialization or generic ROM relocation."
---

# cartridge-mapper-peripheral-analyzer

## Purpose

Identify the implemented cartridge device and its first incorrect bus transaction or state transition.

## When to Use

A game accesses the wrong bank, an RTC/sensor handshake fails, or a special cartridge is misdetected or mapped.

## When Not to Use

A correctly mapped device loses host-file data on restart, an instruction alone computes incorrect flags, or ROM pointers need relocation.

## Inputs

Cartridge identification evidence and read-only asset hash; mapper/device revision; address map; baseline/candidate; register/bus transaction trace; source handlers; primary device docs or hardware captures.

## Workflow

1. Identify cartridge hardware from header plus corroborating code/database/device evidence. Keep ambiguous variants unresolved; do not substitute the closest familiar mapper.
2. Map CPU-visible windows to bank selectors, ROM/RAM/EEPROM enable states and peripheral registers. Separate logical guest addresses, backing file offsets and host pointers.
3. Reproduce baseline and candidate with equal reset/latch state. Capture reads/writes, bank/enable registers and peripheral input around the first bad transaction.
4. Follow address masks, mirroring, bank limits, enable/unlock/latch sequences and device-specific state transitions from source. Distinguish open-bus/unimplemented behavior from a fabricated value.
5. For RTC/rumble/sensors/serial, isolate register protocol from host clock/input/transport adapters. Freeze controllable inputs and state what requires a physical peripheral.
6. Create synthetic bus sequences for boundary banks, disabled storage and reset/latch transitions. Hand persistence bytes to save-nvram-state-validator and event ordering to timing-interrupt-dma-analyzer.
7. Apply only an authorized evidence-backed decoder/device fix. Rerun the failing cartridge path and nearby mapper/device variants; leave unsupported hardware explicitly unsupported.

## Evidence Requirements

Device identity confidence, register/address map, first differing transaction, reset/input state, source locations and authority of expected bus behavior.

## Verification

Compare transaction sequences and game-visible behavior. Reference emulator agreement is separate from real hardware/peripheral validation. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Hardware identity, bank/device state machine diagnosis, reduced bus reproducer, compatibility checks and unsupported paths.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use re for unknown ROM/address-map investigation or log-analyzer for trace grouping; neither replaces device-specific expected behavior. Helpers are conditional and do not grant broader scope or become installation dependencies.
