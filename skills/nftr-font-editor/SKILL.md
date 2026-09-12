---
name: nftr-font-editor
description: Inspect standard little-endian Nintendo DS NFTR font blocks and modify a verified existing three-byte CWDH width entry in a new file. Use for NFTR 폰트 구조·글자폭 검사; glyph insertion, CMAP expansion and variants need a format-specific editor.
---

# NFTR font editor

Original ai-work-skills implementation, version 1.0.0. This is a narrowly scoped inspector and width editor, not a bundled GUI font editor.

1. Record the input hash and preserve the original. Confirm actual on-disk tags: `RTFN`, `FNIF`, `PLGC`, `HDWC`, `PAMC`. Do not substitute the documentation spellings in binary searches.
2. Run `scripts/nftr.py inspect`. Supported header versions are 0x0100/0x0101, little-endian, 16-byte header. Chunk sizes, data pointers, chain cycles, glyph ranges and CMAP methods 0/1/2 are checked. Unsupported structures fail; unknown unrelated blocks remain unchanged.
3. Before editing, establish that the target CWDH uses standard three-byte entries: signed left bearing, unsigned ink width, unsigned advance. Some variants use two-byte widths, and short padded blocks can be ambiguous. Structural validation cannot prove the consumer layout; inspect the game/editor evidence before using set-width.
4. Edit only a known existing width entry, supplying source SHA-256 and the expected original three bytes. Write to a fresh path. The helper preserves file size, offsets, maps and glyph data. It does not resize blocks, insert glyphs or reorder CMAP entries.
5. Compare the complete output with the original: only the selected triple may differ. Reopen the font in a compatible editor and verify affected glyphs in the actual game. CMAP first-match and overlap semantics are consumer-specific; this tool checks bounds and does not certify every mapping lookup.

## Commands

```text
python scripts/nftr.py inspect --font original.nftr
python scripts/nftr.py set-width --font original.nftr --glyph 3 --left 0 --glyph-width 8 --advance 9 --expected-hex 000808 --sha256 SOURCE_SHA256 --output changed.nftr
```

Python 3.10+, no dependencies. Take `expected-hex`, glyph ID and source hash from the inspection report, then corroborate the layout. Field limits are -128..127, 0..255, 0..255. Existing output paths are rejected. A file that does not match the supported layout must be investigated instead of having its checks disabled.

For glyph artwork, new CMAP coverage or larger fonts, inspect the relevant source/editor workflow: [Epicpkmn11 NFTR editor](https://github.com/Epicpkmn11/nftr-editor/blob/2e8ee2affd9316371812815758a51b2fd719e952/js/nftr.js). The source was reviewed as format evidence, not executed or bundled. The Google answer's named standalone editors are not themselves Codex skills.
