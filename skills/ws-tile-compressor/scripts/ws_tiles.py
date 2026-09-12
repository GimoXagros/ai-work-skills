#!/usr/bin/env python3
"""Lossless raw WonderSwan tile packing and exact deduplication, not a ROM codec."""
import argparse
import json
from pathlib import Path

FORMATS = {'planar2': 2, 'planar4': 4, 'packed2': 2, 'packed4': 4}


def pack_tile(pixels, fmt):
    depth = FORMATS[fmt]
    if len(pixels) != 64 or any(type(p) is not int or not 0 <= p < 2 ** depth for p in pixels):
        raise ValueError('Each tile needs exactly 64 palette indices within the bit depth')
    result = bytearray()
    for y in range(8):
        row = pixels[y * 8:y * 8 + 8]
        if fmt.startswith('planar'):
            for plane in range(depth):
                result.append(sum(((p >> plane) & 1) << (7 - x) for x, p in enumerate(row)))
        else:
            per_byte = 8 // depth
            for start in range(0, 8, per_byte):
                result.append(sum(row[start + i] << (8 - depth * (i + 1)) for i in range(per_byte)))
    return bytes(result)


def unpack_tile(data, fmt):
    depth = FORMATS[fmt]
    if len(data) != depth * 8:
        raise ValueError('Incorrect tile byte count')
    result = []
    for y in range(8):
        for x in range(8):
            if fmt.startswith('planar'):
                value = sum(((data[y * depth + plane] >> (7 - x)) & 1) << plane for plane in range(depth))
            else:
                per_byte = 8 // depth
                value = (data[y * depth + x // per_byte] >> (8 - depth * (x % per_byte + 1))) & (2 ** depth - 1)
            result.append(value)
    return result


def pack(spec, deduplicate=False):
    fmt = spec['format']
    if fmt not in FORMATS or not isinstance(spec['tiles'], list) or not spec['tiles']:
        raise ValueError('Known format and nonempty tiles list required')
    unique, indices, lookup = [], [], {}
    for tile in spec['tiles']:
        data = pack_tile(tile, fmt).hex().upper()
        if not deduplicate or data not in lookup:
            lookup[data] = len(unique)
            unique.append(data)
        indices.append(lookup[data])
    return {'codec': 'ws-raw-tiles-v1', 'format': fmt, 'tiles_hex': unique, 'tile_indices': indices,
            'raw_bytes': len(indices) * FORMATS[fmt] * 8,
            'tile_data_bytes': len(unique) * FORMATS[fmt] * 8,
            'note': 'Index-map storage is excluded. Deduplication requires consumer tile-index updates.'}


def unpack(spec):
    if spec['codec'] != 'ws-raw-tiles-v1' or spec['format'] not in FORMATS:
        raise ValueError('Unsupported codec or format')
    tiles = [unpack_tile(bytes.fromhex(data), spec['format']) for data in spec['tiles_hex']]
    indices = spec['tile_indices']
    if not tiles or not indices or any(type(i) is not int or not 0 <= i < len(tiles) for i in indices):
        raise ValueError('Invalid tile index map')
    return {'format': spec['format'], 'tiles': [tiles[i] for i in indices]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['pack', 'unpack'])
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--deduplicate', action='store_true')
    args = parser.parse_args()
    try:
        spec = json.loads(args.input.read_text(encoding='utf-8-sig'))
        if args.action == 'unpack' and args.deduplicate:
            raise ValueError('--deduplicate only applies to pack')
        print(json.dumps(pack(spec, args.deduplicate) if args.action == 'pack' else unpack(spec)))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
