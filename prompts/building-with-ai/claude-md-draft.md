---
title: "Draft a CLAUDE.md for a project"
category: building-with-ai
use_when: "a repo needs agent instructions, or the existing ones are bloated"
inputs: "the repo (or its README and structure), the mistakes agents keep making"
---

# Draft a CLAUDE.md for a project

**Use when:** a repo needs agent instructions, or the existing ones are bloated

**You'll need:** the repo (or its README and structure), the mistakes agents keep making

## Prompt

```text
Draft a CLAUDE.md for this project.

Project: [README, directory structure, package.json or equivalent]
Mistakes agents keep making here: [LIST, or "none yet"]
How we work: [branching, deploys, testing expectations]

Include only what an agent can't figure out by reading the code: a 2-sentence overview, essential commands, key directories, conventions that cause bugs if missed, boundaries (always / ask first / never), and how to verify work before calling it done.

Under 100 lines. No style rules a linter could enforce. Each mistake I listed becomes one rule with a one-line reason.
```
