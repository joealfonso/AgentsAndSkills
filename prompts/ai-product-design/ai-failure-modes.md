---
title: "AI feature failure modes"
category: ai-product-design
use_when: "early in designing any AI feature, before the happy path hardens"
inputs: "what the feature does, the model or approach, who relies on the output"
---

# AI feature failure modes

**Use when:** early in designing any AI feature, before the happy path hardens

**You'll need:** what the feature does, the model or approach, who relies on the output

## Prompt

```text
Map how this AI feature will fail, so I can design for it now.

Feature: [WHAT IT DOES]
Model/approach: [e.g. LLM summarization, classifier, retrieval + generation, agent taking actions]
Who relies on the output and for what decision: [DESCRIBE]

1. List the realistic failure modes for this kind of system: confidently wrong, partially wrong, slow, no answer, outdated data, wrong scope, inconsistent between runs, biased across groups, manipulated by input. Only include ones that are plausible here.
2. For each: how a user would notice (or not), the cost when they don't, and how often to expect it.
3. The design response for each: abstain state, confidence treatment, preview before commit, easy correction, human review route, containment so one bad output doesn't spread.
4. The 2 failures that most need a designed path before launch.

Don't invent failures the described system can't have.
```
