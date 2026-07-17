from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CutguardRepositoryTests(unittest.TestCase):
    def test_lock_precedes_reduction(self):
        text = (ROOT / "rules/canonical.md").read_text(encoding="utf-8").lower()
        self.assertLess(text.index("risk classification happens before reduction"), text.index("the eight-stage method"))
        self.assertIn("a locked guard cannot be removed", text)

    def test_agent_skills_follow_directory_names(self):
        for name in ("cutguard", "cutguard-review"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"\nname: {name}\n", text)
            self.assertIn("\ndescription:", text)

    def test_core_methodology_is_present_across_distributions(self):
        expected = {
            "AGENTS.md": ("classify risk before minimizing", "guards required to protect it are locked"),
            "skills/cutguard/SKILL.md": ("classify risk before minimizing", "required guards are locked"),
            "skills/cutguard-review/SKILL.md": ("classify each touched area", "guards that must be locked"),
        }
        for rel, phrases in expected.items():
            text = (ROOT / rel).read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase, text)

    def test_low_risk_is_proportionate(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Do not turn a CSS edit into an application-security audit", text)

    def test_verified_asvs_mapping(self):
        text = (ROOT / "docs/security-model.md").read_text(encoding="utf-8")
        for item in (
            "v5.0.0-1.2.4", "v5.0.0-2.2.2", "v5.0.0-8.2.2",
            "v5.0.0-8.3.1", "v5.0.0-13.3.1", "v5.0.0-15.3.1",
        ):
            self.assertIn(item, text)
        self.assertNotIn("v5.0.0-14.1.1` | RLS", text)

    def test_adapters_are_exactly_generated(self):
        result = subprocess.run([sys.executable, "scripts/build_adapters.py", "--check"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)
        self.assertFalse((ROOT / "adapters/opencode").exists())
        self.assertFalse((ROOT / "adapters/codex").exists())

    def test_cursor_rule_frontmatter_is_first(self):
        text = (ROOT / "adapters/cursor/.cursor/rules/cutguard.mdc").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("\nalwaysApply: true\n", text.split("---", 2)[1])

    def test_skill_installer(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "scripts/install_skills.py", "--target", "agents", "--project", directory],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0)
            for name in ("cutguard", "cutguard-review"):
                path = Path(directory) / ".agents/skills" / name / "SKILL.md"
                self.assertTrue(path.is_file())

    def test_scenarios_are_specific(self):
        dirs = sorted(p for p in (ROOT / "benchmarks/scenarios").iterdir() if p.is_dir())
        self.assertEqual(len(dirs), 12)
        prompts = [(directory / "prompt.md").read_text(encoding="utf-8") for directory in dirs]
        self.assertEqual(len(prompts), len(set(prompts)))
        self.assertTrue(any("CSS" in prompt or "portfolio" in prompt for prompt in prompts))
        self.assertTrue(any("Supabase" in prompt for prompt in prompts))
        self.assertTrue(any("permanently deletes" in prompt for prompt in prompts))

    def test_benchmark_validator_accepts_no_results(self):
        result = subprocess.run([sys.executable, "scripts/validate_benchmark_results.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_release_version_must_match_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "scripts/package_release.py", "--version", "0.2.0", "--out", directory],
                cwd=ROOT,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)

    def test_release_is_reproducible_and_clean(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            subprocess.run([sys.executable, "scripts/package_release.py", "--out", a], cwd=ROOT, check=True, capture_output=True)
            subprocess.run([sys.executable, "scripts/package_release.py", "--out", b], cwd=ROOT, check=True, capture_output=True)
            one = Path(a, "cutguard-v0.1.0.zip").read_bytes()
            two = Path(b, "cutguard-v0.1.0.zip").read_bytes()
            self.assertEqual(hashlib.sha256(one).digest(), hashlib.sha256(two).digest())
            with zipfile.ZipFile(Path(a, "cutguard-v0.1.0.zip")) as zf:
                names = zf.namelist()
                self.assertTrue(names)
                self.assertTrue(all(name.startswith("cutguard/") for name in names))
                self.assertFalse(any("/.env" in name or "/.git/" in name for name in names))


if __name__ == "__main__":
    unittest.main()
