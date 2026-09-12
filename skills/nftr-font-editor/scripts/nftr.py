#!/usr/bin/env python3
"""Inspect standard little-endian NFTR and edit one verified three-byte width entry."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def inspect(data):
    def u16(at):
        return struct.unpack_from('<H', data, at)[0]

    def u32(at):
        return struct.unpack_from('<I', data, at)[0]

    if len(data) < 16 or data[:4] != b'RTFN' or data[4:6] != b'\xff\xfe':
        raise ValueError('Expected standard little-endian RTFN header')
    if u16(6) not in (0x100, 0x101) or u32(8) != len(data) or u16(12) != 16:
        raise ValueError('Unsupported version, header size, or inconsistent file size')
    chunks, at = {}, 16
    for _ in range(u16(14)):
        if at + 8 > len(data):
            raise ValueError('Truncated chunk header')
        size = u32(at + 4)
        if size < 8 or at + size > len(data):
            raise ValueError('Invalid chunk bounds')
        chunks[at + 8] = {'tag': data[at:at + 4].decode('ascii', errors='replace'), 'offset': at, 'size': size}
        at += size
    if at != len(data):
        raise ValueError('Block count does not cover the file')
    finfs = [c for c in chunks.values() if c['tag'] == 'FNIF']
    if len(finfs) != 1 or finfs[0]['size'] < 28:
        raise ValueError('Expected one standard FINF block')
    finf = finfs[0]['offset']

    def chunk(pointer, tag, minimum):
        found = chunks.get(pointer)
        if not found or found['tag'] != tag or found['size'] < minimum:
            raise ValueError(f'Invalid {tag} data pointer or block size: {pointer:#x}')
        return found

    glyph = chunk(u32(finf + 16), 'PLGC', 16)
    g = glyph['offset']
    cell_width, cell_height, cell_size = data[g + 8], data[g + 9], u16(g + 10)
    bpp = data[g + 14]
    if not cell_width or not cell_height or not cell_size or not 1 <= bpp <= 8:
        raise ValueError('Invalid glyph dimensions, cell size, or bit depth')
    if cell_size * 8 < cell_width * cell_height * bpp:
        raise ValueError('Glyph cell cannot contain the declared pixels')
    glyph_count, padding = divmod(glyph['size'] - 16, cell_size)
    if not glyph_count or padding > 3 or (padding and any(data[g + glyph['size'] - padding:g + glyph['size']])):
        raise ValueError('Invalid glyph payload or padding')
    width_entries, seen = {}, set()
    pointer = u32(finf + 20)
    if not pointer:
        raise ValueError('Missing width chain')
    while pointer:
        if pointer in seen:
            raise ValueError('Cyclic width chain')
        seen.add(pointer)
        current = chunk(pointer, 'HDWC', 16)
        c = current['offset']
        first, last = u16(c + 8), u16(c + 10)
        required = 16 + (last - first + 1) * 3
        if first > last or last >= glyph_count or required > current['size'] or current['size'] - required > 3:
            raise ValueError('Unsupported or invalid CWDH range/three-byte width layout')
        for glyph_id in range(first, last + 1):
            if glyph_id in width_entries:
                raise ValueError('Overlapping width ranges')
            width_at = c + 16 + (glyph_id - first) * 3
            left, ink_width, advance = struct.unpack_from('<bBB', data, width_at)
            width_entries[glyph_id] = {'offset': width_at, 'left': left, 'glyph_width': ink_width,
                                       'advance': advance, 'hex': data[width_at:width_at + 3].hex().upper()}
        pointer = u32(c + 12)
    if seen != {p for p, c in chunks.items() if c['tag'] == 'HDWC'}:
        raise ValueError('Orphan CWDH block')
    maps, seen = [], set()
    pointer = u32(finf + 24)
    while pointer:
        if pointer in seen:
            raise ValueError('Cyclic character-map chain')
        seen.add(pointer)
        current = chunk(pointer, 'PAMC', 20)
        c, size = current['offset'], current['size']
        first, last, method, reserved = struct.unpack_from('<HHHH', data, c + 8)
        if first > last or reserved or method not in (0, 1, 2):
            raise ValueError('Unsupported CMAP header')
        if method == 0:
            if size < 22 or u16(c + 20) + last - first >= glyph_count:
                raise ValueError('Invalid direct CMAP glyph range')
        elif method == 1:
            if size < 20 + 2 * (last - first + 1):
                raise ValueError('Truncated table CMAP')
            if any(u16(c + 20 + 2 * i) not in range(glyph_count) and u16(c + 20 + 2 * i) != 0xFFFF for i in range(last - first + 1)):
                raise ValueError('CMAP references missing glyph')
        else:
            if size < 22 or size < 22 + 4 * u16(c + 20):
                raise ValueError('Truncated scan CMAP')
            for i in range(u16(c + 20)):
                code, tile = struct.unpack_from('<HH', data, c + 22 + i * 4)
                if not first <= code <= last or tile >= glyph_count:
                    raise ValueError('Invalid scan CMAP entry')
        maps.append({'offset': c, 'first': first, 'last': last, 'method': method})
        pointer = u32(c + 16)
    if seen != {p for p, c in chunks.items() if c['tag'] == 'PAMC'}:
        raise ValueError('Orphan CMAP block')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'version': f'{u16(6):04X}',
            'glyph_count': glyph_count, 'cell_width': cell_width, 'cell_height': cell_height,
            'cell_size': cell_size, 'bpp': bpp, 'chunks': list(chunks.values()),
            'width_entries': width_entries, 'character_maps': maps}


def change_width(data, glyph_id, left, glyph_width, advance, expected_hex, expected_sha):
    report = inspect(data)
    if report['sha256'].lower() != expected_sha.lower():
        raise ValueError('Source SHA-256 mismatch')
    if glyph_id not in report['width_entries']:
        raise ValueError('Glyph has no explicit width entry')
    entry = report['width_entries'][glyph_id]
    expected = bytes.fromhex(expected_hex)
    if len(expected) != 3 or expected.hex().upper() != entry['hex']:
        raise ValueError('Expected width bytes mismatch')
    if not -128 <= left <= 127 or not 0 <= glyph_width <= 255 or not 0 <= advance <= 255:
        raise ValueError('Width fields out of range')
    changed = bytearray(data)
    at = entry['offset']
    changed[at:at + 3] = struct.pack('<bBB', left, glyph_width, advance)
    inspect(changed)
    return bytes(changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect', 'set-width'])
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--glyph', type=int)
    parser.add_argument('--left', type=int)
    parser.add_argument('--glyph-width', type=int)
    parser.add_argument('--advance', type=int)
    parser.add_argument('--expected-hex')
    parser.add_argument('--sha256')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        data = args.font.read_bytes()
        if args.action == 'inspect':
            print(json.dumps(inspect(data), indent=2))
        else:
            required = [args.glyph, args.left, args.glyph_width, args.advance, args.expected_hex, args.sha256, args.output]
            if any(v is None for v in required):
                raise ValueError('set-width requires all edit options')
            changed = change_width(data, *required[:-1])
            with args.output.open('xb') as output:
                output.write(changed)
            if args.output.read_bytes() != changed:
                raise ValueError('Written output verification failed')
            print(json.dumps({'output': str(args.output.resolve()), 'sha256': hashlib.sha256(changed).hexdigest()}))
    except (ValueError, KeyError, TypeError, OSError, struct.error) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
