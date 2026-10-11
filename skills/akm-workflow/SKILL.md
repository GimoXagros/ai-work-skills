---
name: akm-workflow
description: Design, operate, migrate, or audit an AKM-style Markdown knowledge system for AI agents. Use when the user mentions DECK6/akm, Agent Knowledge Management, the seven AKM layers, or Learn Back; do not create a knowledge vault for ordinary one-off tasks.
---

# AKM workflow

Adapted for Codex from [DECK6/akm](https://github.com/DECK6/akm/tree/70e99b51b4e6b075dc98aab8754c9ef16f602dfe), MIT, revision `70e99b51b4e6b075dc98aab8754c9ef16f602dfe`. The target AKM checkout is authoritative; this skill supplies routing and operating guidance, not a bundled vault or memory service.

## Establish the target and authority

- Locate the existing knowledge root and map its current structure before writing; never require renamed folders or every AKM layer. For a standard AKM checkout, locate `99-system/ROUTER.md` and `99-system/SCHEMA.md`. Do not create an AKM hierarchy merely because this skill was selected.
- In an existing AKM checkout, read its root instructions or applicable adapter, then `99-system/INDEX.md`, all short pointers in `40-memory/`, and the relevant parts of `ROUTER.md`, `SECURITY.md`, `LOOP.md`, and `VERIFICATION.md` before writing durable material.
- Treat Markdown and original sources as canonical. Runtime indexes, retrieval packets, generated summaries, and adapter state are derived and must never silently outrank their cited source.
- Preserve the user's existing taxonomy, paths, language, and authorization boundaries. A migration or adapter update is not permission to reorganize private notes.

## Scope the workflow

- Existing knowledge spaces start from the requested query, ingestion, correction or maintenance task, not a repeated setup interview. New domains need only the missing domain-specific context. Reuse prior answers; silence is not consent.
- For a new workspace, agree on the useful layers, inbox policy and depth. Omitted layers do not need replacement folders. Record where canonical sources, questions and verification live.
- Distinguish storage layers, ontology (concepts and relation meanings), and explanatory wiki notes. A link is not evidence that a relationship is true.
- This portable adapter does not install the upstream multi-skill suite or its shared runtime. Use only tools actually present in the target checkout.

## Classify before writing

Run new material through the target repository's router. The default AKM meanings are:

| Material | Canonical layer |
|---|---|
| Unmodified external original | `10-sources/` after bounded inbox staging |
| Reusable synthesis true beyond one project | `20-knowledge/` |
| User, organization, project, or domain-specific truth | `30-context/` |
| Short stable pointer required every session | `40-memory/` |
| Repeatable steps with failure points and verification | `50-procedures/` |
| Reproducible run, decision, or handoff worth retaining | `60-actions/` |
| Failure pattern, rubric, audit, or verification result | `70-evaluation/` |
| External deliverable | `80-outputs/` |
| Superseded or deprecated material | `90-archive/` |

Keep long knowledge out of memory and domain facts out of procedures. Store an execution record only when reproduction, verification, recovery, or handoff needs it. Use links instead of duplicating the same body across layers.

## Execute with evidence

1. Load only the memory pointers, procedure, knowledge, and context relevant to the request.
2. Preserve originals and provenance. Separate directly observed facts, interpretations, hypotheses, decisions, and unresolved questions.
3. Treat search or retrieval results as candidates until the cited file or source location is directly read. Connect evidence to named claims when the claim matters.
4. Perform the requested work within its scope. External sending, publication, destructive changes, and secret handling still require their normal authorization.
5. Update `INDEX.md` and add one concise `LOG.md` outcome only when a meaningful durable change was made and the target AKM rules require it.

## Verify by consequence

- Tier 0: low-risk one-off result; check only material facts and tool outcomes.
- Tier 1: durable note; check request fit, schema, provenance, claim support, and discoverability.
- Tier 2: important synthesis or public deliverable; add task-specific criteria and spot-check high-impact claims.
- Tier 3: medical, legal, safety, contract, official, or otherwise consequential work; add a claim ledger and independent second pass.

Report `HOLD` instead of completion when important scope or evidence remains unresolved. Structural lint is useful but does not prove that the work answered the request or that a citation supports a claim.

## Linked knowledge and bounded maintenance

- Reuse stable source, question, concept, relation, assertion and note IDs. Keep evidence kind (`source-supported`, `user-stated`, `llm-proposed`) separate from lifecycle status (`current`, `needs-review`, `disputed`, `deprecated`). Preserve the local schema when it differs.
- Keep immutable originals separate from a mutable source ledger. Record the actual source location, read range and check date; discovery alone is not reading. Synthetic examples and model proposals are not user history.
- When definitions or claims change, update affected notes, examples, question answers and indexes together. Mark remaining affected material `needs-review` in the actual files.
- For delegated maintenance, use the authorized domains, source scope and finite task/time/source budget. Do the authorized edits and re-checks; installation alone does not activate background maintenance. Scheduling and publication require their own user intent.
- Serialize writers to shared canonical state. If the base revision changed, read and integrate it before writing. Keep resumable task IDs and checkpoints; do not repeat a failed task at the same revision without new evidence.
- Verify links/IDs, re-run representative questions, and assess semantic support separately. Record a shared revision as verified only with actual evidence. Budget exhaustion is not completion; report remaining scope explicitly.

## Learn Back

- Record a repeatable failure in `70-evaluation/` first, then fix the responsible layer: stale knowledge in `20-knowledge/`, misunderstood local context in `30-context/`, repeated session mistakes with a short `40-memory/` pointer, or a weak procedure in `50-procedures/`.
- Promote a successful approach to `50-procedures/` only when it is repeatable, has steps, known failure points, and a verification method.
- Keep uncertainty visible. Do not convert a failed attempt into a verified fact or erase it when it may prevent repetition.

## Security and repository updates

- Never store secret values. Record only a secret's name and location when that pointer is genuinely needed.
- Treat private layer content as local. Never force-add ignored layer files, personal conversations, runtime databases, caches, credentials, or generated indexes to Git.
- Update tracked AKM system files and adapters separately from private instance content. Before committing, inspect the staged path list and ensure only intended public system files are included.
- Migrate existing vaults in bounded slices: freeze the mapping, move one representative slice, repair links, lint and reindex, verify, then expand.
- Run only validators present in the target checkout, such as `node scripts/lint.mjs --akm`, `--links`, or `--secrets`, and report each check separately from semantic verification.
