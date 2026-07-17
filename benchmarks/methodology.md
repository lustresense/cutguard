# Preliminary benchmark methodology

Status: design and validation tooling only. No Cutguard result is published.

## Arms

1. Baseline agent with project instructions only
2. Reduction-only instruction
3. Security-only instruction
4. Cutguard unified instruction

## Isolation

Pin the model, agent version, repository commit, tool permissions, effort settings, task prompt, and available dependencies. Load exactly one experimental instruction arm. Record every startup hook, rule, skill, memory file, and instruction source so the baseline is not contaminated.

Use at least four independent runs per task and arm. Preserve raw prompts, transcripts where licensing permits, diffs, command logs, test output, token or cost data, and environment metadata.

## Metrics

- task correctness and target test pass rate;
- locked-invariant and negative-path pass rate;
- added and removed LOC;
- changed files;
- dependencies added;
- duplicated logic and unnecessary architecture;
- false-positive controls on low-risk work;
- review burden using a blinded rubric;
- tokens, cost, and elapsed time when available.

LOC is not the primary success metric. A smaller solution fails when it drops a required guard. A secure solution also loses points when it adds controls unrelated to the threat model.

## Scoring discipline

Define scenario invariants before running models. Blind reviewers to the arm when practical. Publish per-task raw data and disagreements, not only aggregate percentages. Treat safety results as a floor for the tested tasks, never proof of general security.

Each raw run is stored as one JSON file under `results/raw/` and must conform to [`result-record.md`](result-record.md). Validate records with:

```bash
python scripts/validate_benchmark_results.py
```
