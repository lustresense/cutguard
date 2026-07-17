#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "dist", "__pycache__", ".pytest_cache", ".mypy_cache", ".DS_Store"}
FIXED_TIME = (2026, 7, 16, 0, 0, 0)
SEMVER = re.compile(r"^0\.1\.0$")


def included_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED for part in rel.parts):
            continue
        if path.suffix == ".pyc" or path.name.startswith(".env"):
            continue
        yield path, rel


def verify_archive(archive: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        if not names or any(not name.startswith("cutguard/") for name in names):
            raise RuntimeError("archive must contain exactly one cutguard/ top-level directory")
        forbidden = ("/.env", "/.git/", "__pycache__", ".pyc")
        if any(any(item in name for item in forbidden) for name in names):
            raise RuntimeError("archive contains an excluded file")
        with tempfile.TemporaryDirectory() as directory:
            zf.extractall(directory)
            extracted = Path(directory) / "cutguard"
            if not (extracted / "README.md").is_file() or not (extracted / "AGENTS.md").is_file():
                raise RuntimeError("extracted archive is incomplete")
            result = subprocess.run(
                [sys.executable, "scripts/validate_repo.py"],
                cwd=extracted,
                text=True,
                capture_output=True,
            )
            if result.returncode:
                details = (result.stdout + result.stderr).strip()
                raise RuntimeError(f"extracted archive validation failed:\n{details}")


def build(version: str, out: Path) -> Path:
    if not SEMVER.fullmatch(version):
        raise ValueError("version must match the repository release version 0.1.0")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if f"Version: {version} research preview" not in agents:
        raise ValueError("archive version does not match AGENTS.md")
    out.mkdir(parents=True, exist_ok=True)
    archive = out / f"cutguard-v{version}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in included_files():
            info = zipfile.ZipInfo(str(Path("cutguard") / rel), FIXED_TIME)
            mode = 0o755 if path.suffix == ".py" else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            zf.writestr(info, path.read_bytes())
    verify_archive(archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (out / f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"{archive}\nSHA256 {digest}")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--out", default="dist")
    args = parser.parse_args()
    build(args.version, Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
