#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
VERSION = "0.1.0"


def digest() -> str:
    return hashlib.sha256(AGENTS.read_bytes()).hexdigest()[:12]


def marker() -> str:
    return f"<!-- Generated from AGENTS.md; do not edit. cutguard={VERSION}; sha256={digest()} -->\n"


def outputs() -> dict[Path, str]:
    agents = AGENTS.read_text(encoding="utf-8")
    return {
        ROOT / "adapters/claude-code/CLAUDE.md": marker()
        + "@AGENTS.md\n\n## Claude Code\n\n"
        + "Use the imported Cutguard instructions as behavioral context. Install the optional skills from `skills/` into `.claude/skills/` when on-demand commands are preferred. Permissions, sandboxing, and hooks remain separate enforcement controls.\n",
        ROOT / "adapters/gemini-cli/GEMINI.md": marker()
        + "@./AGENTS.md\n\n# Gemini CLI\n\n"
        + "Apply the imported Cutguard instructions. Optional Agent Skills can be installed from `skills/` into `.gemini/skills/` or `.agents/skills/`. Do not treat this context file as an enforcement layer.\n",
        ROOT / "adapters/github-copilot/.github/copilot-instructions.md": marker() + agents,
        ROOT / "adapters/cursor/.cursor/rules/cutguard.mdc": "---\n"
        + "description: Classify risk and lock required security invariants before minimizing code.\n"
        + "alwaysApply: true\n"
        + "---\n\n"
        + marker()
        + agents,
    }


def stale_generated_files(expected: set[Path]) -> list[Path]:
    stale = []
    adapters = ROOT / "adapters"
    if not adapters.exists():
        return stale
    for path in adapters.rglob("*"):
        if not path.is_file() or path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "Generated from AGENTS.md; do not edit." in text and path not in expected:
            stale.append(path)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = outputs()
    bad: list[Path] = []
    for path, content in expected.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                bad.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    stale = stale_generated_files(set(expected))
    if not args.check:
        for path in stale:
            path.unlink()
        stale = []

    if bad or stale:
        print("Adapter drift:")
        for path in bad:
            print(f"- missing or changed: {path}")
        for path in stale:
            print(f"- stale generated file: {path.relative_to(ROOT)}")
        return 1

    print("Adapters match AGENTS.md" if args.check else f"Generated {len(expected)} adapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
