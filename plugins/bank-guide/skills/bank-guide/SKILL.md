---
name: bank-guide
description: Use when Joseph starts a new coding or building project, says "set up this repo" or "/start", asks what agents, skills or plugins he has, asks which agent should do a job, or can't remember what the bank holds. Picks the plugin kit for the project type and enables it in the repo's .claude/settings.json.
---

# Bank guide

The bank is the `joseph-alfonso` plugin marketplace (joealfonso/AgentsAndSkills). Next to this file:

- `catalog.md`: every plugin, agent and skill, plus the kit to enable for each project type. Search it first.
- `templates/`: starting files, including `CLAUDE.md`.

## If he asks what he has, or which agent fits a job

Search `catalog.md` for words from the question. Answer with the name, the plugin it lives in, and one line on what it does. Don't set anything up.

## If he is starting a project

1. **Read the project.** Look at the working directory, any README or CLAUDE.md, and what he said. Pick the kit in `catalog.md` that fits. If two kits fit and would give different setups (a game that is also a web app), ask one question. Otherwise state your pick and go.
2. **Say what the kit adds in three lines or fewer**: the plugins, the agents that come with them, and what he should delete if the project doesn't need it.
3. **Enable it for this repo only.** Merge into `.claude/settings.json` in the project root. Create the file if it is missing. Never overwrite keys that are already there, and show him the result.

```json
{
  "extraKnownMarketplaces": {
    "joseph-alfonso": { "source": { "source": "github", "repo": "joealfonso/AgentsAndSkills" } }
  },
  "enabledPlugins": {
    "dev-team@joseph-alfonso": true
  }
}
```

Add one `"<plugin>@joseph-alfonso": true` line per plugin in the kit. Tell him to restart the session so the plugins load.
4. **CLAUDE.md.** If the project has none, offer `templates/CLAUDE.md` and fill in the stack and commands from the repo. If it has one, leave it alone.

## Keep the roster small

Every enabled agent's description sits in context all session. The base kit is seven agents. Past about twelve, say so and ask what to drop. Project-type plugins go in the project's settings, never in his user settings. Only this plugin and `writing` belong at user level.
