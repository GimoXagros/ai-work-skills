---
name: gba-pointer-fixer
description: Diagnose and repair Game Boy Advance ROM pointer tables during relocation, translation, or hook work. Distinguish ROM offsets, runtime addresses, data pointers, and ARM/THUMB function pointers; verify expected bytes and affected consumers before edits. GBA 포인터 분석·변환·재배치 오류 수정에 사용한다.
---

# GBA Pointer Fixer

This is a custom skill authored for ai-work-skills, version 1.0.0. It is not an
upstream OpenAI or mcpads skill. The Google AI summary that motivated it is not
proof that a downloadable skill or a game-specific pointer format exists.

## Establish the representation

Identify the ROM revision, file size, SHA-256, pointer storage offset, original
bytes, old target, proposed target, and code that consumes the value. Inspect the
project's established build and relocation mechanisms before introducing another.
A numerical match is a candidate, not proof of a pointer or of complete coverage.

Classify each value before converting it:

- A file offset is a position in the dump; it is not a CPU address.
- Plain ROM pointers in the canonical Game Pak window use address = 0x08000000 +
  offset, stored as four little-endian bytes. Confirm this representation in the game.
- Data addresses retain their low bits. An odd byte address is valid data and must
  not be rounded or tagged as code just because it is odd.
- For interworking function pointers consumed by BX or an equivalent established
  calling path, THUMB targets have bit 0 set; the actual entry is halfword aligned.
  ARM targets are word aligned. Do not apply this rule to every branch instruction.
- Relative/packed pointers, RAM targets, banked/custom cartridges, ROM mirrors,
  compressed tables, and encoded instruction immediates require their own verified
  representation. Do not force them through the canonical conversion helper.

Read [pointer-rules.md](references/pointer-rules.md) when choosing a representation
or validating a hook. Check the linked hardware/assembly sources for a detail not
established by the target's evidence.

## Conversion and inspection helper

Use Python 3.10+ and `scripts/gba_pointer.py` relative to this skill's directory.
It only calculates and reads files; it never patches a ROM.

```text
python scripts/gba_pointer.py encode --offset 0x24A1BC --kind data
python scripts/gba_pointer.py encode --offset 0x1234 --kind thumb
python scripts/gba_pointer.py decode --value 0x08001235 --kind thumb
python scripts/gba_pointer.py inspect --rom game.gba --at 0x200 --kind data
```

Use the installed skill's absolute script path when running from a game project.
`--kind` is mandatory: it is a statement backed by caller evidence, not an
automatic classifier. Decode without a file establishes arithmetic only; inspect
also rejects targets outside the actual file. A valid result does not establish
entry length, allocation ownership, complete references, or runtime behavior.

## Repair and verify

For an authorized edit, use the project's patch/build pipeline. Bind the write to
the immutable input hash and expected original four bytes at each confirmed site.
Prepare all writes before applying them; reject overlaps, out-of-range writes,
unexpected bytes, and unexplained changes. Preserve the input and produce a new
output. Retain shared/interior references and do not assume padding is free space.

Relocating a pointer does not relocate its data. Verify the new content is present,
complete, suitably aligned, reachable by its consumer, and survives any copying or
decompression. If modifying a hook instruction, assemble/disassemble for ARM7TDMI
and verify the instruction encoding, displacement, mode, live registers and return
path; changing a pointer word is not an instruction relocation implementation.

Compare the full output diff to the planned writes and report both hashes. Test the
affected dialogue, menu, code path or save/load route with the exact output in an
emulator when available. State separately whether arithmetic, static patch checks,
and runtime checks passed. Never claim the game is repaired from conversion alone.
Return confirmed sites, old/new targets, evidence, changes, and remaining unknowns.

Cheat-device encryption, Action Replay/CodeBreaker conversion, automatic bulk
rewriting of scan matches, and ROM expansion are outside this helper's capability.
