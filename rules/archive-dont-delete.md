# Files: archive, don't delete

Paste into CLAUDE.md for any project where losing a file would hurt.

```markdown
## Deleting files

Never delete files. Move them into `_archive/` at the project root, keeping their path:

    mkdir -p _archive/<dir> && mv <path> _archive/<path>

- Temp paths and regenerable folders (node_modules, dist, build, caches) can be deleted outright.
- `_archive/` is in .gitignore, so archived files leave the repo but stay on disk. Git history still has them.
- If something truly has to be deleted, ask me to do it.
```

Add `_archive/` to the project's `.gitignore` at the same time.

**Why:** a delete can't be undone and an archive can. Moving a file costs nothing, and the occasional "where did that go?" is answered by looking in one folder instead of digging through git history, or finding it was never committed.

**Backed by a hook:** the `guardrails` plugin blocks `rm`, `rmdir`, `unlink`, `shred`, `find -delete`, `xargs rm` and `git rm`, and replies with the exact `mv` commands to run instead. It also blocks git commands that discard uncommitted work (`git clean`, `reset --hard`, `checkout -- .`, `restore`, `stash drop`) and points to `git stash push -u` instead.
