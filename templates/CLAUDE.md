# Project Context

<!-- One or two sentences: what this project is and how to work on it. Keep this whole file under ~150 lines; past that, instructions start getting ignored. -->

When working in this codebase, prioritize readability over cleverness. Ask before making architectural changes.

## About This Project

<!-- Tech stack, architecture pattern, key dependencies. -->

## Key Directories

- `src/` — Source code
- `tests/` — Tests
- `docs/` — Documentation

## Commands

```bash
npm run dev      # Start development server
npm run test     # Run tests
npm run build    # Production build
```

## Conventions That Cause Bugs If Missed

<!-- Only the non-obvious ones. Style belongs in a linter, not here. -->

## Boundaries

- ✅ Always: run tests before calling work done.
- ⚠️ Ask first: schema changes, new dependencies, anything that deploys.
- 🚫 Never: commit secrets, push to `main`.

<!-- Drop in rules from ../rules/ as needed: git-branch-workflow, responsive-overlap-check, model-by-task, kill-by-pid, remove-unreliable-features. -->
