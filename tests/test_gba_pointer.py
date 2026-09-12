import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gba_pointer', ROOT / 'skills/gba-pointer-fixer/scripts/gba_pointer.py')
pointer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pointer)

class PointerTests(unittest.TestCase):
    def test_known_little_endian_word(self):
        self.assertEqual(pointer.encode(0x24A1BC, 'data').to_bytes(4, 'little'), bytes.fromhex('BC A1 24 08'))

    def test_data_low_bit_is_preserved(self):
        self.assertEqual(pointer.decode(0x08001235, 'data'), 0x1235)
        self.assertEqual(pointer.decode(0x08001235, 'thumb'), 0x1234)

    def test_boundaries_and_alignment(self):
        for value, kind in [(0x02000000, 'data'), (0x0A000000, 'data'), (0x08000000, 'thumb'), (0x08000002, 'arm')]:
            with self.subTest(value=value, kind=kind), self.assertRaises(ValueError):
                pointer.decode(value, kind)
        for offset, kind in [(-1, 'data'), (0x2000000, 'data'), (3, 'thumb'), (2, 'arm')]:
            with self.subTest(offset=offset, kind=kind), self.assertRaises(ValueError):
                pointer.encode(offset, kind)
        self.assertEqual(pointer.decode(0x09FFFFFF, 'data'), 0x1FFFFFF)

    def test_inspection_preserves_input_and_rejects_invalid_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'synthetic.gba'
            data = bytearray(64)
            data[4:8] = bytes.fromhex('20 00 00 08')
            path.write_bytes(data)
            result = pointer.inspect(path, 4, 'data')
            self.assertEqual(result['offset'], '0x20')
            self.assertEqual(path.read_bytes(), bytes(data))
            with self.assertRaises(ValueError):
                pointer.inspect(path, 62, 'data')
            data[4:8] = bytes.fromhex('40 00 00 08')
            path.write_bytes(data)
            with self.assertRaises(ValueError):
                pointer.inspect(path, 4, 'data')

    def test_instruction_entry_must_fit_file(self):
        with self.assertRaises(ValueError):
            pointer.decode(0x0800003F, 'thumb', size=63)
        with self.assertRaises(ValueError):
            pointer.decode(0x0800003C, 'arm', size=63)

if __name__ == '__main__':
    unittest.main()
