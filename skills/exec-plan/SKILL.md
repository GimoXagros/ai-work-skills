---
name: exec-plan
description: Create, maintain, and optionally execute a durable multi-phase plan for complex coding work. Use for long-running tasks, handoffs, migrations, or work that needs checkpoints; use Codex built-in /plan for ordinary short plans.
metadata:
  short-description: Maintain a durable execution plan
---

# Exec Plan

Create a self-contained execution plan that another agent or later session can follow without reconstructing the project history. This is an original ai-work-skills implementation based on the current Codex execution-plan pattern; it is not copied from an OpenAI-distributed skill.

## Choose the right planning surface

- Use Codex built-in `/plan` for a short, disposable implementation plan.
- Use this skill when work spans multiple phases or sessions, has consequential migrations or rollout gates, needs explicit handoff state, or must retain decisions and discoveries during execution.
- If the user asks only for a plan, remain read-only and deliver the plan. Execute only when the user also requests implementation.
- A plan records authorized work; it does not grant permission for destructive, externally visible, privileged, or security-sensitive actions beyond the user's request.

## Ground the plan

1. State the outcome, scope, constraints, acceptance evidence, and what must remain unchanged.
2. Inspect the repository instructions, architecture, relevant files, current branch or working state, and available tools needed to avoid invented paths or commands.
3. Separate confirmed facts from assumptions and unknowns. Resolve only questions that materially change the route.
4. Break the work into dependency-ordered phases with observable completion criteria, validation, failure handling, and recovery points.
5. Name files, interfaces, commands, owners, or environments only when confirmed or clearly marked as candidates.

## Durable plan format

Use the user's requested path. Otherwise, propose `EXEC_PLAN.md` in the project only when a durable file is appropriate and file creation is authorized.

```markdown
# <Outcome>

## Purpose and scope
<Goal, boundaries, non-goals, and user-visible result.>

## Current state
- Confirmed facts:
- Assumptions:
- Unknowns:

## Phases
1. <Phase, affected areas, dependencies, and completion evidence.>

## Validation and acceptance
- <Tests, builds, behavior, migration checks, rollout signals, or review evidence.>

## Risks and recovery
- <Failure condition, stop point, rollback or recovery path.>

## Progress
- [ ] <Next executable milestone.>

## Decisions and discoveries
- <Date or phase>: <Decision or evidence that changes later work.>

## Outcome
<Completed result, remaining work, and handoff state.>
```

Omit empty sections for a modest task. For complex work, keep enough context to resume safely but link to canonical specifications and evidence instead of duplicating them into the plan.

## Maintain while executing

- Work from the highest-confidence unblocked milestone. After each meaningful checkpoint, update progress and record only decisions or discoveries that change later work.
- When direct evidence invalidates an assumption, revise affected future phases and explain the change. Do not rewrite settled history or repeatedly restate unchanged steps.
- Keep command output, large diffs, source documents, and secrets out of the plan. Link to stable evidence or record a concise result.
- Mark blocked work with the exact missing authority, decision, dependency, or evidence. Never mark a phase complete from effort alone.
- Finish with observable acceptance results, unresolved risks, and a concrete resume point.

## AKM interoperability

In an AKM project, a task-specific Exec Plan normally belongs in `60-actions/` when reproduction or handoff requires it. A repeatable method moves to `50-procedures/` only after it has known failure points and a verification method. Record recurring plan or execution failures in `70-evaluation/` and correct the responsible procedure instead of adding permanent detail to `40-memory/`.
