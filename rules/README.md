# Rules

Paste-ready blocks for a project's CLAUDE.md. Each one came from a real mistake on one of my projects, and each file says what happened.

| Rule | Add it when |
|---|---|
| [git-branch-workflow](git-branch-workflow.md) | `main` deploys to production |
| [responsive-overlap-check](responsive-overlap-check.md) | The project has a front end |
| [model-by-task](model-by-task.md) | The project uses subagents |
| [kill-by-pid](kill-by-pid.md) | The project runs dev servers |
| [remove-unreliable-features](remove-unreliable-features.md) | The product is built on derived data |
| [archive-dont-delete](archive-dont-delete.md) | Losing a file would hurt |
| [stable-prompt-prefix](stable-prompt-prefix.md) | The project builds requests to the Claude API |

stable-prompt-prefix is the one exception to "my projects": the mistakes behind it are the Claude Code team's, from their post on prompt caching.

git-branch-workflow, kill-by-pid and archive-dont-delete are enforced by the [guardrails](../plugins/guardrails/) plugin, because an instruction can be forgotten and a hook can't. Install guardrails at user level and leave those three out of CLAUDE.md; paste them only where the plugin can't run. Rules about you rather than a project go in `~/.claude/CLAUDE.md` ([template](../templates/user-CLAUDE.md)).

**Add one:** the paste-ready block, then a one-line **Why** with the incident that caused it. A rule without a why gets deleted the first time it's inconvenient.
