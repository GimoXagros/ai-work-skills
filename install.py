#!/usr/bin/env python3
"""Install pinned upstream skills, preserving existing versions in backups."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def inventory(folder):
    if folder.is_symlink():
        raise ValueError(f"Refusing linked skill directory: {folder}")
    result = {}
    for file in sorted(folder.rglob('*')):
        if '__pycache__' in file.relative_to(folder).parts or file.suffix == '.pyc':
            continue
        if file.is_symlink():
            raise ValueError(f"Refusing linked file: {file}")
        if file.is_file():
            result[file.relative_to(folder).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
    return result

def validate(skill):
    if not re.fullmatch(r'[a-z0-9-]+', skill['name']):
        raise ValueError('Invalid skill name')
    if skill.get('source') == 'bundled':
        if skill['path'] != 'skills/' + skill['name']:
            raise ValueError('Invalid bundled skill path')
        return
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', skill['repo']):
        raise ValueError('Invalid GitHub repository')
    if not re.fullmatch(r'[a-f0-9]{40}', skill['ref']):
        raise ValueError('A full immutable commit SHA is required')
    if any(p in ('', '.', '..') for p in skill['path'].split('/')) or '\\' in skill['path']:
        raise ValueError('Invalid source path')

def installed_plugin_matches(skill):
    # Codex plugin cache is managed by Codex, not by this installer.
    codex_root = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    for marker in (codex_root / 'plugins' / 'cache').glob('*/*/*/.codex-marketplace-install.json'):
        try:
            data = json.loads(marker.read_text(encoding='utf-8-sig'))
            source = str(data.get('source', '')).removesuffix('.git')
            target = marker.parent / skill['path'] / 'SKILL.md'
            if source == 'https://github.com/' + skill['repo'] and data.get('revision') == skill['ref'] and target.is_file():
                return target
        except (OSError, ValueError):
            continue
    return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, help='Default: $CODEX_HOME/skills or ~/.codex/skills')
    parser.add_argument('--skill', action='append', help='Install only this name; repeatable')
    parser.add_argument('--offline', action='store_true', help='Use already downloaded .cache content')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'skills-lock.json').read_text(encoding='utf-8'))
    skills = manifest['skills']
    if args.skill:
        known = {s['name'] for s in skills} | {s['requested_name'] for s in skills}
        unknown = set(args.skill) - known
        if unknown:
            parser.error('Unknown or unresolved skills: ' + ', '.join(sorted(unknown)))
        skills = [s for s in skills if s['name'] in args.skill or s['requested_name'] in args.skill]
    if args.list:
        for s in skills:
            origin = s['path'] if s.get('source') == 'bundled' else f"{s['repo']}@{s['ref'][:12]}"
            print(f"{s['requested_name']}: {s['name']} [{s['status']}] {origin}")
        print('Unresolved: ' + ', '.join(manifest['unresolved']))
        return
    dest = args.dest or Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'skills'
    dest = dest.expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    if dest == ROOT or dest in ROOT.parents or ROOT in dest.parents:
        raise ValueError('Installation destination must be outside this repository')
    failed = []
    for skill in skills:
        name = skill['name']
        try:
            validate(skill)
            bundled = skill.get('source') == 'bundled'
            plugin = installed_plugin_matches(skill) if args.dest is None and not bundled else None
            if plugin:
                print(f'CURRENT (plugin): {name} -> {plugin}')
                continue
            cached = ROOT / skill['path'] if bundled else ROOT / '.cache' / skill['ref'] / name
            if not (cached / 'SKILL.md').is_file():
                if bundled:
                    raise ValueError('Bundled skill is missing from this checkout')
                if args.offline:
                    raise ValueError('Pinned source is not cached')
                cached.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run([
                    sys.executable, str(ROOT / 'vendor' / 'skill-installer' / 'install-skill-from-github.py'),
                    '--repo', skill['repo'], '--path', skill['path'], '--ref', skill['ref'],
                    '--dest', str(cached.parent), '--name', name,
                ], check=True)
            text = (cached / 'SKILL.md').read_text(encoding='utf-8-sig')
            if not text.startswith('---') or not re.search(r'^name:\s*[\"\']?' + re.escape(name) + r'[\"\']?\s*$', text, re.M):
                raise ValueError('Skill frontmatter/name validation failed')
            source_hashes = inventory(cached)
            target = dest / name
            if target.is_symlink() or (hasattr(target, 'is_junction') and target.is_junction()):
                raise ValueError('Refusing to replace an existing link or junction')
            if target.exists() and inventory(target) == source_hashes:
                print(f'CURRENT: {name}')
                continue
            with tempfile.TemporaryDirectory(prefix='.skill-stage-', dir=dest.parent) as temporary:
                stage = Path(temporary) / name
                shutil.copytree(cached, stage, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                if inventory(stage) != source_hashes:
                    raise ValueError('Staging verification failed')
                backup = None
                if target.exists():
                    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                    backup = dest.parent / 'skill-backups' / stamp / name
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    target.rename(backup)
                try:
                    stage.rename(target)
                    if inventory(target) != source_hashes:
                        raise ValueError('Installed file verification failed')
                except Exception:
                    if backup and not target.exists():
                        backup.rename(target)
                    raise
            print(f'INSTALLED: {name}' + (f' (previous version: {backup})' if backup else ''))
        except Exception as exc:
            failed.append(name)
            print(f'FAILED: {name}: {exc}', file=sys.stderr)
    print('Unresolved source names (not installed): ' + ', '.join(manifest['unresolved']))
    print('Skills are available on the next Codex turn; reopen a task if discovery has not refreshed.')
    if failed:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
