# Rainbow spreadsheet

My working template for running and synthesizing usability studies. Observations go down the rows, participants go across the columns, and each participant's column gets its own color, so you can see at a glance which observations repeat across people and which come from one person. That's the rainbow.

It keeps the whole study in one place: goals, participants, task scores, every observation (including the team's assumptions going in), loose notes, and the post-study summary.

## The tabs

| # | Tab | What goes in it | When |
|---|---|---|---|
| 1 | [Instructions](1-instructions.csv) | How to use the sheet and the ground rules | Read first |
| 2 | [Information & Goals](2-information-and-goals.csv) | Goals, why this study, decisions it informs, research questions, method, timing, segments to cover, who the sample will miss | Before the study |
| 3 | [Participants](3-participants.csv) | One column per participant: session time, segment, role, experience, tech literacy, setup, recording, focus. `*` marks high-value participants | As sessions are scheduled |
| 4 | [Tasks & Metrics](4-tasks-and-metrics.csv) | Tasks across, participants down, a score per cell, with participant and task means | Tasks before; scores after |
| 5 | [Observations & Assumptions](5-observations-and-assumptions.csv) | **The rainbow.** One observation per row, a `1` under each participant who showed it, a count, a possible solution, and notes. Rows starting with `*` are assumptions the team wrote down before the study | Before, during and after each session |
| 6 | [Notes](6-notes.csv) | A column per participant for anything that doesn't fit elsewhere: context, tools, quotes that explain an outlier | During sessions |
| 7 | [Post Interview](7-post-interview.csv) | Research questions with answers and evidence, findings, feature discoveries, bugs, tool discoveries, outliers to follow up, and which assumptions held | After the study |

## Set it up

**Google Sheets:** create a new sheet, then for each CSV use *File → Import → Upload → Insert new sheet(s)*, in tab order. Rename each tab, then:

1. Give each participant column (P1, P2 ...) on the Observations tab its own light fill color. Use the same colors on Participants and Notes.
2. Add conditional formatting on the Count column (a color scale) so heavily repeated rows stand out, but leave single-participant rows readable; they're outliers, not noise.
3. Freeze the first row and first column on every tab.

**Excel:** open each CSV and move the sheets into one workbook in the same order.

## How it handles anomalies

- **Assumptions go in first.** The team writes what it expects to see as `*` rows before any session. A `*` row that few participants mark is a refuted assumption, and that's a finding, not a blank row.
- **No row gets deleted for having one mark.** Count sorts the rows; it doesn't decide what's worth reporting. Single-participant rows go to the Outliers section of the Post Interview tab with a likely explanation.
- **Notes hold the why.** When one person behaves differently, the Notes and Participants tabs usually explain it (their setup, their role, a workaround).

## Privacy

Use participant IDs on every tab except Participants. Keep names, emails and recordings there only, and delete that tab (or those rows) before sharing results outside the research team.

## Prompts that work with it

- [Rainbow spreadsheet setup](../../prompts/design-work/rainbow-spreadsheet-setup.md): fills tabs 2, 3, 4 and the assumption rows on tab 5 from your study plan.
- [Rainbow spreadsheet analysis](../../prompts/design-work/rainbow-spreadsheet-analysis.md): turns session notes into observation rows, then reads the filled sheet and drafts the Post Interview tab.
- [Research synthesis](../../prompts/design-work/research-synthesis.md) and [Anomaly review](../../prompts/design-work/anomaly-review.md) take an exported sheet as input.
