# game-team

Adds art-director, artist and playtester. Needs a DESIGN.md at the repo root and a docs/ASSETS.md log. Use it next to [dev-team](../dev-team/).

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install game-team@joseph-alfonso
```

**Hook:** `hooks/agent_hook.py` logs each agent run for the [agent harness](../../harness) and enforces its controls. If you copy the agents into a project instead of installing the plugin, copy that script to the project's `.claude/hooks/`.
