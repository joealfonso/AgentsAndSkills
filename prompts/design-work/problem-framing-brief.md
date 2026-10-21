---
title: "Problem framing brief"
category: design-work
use_when: "a new project lands, often as a solution request, and you need to frame the actual problem"
inputs: "the request as you received it, what you know about users and the business"
---

# Problem framing brief

**Use when:** a new project lands, often as a solution request, and you need to frame the actual problem

**You'll need:** the request as you received it, what you know about users and the business

## Prompt

```text
Help me frame this before anyone designs anything.

The request as I received it: [PASTE, e.g. "add an AI summary to the case page"]
What I know: [users, current workflow, data, business goal, constraints, deadline]

Produce a one-page brief:
1. The underlying problem in one sentence, separate from the requested solution.
2. Who has the problem, how often, and what it costs them now.
3. What we know (with source) versus what we're assuming. Mark the 2-3 assumptions that would change the design if wrong.
4. How we'll know it worked: one primary signal, one guardrail metric.
5. Non-goals.
6. The smallest thing we could ship to learn if we're right.
7. Questions for the requester, ranked.

If the requested solution is actually a good answer to the problem, say so.
```
