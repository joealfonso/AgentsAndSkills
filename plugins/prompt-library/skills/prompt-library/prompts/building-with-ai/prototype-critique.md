---
title: "Critique an AI-built prototype"
category: building-with-ai
use_when: "an agent built something and you need to judge it before iterating"
inputs: "the prototype (link or screenshots), what it was supposed to do"
---

# Critique an AI-built prototype

**Use when:** an agent built something and you need to judge it before iterating

**You'll need:** the prototype (link or screenshots), what it was supposed to do

## Prompt

```text
Review this prototype as a demanding design lead.

What it was supposed to do: [GOAL]
The prototype: [LINK, screenshots, or description]

1. Does it do the core job? Walk the main flow and say where it breaks.
2. Visual and interaction quality: hierarchy, spacing, states, feedback, mobile widths. Point to specific screens.
3. Generic AI-default choices to replace (stock gradients, default fonts, placeholder copy, decoration without purpose).
4. The 5 changes that would most improve it, ranked, each phrased as an instruction I can paste back to the agent.

If it's good enough for its purpose, say so and keep the list short.
```
