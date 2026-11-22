# Agents: pick the model by the job

Paste into CLAUDE.md for any project that uses subagents or background sessions.

```markdown
## Subagent models

Set the `model` on every subagent or session by the job, then review every result yourself before it lands:

- **Haiku:** mechanical work. Running and reading test or soak output, measurement scripts, screenshots, renames, doc and log updates, data tweaks, code searches.
- **Sonnet:** routine, well-specified edits.
- **Opus:** design-heavy or tricky work. Architecture, networking, rendering, planning.

Change models by delegating, never by switching the main session's model mid-task. The prompt cache is per model, so a switch makes the new model reread the whole conversation from scratch.
```

**Why:** cost. Most agent work is mechanical, and the biggest model was being used for everything. The no-switching line isn't from an incident of mine. It's from the Claude Code team's [post on prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/).
