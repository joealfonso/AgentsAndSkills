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

1. The future-state blueprint in the same format, with each changed cell marked CHANGED and each new step marked NEW.
2. For each change: which current fail point, wait or handoff it removes, and the lane it lives in. A change that only touches frontstage while the backstage cause stays is cosmetic; flag it.
3. Operational impact per change: staff roles, training, system work, policy changes, and who has to agree.
4. What gets worse or harder for anyone (staff, another team, an edge-case customer).
5. A transition plan: what can change first without the rest, and what depends on what.
6. How we'll know it worked: one customer metric and one operational metric per major change.

Keep exception paths in the future state. A redesign that only fixes the happy path will fail at the same edges.
```
