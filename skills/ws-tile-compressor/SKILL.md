---
name: ws-tile-compressor
description: Pack and unpack WonderSwan 8x8 raw tiles in planar or packed 2bpp/4bpp formats and deduplicate identical tiles losslessly. Use for 원더스완 폰트 타일 변환·중복 제거; game-specific compressed streams require separate reverse engineering.
---

# WonderSwan tile compressor

Original ai-work-skills implementation, version 1.0.0. Here WS means WonderSwan. The user's Google answer discussed WebSocket context compression and supplied no relevant skill.

1. Identify the game's actual video mode and decoder. Separate on-disk compression, raw tile representation, tile indices, palette indices and VRAM allocation. Never infer a game compression codec from the platform name.
2. Use `scripts/ws_tiles.py` only for explicit 8x8 row-major palette-index tiles. Formats are `planar2`, `planar4`, `packed2`, `packed4`. A 2bpp tile is 16 bytes; a 4bpp tile is 32 bytes. Plane bytes are interleaved per row, with the leftmost pixel in bit 7. Packed pixels run from high to low bits.
3. Optional exact deduplication returns a new index map. It does not preserve original tile IDs. Only apply the result after all consumers can be remapped and shared mutable tiles are excluded. Flips, palette remapping and lossy merging are unsupported.
4. Unpack and compare every original pixel and tile index. Budget the index map and tile attributes separately; reported tile-data savings do not include them. For a game's compressed stream, derive its decoder and test exact decompression independently.
5. Deliver the format evidence, round-trip result, tile map and runtime integration checks. No helper writes a ROM, tilemap or VRAM.

## Commands

Input JSON has `format` and `tiles`, each tile a list of exactly 64 integers from 0..3 or 0..15. Coordinates are top-to-bottom rows, left-to-right pixels. Output includes codec `ws-raw-tiles-v1`, `tiles_hex` and `tile_indices` and is accepted by unpack.

```text
python scripts/ws_tiles.py pack --input tiles.json --deduplicate
python scripts/ws_tiles.py unpack --input packed.json
```

Python 3.10+, no dependencies. Save stdout as UTF-8 JSON if using it as input later. The word compressor denotes exact tile deduplication here, not a universal WonderSwan LZ/RLE encoder.

Format checked against the four fetch branches in [ares PPU memory.cpp](https://github.com/ares-emulator/ares/blob/af4cbb04f067682a8a3cf42695ff78bed634b38d/ares/ws/ppu/memory.cpp). The implementation is original; upstream code is not bundled.
