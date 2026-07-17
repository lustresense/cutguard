# Benchmark result record

Store one JSON object per run in `benchmarks/results/raw/*.json`.

Required top-level fields:

```json
{
  "scenario": "S03-premium-api-proxy",
  "arm": "cutguard",
  "run": 1,
  "model": "model-and-version",
  "agent": "agent-and-version",
  "repository": "owner/name",
  "repository_commit": "full-commit-sha",
  "started_at": "2026-07-16T00:00:00Z",
  "ended_at": "2026-07-16T00:10:00Z",
  "exit_status": "completed",
  "metrics": {
    "added_loc": 0,
    "removed_loc": 0,
    "changed_files": 0,
    "dependencies_added": 0,
    "tests_passed": 0,
    "tests_failed": 0,
    "tokens": null,
    "cost_usd": null,
    "elapsed_seconds": 0
  },
  "invariant_results": [
    {"id": "authz-owner", "status": "pass", "evidence": "path:line or test"}
  ],
  "artifacts": {
    "prompt": "relative/path",
    "diff": "relative/path",
    "command_log": "relative/path"
  },
  "notes": ""
}
```

Allowed `arm` values: `baseline`, `reduction-only`, `security-only`, `cutguard`.

Allowed invariant statuses: `pass`, `fail`, `not-run`, `not-applicable`.

A result is publishable only when evidence paths exist in the released raw artifact set or the note explains why an artifact cannot be distributed.
