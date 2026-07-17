#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
TARGETS = {
    "agents": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "gemini": Path(".gemini/skills"),
    "opencode": Path(".opencode/skills"),
}
SKILLS = ("cutguard", "cutguard-review")


def same_tree(a: Path, b: Path) -> bool:
    if not a.is_dir() or not b.is_dir():
        return False
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    if any(not filecmp.cmp(a / name, b / name, shallow=False) for name in cmp.common_files):
        return False
    return all(same_tree(a / name, b / name) for name in cmp.common_dirs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Cutguard Agent Skills into a project.")
    parser.add_argument("--target", choices=sorted(TARGETS), required=True)
    parser.add_argument("--project", default=".")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    destination = project / TARGETS[args.target]
    operations: list[tuple[Path, Path]] = []

    for name in SKILLS:
        src = SOURCE / name
        dst = destination / name
        if not src.is_dir():
            raise SystemExit(f"Missing source skill: {src}")
        if dst.exists() and same_tree(src, dst):
            print(f"Already current: {dst}")
            continue
        if dst.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite {dst}; use --force after reviewing it")
        operations.append((src, dst))

    for src, dst in operations:
        print(f"Install {src.relative_to(ROOT)} -> {dst}")
        if args.dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print("No changes required" if not operations else "Skill installation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
