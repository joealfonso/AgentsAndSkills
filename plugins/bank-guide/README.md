# bank-guide

Install this one at user level. It is the front door for coding projects, the way `design-guide` is for design work.

- `/start` or "set up this repo": reads the project, picks a kit from the [catalog](skills/bank-guide/catalog.md), and writes the matching `enabledPlugins` into the repo's `.claude/settings.json`.
- "What agents do I have" or "which agent does X": searches the catalog and answers with names, no setup.

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install bank-guide@joseph-alfonso
```

The kits live in `PROJECT_KITS` in `scripts/build.py`. The catalog is generated, so after adding a plugin or agent run `python3 scripts/build.py`.
