---
title: "Evaluation plan for an AI feature"
category: ai-product-design
use_when: "before launch, or when someone claims an AI feature 'works'"
inputs: "the feature, the claim, available data and users"
---

# Evaluation plan for an AI feature

**Use when:** before launch, or when someone claims an AI feature 'works'

**You'll need:** the feature, the claim, available data and users

## Prompt

```text
Draft an evaluation plan for [FEATURE] that would convince a skeptic.

The claim we want to make: [e.g. "summaries are accurate enough for agents to act on"]
Available: [test data, labelers, logs, users, budget]

1. Restate the claim as something measurable, and name what "good enough" means for the user's decision.
2. Test set: what cases, how many, how they're sampled, and how to include hard and edge cases rather than only typical ones. How to keep the set from leaking into prompts or tuning.
3. Metrics: task success, error severity (not only error rate), subgroup breakdowns, and consistency across reruns.
4. Who judges: humans, an LLM judge (with how to check the judge against humans), or both.
5. The gap between test and real use, and how to check it after launch (monitoring, a threshold, an owner).
6. What result would make us not ship.

Point out where the claim is stronger than any test could support.
```
