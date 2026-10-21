# Plugins

Everything Claude Code can install from this repo. Each folder is a plugin listed in [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json).

| Plugin | What's in it |
|---|---|
| [writing](writing/) | `write-like-joseph`, my voice for anything written or rewritten |
| [review-personas](review-personas/) | The `review-as` skill and 11 reviewer subagents built from [personas](../personas/) |
| [design-review](design-review/) | Design Review Card, AI Design Evaluation Rubric, AI Readiness Review |
| [prompt-library](prompt-library/) | The `prompt-library` skill and a copy of all 75 [prompts](../prompts/) |
| [job-search](job-search/) | Job digest, Gmail tracker updates, interview prep, resume tailoring |
| [daily-ops](daily-ops/) | Morning briefing and weekly knowledge base cleanup |
| [guardrails](guardrails/) | Hooks that block pattern-based process kills and confirm pushes to main |

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install <plugin>@joseph-alfonso
```

**Layout of a plugin:** `.claude-plugin/plugin.json` (name, version, description), plus any of `skills/<name>/SKILL.md`, `agents/<name>.md`, `hooks/hooks.json`. Bump `version` whenever a plugin changes, or installed copies may not update. Folders marked as generated below are rebuilt by `scripts/build.py`; edit the source instead.
