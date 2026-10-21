---
title: "Service blueprint review"
category: design-work
use_when: "you have a blueprint (yours or someone else's) and want to find what it reveals or hides"
inputs: "the blueprint (table, text, or a description of the board), the goal of the redesign"
---

# Service blueprint review

**Use when:** you have a blueprint (yours or someone else's) and want to find what it reveals or hides

**You'll need:** the blueprint (table, text, or a description of the board), the goal of the redesign

## Prompt

```text
Review this service blueprint.

Blueprint: [PASTE TABLE, or describe the board lane by lane]
Goal of the work it's informing: [e.g. "cut time-to-answer in half", "reduce support tickets"]

Check for:
1. Fail points: where the experience breaks, and the backstage or support cause behind each. Rank by customer impact.
2. Wait points the customer can't see the reason for.
3. Handoffs: count them, and flag any with no owner, no notification, or a manual re-entry of data.
4. Backstage work the customer can feel (delays, repeated questions, inconsistent answers) and its root cause.
5. Support processes doing heavy lifting with no owner: policies, legacy systems, spreadsheets, a single person who knows how it works.
6. Missing pieces: steps without backstage or support detail, exception paths not drawn, lanes left empty because nobody knew. Name who would know.
7. Evidence quality: which parts are observed versus assumed. A blueprint built only from process docs shows the intended service, not the real one.
8. Opportunities, each tied to a specific fail point or handoff, with rough impact and effort.

If the blueprint is thorough for its purpose, say so and keep the list short.
```
