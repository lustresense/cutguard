# Adapter and skill support

Cutguard v0.1.0 ships behavioral instruction files and Agent Skills. It does not claim a hook, sandbox, policy engine, or enforcement plugin for any host.

| Host | Native or supplied mechanism | Repository artifact | Live-tested here |
|---|---|---|---|
| Codex | Hierarchical `AGENTS.md` | root `AGENTS.md` | No |
| OpenCode | `AGENTS.md`; Agent Skills in documented skill paths | root `AGENTS.md`, `skills/*` | No |
| Claude Code | `CLAUDE.md` with imports; Agent Skills under `.claude/skills` | `adapters/claude-code/CLAUDE.md`, `skills/*` | No |
| Gemini CLI | `GEMINI.md` with imports; Agent Skills under `.gemini/skills` or `.agents/skills` | `adapters/gemini-cli/GEMINI.md`, `skills/*` | No |
| Devin Desktop / Cascade | Directory-scoped `AGENTS.md` | root `AGENTS.md` | No |
| GitHub Copilot | `AGENTS.md` and repository custom instructions | root `AGENTS.md`, generated `.github/copilot-instructions.md` | No |
| Cursor | Project Rules under `.cursor/rules` | generated `.cursor/rules/cutguard.mdc` | No |

Gemini CLI documentation currently carries a migration notice for some users to Antigravity CLI. Cutguard does not claim Antigravity compatibility until its instruction and skill discovery behavior is independently documented and checked.

Run `python scripts/build_adapters.py --check` before release. The check compares exact generated content, not only the presence of a marker.

Primary documentation links and check dates are in [`references.md`](references.md).
