---
title: "Anomaly review"
category: design-work
use_when: "after synthesis, before sharing findings, to catch what got left out"
inputs: "the synthesis or findings, the raw notes"
---

# Anomaly review

**Use when:** after synthesis, before sharing findings, to catch what got left out

**You'll need:** the synthesis or findings, the raw notes

## Prompt

```text
Review this research synthesis for what it left out. Don't redo the synthesis.

Synthesis: [PASTE]
Raw notes or transcripts: [PASTE, or the rainbow spreadsheet's Observations and Notes tabs]

1. Dropped observations: things in the raw notes that appear nowhere in the synthesis. Quote each with the participant label.
2. Smoothed contradictions: findings stated as general when some participants contradict them. Name the participants and what they said.
3. Missing segments: groups the sample didn't cover, and which findings are most likely to be different for them.
4. Severity blind spots: rare problems with serious consequences that got outranked by common minor ones.
5. Confirmation risk: findings that match what the team expected going in but have thin evidence.

For each item, say whether it should change a finding, become an outlier note, or prompt follow-up research, and what that follow-up would be.

If the synthesis already accounts for its outliers and contradictions, say "nothing material left out" and stop.
```
