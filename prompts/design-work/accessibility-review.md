---
title: "Accessibility review of a design"
category: design-work
use_when: "before handoff or as a QA pass on a built screen"
inputs: "screens or a description, the component library in use"
---

# Accessibility review of a design

**Use when:** before handoff or as a QA pass on a built screen

**You'll need:** screens or a description, the component library in use

## Prompt

```text
Review this design for accessibility problems that a design system won't catch on its own.

Design: [DESCRIBE, or link/screens]
Component library: [NAME, or "custom"]

Check against WCAG 2.2 AA: focus order and visibility, keyboard operability, what a screen reader would announce (names, roles, states, live updates), contrast for text and meaningful non-text, information carried by color or position alone, target size, motion and reduced-motion, error identification, timeouts, and any AI-generated content (alt text, summaries) that's relied on without review.

For each issue: where, which criterion, impact on a real user in one line, and the fix. Rank by severity. End with what needs testing with a real screen reader because it can't be judged from a static design.
```
