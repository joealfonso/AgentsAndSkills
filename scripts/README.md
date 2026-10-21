# Scripts

| Script | What it does |
|---|---|
| [build.py](build.py) | Syncs `personas/` and `prompts/` into their plugins, generates the review-persona subagents, and rebuilds every index and generated README. Run after adding or editing a persona or prompt. `--check` fails without writing if anything is out of date. |
| [skills.sh](skills.sh) | Draws skills and agents out of the repo without the plugin system: `list`, `link <name>\|all` (symlinks into `~/.claude`), `unlink`, and `zip <name>` for uploading to claude.ai. |
| [check_links.py](check_links.py) | Fails if any relative Markdown link points at a missing file. |
| [test_guard.py](test_guard.py) | 24 cases for the guardrails hook: what it should deny, ask about and allow. |

CI ([`.github/workflows/check.yml`](../.github/workflows/check.yml)) runs `build.py --check`, `check_links.py` and `test_guard.py` on every push, plus JSON and plugin validation.
