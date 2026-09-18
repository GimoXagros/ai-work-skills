"""Offline integration checks; run after the pinned sources have been cached."""
import json
from pathlib import Path
import shutil
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

    def test_list_distinguishes_repository_total_from_selection_without_installing(self):
        manifest = json.loads((ROOT / 'skills-lock.json').read_text(encoding='utf-8'))
        bundled = sum(s.get('source') == 'bundled' for s in manifest['skills'])
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'not-created'
            for selection, active, retired in [([], len(manifest['skills']), len(manifest['retired_skills'])),
                                                (['--skill', 'script-translator-limiter'], 2, 0),
                                                (['--skill', 'create-plan'], 1, 1)]:
                with self.subTest(selection=selection):
                    result = self.invoke(destination, '--list', *selection)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(f"Repository-managed active skills: {len(manifest['skills'])} "
                                  f"(bundled: {bundled}, pinned upstream: {len(manifest['skills']) - bundled})", result.stdout)
                    self.assertIn(f'Selected entries: {active} active, {retired} retired', result.stdout)
                    self.assertFalse(destination.exists())

    def test_existing_custom_files_are_backed_up(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            old = destination / 'exec-plan'
            old.mkdir(parents=True)
            (old / 'SKILL.md').write_text('custom previous skill')
            (old / 'user-notes.txt').write_text('preserve this')
            result = self.invoke(destination, '--skill', 'exec-plan')
            self.assertEqual(result.returncode, 0, result.stderr)
            backups = list((Path(temporary) / 'skill-backups').glob('*/exec-plan'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'user-notes.txt').read_text(), 'preserve this')
            self.assertEqual((backups[0] / 'SKILL.md').read_text(), 'custom previous skill')
            self.assertFalse((old / 'user-notes.txt').exists())

    def test_known_retired_skill_is_backed_up_and_replaced(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            old = destination / 'create-plan'
            shutil.copytree(ROOT / 'retired/create-plan-2.0', old)
            result = self.invoke(destination, '--skill', 'create-plan')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(old.exists())
            self.assertTrue((destination / 'exec-plan/SKILL.md').is_file())
            backups = list((Path(temporary) / 'skill-backups').glob('*/create-plan'))
            self.assertEqual(len(backups), 1)
            self.assertIn('RETIRED: create-plan -> exec-plan', result.stdout)

    def test_unrecognized_retired_skill_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            old = destination / 'create-plan'
            old.mkdir(parents=True)
            (old / 'SKILL.md').write_text('user-owned create-plan')
            result = self.invoke(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(old.is_dir())
            self.assertEqual((old / 'SKILL.md').read_text(), 'user-owned create-plan')
            self.assertIn('PRESERVED (retired name, unrecognized content): create-plan', result.stdout)

    def test_unknown_skill_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.invoke(destination, '--skill', '../unknown')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())

    def test_legacy_name_installs_canonical_skill(self):
        pairs = [('create-retro-game-kr-patch', 'create-kr-patch'),
                 ('binary-parser', 'binary-re'), ('hex-analyzer', 're')]
        for requested, canonical in pairs:
            with self.subTest(requested=requested), tempfile.TemporaryDirectory() as temporary:
                destination = Path(temporary) / 'skills'
                result = self.invoke(destination, '--skill', requested)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((destination / canonical / 'SKILL.md').is_file())
                self.assertFalse((destination / requested).exists())

    def test_translator_installs_and_can_load_its_dependency(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.invoke(destination, '--skill', 'script-translator-limiter')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / 'encoding-mapper' / 'SKILL.md').is_file())
            loaded = subprocess.run([sys.executable, str(destination / 'script-translator-limiter/scripts/check_script.py'), '--help'], capture_output=True)
            self.assertEqual(loaded.returncode, 0, loaded.stderr)

if __name__ == '__main__':
    unittest.main()
