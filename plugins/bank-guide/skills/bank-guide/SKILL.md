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

`catalog.md` only covers plugins, agents and skills. If he's after a prompt, persona, template or rule ("there's a prompt somewhere for...", "what was that persona..."), hand the question to the `design-guide` skill, which indexes every one of them. If design-guide isn't installed, say so and give the install line.

## If he is starting a project

1. **Read the project.** Look at the working directory, any README or CLAUDE.md, and what he said. Pick the kit in `catalog.md` that fits. If two kits fit and would give different setups (a game that is also a web app), ask one question. Otherwise state your pick and go.
2. **Say what the kit adds in three lines or fewer**: the plugins, the agents that come with them, and what he should delete if the project doesn't need it.
3. **Enable it for this repo only.** Merge into `.claude/settings.json` in the project root. Create the file if it is missing. Never overwrite keys that are already there; add the `.env` deny entries to any existing `permissions.deny` list rather than replacing it. Show him the result.

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  },
  "extraKnownMarketplaces": {
    "joseph-alfonso": { "source": { "source": "github", "repo": "joealfonso/AgentsAndSkills" } }
  },
  "enabledPlugins": {
    "dev-team@joseph-alfonso": true
  }
}
```

Add one `"<plugin>@joseph-alfonso": true` line per plugin in the kit. Tell him to restart the session so the plugins load.

Then make sure `.gitignore` has these lines, adding only the missing ones: `.env`, `.env.*`, `.claude/settings.local.json`, `_archive/` (where guardrails moves deleted files), and `node_modules/` if the project uses npm.
4. **CLAUDE.md.** The "How to work here" section is what tells the main session who builds and who reviews, so every coding repo needs it.
   - No CLAUDE.md: offer `templates/CLAUDE.md` and fill in the stack and commands from the repo.
   - A CLAUDE.md without a "How to work here" section: offer to add only that section from the template. Show it first and change nothing else in the file.
   - A CLAUDE.md that already has one: leave it alone.
5. **Commit it.** Put `.claude/settings.json`, `.gitignore` and CLAUDE.md on a branch and commit them. Cloud and remote sessions clone the repo, so a file that only exists on this machine gives them no plugins, hooks or routing. If `.claude/` is in `.gitignore`, say so and ask before changing it.

## What lives where

- **User level, once per machine:** this plugin, `design-guide`, `guardrails` and `writing`. Between them, this plugin and `design-guide` can find anything in the bank from any repo. Hooks at user level guard every repo, including the ones never set up. If `guardrails` isn't installed at user level, say so once and give the install line.
- **The repo's `.claude/settings.json`:** the kit. Kits repeat `guardrails` and `writing` so cloud sessions and other machines get them from the committed file.
- **The repo's CLAUDE.md:** routing and project facts only. Rules about Joseph live in `~/.claude/CLAUDE.md` (`templates/user-CLAUDE.md`). Rules a hook enforces don't go in either.

## Keep the roster small

Every enabled agent's description sits in context all session. `catalog.md` lists how many agents each kit loads; say that number when you enable a kit. Before adding plugins beyond the kit, say how many agents they add and ask. Project-type plugins go in the project's settings, never in his user settings.
