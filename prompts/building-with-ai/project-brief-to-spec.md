---
title: "Project brief to SPEC.md"
category: building-with-ai
use_when: "starting a side project or prototype with a coding agent"
inputs: "your idea, constraints, what done looks like"
---

# Project brief to SPEC.md

**Use when:** starting a side project or prototype with a coding agent

**You'll need:** your idea, constraints, what done looks like

## Prompt

```text
Turn my project idea into a SPEC.md a coding agent can build from. Don't write code.

Idea: [WHAT IT IS AND WHO IT'S FOR]
Constraints: [stack preferences, hosting, budget, must run on phones, etc.]
Done looks like: [THE FIRST VERSION I'D BE HAPPY WITH]

Sections: overview (2 sentences), user stories for v1 only, out of scope, tech stack with one-line reasons, data model, screens and states, commands (dev, test, build, deploy), testing approach, project structure, and boundaries (always do / ask first / never do).

Ask me up to 5 questions first if anything would change the architecture. Keep v1 small enough to finish in a weekend.
```
