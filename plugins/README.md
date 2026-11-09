# Plugins

Everything Claude Code can install from this repo. Each folder is a plugin listed in [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json).

| Plugin | What's in it |
|---|---|
| [design-guide](design-guide/) | **Start here for design work. Install at user level.** The `design-guide` skill: describe what you need, get a diagnosis and the right resource run for you, or find a prompt, persona, template or rule you half-remember |
| [bank-guide](bank-guide/) | **Start here for code. Install at user level.** `/start` and the `bank-guide` skill: pick the plugin kit for a project and enable it in the repo, or find which agent fits a job |
| [guardrails](guardrails/) | **Install at user level.** Hooks that block pattern-based process kills, turn deletes into moves to `_archive/`, and confirm pushes to main |
| [writing](writing/) | `write-like-joseph`, my voice for anything written or rewritten |
| [review-personas](review-personas/) | The `review-as` skill and 13 reviewer subagents built from [personas](../personas/) |
| [design-review](design-review/) | Design Review Card, AI Design Evaluation Rubric, AI Readiness Review |
| [prompt-library](prompt-library/) | The `prompt-library` skill and a copy of all 82 [prompts](../prompts/) |
| [job-search](job-search/) | Job digest, Gmail tracker updates, interview prep, resume tailoring |
| [daily-ops](daily-ops/) | Morning briefing and weekly knowledge base cleanup |
| [dev-team](dev-team/) | Seven working subagents for any coding project: engineer, designer, spec-writer, debugger, code-reviewer, test-writer, marketer |
| [game-team](game-team/) | art-director, artist, playtester |
| [web-team](web-team/) | a11y-auditor, tech-writer |
| [ai-team](ai-team/) | eval-writer |

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install <plugin>@joseph-alfonso
```

**Layout of a plugin:** `.claude-plugin/plugin.json` (name, version, description), plus any of `skills/<name>/SKILL.md`, `agents/<name>.md`, `hooks/hooks.json`. Bump `version` whenever a plugin changes, or installed copies may not update. Folders marked as generated below are rebuilt by `scripts/build.py`; edit the source instead.
