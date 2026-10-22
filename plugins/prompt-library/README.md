# prompt-library

**Skill:** [`prompt-library`](skills/prompt-library/SKILL.md)

Lets Claude run any of the 81 [career prompts](../../prompts/) by name or by task. It picks the prompt, adds my background from `about-me.md`, fills the `[BRACKETS]` from the conversation, asks once for anything missing, and runs it. Ask for "the prompt itself" to get the filled-in text to paste elsewhere.

`skills/prompt-library/prompts/` is a symlink to the top-level [`prompts/`](../../prompts/) folder, which Claude Code turns into real files when it installs the plugin. Edit `prompts/` directly.
