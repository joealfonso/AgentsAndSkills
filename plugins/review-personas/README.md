# review-personas

Runs the [personas](../../personas/) inside Claude.

- **[`review-as` skill](skills/review-as/SKILL.md):** "review this as the burned-out engineer", "rehearse my comp negotiation", or "run the panel" for several reviewers at once. Picks a persona for you if you don't name one.
- **[`agents/`](agents/):** the 11 review-mode personas as Claude Code subagents, so a main session can hand material to, say, `skeptical-hiring-manager` and get a verdict back.

`skills/review-as/personas/` is a symlink to the top-level [`personas/`](../../personas/) folder, which Claude Code turns into real files when it installs the plugin. `agents/` is **generated** by `scripts/build.py` from those personas. Edit `personas/`, not `agents/`.
