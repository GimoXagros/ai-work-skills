---
name: retro-font-allocator
description: Plan retro-game font repertoire storage and active glyph slots using explicit memory budgets, reserved slots and working sets. Use for 한글 폰트 용량·VRAM 슬롯 배분; not CSS font selection or automatic ROM relocation.
---

# Retro font allocator

Original ai-work-skills implementation, version 1.0.0.

1. Separate the complete stored repertoire from simultaneously resident glyphs. Establish bytes per glyph from the actual tile format, storage/bank bounds, usable slot count, reserved UI tiles and loader behavior.
2. Enumerate every scene's working set, pinned glyphs and transition working sets. If old glyphs remain visible during a load, include the union of old and new sets in a transition state. Do not assume arbitrary reloading is supported.
3. Use `scripts/allocate.py` for a deterministic state-local capacity proposal. Check storage overflow, pinned/reserved collisions and active capacity. The result is not a runtime loading schedule or a globally stable mapping: a glyph can receive different slots in different states.
4. If slot identity must persist, pin that glyph consistently or solve the actual lifetime problem. Include non-font allocations, banking, DMA limits, tilemap updates and loading time in a separate integration plan.
5. Deliver the input budget evidence, plan, mapping changes and emulator checks. Never present a capacity calculation alone as proof that the game can use the font.

## Input and command

```json
{"glyphs":["가","나","다"],"bytes_per_glyph":16,"storage_budget_bytes":48,
 "slot_capacity":4,"reserved_slots":[0],"pinned":{"가":1},
 "states":{"menu":["가","나"],"dialogue":["다"],"transition":["가","나","다"]}}
```

```text
python scripts/allocate.py allocation.json
```

Python 3.10+, no dependencies. Glyph identities are explicit nonempty strings. Slots are zero-based. Every pinned glyph consumes a slot in every state. The storage budget covers fixed-size glyph data only; include maps, headers, compressed data and alignment separately. Output is JSON to stdout, with no ROM changes. Compression ratios and automatically inferred lifetimes are unsupported.
