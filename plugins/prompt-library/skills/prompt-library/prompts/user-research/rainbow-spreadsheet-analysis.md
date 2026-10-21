---
title: "Rainbow spreadsheet analysis"
category: user-research
use_when: "during a study to log sessions, or after it to turn a filled rainbow spreadsheet into findings"
inputs: "session notes and/or the exported sheet (Observations, Participants, Tasks & Metrics, Notes tabs)"
---

# Rainbow spreadsheet analysis

**Use when:** during a study to log sessions, or after it to turn a filled rainbow spreadsheet into findings

**You'll need:** session notes and/or the exported sheet (Observations, Participants, Tasks & Metrics, Notes tabs)

## Prompt

```text
Help me with my rainbow spreadsheet. Do the part that fits what I give you.

Session notes to log (if any): [PASTE, labeled with participant ID]
Current sheet (if any): [PASTE the Observations & Assumptions tab, plus Participants, Tasks & Metrics and Notes]

A. Logging a session (when I give notes):
- Match each thing the participant did or said to an existing observation row and mark a 1 in their column.
- Add a new row for anything that matches nothing, even if only this participant did it. Write it as behavior, not interpretation.
- Put context, workarounds and quotes that explain a behavior in Notes.
- Show the rows to add or update as a table.

B. Analyzing the sheet (when I give the filled sheet):
1. Patterns: rows ranked by count, with which participants and segments they come from. Note any pattern that only appears in one segment.
2. Assumptions: each * row as confirmed, refuted or unclear, with its count. Refuted assumptions are findings; list them prominently.
3. Outliers: every row with a single mark. For each, check Participants and Notes for an explanation (segment, setup, experience) and label it: unrepresented segment, high-severity edge case, early signal, or noise with the reason. Never drop one.
4. Tasks: task means and participant means; the tasks that failed most, and whether failures cluster in a segment.
5. Draft the Post Interview tab: each research question with an answer and the evidence (row and participants), primary findings, feature discoveries, key bugs and challenges, tool discoveries, outliers to follow up, and assumptions with their status.

Counts show confidence, not importance. A single participant who couldn't finish a core task outranks a common minor annoyance.
```
