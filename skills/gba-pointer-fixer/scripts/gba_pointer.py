#!/usr/bin/env python3
"""Read-only conversion and inspection of canonical GBA ROM pointers."""
import argparse
import hashlib
import json
from pathlib import Path

BASE = 0x08000000
LIMIT = 0x02000000
KINDS = ('data', 'thumb', 'arm')

def check_kind(kind):
    if kind not in KINDS:
        raise ValueError('kind must be data, thumb, or arm')

def encode(offset, kind):
    check_kind(kind)
    if not 0 <= offset < LIMIT:
        raise ValueError('offset is outside the canonical 32 MiB ROM window')
    alignment = {'data': 1, 'thumb': 2, 'arm': 4}[kind]
    if offset % alignment:
        raise ValueError(f'{kind} entry requires {alignment}-byte alignment')
    return (BASE + offset) | (1 if kind == 'thumb' else 0)

def decode(value, kind, size=None):
    check_kind(kind)
    if not BASE <= value < BASE + LIMIT:
        raise ValueError('value is not in the canonical ROM window')
    if kind == 'thumb' and not value & 1:
        raise ValueError('THUMB function pointer must have bit 0 set')
    address = value & ~1 if kind == 'thumb' else value
    offset = address - BASE
    if encode(offset, kind) != value:
        raise ValueError('pointer representation is inconsistent')
    width = {'data': 1, 'thumb': 2, 'arm': 4}[kind]
    if size is not None and not (0 < size <= LIMIT and offset + width <= size):
        raise ValueError('target or minimum entry width is outside the ROM file')
    return offset

def inspect(path, at, kind):
    data = Path(path).read_bytes()
    if not 0 < len(data) <= LIMIT:
        raise ValueError('only nonempty ROM files up to 32 MiB are supported')
    if at < 0 or at + 4 > len(data):
        raise ValueError('pointer storage is outside the ROM file')
    value = int.from_bytes(data[at:at + 4], 'little')
    offset = decode(value, kind, len(data))
    return dict(pointer=f'0x{value:08X}', offset=f'0x{offset:X}', kind=kind,
                bytes_le=data[at:at + 4].hex(' ').upper(), storage_offset=f'0x{at:X}',
                sha256=hashlib.sha256(data).hexdigest(), size=len(data),
                validation='arithmetic and file bounds only; consumer evidence required')

def number(value):
    return int(value, 0)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('encode', 'decode', 'inspect'):
        sub = commands.add_parser(command)
        sub.add_argument('--kind', choices=KINDS, required=True)
        if command == 'encode':
            sub.add_argument('--offset', type=number, required=True)
        elif command == 'decode':
            sub.add_argument('--value', type=number, required=True)
        else:
            sub.add_argument('--rom', type=Path, required=True)
            sub.add_argument('--at', type=number, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'inspect':
            result = inspect(args.rom, args.at, args.kind)
        else:
            value = encode(args.offset, args.kind) if args.command == 'encode' else args.value
            offset = decode(value, args.kind)
            result = dict(pointer=f'0x{value:08X}', offset=f'0x{offset:X}', kind=args.kind,
                          bytes_le=value.to_bytes(4, 'little').hex(' ').upper(),
                          validation='arithmetic only; consumer evidence required')
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

if __name__ == '__main__':
    main()
