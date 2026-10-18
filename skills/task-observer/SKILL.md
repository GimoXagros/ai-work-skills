---
name: task-observer
description: Review a task for reusable skill improvements when the user asks for workflow observations, a skill retrospective, or improvements based on repeated corrections. Keep observations scoped to that request.
license: CC-BY-4.0
---

# Task observer

Adapted from Eoghan Henn / rebelytics.com, "Task Observer — Continuous Skill Discovery & Improvement", [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), via [iamneilroberts/claude-skills](https://github.com/iamneilroberts/claude-skills/blob/947953f2a0664ac95996a4c7b35794a7cc8fc93a/skills/task-observer/SKILL.md). This Codex adaptation narrows automatic activation and preserves host memory/write permissions.

Review actual task evidence: repeated friction, user corrections, missing capability, a successful repeatable procedure, or a recurring tool limitation. Separate direct observations from interpretations and one-off preferences. Do not infer a new global rule from a single example.

For each useful candidate, record the trigger, observed consequence, affected skill or procedure, smallest proposed change, and a realistic verification scenario. Check whether an existing skill already owns the behavior before proposing another. Do not copy private logs or credentials into public skills.

Deliver observations in the current response by default. Persist a log, edit a skill, schedule a review, or update memory only when the user has authorized that action and the host permits the destination. This skill does not authorize edits to Codex memory, global instructions or plugin caches. An installation request alone does not activate permanent observation or periodic jobs.

When authorized to implement an improvement, use skill-creator guidance, preserve unrelated behavior, and test the affected workflow. Distinguish a proposed change, an applied change and a verified result. Keep the original task moving; do not start an unrelated retrospective during every multi-step task.
