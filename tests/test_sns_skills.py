"""Instagram package closure and executable smoke checks; no account access."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'ig-audit', 'ig-caption', 'ig-carousel', 'ig-comment', 'ig-dm',
         'ig-human', 'ig-plan', 'ig-profile', 'ig-reel', 'ig-reply',
         'ig-repurpose', 'ig-story', 'ig-viral'}


class SnsSkillsTests(unittest.TestCase):
    def test_catalog_and_dependency_closure(self):
        skills = json.loads((ROOT / 'skills-lock.json').read_text(encoding='utf-8'))['skills']
        by_name = {s['name']: s for s in skills}
        self.assertEqual({name for name in by_name if name.startswith('ig-')}, NAMES)
        for name in NAMES:
            entry = by_name[name]
            folder = ROOT / entry['path']
            self.assertTrue((folder / 'UPSTREAM_LICENSE').is_file())
            self.assertTrue((folder / 'assets/voice.md').is_file())
            text = (folder / 'SKILL.md').read_text(encoding='utf-8')
            self.assertNotIn('~/.claude/', text)
            for dependency in entry.get('requires', []):
                self.assertIn(dependency, by_name)
            if '$ig-human' in text:
                self.assertIn('ig-human', entry.get('requires', []))

    def test_all_bundled_python_entrypoints_run(self):
        scripts = [p for name in NAMES for p in (ROOT / 'skills' / name).glob('*.py')]
        self.assertEqual(len(scripts), 6)
        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run([sys.executable, '-X', 'utf8', str(script), '--help'],
                                        cwd=ROOT.parent, capture_output=True,
                                        text=True, encoding='utf-8', timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
