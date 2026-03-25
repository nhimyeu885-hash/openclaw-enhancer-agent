---
name: openclaw-agent-maintainer
description: Audit, optimize, and safely update an OpenClaw enhancer workspace that contains control YAML, agent prompts, docs, examples, and changelog files. Use when Codex needs to maintain the OpenClaw enhancer agent, review drift, validate the workspace contract, classify a proposed change as L0/L1/L2, or prepare a safe hotfix without changing the existing user-facing flow.
---

# OpenClaw Agent Maintainer

## Overview

Maintain the OpenClaw enhancer as a conservative backend layer. Preserve the existing entrypoint, preserve current role boundaries, and prefer `passthrough` or `fallback` whenever an optimization risks making the system harder to use.

## Workflow

### 1. Validate the workspace first

Run `scripts/validate_workspace.py <workspace-path>` before proposing or applying changes.

Expected workspace contract:
- `control/` contains enhancer policy, governance, routing, acceptance, and output schema files
- `prompts/agents/` contains versioned prompts for `homebase`, `openclaw-enhancer`, and supporting agents
- `docs/` and `examples/` explain the current operating model
- `result/system/changelog.md` records every system-level update

Read [workspace-contract.md](references/workspace-contract.md) when you need the full file contract and invariants.

### 2. Review with "hard to use" risk in mind

When auditing or optimizing the enhancer:
- preserve the existing human entrypoint
- preserve the original channel responsibilities
- preserve `DNA -> coach -> result/`
- preserve key conclusions, actions, and status in any summary flow
- treat any UX regression as a blocker unless the user explicitly asks for the tradeoff

Read [review-checklist.md](references/review-checklist.md) when you need a compact review rubric.

### 3. Classify proposed changes before editing

Use this classification:
- `L0`: prompt, config, or cron hotfix that does not alter user-facing flow or core role boundaries
- `L1`: feature or policy enhancement that needs approval
- `L2`: architecture or schema changes that need approval and rollout planning

If a change touches business logic, channel topology, data schema, or core agent responsibilities, do not treat it as `L0`.

Use `scripts/classify_change_scope.py <path> [<path> ...]` for a conservative path-based first pass. Treat its output as a floor, not a license to skip review.

### 4. Apply only safe hotfixes automatically

Auto-apply only when all are true:
- the change is `L0`
- the workspace remains easier or equal to use
- acceptance checks pass or the change is documentation-only
- `result/system/changelog.md` is updated

For any other change, prepare a proposal instead of applying it.

### 5. Record every accepted system change

For `L0` work, add a changelog entry with:
- timestamp
- change level
- target file
- what changed
- why it changed
- review verdict
- acceptance result
- whether fallback or rollback was used

Use `scripts/draft_changelog_entry.py` when you need a clean entry template.

## Quick tasks

### Audit drift

1. Run `scripts/validate_workspace.py <workspace-path>`.
2. Compare current prompts and control files against the workspace contract.
3. Report missing files, missing keys, prompt drift, or examples that no longer match the policy.

### Prepare a safe hotfix

1. Confirm the target is prompt/config/cron only.
2. Confirm the change preserves the existing entrypoint and role boundaries.
3. Apply the edit.
4. Update `result/system/changelog.md`.
5. Report the acceptance status and fallback risk.

### Review a proposed enhancement

1. Classify it as `L0`, `L1`, or `L2`.
2. Call out any risk that would make the system harder to use.
3. If the change is not clearly `L0`, produce a proposal instead of editing files.
