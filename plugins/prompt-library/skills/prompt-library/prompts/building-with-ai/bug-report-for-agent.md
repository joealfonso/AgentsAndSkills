---
title: "Bug report an agent can fix"
category: building-with-ai
use_when: "something is broken and you want an agent (or engineer) to fix it in one pass"
inputs: "what you saw, what you expected, how to reproduce"
---

# Bug report an agent can fix

**Use when:** something is broken and you want an agent (or engineer) to fix it in one pass

**You'll need:** what you saw, what you expected, how to reproduce

## Prompt

```text
Turn my description into a bug report an agent can act on.

What I saw: [DESCRIBE, include screenshots or error text]
What I expected: [DESCRIBE]
Where: [page, device, browser, screen width]
Steps I took: [STEPS, as best I remember]

Write: a one-line title, exact reproduction steps, expected versus actual, environment, any error text verbatim, what I've already ruled out, and how to confirm the fix (including checking the same issue at other widths or states).

Ask me for anything missing that would block reproducing it.
```
