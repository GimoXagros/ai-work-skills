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
    def test_memory_runtime_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertFalse(setup.local_memory_enabled(home))
            config = home / 'config.toml'
            config.write_text('[plugins."claude-mem@claude-mem-local"]\nenabled = true\n[hooks.state]\nvalue = "unchanged"\n')
            with patch.object(setup.subprocess, 'check_output') as call:
                setup.install_plugin('codex', 'claude-mem', home, {})
                call.assert_not_called()
            self.assertIn('unchanged', config.read_text())
            config.write_text('[plugins."claude-mem@claude-mem-local"]\nenabled = false\n[other]\nenabled = true\n')
            self.assertFalse(setup.local_memory_enabled(home))

    def test_ecc_locked_dependencies_and_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / 'plugins/cache/ai-work-skills/ecc/2.2.3'
            target.mkdir(parents=True)
            (target / 'package-lock.json').write_text('{}')
            result = json.dumps({'installedPath': str(target)})
            with patch.object(setup.subprocess, 'check_output', return_value=result), patch.object(setup.shutil, 'which', return_value='npm'), patch.object(setup, 'run') as run:
                setup.install_plugin('codex', 'ecc', home, {})
                self.assertIn('--ignore-scripts', run.call_args.args[0])
                self.assertIn('--omit=dev', run.call_args.args[0])
                self.assertEqual(run.call_args.kwargs['cwd'], target.resolve())
            with patch.object(setup.subprocess, 'check_output', return_value=json.dumps({'installedPath': str(home)})):
                with self.assertRaisesRegex(ValueError, 'Unexpected ECC'):
                    setup.install_plugin('codex', 'ecc', home, {})

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
