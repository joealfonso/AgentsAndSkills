# dev-team

Seven subagents for any coding project. The main session orchestrates, because a subagent can't spawn other subagents. The engineer never reviews its own work.

| Agent | Use it for |
|---|---|
| `engineer` | Building, fixing and refactoring once the goal or spec is clear |
| `designer` | Flows, screens and UI behavior, before implementation |
| `spec-writer` | Milestones and acceptance criteria for anything that isn't a UI flow |
| `debugger` | Finding a root cause before anyone fixes it |
| `code-reviewer` | Reading a diff cold for correctness, security and edge cases |
| `test-writer` | Tests from the spec, not from the implementation |
| `marketer` | Positioning, copy angles, SEO basics, analytics |

Writing under my name is the `write-like-joseph` skill in the `writing` plugin. Reviews as a persona are the `review-as` skill in `review-personas`.

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install dev-team@joseph-alfonso
```

Enable it per project, in that repo's `.claude/settings.json`, so a repo carries only the agents it uses. The `bank-guide` plugin's `/start` does that for you. Bump `version` in `plugin.json` whenever an agent changes.

**Hook:** `hooks/agent_hook.py` logs each agent run for the [agent harness](../../harness) and enforces its controls. If you copy the agents into a project instead of installing the plugin, copy that script to the project's `.claude/hooks/`.
