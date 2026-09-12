"""Synthetic boundary and known-vector tests; no game assets required."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'skills' / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


codec = load('codec', 'encoding-mapper/scripts/codec_table.py')
translator = load('translator', 'script-translator-limiter/scripts/check_script.py')
allocator = load('allocator', 'retro-font-allocator/scripts/allocate.py')
ws = load('ws', 'ws-tile-compressor/scripts/ws_tiles.py')
nftr = load('nftr', 'nftr-font-editor/scripts/nftr.py')
raster = load('raster', 'image-glyph-generator/scripts/rasterize_glyphs.py')


TABLE = {'reserved_codes': ['00'], 'entries': [
    {'code': '8140', 'text': '가', 'width_px': 8},
    {'code': '8141', 'text': '나', 'width_px': 7},
    {'code': 'FE', 'text': '\n', 'kind': 'newline'},
    {'code': 'FD01', 'text': '<WAIT>', 'kind': 'control'}]}


class EncodingTests(unittest.TestCase):
    def test_korean_controls_exact_bytes_round_trip(self):
        table = codec.CodecTable(TABLE)
        raw = bytes.fromhex('8140FD01FE8141')
        self.assertEqual(table.encode('가<WAIT>\n나'), raw)
        self.assertEqual(table.decode(raw), '가<WAIT>\n나')

    def test_collisions_and_reserved_prefix_fail(self):
        for entry in [{'code': '8140', 'text': '다'}, {'code': '82', 'text': '가'},
                      {'code': '81', 'text': '다'}, {'code': '0001', 'text': '다'}]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                table = copy.deepcopy(TABLE)
                table['entries'].append(entry)
                codec.CodecTable(table)

    def test_unknown_and_ambiguous_sequences_fail(self):
        table = codec.CodecTable(TABLE)
        with self.assertRaises(ValueError):
            table.encode('다')
        with self.assertRaises(ValueError):
            table.decode(b'\x81')
        ambiguous = codec.CodecTable({'entries': [
            {'code': '01', 'text': 'a'}, {'code': '02', 'text': 'b'}, {'code': '03', 'text': 'ab'}]})
        with self.assertRaisesRegex(ValueError, 'non-reversible'):
            ambiguous.decode(b'\x01\x02')


class TranslationTests(unittest.TestCase):
    def document(self):
        return {'terminator_hex': '00', 'entries': [{'id': '1', 'source': 'Go<WAIT>',
                'translation': '가나<WAIT>', 'max_bytes': 7, 'max_width_px': 15, 'max_lines': 1}]}

    def test_exact_byte_and_pixel_boundaries(self):
        result = translator.check(self.document(), codec.CodecTable(TABLE))
        self.assertTrue(result['ok'])
        self.assertEqual(result['entries'][0]['bytes'], 7)
        self.assertEqual(result['entries'][0]['line_widths_px'], [15])

    def test_overflows_controls_and_unknowns_rejected(self):
        for key, value in [('max_bytes', 6), ('max_width_px', 14), ('max_lines', 0),
                           ('translation', '가나'), ('translation', '다<WAIT>')]:
            doc = self.document()
            doc['entries'][0][key] = value
            with self.subTest(key=key, value=value):
                self.assertFalse(translator.check(doc, codec.CodecTable(TABLE))['ok'])

    def test_missing_width_and_interior_terminator_fail(self):
        table = copy.deepcopy(TABLE)
        del table['entries'][0]['width_px']
        self.assertFalse(translator.check(self.document(), codec.CodecTable(table))['ok'])
        doc = self.document()
        doc['terminator_hex'] = '8140'
        self.assertFalse(translator.check(doc, codec.CodecTable(TABLE))['ok'])

    def test_newlines_and_duplicate_or_empty_entries(self):
        doc = self.document()
        doc['entries'][0].update(translation='가\n나<WAIT>', max_bytes=8, max_width_px=8, max_lines=2)
        self.assertEqual(translator.check(doc, codec.CodecTable(TABLE))['entries'][0]['line_widths_px'], [8, 7])
        doc['entries'] *= 2
        with self.assertRaises(ValueError):
            translator.check(doc, codec.CodecTable(TABLE))
        doc['entries'] = []
        with self.assertRaises(ValueError):
            translator.check(doc, codec.CodecTable(TABLE))


class AllocationTests(unittest.TestCase):
    def spec(self):
        return {'glyphs': ['a', 'b', 'c'], 'bytes_per_glyph': 16, 'storage_budget_bytes': 48,
                'slot_capacity': 3, 'reserved_slots': [0], 'pinned': {'a': 1},
                'states': {'menu': ['b'], 'dialogue': ['c']}}

    def test_storage_distinct_from_working_set(self):
        result = allocator.allocate(self.spec())
        self.assertEqual(result['storage_bytes'], 48)
        self.assertEqual(result['states']['menu']['slots'], {'a': 1, 'b': 2})
        self.assertEqual(result['states']['dialogue']['slots'], {'a': 1, 'c': 2})

    def test_storage_transition_and_reserved_collisions_fail(self):
        for mutation in [{'storage_budget_bytes': 47}, {'states': {'transition': ['a', 'b', 'c']}},
                         {'pinned': {'a': 0}}, {'pinned': {'a': 1, 'b': 1}}, {'glyphs': []}]:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                spec = self.spec()
                spec.update(mutation)
                allocator.allocate(spec)


class TileTests(unittest.TestCase):
    def test_known_vectors_each_layout(self):
        vectors = [('planar2', list(range(4)) * 16, '5533'),
                   ('packed2', list(range(4)) * 16, '1B1B'),
                   ('planar4', list(range(8)) * 8, '55330F00'),
                   ('packed4', list(range(8)) * 8, '01234567')]
        for fmt, pixels, row in vectors:
            with self.subTest(fmt=fmt):
                expected = bytes.fromhex(row * 8)
                self.assertEqual(ws.pack_tile(pixels, fmt), expected)
                self.assertEqual(ws.unpack_tile(expected, fmt), pixels)

    def test_dedup_preserves_original_tile_order(self):
        spec = {'format': 'planar2', 'tiles': [[0] * 64, [3] * 64, [0] * 64]}
        packed = ws.pack(spec, True)
        self.assertEqual(packed['tile_indices'], [0, 1, 0])
        self.assertEqual(packed['tile_data_bytes'], 32)
        self.assertEqual(ws.unpack(packed), spec)
        self.assertEqual(len(ws.pack(spec)['tiles_hex']), 3)

    def test_invalid_pixel_size_and_map_fail(self):
        for pixels in [[4] * 64, [0] * 63, [True] * 64]:
            with self.assertRaises(ValueError):
                ws.pack_tile(pixels, 'planar2')
        with self.assertRaises(ValueError):
            ws.unpack_tile(bytes(15), 'planar2')
        packed = ws.pack({'format': 'planar2', 'tiles': [[0] * 64]})
        packed['tile_indices'] = [-1]
        with self.assertRaises(ValueError):
            ws.unpack(packed)


def synthetic_nftr():
    # Explicit synthetic standard NFTR: FINF at16, CGLP at44, CWDH at76, CMAP at100.
    def block(tag, payload):
        return tag + struct.pack('<I', len(payload) + 8) + payload
    finf = block(b'FNIF', struct.pack('<BBHBBBBIII', 0, 8, 0, 0, 8, 8, 1, 52, 84, 108))
    glyph = block(b'PLGC', struct.pack('<BBHBBBB', 8, 8, 8, 7, 8, 1, 0) + bytes(16))
    widths = block(b'HDWC', struct.pack('<HHI', 0, 1, 0) + bytes.fromhex('000808FF0708') + bytes(2))
    cmap = block(b'PAMC', struct.pack('<HHHHIH', 65, 66, 0, 0, 0, 0) + bytes(2))
    body = finf + glyph + widths + cmap
    return b'RTFN' + struct.pack('<HHIHH', 0xFEFF, 0x100, 16 + len(body), 16, 4) + body


class NftrTests(unittest.TestCase):
    def test_inspect_and_only_selected_width_changes(self):
        original = synthetic_nftr()
        report = nftr.inspect(original)
        self.assertEqual(report['glyph_count'], 2)
        self.assertEqual(report['width_entries'][1]['left'], -1)
        changed = nftr.change_width(original, 1, -2, 6, 9, 'FF0708', hashlib.sha256(original).hexdigest())
        differences = [i for i, (a, b) in enumerate(zip(original, changed)) if a != b]
        self.assertEqual(differences, [95, 96, 97])
        self.assertEqual(nftr.inspect(changed)['width_entries'][1]['advance'], 9)

    def test_hash_expected_bytes_and_fields_gate_edit(self):
        data = synthetic_nftr()
        sha = hashlib.sha256(data).hexdigest()
        for args in [(1, 0, 8, 8, '000000', sha), (1, 0, 8, 8, 'FF0708', '0' * 64),
                     (1, -129, 8, 8, 'FF0708', sha), (2, 0, 8, 8, 'FF0708', sha)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                nftr.change_width(data, *args)

    def test_truncation_cycle_bad_pointer_and_mapping_fail(self):
        source = synthetic_nftr()
        corruptions = [source[:-1]]
        for at, value in [(48, 999999), (36, 85), (88, 84), (116, 108)]:
            mutated = bytearray(source)
            struct.pack_into('<I', mutated, at, value)
            corruptions.append(mutated)
        bad_map = bytearray(source)
        struct.pack_into('<H', bad_map, 120, 5)
        corruptions.append(bad_map)
        for data in corruptions:
            with self.subTest(data=data), self.assertRaises(ValueError):
                nftr.inspect(data)

    def test_output_collision_preserves_existing_file(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'font.nftr'
            source.write_bytes(synthetic_nftr())
            result = subprocess.run([sys.executable, str(ROOT / 'skills/nftr-font-editor/scripts/nftr.py'),
                'set-width', '--font', str(source), '--output', str(source), '--glyph', '1', '--left', '0',
                '--glyph-width', '8', '--advance', '8', '--expected-hex', 'FF0708',
                '--sha256', hashlib.sha256(source.read_bytes()).hexdigest()], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), synthetic_nftr())


class RasterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A synthetic rectangular test glyph, not a distributable typeface or game asset.
        from fontTools.fontBuilder import FontBuilder
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        cls.temporary = tempfile.TemporaryDirectory()
        cls.font_path = Path(cls.temporary.name) / 'fixture.ttf'
        builder = FontBuilder(1000, isTTF=True)
        builder.setupGlyphOrder(['.notdef', 'A', 'space'])
        builder.setupCharacterMap({65: 'A', 32: 'space'})
        pen = TTGlyphPen(None)
        pen.moveTo((100, 0)); pen.lineTo((600, 0)); pen.lineTo((600, 700)); pen.lineTo((100, 700)); pen.closePath()
        empty = TTGlyphPen(None).glyph()
        builder.setupGlyf({'.notdef': empty, 'A': pen.glyph(), 'space': empty})
        builder.setupHorizontalMetrics({'.notdef': (700, 0), 'A': (700, 100), 'space': (400, 0)})
        builder.setupHorizontalHeader(ascent=800, descent=-200)
        builder.setupNameTable({'familyName': 'SyntheticFixture', 'styleName': 'Regular', 'uniqueFontIdentifier': 'SyntheticFixture', 'fullName': 'SyntheticFixture', 'psName': 'SyntheticFixture'})
        builder.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800, usWinDescent=200)
        builder.setupPost()
        builder.save(cls.font_path)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def spec(self):
        return {'chars': ['A', ' '], 'size': 10, 'cell_width': 8, 'cell_height': 10,
                'baseline': 8, 'allow_empty': [' ']}

    def test_atlas_is_binary_and_reproducible(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / 'a', Path(temporary) / 'b'
            manifest = raster.rasterize(self.font_path, self.spec(), first)
            raster.rasterize(self.font_path, self.spec(), second)
            self.assertEqual((first / 'atlas.png').read_bytes(), (second / 'atlas.png').read_bytes())
            self.assertEqual(manifest['glyphs'][0]['codepoint'], 'U+0041')
            with Image.open(first / 'atlas.png') as atlas:
                self.assertEqual(atlas.size, (16, 10))
                self.assertEqual({v for _, v in atlas.getcolors()}, {0, 255})

    def test_missing_glyph_clipping_and_unexpected_blank_fail_without_output(self):
        for mutation in [{'chars': ['가'], 'allow_empty': []}, {'cell_width': 2}, {'allow_empty': []}, {'chars': ['A', 'A'], 'allow_empty': []}]:
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / 'out'
                spec = self.spec(); spec.update(mutation)
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    raster.rasterize(self.font_path, spec, output)
                self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / 'notes.txt').write_text('keep')
            with self.assertRaises(ValueError):
                raster.rasterize(self.font_path, self.spec(), output)
            self.assertEqual((output / 'notes.txt').read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
