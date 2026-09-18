"""Manifest/entrypoint contracts and real offline installer behavior, without ROMs.

Routing fixtures are documented examples; these tests do not invoke a model or
prove Codex UI discovery, auto-selection, hardware accuracy or game compatibility.
"""
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
NEW = {
    'emulator-regression-tester', 'cpu-isa-differential-analyzer',
    'timing-interrupt-dma-analyzer', 'git-bisect-regression-debugger',
    'nds-homebrew-build-validator', 'graphics-vram-pipeline-debugger',
    'save-nvram-state-validator', 'cartridge-mapper-peripheral-analyzer',
    'sgb-host-debugger', 'gb-link-nifi-debugger', 'arm7-arm946-jit-analyzer',
    'v30mz-cpu-analyzer', 'wonderswan-hardware-analyzer',
}
SECTIONS = ['Purpose', 'When to Use', 'When Not to Use', 'Inputs', 'Workflow',
            'Evidence Requirements', 'Verification', 'Output', 'Guardrails']

def hashes(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts
            and p.suffix != '.pyc'}

class EmulatorSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'skills-lock.json').read_text(encoding='utf-8'))
        cls.by_name = {s['name']: s for s in cls.manifest['skills']}

    def invoke(self, destination, *arguments, root=ROOT):
        return subprocess.run([sys.executable, str(root / 'install.py'), '--offline',
                               '--dest', str(destination), *arguments],
                              capture_output=True, text=True, encoding='utf-8')

    def test_inventory_and_bundled_contract(self):
        baseline = json.loads((ROOT / 'tests/fixtures/pre-emulator-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(set(self.by_name) - {s['name'] for s in baseline['skills']}, NEW)
        self.assertEqual(len(NEW), 13)
        self.assertEqual(self.manifest['schema_version'], 2)
        self.assertEqual(self.manifest['checked_at'], '2026-09-17')
        for name in NEW:
            with self.subTest(name=name):
                item = self.by_name[name]
                self.assertEqual(item['requested_name'], name)
                self.assertEqual(item['source'], 'bundled')
                self.assertEqual(item['path'], 'skills/' + name)
                self.assertEqual(item['status'], 'custom')
                self.assertEqual(item['version'], '1.0.0')
                self.assertFalse(item.get('requires'))
                self.assertTrue((ROOT / item['path'] / 'SKILL.md').is_file())

    def test_existing_entries_pins_and_retirement_unchanged(self):
        baseline = json.loads((ROOT / 'tests/fixtures/pre-emulator-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(baseline['skills']), 15)
        for item in baseline['skills']:
            self.assertEqual(self.by_name[item['name']], item)
        self.assertEqual(self.manifest['retired_skills'], baseline['retired_skills'])
        self.assertEqual(self.manifest['unresolved'], baseline['unresolved'])

    def test_unique_names_and_aliases(self):
        skills = self.manifest['skills']
        names = [s['name'] for s in skills]
        aliases = [s['requested_name'] for s in skills]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(aliases), len(set(aliases)))
        for item in skills:
            if item['name'] != item['requested_name']:
                self.assertNotIn(item['requested_name'], names)
        self.assertFalse(set(names) & {s['name'] for s in self.manifest['retired_skills']})

    def test_valid_acyclic_dependencies(self):
        done = set()
        active = set()
        def visit(name):
            self.assertIn(name, self.by_name)
            self.assertNotIn(name, active, 'dependency cycle')
            if name in done:
                return
            active.add(name)
            for dependency in self.by_name[name].get('requires', []):
                visit(dependency)
            active.remove(name)
            done.add(name)
        for name in self.by_name:
            visit(name)

    def test_entrypoint_frontmatter_and_required_structure(self):
        for name in NEW:
            with self.subTest(name=name):
                text = (ROOT / self.by_name[name]['path'] / 'SKILL.md').read_text(encoding='utf-8')
                parts = text.split('---', 2)
                self.assertEqual(parts[0], '')
                fields = dict(line.split(':', 1) for line in parts[1].strip().splitlines())
                self.assertEqual(set(fields), {'name', 'description'})
                self.assertEqual(fields['name'].strip(), name)
                # JSON-quoted single-line strings are valid YAML scalars, including colons.
                description = json.loads(fields['description'].strip())
                self.assertIsInstance(description, str)
                self.assertTrue(description)
                self.assertLess(len(description), 1024)
                self.assertEqual(re.findall(r'^## (.+)$', parts[2], re.M), SECTIONS)
                self.assertRegex(parts[2], r'(?m)^1\. .+')
                self.assertNotRegex(text, r'(?i)\bTODO\b|\bTBD\b|\[INSERT|<placeholder>')

    def test_evidence_and_asset_guardrails(self):
        # Semantic concepts, not exact sentences. quick_validate separately checks YAML.
        for name in NEW:
            with self.subTest(name=name):
                text = (ROOT / self.by_name[name]['path'] / 'SKILL.md').read_text(encoding='utf-8').lower()
                guard = text.split('## guardrails', 1)[1]
                self.assertRegex(guard, r'(do not|never|prohibit).{0,50}(redistribut|distribut)')
                self.assertIn('copyrighted rom', guard)
                self.assertRegex(guard, r'rom.{0,30}read-only|read-only.{0,30}rom')
                self.assertRegex(guard, r'never claim.{0,60}fixed.{0,60}(test|verif)')
                for concept in ('source evidence', 'baseline', 'candidate', 'first divergence',
                                'minimal', 'unrelated', 'pc', 'reference emulator',
                                'real hardware', 'unsupported'):
                    self.assertIn(concept, guard)

    def test_all_bundles_install_without_upstream_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            checkout = folder / 'checkout'
            checkout.mkdir()
            shutil.copy2(ROOT / 'install.py', checkout / 'install.py')
            bundles = [s for s in self.manifest['skills'] if s.get('source') == 'bundled']
            isolated = {**self.manifest, 'skills': bundles, 'retired_skills': []}
            (checkout / 'skills-lock.json').write_text(json.dumps(isolated), encoding='utf-8')
            for item in bundles:
                shutil.copytree(ROOT / item['path'], checkout / item['path'],
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            destination = folder / 'installed'
            result = self.invoke(destination, root=checkout)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((checkout / '.cache').exists())
            self.assertFalse((checkout / 'vendor').exists())
            self.assertEqual({p.name for p in destination.iterdir()}, {s['name'] for s in bundles})
            for item in bundles:
                self.assertEqual(hashes(destination / item['name']), hashes(ROOT / item['path']))
            again = self.invoke(destination, root=checkout)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(again.stdout.count('CURRENT:'), len(bundles))
            self.assertFalse((folder / 'skill-backups').exists())

    def test_each_new_skill_selects_only_itself_offline(self):
        for name in sorted(NEW):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                destination = Path(temporary) / 'installed'
                unrelated = destination / 'user-owned'
                unrelated.mkdir(parents=True)
                (unrelated / 'notes.txt').write_text('keep', encoding='utf-8')
                result = self.invoke(destination, '--skill', name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual({p.name for p in destination.iterdir()}, {name, 'user-owned'})
                self.assertEqual(hashes(destination / name), hashes(ROOT / self.by_name[name]['path']))
                self.assertEqual((unrelated / 'notes.txt').read_text(), 'keep')

    def test_list_reports_every_new_entry(self):
        result = subprocess.run([sys.executable, str(ROOT / 'install.py'), '--list'],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        listed = {line.split(':', 1)[0] for line in result.stdout.splitlines() if ': ' in line}
        self.assertTrue(NEW <= listed)
        for name in NEW:
            self.assertIn(f'{name}: {name} [custom] skills/{name}', result.stdout)

    def test_readme_count_and_categories_match_manifest(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertEqual(int(re.search(r'\*\*(\d+)개 스킬\*\*', text)[1]), len(self.by_name))
        section = text.split('## 현재 설치되는 스킬')[1].split('## 설치')[0]
        for name in self.by_name:
            self.assertIn('`' + name + '`', section)
        for category in ['계획·요구사항', '품질·분석', '지식 관리', '역공학·한글화',
                         '에뮬레이터 공통 개발', 'GameYob', 'GBARunner3', 'NitroSwan']:
            self.assertIn('| ' + category + ' |', section)

    def test_documented_routing_examples_reference_valid_skills(self):
        examples = json.loads((ROOT / 'tests/fixtures/emulator-routing.json').read_text(encoding='utf-8'))
        self.assertEqual({e['project'] for e in examples}, {'GameYob', 'GBARunner3', 'NitroSwan'})
        self.assertEqual({e['primary'] for e in examples}, NEW)
        requests = set()
        for case in examples:
            self.assertTrue(case['request'] and case['boundary'])
            self.assertIn(case['primary'], self.by_name)
            for helper in case['supporting']:
                self.assertIn(helper, self.by_name)
                self.assertNotEqual(helper, case['primary'])
            self.assertNotIn((case['project'], case['request']), requests)
            requests.add((case['project'], case['request']))
        for project in ('GameYob', 'GBARunner3', 'NitroSwan'):
            self.assertGreaterEqual(sum(e['project'] == project for e in examples), 7)

    def test_unrecognized_retired_code_review_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'installed'
            owned = destination / 'code-review'
            owned.mkdir(parents=True)
            (owned / 'SKILL.md').write_text('user-owned review', encoding='utf-8')
            result = self.invoke(destination, '--skill', 'code-review')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((owned / 'SKILL.md').read_text(), 'user-owned review')
            self.assertIn('PRESERVED (retired name, unrecognized content): code-review', result.stdout)
            self.assertFalse((Path(temporary) / 'skill-backups').exists())

if __name__ == '__main__':
    unittest.main()
