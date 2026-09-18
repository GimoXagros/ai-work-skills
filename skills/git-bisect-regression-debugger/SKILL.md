---
name: git-bisect-regression-debugger
description: "Locate the first emulator regression between confirmed good and bad Git revisions using repeatable builds and deterministic or manual tests. Use for commit-level isolation; not unverified endpoint guesses or history rewriting."
---

# git-bisect-regression-debugger

## Purpose

Identify and verify a regression-inducing commit while preserving user work and separating setup failures from bad behavior.

## When to Use

A failure is known to appear between two revisions of GameYob, GBARunner3 or NitroSwan and a repeatable classifier can distinguish it.

## When Not to Use

No endpoint has been reproduced, tests are irreducibly flaky, or the request is to rewrite branch history.

## Inputs

Confirmed good/bad commit IDs; repository state; isolated checkout/worktree permission; revision-compatible build command; asset hash/input script; predicate and platform; handling of unbuildable revisions.

## Workflow

1. Record original branch/HEAD and dirty state. Use an isolated checkout when available; do not stash, reset or discard user changes. Confirm good and bad with the same environment and predicate.
2. Define the classifier before searching: exit 0 means good; 1–127 except 125 mean bad to git bisect run; 125 means skip; other codes abort. Wrap missing commands/setup faults so they cannot be mistaken for a regression.
3. Repeat endpoints if flakiness is possible and set a bounded trial rule. A mixed result is inconclusive; investigate or stop rather than voting until the desired answer appears.
4. Start bisect with confirmed endpoints. Build each selected revision from clean generated outputs in the isolated environment; save commit, artifact, command and classification evidence.
5. Skip only documented untestable revisions. If required hardware or human judgment is unavailable, stop the automatic run and report the pending commit/checkpoint; never label missing evidence good or bad.
6. Inspect bisect log and skipped neighbors. Report an ambiguous suspect set when skips prevent a unique boundary; record merge/path/first-parent restrictions if used rather than silently pruning history.
7. Rebuild the suspect and relevant parent(s), reproduce both outcomes and inspect the responsible diff. Rerun targeted regression tests; git bisect reset restores the isolated checkout to its recorded start.

## Evidence Requirements

Good/bad endpoint traces, classifier contract, bisect log, skip reasons, suspect/parent results and minimal explanatory diff.

## Verification

A suspect is confirmed only after its parent passes and it fails under the same predicate, with merge topology explained. Search completion alone is insufficient. If tools, assets or hardware are unavailable, report BLOCKED or NOT RUN with the missing evidence; do not fabricate a result.

## Output

Confirmed commit or ambiguous set, reproduction/classifier, source diff hypothesis, log and restored checkout state.

## Guardrails

Prefer source evidence over conjecture and compare baseline with candidate at the first divergence. Make only authorized minimal fixes; avoid unrelated cleanup and never claim “fixed” without a confirming test. Label PC emulator tests, reference emulator observations and real hardware tests separately. Do not invent or silently implement unsupported hardware behavior. Do not redistribute copyrighted ROMs or game assets: record ROM hashes only, never include ROM data; preserve user-provided ROM originals read-only, without copying or modifying them.

Use emulator-regression-tester to establish the predicate and nds-homebrew-build-validator for build failures. Reference: https://git-scm.com/docs/git-bisect . Do not force-push or rewrite history. Helpers are conditional and do not grant broader scope or become installation dependencies.
