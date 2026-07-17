#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md",
    "CHANGELOG.md", "THIRD_PARTY_NOTICES.md", ".gitignore",
    "rules/canonical.md", "skills/cutguard/SKILL.md",
    "skills/cutguard-review/SKILL.md", "docs/architecture.md",
    "docs/security-model.md", "docs/using-cutguard.md",
    "docs/adapter-support.md", "docs/references.md",
    "benchmarks/methodology.md", "benchmarks/result-record.md",
    "benchmarks/scenarios/README.md", "benchmarks/results/README.md",
    "scripts/build_adapters.py", "scripts/install_skills.py",
    "scripts/validate_benchmark_results.py", "scripts/package_release.py",
    "tests/test_repository.py", ".github/workflows/ci.yml",
]
FORBIDDEN_CLAIMS = [
    r"\b100% secure\b", r"\bimpenetrable\b", r"\bunhackable\b",
    r"\bASVS[- ]compliant\b", r"\bASVS[- ]certified\b",
    r"\bSSDF[- ]certified\b", r"\bproduction[- ]ready\b",
]
SECRET_PATTERNS = [
    r"sk_live_[A-Za-z0-9]{16,}", r"sk-[A-Za-z0-9_-]{20,}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
]
SKILL_NAME = re.compile(r"^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", re.M)
DESCRIPTION = re.compile(r"^description:\s*(.+)$", re.M)


def allowed_context(line: str) -> bool:
    low = line.lower()
    return any(x in low for x in ("do not claim", "does not claim", "not a claim", "not production", "without", "forbidden", "never claim"))


def markdown_links(text: str):
    return re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    canonical = (ROOT / "rules/canonical.md").read_text(encoding="utf-8")
    top = canonical[:3000].lower()
    if "risk classification happens before reduction" not in top:
        errors.append("locking precedence is not near the top of canonical.md")
    if "guards required to protect that boundary become locked" not in top:
        errors.append("guard lock is not near the top of canonical.md")
    for phrase in ("what concrete threat", "which trust boundary", "smallest adequate control", "how will it be verified"):
        if phrase not in canonical.lower():
            errors.append(f"canonical four-question gate missing: {phrase}")

    semantic_rules = {
        "AGENTS.md": ("classify risk before minimizing", "guards required to protect it are locked", "do not turn a css edit"),
        "skills/cutguard/SKILL.md": ("classify risk before minimizing", "required guards are locked", "do not turn low-risk styling work"),
        "skills/cutguard-review/SKILL.md": ("classify each touched area", "guards that must be locked", "security theater"),
    }
    for rel, phrases in semantic_rules.items():
        text = (ROOT / rel).read_text(encoding="utf-8").lower()
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"core methodology drift in {rel}: missing '{phrase}'")

    version_files = {
        "AGENTS.md": "Version: 0.1.0 research preview",
        "rules/canonical.md": "Version 0.1.0",
        "skills/cutguard/SKILL.md": 'version: "0.1.0"',
        "skills/cutguard-review/SKILL.md": 'version: "0.1.0"',
        "CHANGELOG.md": "## 0.1.0",
    }
    for rel, marker in version_files.items():
        if marker not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"version drift in {rel}: expected {marker}")

    for skill_dir in (ROOT / "skills").iterdir():
        if not skill_dir.is_dir():
            continue
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing SKILL.md: {skill_dir.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"skill frontmatter is not first: {path.relative_to(ROOT)}")
            continue
        match = SKILL_NAME.search(text.split("---", 2)[1])
        if not match or match.group(1) != skill_dir.name:
            errors.append(f"skill name must match directory: {path.relative_to(ROOT)}")
        if not DESCRIPTION.search(text.split("---", 2)[1]):
            errors.append(f"skill description missing: {path.relative_to(ROOT)}")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_CLAIMS:
            for line in text.splitlines():
                if re.search(pattern, line, re.I) and not allowed_context(line):
                    errors.append(f"unsupported claim in {path.relative_to(ROOT)}: {line.strip()}")
        for link in markdown_links(text):
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = link.split("#", 1)[0]
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"broken relative link in {path.relative_to(ROOT)}: {link}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "dist"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            for line in text.splitlines():
                if re.search(pattern, line) and "EXAMPLE" not in line and "pattern" not in line.lower():
                    errors.append(f"possible credential in {path.relative_to(ROOT)}")

    scenario_dirs = sorted(p for p in (ROOT / "benchmarks/scenarios").iterdir() if p.is_dir())
    if len(scenario_dirs) != 12:
        errors.append(f"expected 12 benchmark scenarios, found {len(scenario_dirs)}")
    prompts: list[str] = []
    for directory in scenario_dirs:
        for name in ("prompt.md", "invariants.md", "negative_tests.md"):
            path = directory / name
            if not path.is_file() or path.stat().st_size < 180:
                errors.append(f"incomplete scenario file: {path.relative_to(ROOT)}")
        if (directory / "prompt.md").exists():
            prompts.append((directory / "prompt.md").read_text(encoding="utf-8"))
    if len(prompts) != len(set(prompts)):
        errors.append("duplicate benchmark prompts")

    cursor_rule = ROOT / "adapters/cursor/.cursor/rules/cutguard.mdc"
    if cursor_rule.is_file():
        cursor_text = cursor_rule.read_text(encoding="utf-8")
        if not cursor_text.startswith("---\n"):
            errors.append("Cursor rule frontmatter must be the first content in cutguard.mdc")
        if "\nalwaysApply: true\n" not in cursor_text.split("---", 2)[1]:
            errors.append("Cursor rule frontmatter is missing alwaysApply: true")

    for obsolete in (
        "skills/core", "skills/review", "adapters/opencode", "adapters/codex",
        "adapters/windsurf", "adapters/github-copilot-chat",
    ):
        if (ROOT / obsolete).exists():
            errors.append(f"obsolete path remains: {obsolete}")

    commands = [
        [sys.executable, str(ROOT / "scripts/build_adapters.py"), "--check"],
        [sys.executable, str(ROOT / "scripts/validate_benchmark_results.py")],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            errors.append(f"command failed: {' '.join(command)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
