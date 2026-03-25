#!/usr/bin/env python3
from pathlib import Path
import sys


REQUIRED_FILES = [
    "README.md",
    "control/enhancer-policy.yaml",
    "control/change-governance.yaml",
    "control/acceptance-checklist.yaml",
    "control/channel-routing.yaml",
    "control/enhancer-output-schema.yaml",
    "control/l0-worker.yaml",
    "control/gray-rollout.yaml",
    "control/metrics-policy.yaml",
    "prompts/agents/homebase.md",
    "prompts/agents/openclaw-enhancer.md",
    "prompts/agents/openclaw-core-config.md",
    "prompts/agents/dna-caster.md",
    "prompts/agents/coach.md",
    "docs/openclaw-enhancer-design.md",
    "docs/openclaw-enhancer-compare.md",
    "docs/openclaw-agent-maintainer-skill.md",
    "docs/l0-enhancer-mvp.md",
    "examples/task-before-after.md",
    "examples/summary-sample.md",
    "examples/l0-hotfix-log.md",
    "examples/fallback-sample.md",
    "examples/runtime-post-input.json",
    "examples/runtime-fallback-input.json",
    "examples/manual-review-template.csv",
    "result/system/changelog.md",
    "scripts/l0_enhancer_worker.py",
    "scripts/summarize_enhancer_metrics.py",
    "scripts/record_manual_review.py",
    "scripts/test_l0_enhancer_worker.py",
    "skills/openclaw-agent-maintainer/SKILL.md",
    "skills/openclaw-agent-maintainer/agents/openai.yaml",
]

REQUIRED_POLICY_KEYS = [
    "optimization_stage:",
    "fidelity_priority:",
    "token_budget_mode:",
    "dedupe_policy:",
    "summary_mode:",
    "safe_l0_autofix:",
]

REQUIRED_MVP_KEYS = [
    "risk_scope:",
    "low_risk_actions:",
    "allowed_channels:",
    "metrics_file:",
]

REQUIRED_OUTPUT_FIELDS = [
    "run_mode:",
    "optimization_actions:",
    "fallback_used:",
    "token_saving_estimate:",
    "ux_risk:",
]


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    if missing:
        print("[FAIL] Missing required files:")
        for item in missing:
            print(f"  - {item}")
        return 1

    policy_text = (root / "control/enhancer-policy.yaml").read_text(encoding="utf-8")
    for key in REQUIRED_POLICY_KEYS:
        if key not in policy_text:
            return fail(f"Missing policy key: {key}")

    mvp_text = "\n".join(
        (root / path).read_text(encoding="utf-8")
        for path in [
            "control/l0-worker.yaml",
            "control/gray-rollout.yaml",
            "control/metrics-policy.yaml",
        ]
    )
    for key in REQUIRED_MVP_KEYS:
        if key not in mvp_text:
            return fail(f"Missing MVP control key: {key}")

    output_text = (root / "control/enhancer-output-schema.yaml").read_text(encoding="utf-8")
    for field in REQUIRED_OUTPUT_FIELDS:
        if field not in output_text:
            return fail(f"Missing output schema field: {field}")

    homebase_text = (root / "prompts/agents/homebase.md").read_text(encoding="utf-8")
    enhancer_text = (root / "prompts/agents/openclaw-enhancer.md").read_text(encoding="utf-8")
    if "openclaw-enhancer" not in homebase_text:
        return fail("homebase prompt does not reference openclaw-enhancer")
    if "passthrough" not in enhancer_text or "fallback" not in enhancer_text:
        return fail("enhancer prompt does not define all run modes")

    changelog_text = (root / "result/system/changelog.md").read_text(encoding="utf-8")
    if "变更等级" not in changelog_text or "审查结论" not in changelog_text:
        return fail("changelog template is incomplete")

    print("[OK] OpenClaw enhancer workspace is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
