---
title: "Future-state blueprint"
category: design-work
use_when: "you have a current-state blueprint and need to design and justify the improved service"
inputs: "the current-state blueprint, goals, constraints"
---

# Future-state blueprint

**Use when:** you have a current-state blueprint and need to design and justify the improved service

**You'll need:** the current-state blueprint, goals, constraints

## Prompt

```text
Design a future-state service blueprint from this current state.

Current state: [PASTE BLUEPRINT]
Goals: [OUTCOMES, with targets if known]
Constraints: [budget, systems that can't change, policy, staffing, timeline]

Use the same structure as the current state: context line, persona strip, phases, and the lanes (actions, evidence and frontstage, backstage, support systems, risks and open questions) with the lines of interaction and visibility.

1. Mark every changed cell "Proposal:" and say in a few words what it replaces. Keep Assumed and Open tags where they still apply.
2. For each proposal, name the current risk or problem it addresses. A change that only touches the evidence and frontstage lane (a new screen, better copy) while the backstage cause stays is cosmetic; flag it.
3. Rewrite the risks lane for the future state: new risks the changes introduce, with fallbacks.
4. Operational impact per change: roles, training, systems, policy, and who has to agree (name the owner from support systems).
5. What gets worse or harder for anyone, including secondary and tertiary personas.
6. A transition order: what can change first without the rest, and what waits on a dependency or a long lead time.
7. How we'll know it worked: one persona-facing metric and one operational metric per major change.
```
