"""v3 packaging/installation contracts; no model or parser behavior is simulated."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/log-analyzer'

def inventory(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}

class LogAnalyzerTests(unittest.TestCase):
    def test_v3_manifest_no_runtime_dependency(self):
        manifest = json.loads((ROOT / 'skills-lock.json').read_text(encoding='utf-8'))
        entry = next(s for s in manifest['skills'] if s['name'] == 'log-analyzer')
        self.assertEqual(entry['version'], '3.0.0')
        self.assertEqual(entry['requested_name'], 'log-analyzer')
        self.assertEqual(entry['path'], 'skills/log-analyzer')
        self.assertEqual(entry['source'], 'bundled')
        self.assertEqual(entry['status'], 'custom')
        self.assertFalse(entry.get('requires'))
        self.assertFalse(entry.get('tool_requirements'))
        self.assertEqual(manifest['checked_at'], '2026-09-19')

    def test_frontmatter_modes_and_major_sections(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        prefix, frontmatter, body = text.split('---', 2)
        self.assertEqual(prefix, '')
        fields = dict(line.split(':', 1) for line in frontmatter.strip().splitlines())
        self.assertEqual(fields['name'].strip(), 'log-analyzer')
        description = json.loads(fields['description'].strip())
        self.assertTrue(description)
        self.assertLess(len(description), 1024)
        for section in ('Purpose', 'When to Use', 'When Not to Use', 'Intake',
                        'Core Workflow', 'Analysis Modes', 'Normalization Rules',
                        'Signature Guidance', 'Emulator-specific Routing',
                        'Evidence Requirements', 'Output', 'Handoffs', 'Guardrails'):
            self.assertIn('## ' + section + '\n', body)
        for mode in ('Incident Triage', 'Error Extraction', 'Pattern Analysis',
                     'Baseline Comparison', 'First Divergence', 'Build/Test Failure',
                     'Multi-run Comparison', 'Session/Timeline Analysis'):
            self.assertIn('### ' + mode + '\n', body)

    def test_references_are_packaged_and_no_unfinished_scaffold(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        refs = re.findall(r'\]\((references/[^)]+)\)', text)
        self.assertEqual(set(refs), {'references/comparison.md', 'references/signatures.md'})
        for ref in refs:
            self.assertTrue((SKILL / ref).is_file())
        for path in SKILL.rglob('*.md'):
            self.assertNotRegex(path.read_text(encoding='utf-8'), r'(?i)\bTODO\b|\bTBD\b|<placeholder>')
        self.assertFalse((SKILL / 'scripts').exists(), 'v3 is deliberately a workflow skill')

    def test_selected_offline_install_without_vendor_or_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            checkout = folder / 'checkout'
            checkout.mkdir()
            shutil.copy2(ROOT / 'install.py', checkout / 'install.py')
            # Keep the full manifest: selection must not attempt any upstream download.
            shutil.copy2(ROOT / 'skills-lock.json', checkout / 'skills-lock.json')
            shutil.copytree(SKILL, checkout / 'skills/log-analyzer')
            dest = folder / 'installed'
            command = [sys.executable, str(checkout / 'install.py'), '--offline',
                       '--skill', 'log-analyzer', '--dest', str(dest)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual({p.name for p in dest.iterdir()}, {'log-analyzer'})
            self.assertEqual(inventory(dest / 'log-analyzer'), inventory(SKILL))
            again = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertIn('CURRENT: log-analyzer', again.stdout)
            self.assertFalse((folder / 'skill-backups').exists())
            self.assertFalse((checkout / '.cache').exists())

    def test_upgrade_backs_up_all_old_files_and_preserves_unrelated_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            dest = folder / 'installed'
            old = dest / 'log-analyzer'
            old.mkdir(parents=True)
            (old / 'SKILL.md').write_text('---\nname: log-analyzer\n---\nPrior local version', encoding='utf-8')
            (old / 'local-notes.txt').write_text('preserve user notes', encoding='utf-8')
            previous = inventory(old)
            other = dest / 'unrelated'
            other.mkdir()
            (other / 'SKILL.md').write_text('keep unchanged', encoding='utf-8')
            unrelated = inventory(other)
            result = subprocess.run([sys.executable, str(ROOT / 'install.py'), '--offline',
                                     '--skill', 'log-analyzer', '--dest', str(dest)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            backups = list((folder / 'skill-backups').glob('*/log-analyzer'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(inventory(backups[0]), previous)
            self.assertEqual(inventory(old), inventory(SKILL))
            self.assertEqual(inventory(other), unrelated)

if __name__ == '__main__':
    unittest.main()
