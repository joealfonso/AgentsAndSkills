# Agent harness

Everything the subagents in `plugins/*/agents/` are told beyond their role sentence has to earn its place. A rule gets in when a real run failed without it, and it stays while something proves it still helps. [controls.json](controls.json) is the whole harness, and [scripts/agent_harness.py](../scripts/agent_harness.py) runs it.

## A control

| Field | What it holds |
|---|---|
| `rule` | The line in the agent prompt, word for word |
| `failure` | The real session where an agent got it wrong. No failure on record, no control |
| `backed_by` | `prose` if only the prompt carries it, or the hook or script that enforces it |
| `block` / `allow` | A case the control must catch and one it must let through, so it can't pass by blocking everything |
| `eval` | For hook controls, the prose-only cases `--eval` runs to prove the rule itself does something |
| `proven` | The last eval: model, date, pass counts with the rule and with it cut |
| `expires` | When it becomes dead weight: a date, N clean logged runs in a row, or a model change. A hook expires on real runs only, since short eval cases pass where real runs fail |

## The loop

1. Run the agents for real. The SubagentStop hook logs every run (agent, verdict, whether it was blocked) to `~/.claude/agent-harness/usage.jsonl`.
2. Garden every few weeks: `python3 scripts/agent_harness.py --garden`. It mines past session transcripts for these agents' final reports and the tools they used, then summarises the log, lists expired controls and counts unbacked rules.
3. Turn a real failure into a control: the rule, the session it came from, a block case and an allow case, and an expiry. Back it with a hook or script when a script can check it.
4. `--eval ID` runs the cases n times with the rule and n times with it cut. A rule is PROVEN when it's followed in at least 75% of runs and at least 50 points more often than without it. REDUNDANT and IGNORED rules come out.
5. `--smoke` replays every case that last passed, once each, after a model upgrade. `--expired` says what to delete.
6. `--prune` deletes any prompt line with no control behind it.

CI runs `--check` and [scripts/test_agent_harness.py](../scripts/test_agent_harness.py), which need no model. `--eval` and `--smoke` call `claude -p` in safe mode, so they need a logged-in `claude` and are run by hand.

## Where it stands (2026-10-30)

Every past session on this machine held 5 runs of these agents, all in one animal-range-finder session on 2026-10-28: code-reviewer twice, and engineer, designer and a11y-auditor once each. 21 of the 25 agents had never been run as subagents.

- **Controlled.** 0 of 3 code-reviewer and a11y-auditor reports put the verdict last, as their prompts asked. The verdict rule is now enforced by [agent_hook.py](../plugins/dev-team/hooks/agent_hook.py), which blocks the stop once and asks for the line.
- **Pruned.** 234 prompt rules plus 2 preamble sentences had no failure on record and no eval behind them, so they were deleted. Agents are now their role sentence plus any controlled rule. The review-persona verdict line moved to the `review-as` skill, which is what consumes it.
- **Fewer tools.** The four agents with real runs lost the tools those runs never used. a11y-auditor did everything through Bash. code-reviewer and engineer never used Grep or Glob, and designer never used Edit. If a later run needs one back, the transcript will show the failed attempt.
- **Seen, not yet controlled.** The designer, engineer and a11y-auditor all said they couldn't render the app, and the parent session had to check it in a browser itself. That's how the too-sparse stipple and the contrast failures were found. The fix is a tool, not a rule: give these agents a way to run the app and screenshot it.
- **Evaluated 2026-10-30 on sonnet.** Both verdict rules are PROVEN: followed in 4 of 4 runs with the rule and 0 of 4 with it cut, on both the block and the allow case. The hooks stay anyway: these short cases pass while the long, tool-heavy real reviews failed 3 of 3, so the hooks expire on 20 clean real runs, not on an eval.

## Installing the hook

Plugin installs register it through each plugin's `hooks/hooks.json`. Agents copied into a project's `.claude/agents/` carry it in their frontmatter, which looks for `.claude/hooks/agent_hook.py` in the project and then `~/.claude/hooks/agent_hook.py`. Copy [the script](../plugins/dev-team/hooks/agent_hook.py) to one of those, or run `scripts/skills.sh link <agent>`, which links it. If it's missing, the hook does nothing.
