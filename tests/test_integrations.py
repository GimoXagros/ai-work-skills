"""Catalog coverage, immutable provenance and archive boundary regression checks."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import hashlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import setup_integrations as setup


class IntegrationTests(unittest.TestCase):
    def test_catalog_and_plugin_pins(self):
        lock = setup.read_lock()
        self.assertEqual(lock['requested_links'], 23)
        self.assertEqual(len(lock['repositories']), 22)
        repos = {r['repo'].lower(): r for r in lock['repositories']}
        self.assertEqual(len(repos), 22)
        for row in repos.values():
            self.assertRegex(row['ref'], r'^[0-9a-f]{40}$')
        market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(len(market['plugins']), 5)
        for plugin in market['plugins']:
            source = plugin['source']
            key = source['url'].removeprefix('https://github.com/').removesuffix('.git').lower()
            self.assertEqual(source['ref'], repos[key]['ref'])

    def test_runtime_package_lock_consistency(self):
        pkg = json.loads((ROOT / 'tools/npm/package.json').read_text())
        lock = json.loads((ROOT / 'tools/npm/package-lock.json').read_text())
        self.assertEqual(pkg['dependencies'], lock['packages']['']['dependencies'])
        for name, version in pkg['dependencies'].items():
            self.assertRegex(version, r'^\d+\.\d+\.\d+$')
            self.assertEqual(lock['packages']['node_modules/' + name]['version'], version)

    def test_checksum_and_archive_traversal_rejected(self):
        raw = io.BytesIO()
        with zipfile.ZipFile(raw, 'w') as archive:
            archive.writestr('../outside.txt', 'outside')
        data = raw.getvalue()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(setup.urllib.request, 'urlopen', return_value=io.BytesIO(data)):
                with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                    setup.unpack_verified('https://example.invalid/test', '0' * 64, Path(tmp) / 'target')
            with patch.object(setup.urllib.request, 'urlopen', return_value=io.BytesIO(data)):
                with self.assertRaisesRegex(ValueError, 'escapes destination'):
                    setup.unpack_verified('https://example.invalid/test', hashlib.sha256(data).hexdigest(), Path(tmp) / 'target')
            self.assertFalse((Path(tmp) / 'outside.txt').exists())

    def test_environment_quotes_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / 'toolchains').mkdir()
            setup.save_environment(home, [home / "person's tools"])
            text = (home / 'toolchains/ai-work-skills-env.ps1').read_text()
            self.assertIn("person''s tools", text)
            self.assertNotIn('SetEnvironmentVariable', text)
