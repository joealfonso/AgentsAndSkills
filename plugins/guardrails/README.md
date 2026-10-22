# guardrails

A `PreToolUse` hook ([`hooks/guard.py`](hooks/guard.py)) that checks every Bash command Claude is about to run.

| Command | What happens | Rule it enforces |
|---|---|---|
| `pkill`, `killall`, `pgrep`/`pidof`/`ps \| grep` feeding `kill`, `xargs kill`, `kill -1`, `kill 0`, `kill -<pgid>` | **Denied**, with instructions to find the PID with `lsof` and kill that | [kill-by-pid](../../rules/kill-by-pid.md) |
| `rm`, `rmdir`, `unlink`, `shred`, `srm`, `find -delete`, `find -exec rm`, `xargs rm`, `git rm` | **Denied**, with the exact `mkdir -p` + `mv` commands that move each file into `_archive/` with its path kept | [archive-dont-delete](../../rules/archive-dont-delete.md) |
| `git clean` (except `-n`), `git reset --hard`, `git checkout --` / `.` / `-f`, `git restore` (except `--staged` alone), `git switch -f`, `git stash drop`/`clear` | **Denied**, with a recoverable alternative (`git stash push -u`, `git reset --keep`, `git clean -n` then archive) | [archive-dont-delete](../../rules/archive-dont-delete.md) |
| A `git push` that updates `main` or `master` | **Asks you** first (you can still approve) | [git-branch-workflow](../../rules/git-branch-workflow.md) |
| Everything else | Allowed, no output | |

Push detection covers explicit refspecs (`origin main`, `HEAD:main`, `+refs/heads/master`), `--all` and `--mirror`, and a bare `git push` while on `main`, including after `cd` or with `git -C`. Text that merely mentions these commands, like a commit message, is allowed.

**Deletes that are still allowed:** anything under a temp folder (`/tmp`, `/private/tmp`, `/var/folders`), regenerable folders anywhere in the path (`node_modules`, `dist`, `build`, `__pycache__`, `.next`, `.turbo`, `.cache`, `coverage`, `.venv` and similar), and `git rm --cached`, which keeps the file. A command that mixes allowed and blocked paths is denied, and the suggestion lists only the blocked ones. `find` deletes are denied unless the search root itself is allowed, and `xargs` deletes are always denied, since in both cases the files aren't known until the command runs.

**Your own exceptions:** set `GUARDRAILS_DELETE_ALLOW`, colon-separated. Entries with a slash are path prefixes (`/data/exports`); anything else is a folder name matched anywhere in the path (`.drafts`).

Files outside the project are archived next to where they live (`<dir>/_archive/`). Add `_archive/` to `.gitignore` so archived files leave the repo but stay on disk.

**Wrapped commands:** the body of `bash -c`, `sh -c`, `zsh -c` (including combined flags like `-lc`) and `eval` is checked as if it ran directly, nested up to five levels.

**What it doesn't catch:** this is a check on command text, not a sandbox. Deletes written in another language (`python3 -c "shutil.rmtree(...)"`, `node -e`), emptying a file with `>` or `truncate`, `rsync --delete`, a script file run with `bash script.sh`, and file edits or deletes made through other tools (Write, MCP servers) all get through. It stops the common mistakes, not a determined workaround.

Tests: `python3 scripts/test_guard.py` (117 cases, also run in CI).
