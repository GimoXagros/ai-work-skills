"""Strict, explicit ROM text tables. No encoding guessing or replacement fallback."""
import argparse
import hashlib
import json
from pathlib import Path
import re

def hex_bytes(value):
    if not isinstance(value, str) or not re.fullmatch(r'(?:[0-9a-fA-F]{2})+', value):
        raise ValueError('code must be nonempty hex pairs without separators')
    return bytes.fromhex(value)

class CodecTable:
    def __init__(self, spec):
        self.entries = spec['entries']
        if not isinstance(self.entries, list) or not self.entries:
            raise ValueError('entries must be a nonempty list')
        self.by_code, self.by_text = {}, {}
        reserved = [hex_bytes(c) for c in spec.get('reserved_codes', [])]
        for entry in self.entries:
            code, text = hex_bytes(entry['code']), entry['text']
            if not isinstance(text, str) or not text:
                raise ValueError('empty/non-string text token')
            if code in self.by_code or text in self.by_text:
                raise ValueError('duplicate byte code or text token')
            if entry.get('kind', 'glyph') not in ('glyph', 'control', 'newline'):
                raise ValueError('unsupported token kind')
            if 'width_px' in entry and (type(entry['width_px']) is not int or entry['width_px'] < 0):
                raise ValueError('width_px must be a nonnegative integer')
            if any(code.startswith(r) or r.startswith(code) for r in reserved):
                raise ValueError('code collides with a reserved code/prefix')
            self.by_code[code] = entry
            self.by_text[text] = entry
        codes = sorted(self.by_code)
        if any(b.startswith(a) for a, b in zip(codes, codes[1:])):
            raise ValueError('byte codes must be prefix-free for this stateless codec')
        self.text_keys = sorted(self.by_text, key=lambda s: (-len(s), s))

    def tokens(self, text):
        result, position = [], 0
        while position < len(text):
            match = next((s for s in self.text_keys if text.startswith(s, position)), None)
            if match is None:
                raise ValueError(f'unmapped character at text offset {position}: U+{ord(text[position]):04X}')
            result.append(self.by_text[match])
            position += len(match)
        return result

    def encode(self, text):
        return b''.join(hex_bytes(e['code']) for e in self.tokens(text))

    def decode(self, data):
        result, position = [], 0
        while position < len(data):
            match = next((c for c in self.by_code if data.startswith(c, position)), None)
            if match is None:
                raise ValueError(f'unmapped bytes at file offset {position}')
            result.append(self.by_code[match]['text'])
            position += len(match)
        text = ''.join(result)
        if self.encode(text) != data:
            raise ValueError('text aliases/ligatures make this byte sequence non-reversible')
        return text

    def controls(self, text):
        keys = sorted((e['text'] for e in self.entries if e.get('kind') == 'control'), key=len, reverse=True)
        pattern = '|'.join(re.escape(k) for k in keys)
        return re.findall(pattern, text) if pattern else []

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['validate', 'encode', 'decode'])
    p.add_argument('--table', type=Path, required=True)
    p.add_argument('--text')
    p.add_argument('--hex')
    args = p.parse_args()
    try:
        raw = args.table.read_bytes()
        table = CodecTable(json.loads(raw.decode('utf-8-sig')))
        if args.action == 'encode':
            if args.text is None:
                raise ValueError('--text is required')
            result = {'hex': table.encode(args.text).hex().upper()}
        elif args.action == 'decode':
            if args.hex is None:
                raise ValueError('--hex is required')
            result = {'text': table.decode(bytes.fromhex(args.hex))}
        else:
            result = {'entries': len(table.entries), 'sha256': hashlib.sha256(raw).hexdigest(), 'valid': True}
        print(json.dumps(result, ensure_ascii=True, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.error(str(exc))

if __name__ == '__main__':
    main()
