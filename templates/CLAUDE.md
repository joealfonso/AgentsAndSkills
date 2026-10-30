# <Project name>

<One sentence: what this is and who it's for. Keep this whole file under ~150 lines; past that, instructions start getting ignored.>

## Stack and commands

- Stack: <fill in>
- Run: <fill in>
- Test: <fill in>

## Key directories

<Only the ones that aren't obvious. Delete this section if the layout explains itself.>

## How to work here

<This block assumes the dev-team plugin is enabled. Delete it if the project doesn't use subagents.>

The main session orchestrates. Subagents can't spawn other subagents, so delegate from here.

- UI or flow work: designer writes the spec first, then engineer builds it.
- Everything else (backend, tools, data, game systems): spec-writer writes the acceptance criteria first, so test-writer has something to test against.
- Something is broken and the cause isn't obvious: debugger finds the root cause, then engineer fixes it.
- engineer never reviews its own work. After a change, run code-reviewer on the diff and test-writer against the spec.
- Anything that goes out under my name: use the write-like-joseph skill. marketer handles positioning, copy angles, and analytics.
- To review work as a persona, say "review this as the burned-out engineer" and the review-as skill runs it. Personas are reviewer roles. User personas are a different thing and live in docs/research/personas/.

## Conventions that cause bugs if missed

<Only the non-obvious ones. Style belongs in a linter, not here.>

## Rules

- No em dashes. Use commas. Say "I" for my own work, not "we".
- Don't invent metrics, results, or quotes. Leave a marked gap and ask.
- Primary sources over Wikipedia. Say so when you can't find one.
- Never weaken or delete a test to make it pass.

## Boundaries

- Always: run tests before calling work done.
- Ask first: schema changes, new dependencies, anything that deploys.
- Never: commit secrets, push to `main`.

## Project notes

<Decisions, constraints, links. Keep it short.>

<!-- More rules to paste in from ../rules/: git-branch-workflow, responsive-overlap-check, model-by-task, kill-by-pid, remove-unreliable-features, archive-dont-delete. -->
