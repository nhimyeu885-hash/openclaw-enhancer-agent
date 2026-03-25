#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


def normalize_unit(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    lowered = re.sub(r"[。.!！？;；,，:：\\-—]+$", "", lowered)
    return lowered


def split_units(text: str) -> list[str]:
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]
    if len(lines) > 1:
        return lines
    parts = re.split(r"(?<=[。.!！？])\s*", text)
    return [part.strip() for part in parts if part.strip()]


def dedupe_units(units: list[str]) -> list[str]:
    seen = set()
    kept = []
    for unit in units:
        marker = normalize_unit(unit)
        if marker and marker not in seen:
            seen.add(marker)
            kept.append(unit)
    return kept


def compress_text(text: str) -> str:
    return "\n".join(dedupe_units(split_units(text))).strip()


def contains_verbatim_marker(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def build_structured_sections(text: str, max_items: int) -> dict[str, list[str]]:
    sections = {"结论": [], "行动项": [], "风险": [], "状态": []}
    fallback_bucket = []
    for unit in dedupe_units(split_units(text)):
        lowered = unit.lower()
        if any(keyword in lowered for keyword in ["下一步", "行动", "todo", "建议", "action"]):
            sections["行动项"].append(unit)
        elif any(keyword in lowered for keyword in ["风险", "阻塞", "高危", "risk", "block"]):
            sections["风险"].append(unit)
        elif any(keyword in lowered for keyword in ["状态", "进度", "status"]):
            sections["状态"].append(unit)
        elif any(keyword in lowered for keyword in ["结论", "发现", "summary", "结果"]):
            sections["结论"].append(unit)
        else:
            fallback_bucket.append(unit)

    for unit in fallback_bucket:
        if len(sections["结论"]) < max_items:
            sections["结论"].append(unit)
        elif len(sections["状态"]) < max_items:
            sections["状态"].append(unit)

    return {key: values[:max_items] for key, values in sections.items()}


def format_structured_text(sections: dict[str, list[str]]) -> str:
    blocks = []
    for title, items in sections.items():
        if not items:
            continue
        lines = [f"{title}："]
        lines.extend(f"- {item}" for item in items)
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def completeness_ratio(text: str, must_keep: list[str]) -> float:
    if not must_keep:
        return 1.0
    lowered = text.lower()
    hits = sum(1 for item in must_keep if item.lower() in lowered)
    return hits / len(must_keep)


def pick_manual_review(task_id: str, channel: str, sample_rate: float, sample_channels: list[str]) -> bool:
    if channel not in sample_channels or sample_rate <= 0:
        return False
    bucket = int(hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF
    return bucket < sample_rate


def make_report(payload: dict, run_mode: str, sections: dict[str, list[str]], optimized_text: str) -> dict:
    strategy = "保留原始流程" if run_mode != "optimize" else "启用 L0 去重/结构化/短报增强"
    return {
        "任务目标": payload.get("user_goal", ""),
        "路由与增强策略": strategy,
        "关键信息/结论": sections.get("结论", []),
        "行动项": sections.get("行动项", []),
        "风险与状态": sections.get("风险", []) + sections.get("状态", []),
        "优化后文本": optimized_text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the OpenClaw L0 enhancer worker.")
    parser.add_argument("--input", required=True, help="Path to the input JSON envelope.")
    parser.add_argument("--output", help="Optional path to write the output JSON envelope.")
    parser.add_argument("--worker-config", default=str(ROOT / "control/l0-worker.yaml"))
    parser.add_argument("--rollout-config", default=str(ROOT / "control/gray-rollout.yaml"))
    parser.add_argument("--metrics-config", default=str(ROOT / "control/metrics-policy.yaml"))
    parser.add_argument("--metrics-file", help="Override metrics jsonl path.")
    parser.add_argument("--skip-metrics", action="store_true")
    args = parser.parse_args()

    worker_config = load_yaml(Path(args.worker_config))
    rollout_config = load_yaml(Path(args.rollout_config))
    metrics_policy = load_yaml(Path(args.metrics_config))
    payload = load_json(Path(args.input))

    channel = payload.get("channel", "#homebase")
    stage = payload.get("stage", "post_result")
    raw_text = payload.get("raw_text") or payload.get("text") or payload.get("content") or ""
    must_keep = payload.get("must_keep") or []
    require_verbatim = bool(payload.get("require_verbatim"))
    task_id = payload.get("task_id") or f"task-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    pre_config = worker_config.get("pre_dispatch", {})
    post_config = worker_config.get("post_result", {})
    rollout_channels = rollout_config.get("allowed_channels", [])
    rollout_stages = rollout_config.get("allowed_stages", [])

    before_tokens = estimate_tokens(raw_text)
    optimized_text = raw_text
    run_mode = "optimize"
    actions = []
    ux_risk = "low"

    if rollout_config.get("enabled") and (channel not in rollout_channels or stage not in rollout_stages):
        run_mode = "passthrough"
        actions.append("gray-rollout-skip")
    elif require_verbatim or contains_verbatim_marker(raw_text, pre_config.get("verbatim_markers", [])):
        run_mode = "fallback"
        actions.append("verbatim-request-detected")
        ux_risk = "high"
    elif len(raw_text) < pre_config.get("min_chars_for_optimization", 0):
        run_mode = "passthrough"
        actions.append("text-too-short-for-optimization")
    else:
        optimized_text = compress_text(raw_text)
        actions.extend(["dedupe", "compress"])
        if stage == "post_result":
            sections = build_structured_sections(optimized_text, post_config.get("max_section_items", 4))
            optimized_text = format_structured_text(sections)
            actions.extend(["structure", "brief-report"])
        else:
            sections = {"结论": [], "行动项": [], "风险": [], "状态": []}

        if must_keep and completeness_ratio(optimized_text, must_keep) < 1.0:
            run_mode = "fallback"
            optimized_text = raw_text
            actions.append("fallback-preserve-must-keep")
            ux_risk = "high"

    if stage == "post_result":
        sections = build_structured_sections(optimized_text if run_mode == "optimize" else raw_text, post_config.get("max_section_items", 4))
    else:
        sections = {"结论": [], "行动项": [], "风险": [], "状态": []}

    after_tokens = estimate_tokens(optimized_text)
    token_saved = max(0, before_tokens - after_tokens)
    saving_ratio = 0.0 if before_tokens == 0 else token_saved / before_tokens
    completeness = completeness_ratio(optimized_text if run_mode == "optimize" else raw_text, must_keep)
    manual_review_required = pick_manual_review(
        task_id,
        channel,
        metrics_policy.get("manual_review", {}).get("sample_rate", 0.0),
        metrics_policy.get("manual_review", {}).get("sample_channels", []),
    )

    result = {
        "task_id": task_id,
        "stage": stage,
        "channel": channel,
        "run_mode": run_mode,
        "optimization_actions": actions,
        "fallback_used": run_mode == "fallback",
        "token_saving_estimate": f"{token_saved} tokens (~{saving_ratio:.0%})",
        "ux_risk": ux_risk,
        "optimized_text": optimized_text,
        "structured_sections": sections,
        "report": make_report(payload, run_mode, sections, optimized_text),
    }

    if args.output:
        write_json(Path(args.output), result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.skip_metrics:
        metrics_path = ROOT / (args.metrics_file or metrics_policy.get("metrics_file", "result/system/metrics/enhancer-metrics.jsonl"))
        append_jsonl(
            metrics_path,
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "task_id": task_id,
                "channel": channel,
                "stage": stage,
                "run_mode": run_mode,
                "token_before_estimate": before_tokens,
                "token_after_estimate": after_tokens,
                "token_saved_estimate": token_saved,
                "fallback_used": run_mode == "fallback",
                "completeness_proxy_ratio": round(completeness, 4),
                "manual_review_required": manual_review_required,
            },
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
