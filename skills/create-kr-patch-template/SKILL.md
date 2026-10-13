---
name: create-kr-patch-template
description: Set up or adapt a reproducible Korean retro-game patch project using mcpads/create-kr-patch-template. Use when starting a patch project or organizing supported inputs, adopted specifications, translations, build ownership and verification. Preserve existing project structure when adapting a mature project.
---

# Korean patch project template

Read the pinned [template README](https://github.com/mcpads/create-kr-patch-template/blob/c0e930286ccba37e6b83b9405a06e0b0ea4e6293/README.md) and [project guidelines](https://github.com/mcpads/create-kr-patch-template/blob/c0e930286ccba37e6b83b9405a06e0b0ea4e6293/AGENTS.md). Fetch or clone this revision into a separate staging directory when actual template files are needed; preserve the upstream LICENSE with copied files. This skill is an independently written router, not a complete game patcher or a Rust installation.

Establish the target game/platform, supported source hashes, intended translation scope and current build entrypoint. For a new project, adapt the template to those facts. For an existing project, map its actual locations to template roles instead of overwriting existing AGENTS.md, assets or build configuration.

Keep current status, product decisions, adopted specifications, research evidence, translation inputs and font sources identifiable. Read the upstream config and translation guidelines when implementing those contracts. Keep copyrighted game inputs and private runtime evidence out of public source control.

Connect the declared source and adopted inputs to one reproducible build. Require source identity checks, Expected Write or equivalent byte ownership, original-byte guards, span/overlap/protected-region checks and output readback. Calculate changing counts from current inputs. Separate translation progress from approval of the exact release inputs.

The optional reference/conformance and reference/rust folders demonstrate write guards; select them only when relevant to the chosen implementation. Copy reference/ as a complete licensed unit if used. Do not introduce Rust or a new layout solely to follow an example.

Deliver the actual project changes, build instructions, current verification evidence and remaining conditions. Use create-kr-patch for game investigation and kr-patch-qa for QA when available; template creation alone does not prove a playable patch.
