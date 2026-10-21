# Claude Code

Notes, patterns and pointers for how I set up and run Claude Code.

| File | What it is |
|---|---|
| [setup-patterns.md](setup-patterns.md) | Patterns for a mature Claude Code setup: hooks over prose rules, a tracker as the system of record, model tiers, a cheap judgment model, typed memory, domain MCP servers, and verification |

## Claude Code pieces elsewhere in this repo

| Where | What |
|---|---|
| [plugins/guardrails](../plugins/guardrails/) | PreToolUse hooks: blocks pattern-based process kills, asks before pushes to main |
| [rules/](../rules/) | CLAUDE.md blocks, each from a real mistake |
| [templates/CLAUDE.md](../templates/CLAUDE.md) | Starter CLAUDE.md |
| [templates/writing-claude-md-and-specs.md](../templates/writing-claude-md-and-specs.md) | What belongs in a CLAUDE.md, and how to write specs agents can build from |
| [prompts/building-with-ai](../prompts/building-with-ai/) | Prompts for specs, CLAUDE.md drafts, subagent briefs, bug reports, prototype critiques |
| [plugins/](../plugins/) | Everything installable as Claude Code plugins |

## How my setup compares

| Pattern | What I have | Worth adding |
|---|---|---|
| Rules enforced by hooks | `guardrails` blocks `pkill`/`killall` and confirms pushes to main | Adopt the "corrected twice becomes a hook" rule. Candidates: deletes become moves to `_archive/`; block closing keywords in commit messages if I ever want my own close-out step |
| Tracker as system of record | Nothing. Work lives in chat and commits | A GitHub Issues setup with one status label per issue and human-only `backlog → ready` and `review → done` |
| Main session orchestrates, model tiers | [model-by-task](../rules/model-by-task.md) rule (Haiku / Sonnet / Opus by job) | Keep the main session to planning and review on bigger projects |
| Cheap judgment model | Nothing | Only worth it for large piles (past roughly 45-60 items). Measure break-even before building |
| Skills for repeated workflows | `review-as` (its "run the panel" mode is close to "ask the board"), `prompt-library`, `design-review` | A "work the ready queue" skill once there's a tracker |
| Typed memory | Claude Code's memory already uses user / feedback / project / reference files with one fact each | `stale_after` dates, `verified: by human`, TRAP entries, and putting memory under version control |
| Domain MCP servers | A personal knowledge base MCP (not in this repo) | A `help()` tool on any server I write; prefer leaving out risky verbs over permissioning them |
| Standing infrastructure rules | Not applicable yet | |
| Verify, don't assert | CI on this repo, the layout overlap rule, browser checks before calling UI work done | Render documents to images and look before delivering |
