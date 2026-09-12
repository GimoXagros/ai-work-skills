---
name: encoding-mapper
description: Build and verify explicit byte-to-text tables for retro-game scripts, Hangul glyph IDs and control codes. Use for ROM 인코딩 테이블 작성, 충돌 검사, 텍스트 추출·재삽입 왕복 검증; not repository file routing or automatic codec guessing.
---

# Encoding mapper

Original ai-work-skills implementation, version 1.0.0. The supplied Google answer did not provide an installable skill. Use this alongside create-kr-patch when available.

1. Establish the exact input revision and text consumer. Separate file offsets, byte codes, Unicode text and glyph indices. Identify terminators, newline tokens, parameterized controls, banks and decoder state from evidence.
2. Build one explicit table used by extraction, translation validation and font generation. Preserve the selected character order and normalization policy; do not silently normalize Hangul, replace unknown characters or assign reserved codes.
3. Use `scripts/codec_table.py` only for stateless, prefix-free byte codes. Its text encoder uses longest-match tokens. Stateful encodings, parameterized controls, aliases and ambiguous ligatures need a game-specific decoder. Table validation alone does not establish reversibility for every possible text sequence.
4. Validate the table, decode representative original bytes, and re-encode them byte-for-byte. Include control boundaries and all supported glyphs. An ambiguous decoded token sequence fails instead of being silently canonicalized.
5. Record unknown bytes with input offset and surrounding data. Deliver the table, its hash, tests and remaining unknowns before reinsertion. The helper never modifies a ROM.

## Input and commands

Table JSON (UTF-8):

```json
{"reserved_codes":["00"],"entries":[
  {"code":"8140","text":"가","width_px":8},
  {"code":"8141","text":"나","width_px":8},
  {"code":"FE","text":"\n","kind":"newline"},
  {"code":"FD01","text":"<WAIT>","kind":"control"}
]}
```

Run with Python 3.10+; paths below are relative to this skill directory:

```text
python scripts/codec_table.py validate --table table.json
python scripts/codec_table.py encode --table table.json --text "가나<WAIT>"
python scripts/codec_table.py decode --table table.json --hex 81408141FD01
```

Each code is nonempty hexadecimal pairs without separators. Duplicate bytes/text, reserved-prefix collisions and non-prefix-free codes fail. `width_px` is the observed rendering advance for a glyph token; derive it from the actual font/consumer. Controls and newline tokens have dedicated kinds. The table only recognizes controls explicitly enumerated in it; parameter values cannot be inferred from a placeholder.
