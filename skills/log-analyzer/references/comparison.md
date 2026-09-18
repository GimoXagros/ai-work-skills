# Reproducible comparison protocol

Use this when good and failing logs are available. It is an analysis procedure, not a shipped parser or a guarantee of automatic first-divergence detection.

## Record model and coverage

Retain `(file, physical line range/record index, run, session, attempt, raw time, clock domain, component, event, fields, redacted message)` where the input supports it; absent fields stay unknown. A multiline traceback is one meaningful record with its original line range. CSV quoted newlines and JSONL parse failures need explicit handling. State encoding and decode-error locations before comparison. Missing final newline is not by itself proof of truncation; missing closing structure/expected completion plus capture evidence may indicate a partial tail.

No helper is bundled because no common project log schema or repeated fixed parser workload was established. Use available read/search tools or a task-local read-only parser for a confirmed format. For large inputs, inspect bounded windows/stream records rather than copying all logs into context; state any sampling and do not claim a global first difference from a sample.

## Ordered alignment

1. Check comparable workload, logging level, inputs, platform and completion. First establish within-run order; concurrency may allow multiple valid interleavings.
2. Declare normalization rules with stable IDs and order. Apply equally; preserve raw values and original line mapping. Review a before/after sample for semantic loss, especially addresses, cycle counts and failure codes.
3. Partition by meaningful session/attempt/phase. Find the earliest common anchor supported by operation identity, not merely a repeated generic message or matching timestamp. Different start times do not justify aligning unrelated operations.
4. Compare ordered events and their significant fields. At a mismatch, inspect bounded lookahead to distinguish insertion, deletion, changed value and reordering. Verify the next anchor using neighboring events/IDs; repeated identical anchors can make alignment ambiguous.
5. Keep the insertion/deletion as a difference even if streams later resynchronize. Do not use unordered membership, aggressive fuzzy matching or sequence matching heuristics as proof of equivalence. For repeated blocks, report an interval until an independent sequence/operation marker disambiguates it.
6. Find the earliest supported divergence within the verified coverage. Absence needs both coverage and expected-event evidence. A capture ending early yields an unresolved missing suffix, not automatically a crash. Keep first observed failure separate from first difference and downstream causal hypotheses.
7. Extract adjustable meaningful-record context around the boundary, retaining full multiline events and both anchors; show physical source locations. Recheck the finding against raw redacted records to detect normalization mistakes.

## Synthetic worked example (not a project log format)

Baseline records: line 1 `phase=boot ready`; line 2 `phase=copy channel=3 state=start`; line 3 `phase=copy channel=3 state=done`; line 4 `phase=frame present`.
Candidate records: line 1 `phase=boot ready`; line 2 `phase=copy channel=3 state=start`; line 3 `phase=copy channel=3 state=timeout`; line 4 `phase=frame error`.

After confirming matching operation/inputs, the first observable divergence is line 3 in both files (done versus timeout). Candidate line 4 is a later difference; a dependency trace is needed to attribute it to the timeout. An error-pattern search finding only line 4 would miss the boundary. If candidate instead inserts `phase=diagnostic note` before completion, record that insertion and resynchronize at completion; do not call it a semantic failure without further evidence.

## Clock and repeated-run checks

Keep original time and any derived offset separately. Known UTC offsets permit conversion; unknown timezone does not. Synchronization anchors must identify the same event and justify error bounds. If uncertainty intervals overlap, event order is unresolved. Never synthesize a one-second spacing to repair a reset clock. Timestamp-free logs retain file/operation order in separate lanes, not an invented global timeline.

Compare both timing fields and event values when timing matters; suppressing wall-clock starts must not suppress elapsed-duration regressions. Run matrices record each actual outcome, absent data and exposure: e.g. baseline timeout 0/3 versus candidate 1/3 is observed intermittency, not deterministic regression. Matched patterns without comparable workload or captured outcomes cannot establish a pass rate.
