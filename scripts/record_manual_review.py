#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def parse_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("pass must be true/false")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a manual completeness review event.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--pass", dest="did_pass", required=True, type=parse_bool)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    policy = load_yaml(ROOT / "control/metrics-policy.yaml")
    review_path = ROOT / policy["manual_review_file"]
    append_jsonl(
        review_path,
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": args.task_id,
            "reviewer": args.reviewer,
            "completeness_pass": args.did_pass,
            "notes": args.notes,
        },
    )
    print(f"[OK] recorded manual review for {args.task_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
