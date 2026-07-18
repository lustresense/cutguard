---
name: cutguard-review
description: Review a code diff or repository change for both unnecessary implementation and missing trust-boundary controls. Use for pull requests, generated code, migrations, API routes, database policies, external integrations, uploads, auth flows, and release reviews.
license: MIT
compatibility: Works as an Agent Skill in clients that support the open SKILL.md format. Requires access to the diff and relevant repository files.
metadata:
  author: lustresense
  version: "0.1.0"
---

# Cutguard review

## Review order

1. State the intended behavior from the actual diff and callers.
2. Classify each touched area as low risk, trust-boundary, or high impact.
3. Reconstruct the guards that must be locked before considering reduction.
4. Find unnecessary files, dependencies, wrappers, endpoints, copied checks, and speculative abstractions.
5. Find missing or misplaced validation, function/field/data authorization, ownership, secret isolation, database integrity, abuse controls, failure handling, and negative tests.
6. Find security theater. Every proposed control must name its threat, boundary, smallest adequate implementation, and verification.
7. Verify findings against code and existing project patterns; do not report scanner-like conclusions from filenames alone.

## Findings format

```text
[BLOCKING — MISSING GUARD] path:line
Threat:
Boundary:
Smallest adequate fix:
Verification:

[REDUCE] path:line
Why unnecessary:
Smaller existing option:

[THEATER] path:line
Why it does not enforce the claimed boundary:
Smallest adequate replacement or deletion:
```

End with checks actually run and residual uncertainty. A clean review means no evidence of a problem in the inspected scope, not proof that the repository is secure.
