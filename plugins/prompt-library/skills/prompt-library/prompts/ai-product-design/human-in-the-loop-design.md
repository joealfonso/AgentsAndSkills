---
title: "Human-in-the-loop design"
category: ai-product-design
use_when: "an AI feature takes or recommends actions with real consequences"
inputs: "the actions, stakes, volume, who reviews"
---

# Human-in-the-loop design

**Use when:** an AI feature takes or recommends actions with real consequences

**You'll need:** the actions, stakes, volume, who reviews

## Prompt

```text
Design the human oversight for this AI workflow.

What the AI does: [RECOMMENDS / DRAFTS / EXECUTES what]
Stakes if wrong: [WHO IS AFFECTED, how reversible]
Volume: [items per day or per user]
Reviewer: [ROLE, expertise, time available]

1. Which actions need a human before they take effect, which can be reviewed after, and which can run unattended. Justify each by stakes and reversibility.
2. The review interface: what the reviewer sees, how they approve, edit, reject, and how rejection feeds back.
3. How to keep reviewers from rubber-stamping at this volume (sampling, friction on high-stakes items, showing disagreement, not pre-selecting the AI answer).
4. How a wrong action that slipped through gets found and reversed.
5. What gets logged so decisions can be audited later.
```
