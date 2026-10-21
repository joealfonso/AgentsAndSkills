---
title: "AI behavior spec"
category: ai-product-design
use_when: "you need to tell engineering and the model exactly how an AI feature should behave"
inputs: "the feature, users, examples of good and bad output"
---

# AI behavior spec

**Use when:** you need to tell engineering and the model exactly how an AI feature should behave

**You'll need:** the feature, users, examples of good and bad output

## Prompt

```text
Write a behavior spec for [AI FEATURE] that engineering can turn into prompts, tests and guardrails.

Users and context: [WHO, WHERE IN THE WORKFLOW]
Good output examples: [PASTE 1-3]
Bad output examples: [PASTE 1-3, with what's wrong]

Sections:
1. Purpose in one sentence.
2. Inputs the system can rely on and inputs it must not trust.
3. Required behaviors, as testable "must" statements.
4. Prohibited behaviors.
5. When to abstain or hand off to a human, with the exact user-facing message.
6. Tone and length rules.
7. 8-10 test cases (input, expected behavior, why), including adversarial and edge cases.

Write every rule so a test could check it. Flag rules that can't be tested as written.
```
