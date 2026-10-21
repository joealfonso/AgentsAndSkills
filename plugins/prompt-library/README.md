# prompt-library

**Skill:** [`prompt-library`](skills/prompt-library/SKILL.md)

Lets Claude run any of the 75 [career prompts](../../prompts/) by name or by task. It picks the prompt, adds my background from `about-me.md`, fills the `[BRACKETS]` from the conversation, asks once for anything missing, and runs it. Ask for "the prompt itself" to get the filled-in text to paste elsewhere.

`skills/prompt-library/prompts/` is **generated** by `scripts/build.py` from `prompts/`. Edit the source files, not these copies.
