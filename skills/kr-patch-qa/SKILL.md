---
name: kr-patch-qa
description: Apply static-first QA to Korean retro-game patches, including text and glyph coverage, binary layout, RC readback, freeze regressions and release evidence. Use for 한글화 QA, 한글 패치 검수, RC 검증 or 배포 전 QA. Emulator execution is optional and must be reported separately.
---

# Korean patch QA

Use the pinned [upstream skill](https://github.com/gagnonjung/kr-patch-qa/blob/cab74ca62c817e1b4626644d99f254b59796e80d/skills/kr-patch-qa/SKILL.md) and [QA standard](https://github.com/gagnonjung/kr-patch-qa/blob/cab74ca62c817e1b4626644d99f254b59796e80d/LOCALIZATION_QA_STANDARD.md) as the source for detailed QA requirements. Read the relevant standard sections through web tools or a local checkout at this exact revision before applying them. If the source is unavailable, report that limitation and do not claim complete upstream-standard conformance. This independently written entrypoint keeps the upstream's repository-root document outside the local skill installation; it does not redistribute the unlicensed upstream documents.

Identify the source image, candidate image, build revision, last known good baseline and declared translation population. Record hashes and distinguish unique text, physical occurrences and excluded consumers.

Inspect source text, controls, renderer budgets and glyph mappings first, then changed binary spans, pointer consumers, archive sizes and final-image readback. Capture the actual evidence and missing coverage for each check. Preserve ambiguous naturalness and speaker findings for review rather than applying blind replacements.

Report SOURCE_QA, STATIC_BINARY_QA, RC_BUILD, RC_READBACK_QA and RUNTIME_SMOKE independently. Without executing the exact candidate, runtime remains NOT RUN. Runtime-required promotion or release needs observations on that candidate, including cold-boot versus save-state provenance. Use available emucap tools for these observations when requested; they are not a dependency for static QA.

Use create-kr-patch for investigation and patch implementation when available. This skill evaluates evidence and QA status; do not rebuild or publish a game merely because a QA report was requested.
