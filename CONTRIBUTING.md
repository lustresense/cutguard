# Contributing

Methodology changes start in `rules/canonical.md`. Keep `AGENTS.md` concise. Skills must remain self-contained when installed outside this repository. Generated adapters must never be edited by hand.

Before a pull request:

```bash
python scripts/build_adapters.py
python scripts/build_adapters.py --check
python scripts/validate_repo.py
python scripts/validate_benchmark_results.py
python -m unittest discover -s tests
```

A security control must name its threat, boundary, smallest adequate implementation, and verification. A reduction proposal must show that required invariants remain intact. A compatibility claim must link to current primary documentation or be labeled unverified.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
