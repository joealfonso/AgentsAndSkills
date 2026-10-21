---
title: "Subagent or delegation brief"
category: building-with-ai
use_when: "handing a task to another agent or session that starts with no context"
inputs: "the task, files involved, what done looks like"
---

# Subagent or delegation brief

**Use when:** handing a task to another agent or session that starts with no context

**You'll need:** the task, files involved, what done looks like

## Prompt

```text
Write a self-contained brief for an agent that knows nothing about this project.

Task: [WHAT TO DO]
Relevant files and areas: [PATHS]
What I've already learned: [FINDINGS, dead ends]
Done looks like: [OBSERVABLE RESULT, how to verify]

The brief must include: the goal in one sentence, context it needs (and only that), exact files, constraints (don't touch X, stop processes by PID only, don't push to main), how to verify, and what to report back in what format.

Under 250 words. If something in my request is ambiguous enough that the agent would guess, ask me first.
```
