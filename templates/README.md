# Templates

| File | Use it for |
|---|---|
| [CLAUDE.md](CLAUDE.md) | The one starter for a new project's agent instructions: stack and commands, how the main session delegates to the dev-team agents (with a skip rule for small changes), and the boundaries no hook enforces. `/start` (bank-guide) writes it into a repo, or adds just the routing section to an existing CLAUDE.md. This is the only copy |
| [user-CLAUDE.md](user-CLAUDE.md) | Copy as-is to `~/.claude/CLAUDE.md`. Rules about me (voice, sourcing, no invented metrics) that load in every session and every repo, so project CLAUDE.md files don't each carry a copy. Keep it short: it shares the instruction budget with each project's CLAUDE.md |
| [service-blueprint.md](service-blueprint.md) | A blank service blueprint for digital products: context line, persona strip, phases, lanes from actions to risks and open questions, Proposal / Assumed / Open tags, and a done checklist. Matches the [service blueprint prompts](../prompts/design-work/) |
| [rainbow-spreadsheet/](rainbow-spreadsheet/) | My usability study spreadsheet as 7 importable tabs: goals, participants, task scores, the observations-by-participant rainbow with assumptions, notes, and a post-interview summary |
| [self-evaluation-log.md](self-evaluation-log.md) | A running log of persona verdicts on your own work, with pattern tags and a quarterly review so repeat flags turn into growth areas and clean passes into brag doc evidence |
| [writing-claude-md-and-specs.md](writing-claude-md-and-specs.md) | Notes on what belongs in a CLAUDE.md (and what doesn't), and five practices for writing specs agents can build from |

Pair the template with blocks from [rules](../rules/) (not the three [guardrails](../plugins/guardrails/) already enforces), and with the [building-with-AI prompts](../prompts/building-with-ai/) to draft a CLAUDE.md or SPEC.md from a real project.
