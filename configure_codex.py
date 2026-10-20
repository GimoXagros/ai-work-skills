"""Opt-in local Codex skill budget and Chrome MCP setup; preserves user approvals."""
import datetime
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time

from setup_integrations import read_lock, run


def set_skill_budget(codex):
    """Use Codex's config writer instead of rewriting unrelated TOML settings."""
    with subprocess.Popen([codex, 'app-server', '--stdio'], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, text=True, encoding='utf-8') as proc:
        replies = queue.Queue()

        def read():
            for line in proc.stdout:
                try:
                    replies.put(json.loads(line))
                except ValueError:
                    continue
            replies.put(None)

        threading.Thread(target=read, daemon=True).start()

        def call(identifier, method, params):
            proc.stdin.write(json.dumps({'id': identifier, 'method': method, 'params': params}) + '\n')
            proc.stdin.flush()
            deadline = time.monotonic() + 30
            while True:
                reply = replies.get(timeout=max(0, deadline - time.monotonic()))
                if reply is None:
                    raise RuntimeError('Codex app-server closed before replying')
                if reply.get('id') == identifier:
                    if 'error' in reply:
                        raise RuntimeError(str(reply['error']))
                    return reply['result']

        try:
            call(1, 'initialize', {'clientInfo': {'name': 'ai-work-skills', 'version': '1.0'}})
            proc.stdin.write('{"method":"initialized"}\n')
            proc.stdin.flush()
            call(2, 'config/value/write', {'keyPath': 'skills.max_context_tokens',
                                         'value': 10000, 'mergeStrategy': 'upsert'})
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()


def configure(home, codex):
    lock = read_lock()
    toolchains = home / 'toolchains'
    node = toolchains / ('node-v' + lock['bootstrap']['node']['version'] + '-win-x64/node.exe')
    entry = toolchains / 'ai-work-skills-npm/node_modules/chrome-devtools-mcp/build/src/bin/chrome-devtools-mcp.js'
    for path in (node, entry):
        if not path.is_file():
            raise FileNotFoundError('Run setup_integrations.py --install first: ' + str(path))
    backup = home / 'integration-backups' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ-codex')
    backup.mkdir(parents=True)
    config = home / 'config.toml'
    if config.exists():
        shutil.copy2(config, backup / 'config.toml')
    print('Config backup:', backup)
    set_skill_budget(codex)
    run([codex, 'mcp', 'add', 'chrome-devtools', '--env', 'CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1',
         '--', node, entry, '--headless', '--isolated', '--no-usage-statistics', '--no-performance-crux'])
    print('Configured skill catalog budget 10000 and Chrome MCP. Restart Codex.')
    print('Tool approval and hook trust remain user decisions. See docs/BROWSER_SETUP.md.')


if __name__ == '__main__':
    codex = shutil.which('codex')
    if not codex:
        raise SystemExit('Codex CLI must be installed and available on PATH.')
    configure(Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).resolve(), codex)
