# Investigation stages

Adapted from vgrichina/re-skill, commit `64c3bffb54ae4b9d99804a03fa4f179f4dd080c5`. Select stages and checkpoints that answer the user's question. These are project activities, not preinstalled command names.

## 1. Identify

Record file hash, size, header observations, likely platform/CPU and entry points. Consult the actual platform memory map, including mapper/bank registers and RAM/VRAM boundaries. Start a data-range map with unknown areas left unclassified. Confirm header offsets and sizes instead of relying on extensions.

## 2. Decode compressed regions when relevant

Find a known codec or the actual decompression consumer. Entropy alone does not identify compression. Preserve the original bytes, decoder assumptions and output limits. Record which source regions produce which decoded ranges. Verify decompression before disassembling or rendering those ranges.

## 3. Disassemble and annotate

Choose a tool that supports the actual CPU, mode and banking. Decode bounded regions, retain instruction bytes and addresses, and annotate targets from the label map. Handle relocation and indirect control flow explicitly. If a custom helper is required, validate opcodes and address calculations against known vectors or independent traces before trusting its output.

A few representative functions cross-checked against emulator traces provide a useful checkpoint; this does not validate every code path or justify interpreting all bytes as instructions.

## 4. Extract relevant assets

Establish tile layout, bit depth, palette interpretation, attribute tables and tilemap stride. Decode only the assets needed for the task, preserving source offsets and indices. Compare representative outputs against the original running game. A small visual catalog is useful when many assets need comparison; a full website is not required for one hex lookup.

## 5. Map data structures

Use repeated patterns as hypotheses. Establish field widths, signedness, endianness, fixed-point scaling, struct stride and pointer levels from consumers. Resolve banked pointers with the active mapping. Confirm important fields against controlled emulator memory observations.

## 5.5. Controlled execution when static evidence is insufficient

Prefer an existing compatible debugger/emulator with breakpoints, traces and memory dumps. Script a reproducible scenario for the specific question. A targeted custom interpreter is an optional separate effort when existing tooling cannot provide the required evidence; its own CPU/memory behavior must be validated before it can establish game behavior.

## 6. Validate findings

Replay the relevant scenario in an emulator that actually supports the target platform. Compare decoded data, sprites, positions or control flow with observations. Mark findings verified only after the matching check; retain discrepancies and unknowns. A single screenshot or successful boot is limited evidence.

## 7. Web port, only when requested

Before reimplementing behavior, document the known binary architecture and the proposed implementation mapping. Port one understood subsystem at a time. Compare frames and gameplay state across representative scenarios. Do not extend a ROM analysis request into a web port or publication automatically.
