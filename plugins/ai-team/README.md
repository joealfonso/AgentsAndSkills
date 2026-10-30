# ai-team

Adds eval-writer, which writes evals under evals/. Use it next to [dev-team](../dev-team/).

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install ai-team@joseph-alfonso
```

**Hook:** `hooks/agent_hook.py` logs each agent run for the [agent harness](../../harness) and enforces its controls. If you copy the agents into a project instead of installing the plugin, copy that script to the project's `.claude/hooks/`.
