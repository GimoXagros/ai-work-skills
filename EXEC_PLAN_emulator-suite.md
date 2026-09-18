# Emulator development suite

## Purpose and scope
Add thirteen evidence-led emulator development skills to ai-work-skills, preserve the existing fifteen entries, installer safety and retired policies, validate, install locally and push a feature branch.
Emulator project sources, ROMs, .system, plugin cache, authentication and global settings are outside mutation scope.

## Current state
Started on clean main at 06badc7e4b6f6f7f1f2bfde4ec0c23b2ae8a8efc, equal to origin/main after fetch. Existing baseline: 31 tests passed on 2026-09-18.
Requested manifest/release version date is 2026-09-17; actual execution date is 2026-09-18.

## Phases and progress
- [x] Audit repository, current skill roles and read-only project integration paths.
- [x] Create isolated feature branch and record baseline inventory locally in ignored .cache.
- [x] Write thirteen independent custom skill entrypoints and extend schema 2 manifest.
- [x] Add preservation, offline selection, structure and routing-example checks.
- [x] Update inventory, audit and release documentation.
- [x] Run validators and full suite; inspect all thirteen entrypoints.
- [x] Install on this PC and verify new hashes plus preservation of old skills/protected directories.
- [x] Review all entrypoints and diff; seal acceptance evidence for feature-branch commit/push.

## Validation and acceptance
Baseline manifest fixture must equal the current original entries and retirement rules. New entries must install offline independently and all bundled entries must install together. Existing whole-manifest install and helper regression checks must pass. README count must equal active manifest count.
Use project evidence and static routing cases to review selection scopes; do not claim that document tests establish live Codex auto-selection or hardware accuracy.

## Risks and recovery
Stop before push on any failing verification. Installer backs up changed targets; existing matching skills should remain CURRENT. Keep temporary/cache data untracked. No forced update, history rewrite or cleanup of user-owned directories.

## Decisions and discoveries
Existing ROM-analysis, text/font and frontend/log skills do not supply emulator subsystem execution contracts. Thirteen roles remain separate; no existing skill is deleted or revised. New entrypoints need no runtime scripts or hard dependencies. Installer and setup_tools need no changes.
GameYob host coverage distinguishes CPU dispatch from semantics and OBJ transfer from final composition. GBARunner3 uses translation/direct execution and host mapping/cache/MPU boundaries. NitroSwan separates ARMV30MZ CPU from Sphinx and cartridge/EEPROM subsystems.

## Outcome
Implementation and local installation verified: 43 tests PASS, thirteen quick_validate checks PASS, old skill and protected-directory inventories preserved. Final evidence is recorded in REVIEW.md. Delivery is gated on this acceptance state; branch HEAD and remote tracking record the subsequent commit/push outcome.

Independent explicit-call forward test: three synthetic SGB, paired NiFi and high-code cases correctly retained missing evidence and avoided fixed/accuracy claims. Added the demonstrated hash-proof boundary to ARM JIT evidence guidance. This is not live UI auto-selection or hardware execution. First extended suite: 43 tests PASS.
