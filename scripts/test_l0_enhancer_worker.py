#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "scripts/l0_enhancer_worker.py"


def run_case(input_name: str) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        output_path = temp_root / "output.json"
        metrics_path = temp_root / "metrics.jsonl"
        subprocess.run(
            [
                sys.executable,
                str(WORKER),
                "--input",
                str(ROOT / "examples" / input_name),
                "--output",
                str(output_path),
                "--metrics-file",
                str(metrics_path),
            ],
            check=True,
        )
        return json.loads(output_path.read_text(encoding="utf-8"))


def main() -> int:
    optimized = run_case("runtime-post-input.json")
    fallback = run_case("runtime-fallback-input.json")

    assert optimized["run_mode"] == "optimize", "post input should optimize"
    assert "高风险越狱补丁缺口" in optimized["optimized_text"], "must_keep phrase should survive optimization"
    assert fallback["run_mode"] == "fallback", "verbatim input should fallback"
    assert fallback["fallback_used"] is True, "fallback_used should be true"
    print("[OK] L0 enhancer worker tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
