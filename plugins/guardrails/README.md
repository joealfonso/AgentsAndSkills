# guardrails

A `PreToolUse` hook ([`hooks/guard.py`](hooks/guard.py)) that checks every Bash command Claude is about to run.

| Command | What happens | Rule it enforces |
|---|---|---|
| `pkill`, `killall`, `pgrep ... \| kill` | **Denied**, with instructions to find the PID with `lsof` and kill that | [kill-by-pid](../../rules/kill-by-pid.md) |
| `rm`, `rmdir`, `unlink`, `shred`, `srm`, `find -delete`, `find -exec rm`, `xargs rm`, `git rm` | **Denied**, with the exact `mkdir -p` + `mv` commands that move each file into `_archive/` with its path kept | [archive-dont-delete](../../rules/archive-dont-delete.md) |
| A `git push` that updates `main` or `master` | **Asks you** first (you can still approve) | [git-branch-workflow](../../rules/git-branch-workflow.md) |
| Everything else | Allowed, no output | |

Push detection covers explicit refspecs (`origin main`, `HEAD:main`, `+refs/heads/master`), `--all` and `--mirror`, and a bare `git push` while on `main`, including after `cd` or with `git -C`. Text that merely mentions these commands, like a commit message, is allowed.

**Deletes that are still allowed:** anything under a temp folder (`/tmp`, `/private/tmp`, `/var/folders`), regenerable folders anywhere in the path (`node_modules`, `dist`, `build`, `__pycache__`, `.next`, `.turbo`, `.cache`, `coverage`, `.venv` and similar), and `git rm --cached`, which keeps the file. A command that mixes allowed and blocked paths is denied, and the suggestion lists only the blocked ones. `find` deletes are denied unless the search root itself is allowed, and `xargs` deletes are always denied, since in both cases the files aren't known until the command runs.

**Your own exceptions:** set `GUARDRAILS_DELETE_ALLOW`, colon-separated. Entries with a slash are path prefixes (`/data/exports`); anything else is a folder name matched anywhere in the path (`.drafts`).

Files outside the project are archived next to where they live (`<dir>/_archive/`). Add `_archive/` to `.gitignore` so archived files leave the repo but stay on disk.

Tests: `python3 scripts/test_guard.py` (61 cases, also run in CI).
