# design-guide

The front door to the bank. Describe what you need in your own words, and the `design-guide` skill works out where you are in the work, tells you what's missing, and runs the right resource. You don't need to know what's in the repo.

```
/plugin install design-guide@joseph-alfonso
```

Then ask the way you'd ask a colleague:

- "We've been asked to add AI summaries to the dashboard. Where do I start?"
- "Is this spec ready for engineering?" (with the spec attached)
- "I have 12 interview transcripts and a readout on Friday."
- "What should I use to check my AI feature before launch?"

It answers with a short read (the stage, the one missing thing, what to do, what comes after), then runs the prompt, persona, template or review framework. If you only asked what to use, it stops at the read.

**How it reaches everything:** `skills/design-guide/` links to the top-level `prompts/`, `personas/`, `templates/` and `rules/` folders and to the design-review skills (as `frameworks/`). Claude Code turns those links into real files when it installs the plugin, and `scripts/skills.sh zip design-guide` bundles them for claude.ai. `catalog.md` is **generated** by `scripts/build.py` from the stage map in [tools/stages.html](../../tools/stages.html) and the frontmatter of every prompt, persona and skill. To change where a resource is placed, edit the stage map, not the catalog.
