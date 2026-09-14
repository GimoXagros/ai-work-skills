---
name: create-plan
description: Create a grounded, tool-aware execution plan for coding work when the user explicitly asks for a plan. Return the plan without editing unless the user also requests implementation.
metadata:
  short-description: Create a grounded execution plan
---

# Create plan

Create an actionable plan from the user's real goal, the current workspace, and the capabilities actually available. A plan is a decision aid and execution contract, not a substitute for inspecting the project or permission for extra work.

## Ground the plan

1. Identify the requested outcome, constraints, target environment, and what must remain unchanged.
2. Inspect only the repository instructions, architecture, relevant files, and current state needed to avoid invented paths or steps. Stay read-only when the user requested only a plan.
3. Note applicable skills, tools, tests, deployment mechanisms, and external dependencies only when they materially affect the route. Do not dump every available tool into the plan or assume a tool is installed.
4. Distinguish confirmed facts from assumptions. Ask a concise question only when different answers would materially change the plan; otherwise state the assumption.
5. Select the smallest planning depth that makes the work executable:
   - Quick change: 3–5 ordered steps.
   - Multi-file implementation: 6–10 ordered steps with validation and rollback considerations.
   - Long-running or risky work: phases with checkpoints, acceptance evidence, recovery points, and explicit decision gates.

## Write executable steps

- Lead with the intended outcome and high-level approach.
- Use verb-first steps in dependency order. Name likely files, modules, interfaces, migrations, or commands only when confirmed or clearly labeled as candidates.
- Include data flow, compatibility, edge cases, and failure handling where they affect design.
- Tie validation to observable behavior: tests, builds, rendered output, command results, migration checks, or rollout signals. Do not use “verify it works” as an unqualified step.
- Call out destructive, externally visible, security-sensitive, or irreversible actions as separate gates. A plan never grants authorization to perform them.
- Keep unknowns visible. Do not manufacture detail to make the plan look complete.

## Output shape

Use only the sections that add value; do not force empty headings.

```markdown
# Plan

<Outcome and approach in 1–3 sentences.>

## Assumptions
- <Only material assumptions or constraints.>

## Steps
1. <Concrete ordered action and affected area.>
2. <Concrete ordered action and affected area.>

## Validation
- <Observable acceptance check.>

## Risks or decisions
- <Only unresolved choices or meaningful failure/rollback concerns.>
```

For a very small task, a short numbered list is preferable to a ceremonial document. For a long-running task, include phase completion criteria so another agent or session can resume without re-planning from scratch.

## Plan and implementation requests

If the user asks only for a plan, stop after delivering it. If the user asks to plan and implement, use the plan as a live guide rather than a frozen script: begin with the highest-confidence dependency, update later steps when direct evidence invalidates an assumption, and report material deviations with their reason. Do not repeatedly rewrite the plan when the route has not changed.

When the project already uses AKM, a one-off plan is normally an action artifact rather than a procedure. Preserve it only when reproduction or handoff needs it; promote it to a reusable procedure only after repeated success, known failure points, and a verification method exist.
