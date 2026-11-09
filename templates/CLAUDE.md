# <Project name>

<One sentence: what this is and who it's for. Keep this whole file under ~150 lines; past that, instructions start getting ignored.>

<!--
What goes where (delete this comment once the file is filled in):
- Hard rules are hooks, not lines here. The guardrails plugin already blocks pattern kills, deletes
  (moves them to _archive/), git commands that discard work, and asks before a push to main.
  Don't paste kill-by-pid, archive-dont-delete or git-branch-workflow in here.
- Rules about me (voice, sourcing, no invented metrics) live in ~/.claude/CLAUDE.md, from the bank's
  templates/user-CLAUDE.md. They load in every repo without being copied.
- This file holds what only this project knows: commands, routing, conventions, boundaries.
-->

## Stack and commands

- Stack: <fill in>
- Run: <fill in>
- Test: <fill in>

## Key directories

<Only the ones that aren't obvious. Delete this section if the layout explains itself.>

## How to work here

<Assumes the dev-team plugin is enabled. Delete the section if the project doesn't use subagents.>

The main session plans, delegates and reviews. Subagents can't spawn other subagents, so all delegation happens from here.

- Small change (one file, obvious fix, no new behavior): do it directly, then run the tests. No chain.
- Anything bigger runs in this order:
  1. Spec. UI or flow work: designer. Everything else: spec-writer, with acceptance criteria.
  2. Build: engineer, from the spec. If the cause of a bug isn't obvious, debugger finds it first.
  3. Check: code-reviewer on the diff and test-writer against the spec, in parallel. engineer never reviews its own work.
  4. FLAGS from either go back to engineer, then check again. Done when both are clean and the tests pass.
- Extra agents, if their plugin is enabled: a11y-auditor after UI changes, playtester after game-rule changes, eval-writer before any LLM feature ships.
- To review as a persona, say "review this as the burned-out engineer" (review-as skill). Those are reviewer roles. User personas are a different thing: keep them in docs/research/personas/.

## Conventions that cause bugs if missed

<Only the non-obvious ones. Style belongs in a linter, not here.>

## Boundaries

<Only what no hook enforces.>

- Always: run the tests before calling work done. Never weaken or delete a test to make it pass.
- Ask first: schema changes, new dependencies, anything that deploys.
- Never: commit secrets, commit straight to `main` (branch first).

## Project notes

<Decisions, constraints, links. Keep it short.>

<!-- Other rules worth pasting, if they fit this project: responsive-overlap-check (front ends),
model-by-task (heavy subagent use), remove-unreliable-features (derived data).
https://github.com/joealfonso/AgentsAndSkills/tree/main/rules -->
