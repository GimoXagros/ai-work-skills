# Representation notes

The helper deliberately supports the canonical ROM window only. It accepts a file
offset from 0 through 0x01FFFFFF and a corresponding CPU address from 0x08000000
through 0x09FFFFFF. It rejects RAM, save-memory addresses and alternative windows
instead of silently masking high bits. Establish mirroring or special mappings in
the target before implementing support for them.

For data at offset 0x24A1BC, the pointer is 0x0824A1BC and the four stored bytes are
BC A1 24 08. For a THUMB function entry at offset 0x1234, a BX-consumed function
pointer is 0x08001235 (35 12 00 08). An ARM entry at the same offset is 0x08001234.
The data pointer 0x08001235 instead points to byte offset 0x1235: preserve that bit.

BX selects instruction state from the target's low bit. Direct B/BL instructions
encode displacements and are not four-byte absolute pointer slots. ARM7TDMI also
has instruction-specific PC semantics; use its assembler and decoder for hooks.
Do not import ARMv5+ BLX encodings into an ARMv4T target.

Storage alignment and target alignment are separate questions. The helper can read
four bytes at an unaligned file position, but that does not prove the game can load
the word correctly with its chosen instruction. Inspect the consuming routine.

## Sources and provenance

- [Tonc: GBA hardware](https://gbadev.net/tonc/hardware.html) — memory regions,
  ROM base and conventional cartridge size limit.
- [Tonc: ARM assembly](https://gbadev.net/tonc/asm.html) — interworking, BX,
  branch instructions and ARM/THUMB distinctions.
- [ARM7TDMI Technical Reference Manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819)
  — architecture reference linked by Tonc; consult for instruction-specific work.
- [mcpads reinsertion guidance](https://github.com/mcpads/create-retro-game-kr-patch/blob/56b31cc138926d769de97820df76e11beec6abb0/skills/create-kr-patch/references/strategy/reinsertion.md)
  — consumer evidence, relocation and expected-write checks.
- [Original user-shared Google AI answer](https://share.google/aimode/Ae9wpvuK7SkxrN8nv)
  — motivation only, not an upstream distribution or authoritative specification.

The cited [proflead/codex-skills-library](https://github.com/proflead/codex-skills-library)
did not contain gba-pointer-fixer in its master tree when checked on 2026-09-12.
This repository supplies its own implementation under the requested name.
