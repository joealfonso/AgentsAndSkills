---
title: "Research synthesis"
category: design-work
use_when: "you have interview notes, test results or transcripts and need findings"
inputs: "notes or transcripts labeled by participant, the research questions"
---

# Research synthesis

**Use when:** you have interview notes, test results or transcripts and need findings

**You'll need:** notes or transcripts labeled by participant, the research questions

## Prompt

```text
Synthesize these research notes.

Research questions: [LIST]
Notes/transcripts: [PASTE, labeled by participant]

1. Findings, each as one sentence a stakeholder could repeat, ranked by how much they affect the decision.
2. For each finding: how many participants support it (e.g. 4 of 6), 1-2 short quotes with participant label, and every participant who contradicts it.
3. Answers to each research question, or "not answered" with what's missing.
4. Outliers. List every observation that only one participant raised and every behavior that fits no finding. Don't call these themes, but never drop them. For each, give the most likely explanation:
   - an unrepresented segment (this person belongs to a group the sample barely covers),
   - a high-severity edge case (rare but costly when it happens),
   - an early signal (could become common as usage grows or changes),
   - noise (explain why: a misunderstanding, a test artifact, an unrelated issue).
   Say what would confirm or rule out each explanation.
5. Severity alongside frequency. For problems, rate impact (blocks the task / costly workaround / annoyance). One participant losing data outranks five with a mild annoyance; rank accordingly.
6. Coverage: which user groups or situations these participants don't represent, so the findings aren't over-applied.
7. Recommendations, separated from findings, each tied to the findings or outliers behind it.

Mark weak evidence as weak. Counting is for confidence, not for deciding what's worth reporting.
```
