# Cutguard

**Cut code, not corners.**

Cutguard is an open-source reasoning method and Agent Skills package for AI coding agents. It classifies risk and locks the controls required at a trust boundary before the agent starts reducing code, files, dependencies, or architecture.

> Build less. Secure what remains. Prove that it works.

## Why it exists

Coding agents often fail in opposite directions. They overbuild small features, or they produce a compact prototype that exposes credentials, trusts client-side checks, skips object ownership, omits database policies, or leaves paid endpoints open to abuse.

Cutguard resolves that conflict through order:

1. **Understand** the task and the existing system.
2. **Classify risk** before discussing implementation size.
3. **Lock invariants** required at each trust boundary.
4. **Challenge necessity** and remove unnecessary scope.
5. **Reuse before writing** new code or dependencies.
6. **Implement the smallest secure solution.**
7. **Attack negative paths.**
8. **Report evidence and residual risk.**

A feature may be removed or simplified. A required authorization, ownership, validation, secret-isolation, abuse-control, or data-integrity guard may not be removed merely to reduce LOC, files, tokens, or delivery time.

## Use it as project instructions

Codex, OpenCode, and Devin Desktop/Cascade read a root `AGENTS.md` directly. Copy it into the target repository:

```bash
cp AGENTS.md /path/to/project/AGENTS.md
```

Host-specific instruction adapters are provided only where a separate file is useful:

```bash
python scripts/build_adapters.py
python scripts/build_adapters.py --check
```

## Use it as Agent Skills

The reusable skills follow the Agent Skills specification:

- `skills/cutguard` for implementation and refactoring;
- `skills/cutguard-review` for diff and pull-request review.

Install them safely with the standard-library installer:

```bash
# Claude Code project skills
python scripts/install_skills.py --target claude --project /path/to/project

# Gemini CLI project skills
python scripts/install_skills.py --target gemini --project /path/to/project

# OpenCode project skills
python scripts/install_skills.py --target opencode --project /path/to/project

# Generic .agents/skills location used by compatible clients
python scripts/install_skills.py --target agents --project /path/to/project
```

The installer refuses to overwrite an existing skill unless `--force` is supplied.

## Risk-scaled behavior

A typography adjustment should remain a localized change with a proportionate build or visual check. It should not trigger a full application-security review.

A route that reads user-owned data must authenticate, enforce data-specific authorization or ownership, validate untrusted identifiers, limit returned fields, and test unauthenticated and cross-user access. It should reuse existing auth and database helpers instead of creating a new security framework.

## Examples

- [`examples/client-env-exposure`](examples/client-env-exposure/README.md): move paid-provider credentials out of browser-delivered code.
- [`examples/premium-api-proxy`](examples/premium-api-proxy/README.md): keep a paid upstream small, bounded, authenticated, and failure-safe.
- [`examples/supabase-rls`](examples/supabase-rls/README.md): add operation-specific ownership policies and cross-user checks.

## Verified support boundaries

These are behavioral instructions and skills, not technical enforcement plugins. “Documented” means the relevant discovery path is documented by the host; live installation was not exercised across every host in this release.

| Host | Method | Status |
|---|---|---|
| Codex | root `AGENTS.md` | Documented native instruction loading |
| OpenCode | root `AGENTS.md`; `.opencode/skills` or compatible skill paths | Documented native rules and Agent Skills |
| Claude Code | `CLAUDE.md` importing `AGENTS.md`; `.claude/skills` | Documented imports and Agent Skills |
| Gemini CLI | `GEMINI.md` importing `AGENTS.md`; `.gemini/skills` or `.agents/skills` | Documented context imports and Agent Skills |
| Devin Desktop / Cascade | root `AGENTS.md` | Documented native discovery |
| GitHub Copilot | root `AGENTS.md` or `.github/copilot-instructions.md` | Documented repository instructions |
| Cursor | `.cursor/rules/cutguard.mdc` | Documented rules format; live use not tested |

See [`docs/adapter-support.md`](docs/adapter-support.md) and [`docs/references.md`](docs/references.md).

## Benchmark status

No Cutguard performance or safety result is published. The repository contains a reproducible methodology, twelve scenario packets, a raw-result format, and validation tooling—not completed comparative model runs. No reduction or safety percentage should be attributed to Cutguard until raw runs, isolation details, scoring, and limitations are published.

## Validate and package

```bash
python scripts/build_adapters.py --check
python scripts/validate_repo.py
python scripts/validate_benchmark_results.py
python -m unittest discover -s tests
python scripts/package_release.py --version 0.1.0 --out dist
```

## Limits

Cutguard is an assistive methodology. It is not a vulnerability scanner, penetration test, compliance certification, or guarantee of secure code. Instruction files guide model behavior; they do not enforce permissions, isolation, branch protection, or deployment policy. High-impact changes still require human review and appropriate security tooling.

## Attribution

Created by **Farchan Deano** (`lustresense`).

Inspired by [Ponytail](https://github.com/DietrichGebert/ponytail) and [raroque/vibe-security-skill](https://github.com/raroque/vibe-security-skill), with security references drawn from OWASP ASVS, OWASP agentic-security guidance, NIST SSDF, OpenSSF, and official provider documentation. Cutguard is independently written and does not imply endorsement by those projects or organizations.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## License

MIT. See [`LICENSE`](LICENSE).
