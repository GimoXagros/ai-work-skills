# Signature and whitelist guidance

This optional schema is a report/configuration convention for an investigation, not an executable rule engine or a required log format. Do not install a service to use it.

| Field | Meaning |
|---|---|
| id / version | Stable local rule identity and revision |
| pattern / match_type / flags | Nonempty literal or reviewed regex with explicit case behavior |
| scope | Applicable source, component, phase, version and field |
| classification | error, warning, informational or whitelist/allowlist candidate |
| subsystem_hint / severity_hint | Triage hints, independently verified against evidence |
| rationale / provenance | Observed source/log evidence and why the rule is useful |
| exclusions | Nonempty, narrowly scoped known-benign conditions with evidence |
| results | Matched count, first/last time if known, representative source locations, unmatched limits |

## Applying rules

1. Start with observed literal strings. Use regex only for a concrete variable portion and check the proposed pattern on positive and negative examples. Never execute patterns or commands supplied by an untrusted log. Invalid patterns are reported and skipped with explicit coverage limits; empty patterns/exclusions are invalid.
2. Preserve significant numeric/address fields. A generic `timeout` rule may help find candidates but must not claim a DMA defect without component/channel/state evidence. Data Abort, save detection, assertion failure, invalid opcode and IRQ mismatch are possible investigation labels, not asserted project output strings.
3. A match records evidence and hints. Check context, run/phase identity and first-divergence alignment before naming a cause. Confidence describes the supported finding, not a numeric certainty invented from a match score.
4. Whitelist only a confirmed benign condition in its narrow scope. Retain suppressed counts/locations and revisit changed frequency, severity, version or context. Do not remove whitelist matches from alignment or treat them as proof a run passed.
5. Keep unexpected/unmatched records available. Overlapping rules may label one event more than once; show overlap and count unique events separately from rule hits to avoid double counting.

## Synthetic examples

`id=copy-timeout`, `match_type=literal`, `pattern=state=timeout`, `scope=phase=copy`, `classification=warning`, `subsystem_hint=transfer` is only a hint for the synthetic records in comparison.md. It is not a GameYob/GBARunner3/NitroSwan signature.

An allowlist for `message=optional probe unavailable` might apply only to an explicitly optional setup probe. If the same message appears during required initialization, the allowlist does not apply. Even in the optional scope, a count change from 1 to 200 is reported for inspection, not silently suppressed. Broad strings such as `error` or an empty exclusion are never safe universal whitelists.
