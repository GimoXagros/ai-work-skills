"""Offline integration checks; run after the pinned sources have been cached."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InstallerTests(unittest.TestCase):
    def invoke(self, destination, *arguments):
        return subprocess.run([sys.executable, str(ROOT / 'install.py'), '--offline',
                               '--dest', str(destination), *arguments],
                              capture_output=True, text=True)

    def test_clean_install_and_repeat_all_skills(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.invoke(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((ROOT / 'skills-lock.json').read_text())
            for skill in manifest['skills']:
                self.assertTrue((destination / skill['name'] / 'SKILL.md').is_file())
            again = self.invoke(destination)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(again.stdout.count('CURRENT:'), len(manifest['skills']))
            self.assertFalse((Path(temporary) / 'skill-backups').exists())

    def test_existing_custom_files_are_backed_up(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            old = destination / 'create-plan'
            old.mkdir(parents=True)
            (old / 'SKILL.md').write_text('custom previous skill')
            (old / 'user-notes.txt').write_text('preserve this')
            result = self.invoke(destination, '--skill', 'create-plan')
            self.assertEqual(result.returncode, 0, result.stderr)
            backups = list((Path(temporary) / 'skill-backups').glob('*/create-plan'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'user-notes.txt').read_text(), 'preserve this')
            self.assertEqual((backups[0] / 'SKILL.md').read_text(), 'custom previous skill')
            self.assertFalse((old / 'user-notes.txt').exists())

    def test_unknown_skill_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.invoke(destination, '--skill', '../unknown')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())

    def test_legacy_name_installs_canonical_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.invoke(destination, '--skill', 'create-retro-game-kr-patch')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / 'create-kr-patch' / 'SKILL.md').is_file())
            self.assertFalse((destination / 'create-retro-game-kr-patch').exists())

if __name__ == '__main__':
    unittest.main()
