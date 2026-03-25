# Review Checklist

Use this checklist when reviewing the enhancer workspace.

## UX safety

- Does the change keep the existing user entrypoint?
- Does the change avoid adding mandatory new commands or steps?
- Does the change keep the current channel responsibilities understandable?

## Capability safety

- Does the change keep original task capability intact?
- Does the summary logic preserve key conclusions, actions, and blockers?
- Does fallback or passthrough still work when compression is risky?
- Does the L0 worker stay within low-risk scope instead of drifting into business logic edits?

## Governance safety

- Is the change level classified correctly?
- Is a non-`L0` change being wrongly auto-applied?
- Is the changelog updated for accepted system changes?

## Drift signals

- Policy file and prompt file disagree on run modes or hotfix rules
- Examples no longer match the current policy
- Docs describe a user entrypoint that the prompts do not preserve
- Metrics files or manual review loop are defined in docs but missing in runtime scripts
