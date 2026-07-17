#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "benchmarks/results/raw"
ARMS = {"baseline", "reduction-only", "security-only", "cutguard"}
STATUSES = {"pass", "fail", "not-run", "not-applicable"}
TOP_FIELDS = {
    "scenario", "arm", "run", "model", "agent", "repository",
    "repository_commit", "started_at", "ended_at", "exit_status",
    "metrics", "invariant_results", "artifacts", "notes",
}
METRICS = {
    "added_loc", "removed_loc", "changed_files", "dependencies_added",
    "tests_passed", "tests_failed", "tokens", "cost_usd", "elapsed_seconds",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path.name}: invalid JSON: {exc}"]

    missing = TOP_FIELDS - data.keys()
    if missing:
        errors.append(f"{path.name}: missing fields {sorted(missing)}")
    if data.get("arm") not in ARMS:
        errors.append(f"{path.name}: invalid arm {data.get('arm')!r}")
    if not isinstance(data.get("run"), int) or data.get("run", 0) < 1:
        errors.append(f"{path.name}: run must be a positive integer")

    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        errors.append(f"{path.name}: metrics must be an object")
    else:
        missing_metrics = METRICS - metrics.keys()
        if missing_metrics:
            errors.append(f"{path.name}: missing metrics {sorted(missing_metrics)}")

    results = data.get("invariant_results")
    if not isinstance(results, list):
        errors.append(f"{path.name}: invariant_results must be an array")
    else:
        for index, item in enumerate(results):
            if not isinstance(item, dict):
                errors.append(f"{path.name}: invariant result {index} must be an object")
                continue
            if not item.get("id") or item.get("status") not in STATUSES or "evidence" not in item:
                errors.append(f"{path.name}: invalid invariant result {index}")

    return errors


def main() -> int:
    files = sorted(RAW.glob("*.json"))
    if not files:
        print("No raw benchmark result files; no Cutguard benchmark claim is published")
        return 0
    errors = [error for path in files for error in validate(path)]
    if errors:
        print("Benchmark result validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {len(files)} raw benchmark result files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
