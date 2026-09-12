#!/usr/bin/env python3
"""Rasterize explicit font glyphs into fixed cells with coverage and clipping checks."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile


def rasterize(font_path, spec, output):
    import PIL
    from PIL import Image, ImageDraw, ImageFont
    import fontTools
    from fontTools.ttLib import TTFont

    font_path, output = Path(font_path), Path(output)
    chars = spec['chars']
    if not isinstance(chars, list) or not chars or any(not isinstance(c, str) or len(c) != 1 for c in chars):
        raise ValueError('chars must contain individual Unicode code points; shaping is unsupported')
    if len(set(chars)) != len(chars):
        raise ValueError('Duplicate characters')
    size, width, height = spec['size'], spec['cell_width'], spec['cell_height']
    baseline, x_offset, threshold = spec['baseline'], spec.get('x_offset', 0), spec.get('threshold', 128)
    if any(type(v) is not int or not 1 <= v <= 512 for v in (size, width, height)):
        raise ValueError('size and cell dimensions must be integers 1..512')
    if type(baseline) is not int or not 0 <= baseline <= height or type(x_offset) is not int:
        raise ValueError('Invalid baseline or x_offset')
    if type(threshold) is not int or not 1 <= threshold <= 255:
        raise ValueError('threshold must be 1..255')
    allow_empty = spec.get('allow_empty', [])
    if not isinstance(allow_empty, list) or any(c not in chars for c in allow_empty):
        raise ValueError('allow_empty must be a subset of chars')
    if output.exists():
        raise ValueError('Output directory already exists; choose a new path')
    with TTFont(font_path, fontNumber=0) as ttfont:
        cmap = ttfont.getBestCmap() or {}
        missing = [f'U+{ord(c):04X}' for c in chars if not cmap.get(ord(c)) or cmap[ord(c)] == '.notdef']
    if missing:
        raise ValueError('Font lacks glyphs: ' + ', '.join(missing))
    font = ImageFont.truetype(str(font_path), size, index=0, layout_engine=ImageFont.Layout.BASIC)
    columns = min(16, len(chars))
    atlas = Image.new('L', (columns * width, ((len(chars) + columns - 1) // columns) * height), 0)
    records = []
    for glyph_id, char in enumerate(chars):
        # Render with padding before cropping; actual ink bounds detect clipping, including antialiasing.
        left, top, right, bottom = font.getbbox(char, anchor='ls')
        pad = max(size * 4, abs(left), abs(top), abs(right), abs(bottom), abs(x_offset)) + 8
        canvas = Image.new('L', (width + pad * 2, height + pad * 2), 0)
        ImageDraw.Draw(canvas).text((pad + x_offset, pad + baseline), char, font=font, fill=255, anchor='ls')
        bounds = canvas.getbbox()
        if bounds and (bounds[0] < pad or bounds[1] < pad or bounds[2] > pad + width or bounds[3] > pad + height):
            raise ValueError(f'Glyph U+{ord(char):04X} clips the cell; adjust dimensions or baseline explicitly')
        cell = canvas.crop((pad, pad, pad + width, pad + height)).point(lambda p: 255 if p >= threshold else 0)
        if cell.getbbox() is None and char not in allow_empty:
            raise ValueError(f'Glyph U+{ord(char):04X} has no visible pixels; explicitly allow intended blank glyphs')
        atlas.paste(cell, ((glyph_id % columns) * width, (glyph_id // columns) * height))
        records.append({'glyph_id': glyph_id, 'char': char, 'codepoint': f'U+{ord(char):04X}',
                        'ink_bbox': cell.getbbox(), 'font_advance_px': font.getlength(char)})
    manifest = {'schema_version': 1, 'font_sha256': hashlib.sha256(font_path.read_bytes()).hexdigest(),
                'settings': spec, 'columns': columns, 'glyphs': records,
                'pillow': PIL.__version__, 'fonttools': fontTools.__version__,
                'note': 'Atlas contains binary luminance pixels; console tile packing is a separate operation.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.glyph-stage-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'result'
        stage.mkdir()
        atlas.save(stage / 'atlas.png')
        (stage / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        stage.rename(output)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = rasterize(args.font, json.loads(args.spec.read_text(encoding='utf-8-sig')), args.output)
        print(json.dumps({'output': str(args.output.resolve()), 'glyph_count': len(result['glyphs'])}))
    except (ValueError, KeyError, TypeError, OSError, ImportError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
