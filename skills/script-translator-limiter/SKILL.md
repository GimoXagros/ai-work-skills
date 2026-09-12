---
name: script-translator-limiter
description: Translate retro-game dialogue within explicit encoded byte, line and pixel budgets while preserving control tokens. Use for 길이 제한 한글 번역 and reinsertion validation with an encoding-mapper table; never silently truncate text.
---

# Script translator limiter

Original ai-work-skills implementation, version 1.0.0. Requires the sibling `encoding-mapper` skill; the repository installer includes it automatically.

1. Preserve entry IDs, speaker/context, glossary and source text. Obtain actual storage capacity, terminator bytes, line count and font advances from the game. Character count is not byte count.
2. Translate the meaning in natural Korean within those constraints. Preserve each declared control token in value, count and order. Do not invent plot context, remove controls, abbreviate proper names without agreement, or auto-truncate a failing line.
3. Run `scripts/check_script.py` with the same table used for reinsertion. Revise failures and rerun. If the meaning cannot fit, report alternatives or a separately justified relocation/font change.
4. Review terminology and meaning separately from mechanical checks. Verify rendered line breaks, variable substitutions, timing and boundary entries in the target emulator. A passing report does not prove translation quality or game compatibility.

## Input

UTF-8 script JSON:

```json
{"terminator_hex":"00","entries":[
  {"id":"dialogue-001","source":"Go!<WAIT>","translation":"가나<WAIT>",
   "max_bytes":7,"max_width_px":16,"max_lines":1}
]}
```

`max_bytes` includes the terminator appended by the eventual writer. Explicit empty `terminator_hex` means a length-delimited format. Every entry needs a unique ID, source, translation and nonnegative byte budget. Pixel and line limits are optional. A pixel limit requires a width for every translated glyph token. Newlines must be `kind: newline` in the table. Controls must be fully enumerated in both source and target notation before checking.

```text
python scripts/check_script.py --table table.json --script translation.json
```

The command writes a JSON report to stdout; exit 0 passes, 1 indicates failing entries, 2 invalid input. It never rewrites the script or ROM. It conservatively rejects terminator bytes anywhere inside the encoded payload. Games whose decoder distinguishes terminators only at token boundaries need a game-specific check. Variable-width substitutions, kerning, scrolling and parameterized controls require separate runtime-aware checks.
