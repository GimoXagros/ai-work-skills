# v2026.11.24.3

- Pin Claude-Mem 16.1.2 at a046a6a9fd8fb1cc56466194487dca94e8212409.
- Preserved existing local settings and backed up SQLite databases before upgrade. The isolated rehearsal passed SQLite integrity checks and preserved record counts for four core tables.
- After Codex restart, the live 16.1.2 worker returned status ok, initialized true and mcpReady true on port 37742.
- Full hook-event coverage was outside the validation scope.
