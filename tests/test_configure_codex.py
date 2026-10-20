import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import configure_codex as config


class ConfigureTests(unittest.TestCase):
    def test_rpc_writes_only_budget_and_closes_process(self):
        proc = MagicMock()
        proc.__enter__.return_value = proc
        proc.stdout = io.StringIO('{"id":1,"result":{}}\n{"id":2,"result":{}}\n')
        proc.stdin = io.StringIO()
        with patch.object(config.subprocess, 'Popen', return_value=proc):
            config.set_skill_budget('codex')
        calls = [json.loads(line) for line in proc.stdin.getvalue().splitlines()]
        self.assertEqual(calls[-1]['params'], {
            'keyPath': 'skills.max_context_tokens', 'value': 10000, 'mergeStrategy': 'upsert'})
        proc.terminate.assert_called_once()

    def test_rpc_error_is_not_reported_as_success(self):
        proc = MagicMock()
        proc.__enter__.return_value = proc
        proc.stdout = io.StringIO('{"id":1,"error":{"message":"unsupported"}}\n')
        proc.stdin = io.StringIO()
        with patch.object(config.subprocess, 'Popen', return_value=proc):
            with self.assertRaisesRegex(RuntimeError, 'unsupported'):
                config.set_skill_budget('codex')
        proc.terminate.assert_called_once()

    def test_missing_install_does_not_touch_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / 'config.toml'
            target.write_text('[hooks.state]\nkeep = "trusted"\n')
            with patch.object(config, 'set_skill_budget') as write:
                with self.assertRaises(FileNotFoundError):
                    config.configure(home, 'codex')
                write.assert_not_called()
            self.assertEqual(target.read_text(), '[hooks.state]\nkeep = "trusted"\n')

    def test_backup_and_absolute_launcher_without_approval_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            version = config.read_lock()['bootstrap']['node']['version']
            node = home / f'toolchains/node-v{version}-win-x64/node.exe'
            entry = home / 'toolchains/ai-work-skills-npm/node_modules/chrome-devtools-mcp/build/src/bin/chrome-devtools-mcp.js'
            for path in (node, entry):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            original = '[hooks.state]\nkeep = "trusted"\n'
            (home / 'config.toml').write_text(original)
            with patch.object(config, 'set_skill_budget'), patch.object(config, 'run') as run:
                config.configure(home, 'codex')
            backups = list((home / 'integration-backups').glob('*/config.toml'))
            self.assertEqual(backups[0].read_text(), original)
            command = run.call_args.args[0]
            self.assertIn(node, command)
            self.assertIn(entry, command)
            self.assertNotIn('--dangerously-bypass-hook-trust', command)
            self.assertNotIn('--ask-for-approval', command)
