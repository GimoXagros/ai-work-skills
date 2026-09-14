---
name: re
description: Investigate retro-game ROMs and hex dumps with bank-aware address maps, annotated disassembly, asset extraction and emulator cross-checks. Use for retro-game hex-analyzer requests or an existing REVERSE.md investigation; general executable triage can use binary-re.
---

# Retro-game reverse engineering

Codex adaptation of [vgrichina/re-skill](https://github.com/vgrichina/re-skill/tree/64c3bffb54ae4b9d99804a03fa4f179f4dd080c5), MIT, revision `64c3bffb54ae4b9d99804a03fa4f179f4dd080c5`. The upstream skill is named `re`; `hex-analyzer` is the user's requested capability, not its original package name.

## Start or resume

- Read the project's applicable instructions and existing investigation notes. If the user supplies a binary, first check whether it already belongs to a documented project; a path alone is not a reason to replace existing notes.
- For a new investigation, use [reverse_template.md](reverse_template.md) and [dead_ends_template.md](dead_ends_template.md) to create project-local notes. Record input SHA-256, platform evidence, CPU, entry points, file layout and unresolved regions. Add a focused next task. Preserve the source binary.
- For an existing investigation, read `REVERSE.md`, `labels.csv` and `dead_ends.md`; resume the highest-priority task within the user's scope. Read recent project session logs if they exist. Use available file/search tools instead of Claude-specific live-context shell macros.
- Read [phases.md](phases.md) for the relevant investigation stage. A hex inspection request does not imply a full disassembler, custom emulator or web port project.

## Evidence and addresses

Keep file offsets, CPU addresses, banks, RAM addresses and VRAM tile indices in separate fields. Every finding should include its input revision, byte range/address space, tool or observation, confidence and consumer when known.

- Flat images: `offset,name,comment`, with `0x` offsets.
- Banked ROMs: `bank,addr,name,comment`; document bank selection and mapped address ranges. RAM labels should identify RAM explicitly rather than being interpreted as ROM offsets.
- Segmented executables: retain segment and offset plus the load/relocation assumptions; do not treat `SEG:OFF` or `DS:offset` as a direct file offset.

File extensions and recognizable headers suggest a format; they do not prove code boundaries, asset type or compression. Confirm CPU mode and banking before interpreting opcodes. The Game Boy CPU is SM83/LR35902, not a generic Z80; use the correct instruction definitions.

When a hypothesis becomes supported, update `REVERSE.md` and labels promptly. Keep candidate interpretations distinct from verified facts. If repeated calls produce no new evidence, record the failed approach and split or reconsider the task; do not mark the underlying question solved merely because it was split.

## Investigation pitfalls

- Relocations can change pointer/call bytes between the original file and loaded memory. Use relocation-aware cross-references where appropriate.
- Compressed sections need their actual decoder and an explicit original-to-decoded address map. Preserve raw and decoded images; compression of one section does not imply replacing the entire input.
- Pointer tables can be indirect or bank-dependent. Follow them only after verifying bounds and the consuming code.
- A tile index may pass through attribute or remapping tables before reaching VRAM. Verify layout, stride, palette and flipping against rendering.
- Menu text and counters may be assembled at runtime. Trace their consumers rather than concluding they are absent because a string search failed.
- A changing byte in a memory-dump comparison is a candidate state variable. Corroborate with controlled input changes and read/write traces before assigning gameplay meaning.

## AKM-compatible investigation memory

When the project already uses AKM, or the user requests durable cross-session knowledge, route reusable findings through that project's `ROUTER.md`: verified platform and format knowledge belongs in `20-knowledge/`, project-specific maps and constraints in `30-context/`, repeatable analysis steps in `50-procedures/`, reproducible decisions or handoffs in `60-actions/`, and recurring dead ends or verification failures in `70-evaluation/`. Keep only short pointers in `40-memory/`. Do not create an AKM tree or persist one-off observations unless requested.

Treat search hits and pattern matches as candidates until the exact bytes, consumer, trace, or authoritative source are read. For durable notes, record the input hash and address space, verify discoverability and claim support, and use the failure record to correct the responsible map, procedure, or rubric instead of merely appending another session log.

## Tools and completion

This skill ships instructions and note templates, **not** `dis.py`, `xref.py`, a CPU database, an emulator or a compression decoder. Inspect the actual project's tools before invoking them. Use a suitable existing disassembler/emulator where available; create only missing, task-specific helpers and validate their output against independent traces or known vectors. Do not invent CLI options from proposed tool names.

For a hex inspection, deliver bounded byte ranges, candidate structures, verified mappings and remaining uncertainties. For deeper analysis, add only relevant checks: disassembly versus emulator traces, extracted assets versus frames, and decoded fields versus memory dumps. Preserve test inputs and a reproducible command trail.

Web reimplementation and its comparison documents are optional and require that scope in the user's request. The upstream Claude CLI loop and installer are not included; use the current Codex task normally. No automatic session loop, Git commit or publication is implied by invoking this skill.
