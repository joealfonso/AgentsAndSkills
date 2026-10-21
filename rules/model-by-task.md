# Agents: pick the model by the job

Paste into CLAUDE.md for any project that uses subagents or background sessions.

```markdown
## Subagent models

Set the `model` on every subagent or session by the job, then review every result yourself before it lands:

- **Haiku:** mechanical work. Running and reading test or soak output, measurement scripts, screenshots, renames, doc and log updates, data tweaks, code searches.
- **Sonnet:** routine, well-specified edits.
- **Opus:** design-heavy or tricky work. Architecture, networking, rendering, planning.
```

**Why:** cost. Most agent work is mechanical, and the biggest model was being used for everything.
