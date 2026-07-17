# Using Cutguard

## As repository instructions

Copy `AGENTS.md` to the target project's root. Add a host adapter only when the host needs or benefits from a separate file.

Cutguard should sit beside project-specific instructions, not replace them. Add the real build commands, architecture constraints, data model, and verification commands for the target repository.

## As Agent Skills

Use `scripts/install_skills.py` or copy the two directories manually into a supported skill-discovery path:

- Claude Code: `.claude/skills/`
- Gemini CLI: `.gemini/skills/` or `.agents/skills/`
- OpenCode: `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`

The `skills/` directory in this repository is the distribution source; it is not assumed to be auto-discovered from its current location.

## Prompting

Implementation:

```text
Implement this task using Cutguard. Classify risk before minimizing, lock the relevant invariants, reuse existing project capabilities, and report only checks you actually run.
```

Review:

```text
Review this diff with cutguard-review. Report unnecessary implementation, missing guards, and security theater with the smallest adequate fix.
```

## Prototype work

State the boundary precisely: local-only, mock data, no production credentials, and no claim of deployability. When the prototype moves toward deployment, re-run risk classification instead of carrying shortcuts forward implicitly.
