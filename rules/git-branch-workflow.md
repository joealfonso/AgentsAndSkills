# Git: branches and PRs, never straight to main

Paste into a project's CLAUDE.md when `main` deploys to production.

```markdown
## Git workflow

- Commit, push or merge only when I ask, and each ask covers only the change it's about.
- New work goes on a feature branch. Never commit or push straight to `main`.
- After pushing a branch, open a PR into `main` and give me the link. Don't merge it unless I say so.
- When a change is finished and tested, offer in one line to open a PR. Skip the offer for exploratory or throwaway changes.
- Keep my main checkout matching GitHub: when something lands on `origin/main`, run `git pull --ff-only`. Only fast-forward. If there are uncommitted changes, local commits, or the checkout isn't on `main`, don't pull, tell me what's in the way.
```

**Why:** on more than one project, a single "commit and merge" turned into several unrequested pushes to a branch that deploys to production.

**Backed by a hook:** the `guardrails` plugin makes Claude ask you before any push that would update `main` or `master`.
