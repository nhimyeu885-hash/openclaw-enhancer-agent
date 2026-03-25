#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def main() -> int:
    policy = load_yaml(ROOT / "control/metrics-policy.yaml")
    metrics_rows = load_jsonl(ROOT / policy["metrics_file"])
    review_rows = load_jsonl(ROOT / policy["manual_review_file"])
    review_by_task = {row["task_id"]: row for row in review_rows if "task_id" in row}

    total = len(metrics_rows)
    fallback_count = sum(1 for row in metrics_rows if row.get("fallback_used"))
    total_saved = sum(row.get("token_saved_estimate", 0) for row in metrics_rows)
    sampled = [row for row in metrics_rows if row.get("manual_review_required")]
    reviewed = [review_by_task[row["task_id"]] for row in sampled if row["task_id"] in review_by_task]
    passed = [row for row in reviewed if row.get("completeness_pass") is True]

    summary = {
        "runs": total,
        "avg_token_saved_estimate": 0 if total == 0 else round(total_saved / total, 2),
        "fallback_rate": 0 if total == 0 else round(fallback_count / total, 4),
        "manual_review_required": len(sampled),
        "manual_review_completed": len(reviewed),
        "manual_completeness_pass_rate": "n/a" if not reviewed else round(len(passed) / len(reviewed), 4),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
