# Workspace Contract

## Required files

The target OpenClaw enhancer workspace should contain:

- `README.md`
- `control/enhancer-policy.yaml`
- `control/change-governance.yaml`
- `control/acceptance-checklist.yaml`
- `control/channel-routing.yaml`
- `control/enhancer-output-schema.yaml`
- `control/l0-worker.yaml`
- `control/gray-rollout.yaml`
- `control/metrics-policy.yaml`
- `prompts/agents/homebase.md`
- `prompts/agents/openclaw-enhancer.md`
- `prompts/agents/openclaw-core-config.md`
- `prompts/agents/dna-caster.md`
- `prompts/agents/coach.md`
- `docs/openclaw-enhancer-design.md`
- `docs/openclaw-enhancer-compare.md`
- `docs/openclaw-agent-maintainer-skill.md`
- `docs/l0-enhancer-mvp.md`
- `examples/task-before-after.md`
- `examples/summary-sample.md`
- `examples/l0-hotfix-log.md`
- `examples/fallback-sample.md`
- `examples/runtime-post-input.json`
- `examples/runtime-fallback-input.json`
- `examples/manual-review-template.csv`
- `result/system/changelog.md`

## Invariants

- Keep `#homebase` as the human entrypoint.
- Keep `openclaw-enhancer` as a backend layer, not a new entrypoint.
- Keep `DNA -> coach -> result/` intact.
- Keep the control YAML files as the source of truth for policy and governance.
- Keep the L0 worker limited to low-risk transformations such as dedupe, structure, and brief report.
- Keep changelog entries for every accepted system-level update.

## Output contract

Every enhancer run should expose:
- `run_mode`
- `optimization_actions`
- `fallback_used`
- `token_saving_estimate`
- `ux_risk`

Every structured result should still preserve:
- task goal
- key conclusions
- key actions
- risk/status
