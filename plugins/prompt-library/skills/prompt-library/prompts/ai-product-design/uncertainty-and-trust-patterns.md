---
title: "Designing uncertainty and trust"
category: ai-product-design
use_when: "you need to decide how the UI shows confidence, sources and reasoning"
inputs: "the output type, how confidence is available from the model, the user's decision"
---

# Designing uncertainty and trust

**Use when:** you need to decide how the UI shows confidence, sources and reasoning

**You'll need:** the output type, how confidence is available from the model, the user's decision

## Prompt

```text
Help me design how this AI output communicates uncertainty and reasoning.

Output: [WHAT THE AI PRODUCES]
What we can actually know about confidence: [e.g. calibrated score, retrieval match count, none]
The user's decision: [WHAT THEY DO WITH THE OUTPUT, and the stakes]

1. Is a confidence signal honest here, given what we can actually measure? If the model's scores aren't calibrated, say so and suggest alternatives (source counts, agreement checks, abstaining).
2. Three treatment options from lightest to heaviest (e.g. inline source chips, a "why" panel, a review-required state), with what each costs the user in time.
3. How low-confidence results should look and behave differently from high-confidence ones.
4. How the same signals reach screen reader users.
5. How to avoid automation bias: making it as easy to disagree as to accept.

Recommend one option for this stakes level.
```
