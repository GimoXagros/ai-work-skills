---
name: image-glyph-generator
description: Rasterize a selected font into verified fixed-cell retro-game glyph atlases with explicit character ordering, coverage and clipping checks. Use for 한글 글리프 비트맵 생성; use imagegen separately when the user requests AI-generated artwork.
---

# Image glyph generator

Original ai-work-skills implementation, version 1.0.0. This skill provides reproducible font rasterization; the supplied Google answer's unverified image-generation CLI options are not used.

1. Choose the font asset explicitly with the user or existing project. Record its hash and usage terms. Do not bundle a system font, silently replace missing glyphs or synthesize Hangul from arbitrary strokes.
2. Establish the game's cell geometry, baseline, bit depth, character order and encoding map. Keep Unicode normalization explicit. This helper accepts single Unicode code points, not complex-script shaping, ligatures or composed sequences.
3. In a project virtual environment, install this skill's pinned `requirements.txt`. Run the helper on an explicit spec. Missing glyphs, duplicates, clipping and unexpected blank output fail before output is published. No auto-shrinking or fallback font is applied.
4. Inspect the generated atlas at native size and enlarged nearest-neighbor scale. Verify Hangul distinction, punctuation, baseline, spacing and any threshold artifacts. For actual AI-generated visual candidates, invoke the available imagegen skill/tool; treat those as artwork needing independent glyph identity checks.
5. Pack pixels into the game's actual tile format separately and validate the encoding-to-glyph mapping. Deliver atlas, manifest, selected source hash and parameters. Byte reproducibility across hosts also depends on font and rasterizer builds; compare artifact hashes before reuse.

## Input and command

UTF-8 JSON spec:

```json
{"chars":["가","나"," "],"size":12,"cell_width":16,"cell_height":16,
 "baseline":13,"x_offset":0,"threshold":128,"allow_empty":[" "]}
```

```text
python -m pip install -r requirements.txt
python scripts/rasterize_glyphs.py --font selected.ttf --spec glyphs.json --output new-atlas
```

Use Python 3.10+ supported by the pinned dependencies. `size` and cell dimensions are 1..512; baseline is measured from the cell top. `x_offset` positions the baseline origin horizontally. `threshold` is 1..255. TTF/OTF and collection face 0 are supported by the installed font libraries; select a separate face file if another face is needed.

The output directory must not already exist. It contains `atlas.png` (black background, white glyph pixels, up to 16 columns) and `manifest.json` (ordered glyph IDs, code points, ink bounds, advances, font hash and library versions). Blank space must be explicitly allowed. The atlas is binary luminance, not a transparent icon or console-ready tile file.

API references: [Pillow ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html), [fontTools TTFont](https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html).
