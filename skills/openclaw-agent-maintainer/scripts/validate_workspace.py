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
    "prompts/agents/homebase.md",
    "prompts/agents/openclaw-enhancer.md",
    "prompts/agents/openclaw-core-config.md",
    "prompts/agents/dna-caster.md",
    "prompts/agents/coach.md",
    "docs/openclaw-enhancer-design.md",
    "docs/openclaw-enhancer-compare.md",
    "docs/openclaw-agent-maintainer-skill.md",
    "examples/task-before-after.md",
    "examples/summary-sample.md",
    "examples/l0-hotfix-log.md",
    "examples/fallback-sample.md",
    "result/system/changelog.md",
]

REQUIRED_POLICY_KEYS = [
    "optimization_stage:",
    "fidelity_priority:",
    "token_budget_mode:",
    "dedupe_policy:",
    "summary_mode:",
    "safe_l0_autofix:",
]


def check_text_contains(path: Path, snippets: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [snippet for snippet in snippets if snippet not in text]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_workspace.py <workspace-path>")
        return 1

    root = Path(sys.argv[1]).resolve()
    missing = [item for item in REQUIRED_FILES if not (root / item).exists()]
    if missing:
        print("[FAIL] Missing files:")
        for item in missing:
            print(f"  - {item}")
        return 1

    policy_missing = check_text_contains(root / "control/enhancer-policy.yaml", REQUIRED_POLICY_KEYS)
    if policy_missing:
        print("[FAIL] Missing policy keys:")
        for item in policy_missing:
            print(f"  - {item}")
        return 1

    homebase_text = (root / "prompts/agents/homebase.md").read_text(encoding="utf-8")
    enhancer_text = (root / "prompts/agents/openclaw-enhancer.md").read_text(encoding="utf-8")
    changelog_text = (root / "result/system/changelog.md").read_text(encoding="utf-8")

    failures = []
    if "openclaw-enhancer" not in homebase_text:
        failures.append("homebase prompt is not wired to openclaw-enhancer")
    if "passthrough" not in enhancer_text or "fallback" not in enhancer_text:
        failures.append("enhancer prompt does not define all run modes")
    if "变更等级" not in changelog_text or "审查结论" not in changelog_text:
        failures.append("changelog template is incomplete")

    if failures:
        print("[FAIL] Contract violations:")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("[OK] Workspace contract looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
