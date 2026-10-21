# guardrails

A `PreToolUse` hook ([`hooks/guard.py`](hooks/guard.py)) that checks every Bash command Claude is about to run.

| Command | What happens | Rule it enforces |
|---|---|---|
| `pkill`, `killall`, `pgrep ... \| kill` | **Denied**, with instructions to find the PID with `lsof` and kill that | [kill-by-pid](../../rules/kill-by-pid.md) |
| A `git push` that updates `main` or `master` | **Asks you** first (you can still approve) | [git-branch-workflow](../../rules/git-branch-workflow.md) |
| Everything else | Allowed, no output | |

Push detection covers explicit refspecs (`origin main`, `HEAD:main`, `+refs/heads/master`), `--all` and `--mirror`, and a bare `git push` while on `main`, including after `cd` or with `git -C`. Text that merely mentions these commands, like a commit message, is allowed.

Tests: `python3 scripts/test_guard.py` (24 cases, also run in CI).
