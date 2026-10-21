---
title: "Edge case and state sweep"
category: design-work
use_when: "before handoff, to find the states and cases nobody designed"
inputs: "the flow or screens, the data involved"
---

# Edge case and state sweep

**Use when:** before handoff, to find the states and cases nobody designed

**You'll need:** the flow or screens, the data involved

## Prompt

```text
Sweep this design for missing states and edge cases.

Flow: [DESCRIBE STEPS or paste spec]
Data involved: [entities, typical and extreme volumes, permissions]

Check: empty, loading (including slow), error with a next step, partial success, overflow and very long strings, zero and thousands of items, permission differences, offline or flaky network, first-time versus returning, concurrent edits, undo, destructive actions, small screens and large text, keyboard and screen reader paths.

List only cases that can actually occur in this flow, each with: where it happens, what the user would see today if unspecified, and a suggested treatment in one line. Rank by likelihood times damage. Skip states the spec already covers.
```
