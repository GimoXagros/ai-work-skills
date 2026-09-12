"""Check encoded game text budgets and control-token preservation; never truncate."""
import argparse
import importlib.util
import json
from pathlib import Path

CODEC = Path(__file__).resolve().parents[2] / 'encoding-mapper/scripts/codec_table.py'
if not CODEC.is_file():
    raise SystemExit('Install the required encoding-mapper skill alongside this skill.')
spec = importlib.util.spec_from_file_location('retro_codec', CODEC)
codec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codec)

def nonnegative(value, field):
    if type(value) is not int or value < 0:
        raise ValueError(f'{field} must be a nonnegative integer')
    return value

def check(document, table):
    terminator = bytes.fromhex(document['terminator_hex'])
    if not isinstance(document['entries'], list) or not document['entries']:
        raise ValueError('entries must be a nonempty list')
    rows, ids = [], set()
    for entry in document['entries']:
        key = entry['id']
        if not isinstance(key, str) or not key or key in ids:
            raise ValueError('entry ids must be unique nonempty strings')
        ids.add(key)
        errors = []
        try:
            text = entry['translation']
            if not isinstance(entry['source'], str) or not isinstance(text, str):
                raise ValueError('source and translation must be strings')
            tokens = table.tokens(text)
            data = table.encode(text)
            if terminator and terminator in data:
                errors.append('terminator occurs inside encoded text; consumer semantics require review')
            byte_count = len(data) + len(terminator)
            if byte_count > nonnegative(entry['max_bytes'], 'max_bytes'):
                errors.append('encoded byte budget exceeded (including terminator)')
            if table.controls(entry['source']) != table.controls(text):
                errors.append('control tokens changed in value, count or order')
            line_widths = [0]
            for token in tokens:
                if token.get('kind') == 'newline':
                    line_widths.append(0)
                elif token.get('kind', 'glyph') == 'glyph':
                    if 'max_width_px' in entry and 'width_px' not in token:
                        raise ValueError('pixel budget requested but glyph width is missing')
                    line_widths[-1] += token.get('width_px', 0)
            if 'max_width_px' in entry and max(line_widths) > nonnegative(entry['max_width_px'], 'max_width_px'):
                errors.append('line pixel budget exceeded')
            if 'max_lines' in entry and len(line_widths) > nonnegative(entry['max_lines'], 'max_lines'):
                errors.append('line count exceeded')
            rows.append({'id': key, 'ok': not errors, 'bytes': byte_count,
                         'line_widths_px': line_widths if 'max_width_px' in entry else None,
                         'lines': len(line_widths), 'errors': errors})
        except (ValueError, KeyError, TypeError) as exc:
            rows.append({'id': key, 'ok': False, 'errors': [str(exc)]})
    return {'ok': all(r['ok'] for r in rows), 'entries': rows,
            'scope': 'declared table, control tokens and budgets only; not translation-quality or runtime validation'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--table', type=Path, required=True)
    p.add_argument('--script', type=Path, required=True)
    args = p.parse_args()
    try:
        table = codec.CodecTable(json.loads(args.table.read_text(encoding='utf-8-sig')))
        result = check(json.loads(args.script.read_text(encoding='utf-8-sig')), table)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0 if result['ok'] else 1
    except (OSError, ValueError, TypeError, KeyError) as exc:
        p.error(str(exc))

if __name__ == '__main__':
    raise SystemExit(main())
