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

git-branch-workflow, kill-by-pid and archive-dont-delete are also enforced by the [guardrails](../plugins/guardrails/) plugin, because an instruction can be forgotten and a hook can't.

**Add one:** the paste-ready block, then a one-line **Why** with the incident that caused it. A rule without a why gets deleted the first time it's inconvenient.
