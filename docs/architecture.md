# Repository architecture

`rules/canonical.md` is the complete methodology reference. `AGENTS.md` is the portable always-on instruction file. `skills/cutguard` and `skills/cutguard-review` are self-contained Agent Skills so they remain usable when installed outside this repository.

Host-specific adapters are generated from `AGENTS.md` only when a host benefits from a separate file. Codex, OpenCode, and Devin Desktop/Cascade use the root `AGENTS.md` directly, so duplicate adapter copies are intentionally absent.

Benchmark scenario packets are research inputs, not completed model runs. Raw results live under `benchmarks/results/raw/` and must pass `scripts/validate_benchmark_results.py` before aggregate claims are published.

Executable tooling uses the Python standard library to avoid adding a package manager and dependency supply chain for simple generation, installation, validation, and packaging tasks.
