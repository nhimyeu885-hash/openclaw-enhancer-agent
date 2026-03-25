#!/usr/bin/env python3
from pathlib import Path
import sys


L0_PREFIXES = {
    "control/enhancer-policy.yaml",
    "control/acceptance-checklist.yaml",
    "control/enhancer-output-schema.yaml",
    "prompts/agents/openclaw-enhancer.md",
    "prompts/agents/openclaw-core-config.md",
    "result/system/changelog.md",
    "docs/openclaw-enhancer-design.md",
    "docs/openclaw-enhancer-compare.md",
    "docs/openclaw-agent-maintainer-skill.md",
    "docs/l0-enhancer-mvp.md",
    "examples/task-before-after.md",
    "examples/summary-sample.md",
    "examples/l0-hotfix-log.md",
    "examples/fallback-sample.md",
}

L1_PREFIXES = {
    "control/channel-routing.yaml",
    "control/l0-worker.yaml",
    "control/gray-rollout.yaml",
    "control/metrics-policy.yaml",
    "prompts/agents/homebase.md",
    "prompts/agents/dna-caster.md",
    "prompts/agents/coach.md",
    "scripts/l0_enhancer_worker.py",
    "scripts/summarize_enhancer_metrics.py",
    "scripts/record_manual_review.py",
    "scripts/test_l0_enhancer_worker.py",
}


def normalize(path_text: str) -> str:
    return Path(path_text).as_posix().lstrip("./")


def classify(path_text: str) -> tuple[str, str]:
    normalized = normalize(path_text)
    if normalized in L0_PREFIXES:
        return "L0", "safe hotfix candidate if content does not change user-facing flow"
    if normalized in L1_PREFIXES:
        return "L1", "changes runtime behavior or role boundaries and should go through approval"
    if normalized.startswith("control/") or normalized.startswith("prompts/agents/") or normalized.startswith("scripts/"):
        return "L2", "core control, runtime, or prompt change outside the safe allowlist"
    return "L0", "non-core doc/example update candidate"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: classify_change_scope.py <path> [<path> ...]")
        return 1

    levels = []
    for item in sys.argv[1:]:
        level, reason = classify(item)
        levels.append(level)
        print(f"{normalize(item)} => {level} ({reason})")

    overall = "L0"
    if "L2" in levels:
        overall = "L2"
    elif "L1" in levels:
        overall = "L1"
    print(f"overall => {overall}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
