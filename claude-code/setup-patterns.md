# Claude Code setup patterns

Patterns for a mature Claude Code setup, as a starting point to adapt. Every piece described here can be built by asking Claude for it in plain language.

## The nine patterns

### 1. Enforce rules with hooks, not prose

CLAUDE.md rules drift. Rule of thumb: **correct the same behavior twice, and it becomes a PreToolUse hook that denies the call.** Examples:

- Deletes are blocked and turned into a move to an `_archive/` folder.
- All git goes through one wrapper script, never `cd && git`.
- Commit messages can't use closing keywords (`fixes #12`), because those auto-close issues and skip the close-out process.
- Writes to day-job systems (ticketing, work email, work repos) need approval for that specific action; reads are allowed.
- Work content can only go to approved models, with no override.

CLAUDE.md stays short and points to detail. Hooks do the enforcing.

### 2. A tracker is the system of record, and the workflow lives inside the tools

Use an issue tracker (self-hosted GitLab or GitHub Issues) behind an MCP server that bakes the workflow in, so the model can't skip it. Every issue has exactly one type label and one status label, and status is a state machine:

| Transition | Who can make it | Condition |
|---|---|---|
| backlog → ready | Human only | |
| ready → in-progress | Agent | |
| in-progress → blocked | Agent | Must post a question on the issue instead of guessing |
| in-progress → review | Agent | Requires an open merge request |
| review → done | Human only | |

Closing an issue is one tool call that runs the whole close-out: link the commits, log estimated effort, set the final status, close, and sync the wiki. Raw API calls are banned because they bypass the rules. **The tracker and the human decide when work is done, not the model.** Claude can write every issue from a prompt like "create an issue to do X, validated against the current code," which scales to hundreds of issues across many projects.

### 3. The main session orchestrates; subagents do the work by model tier

The main thread plans and dispatches but doesn't edit code.

| Tier | Work |
|---|---|
| Haiku | Short drafts, finding docs, one-line fixes |
| Sonnet | Implementing a clear spec, reading and summarizing docs |
| Strongest model | Bugs several attempts haven't cracked, real architecture tradeoffs |
| A classifier below all of these | Typed yes/no, pick-one, or score judgments over large piles; never writes |

Other vendors' coding agents can be asked for a second opinion, run headless in a throwaway worktree, and never write to the real repo. Claude reviews what comes back.

### 4. A cheap judgment model under the agents

A lot of the work is judging, not writing: is this issue ready, is this alert noise, does this description match its diff. Put a small model that only returns typed answers behind an MCP server. The rule: **the cheap model decides, Claude writes, and when the cheap model is unsure, Claude decides.** File contents go to the classifier directly, so they never fill Claude's context; Claude only reads the items marked "decide". Question sets are saved, and confidence thresholds are tuned per question against real outcomes, because generic thresholds left most items borderline.

Two lessons worth keeping:

- **Measure the break-even.** Each extra round trip resends the orchestrator's whole context. On small piles the cheap model cost more than letting the big model read everything; it only paid off past roughly 45-60 items. On a large pile it cut the big model's tokens about 4x by cost.
- **Anything sent to an outside model leaves the machine.** An early run sent a file containing a login. Every item now goes through a credential screen, work content is blocked outright, and held-back items are listed, not silently dropped.

### 5. Skills turn repeated workflows into one command

- Work the ready queue: one subagent per ready issue, each in its own worktree, in three phases (validate and lock, implement, review). Opens a merge request and hands the issue to review. Never merges or closes.
- Groom the backlog: check issues against a definition of ready, draft acceptance criteria from the real code, promote only the issues the human names.
- Work a milestone stage by stage until nothing is left that doesn't need the human.
- Ask the board: personas argue a decision, map where they agree and split, and give one recommendation.

### 6. Memory is a typed knowledge base

One fact per file with typed frontmatter (user, feedback, project, reference), plus:

- `stale_after` dates on anything that ages (versions, IPs, prices, owners), with a session-start hook that flags stale facts.
- `status: deprecated` instead of deleting, so history stays.
- `verified: by human`, which outranks anything the model inferred.
- A hook that validates every memory write, fixes links and rebuilds the index.
- **TRAP** entries for things that once cost hours ("this command exits 0 but does nothing"). These are the most valuable entries.

The memory store is version-controlled.

### 7. Write MCP servers for your own domains

Homelab provisioning, git hosting, the classifier, game-modding tools, and a read-only work mailbox with no send or delete verb at all: **the safest permission is a capability that doesn't exist.** Every server has a `help()` tool that lists what it can do, so the model looks things up instead of guessing.

### 8. Standing rules for infrastructure

When a VM, host or container is created, three things happen in the same pass: it's added to the inventory and proven reachable with a real command, it gets a start-page tile if it has a web UI, and its timezone is set. CI fails any container missing a timezone.

### 9. Verify, don't assert

- Check before asking the human or claiming something.
- Verify deliveries by file hash.
- Render Word documents to images and look at the pages before showing them.
- Compile before every deploy.

## Common mistakes

1. Prose rules expected to stick. Use hooks.
2. No system of record. A tracker with a state machine should decide what's done.
3. One model for everything. Route by difficulty and keep the orchestrator clean.
4. Memory as a dumping ground. Type it, date it, mark what's verified, record traps.
5. Only generic MCP servers. The best ones are written for your domain, with your rules inside.
6. Trusting "done". Build verification into the workflow.
7. An expensive model for every decision. Add a cheap classifier, but measure break-even first.
