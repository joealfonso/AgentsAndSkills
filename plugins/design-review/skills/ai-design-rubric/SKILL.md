---
name: ai-design-rubric
description: Score AI-generated or AI-assisted design output before it ships with Joseph's AI Design Evaluation Rubric. A 30-second gut-check, then 18 criteria across six pillars (agency, transparency, honesty, equity, real friction reduction, failure design) with gate criteria, ending in a ship verdict. Use for "evaluate this AI feature", "is this AI design ready to ship", "AI rubric", or before building a case study around an AI feature.
---

# AI Design Evaluation Rubric

A working checklist for judging AI-generated or AI-assisted design output before it ships, a case study is built around it, or it goes in front of a user. It came out of designing the AI integration layer for a large enterprise employee-management platform (4.8B+ documents a year, 67 countries), generalized for any AI-assisted feature.

For a lighter pass use `design-review-card`. For a regulated or high-consequence feature that needs a defensible record, use `ai-readiness-review`.

## Step 1: Quick gut-check

Answer yes or no from the material. Any "no" means run the full rubric before this ships.

1. Can the user see why the AI did what it did, not just what it did?
2. Does the system say "I don't know" or flag uncertainty, instead of guessing with confidence?
3. Can a human override, edit, or undo this before there's a real-world consequence?
4. Has this been tested with assistive technology (screen reader, keyboard-only), not just reviewed visually?
5. Would you be comfortable explaining this AI's decision to the person it affected, face to face?

If Joseph only asked for the gut-check, stop after reporting it.

## Step 2: Full rubric

Score each criterion **0** (not addressed), **1** (partially addressed) or **2** (fully addressed). Mark **N/A** only when genuinely irrelevant; N/A is excluded from scoring. **Gate** criteria block a ship verdict on their own if scored 0, regardless of total.

Score from what the material shows. A 2 needs something you can point to (a screen, a spec line, a test result). If you can't see it, it's a 0 or 1, or ask for the missing piece.

**Agency: surface, don't decide.** The AI's job is to inform a human decision, not quietly replace one.
- a1. The system presents options, evidence, or analysis rather than silently executing irreversible actions on the user's behalf. *Good: an analysis panel with reasoning. Red flag: an action taken with a small "undo" link buried after the fact.*
- a2. A human can see what the AI is about to do before it happens, not only after. *Good: a preview or proposal state. Red flag: results appear with no preceding confirmation step.*
- a3. **[Gate]** High-stakes actions (financial, legal, personal data, compliance, employment) always route through explicit human confirmation. *Good: an explicit approve/reject step for anything with real consequences.*

**Transparency: reasoning is legible.** A user should never have to trust the AI blindly.
- t1. A confidence level or certainty signal is shown, not just a final answer. *Good: "High confidence, based on 3 matching records." Red flag: a bare output with no indication of how sure the system is.*
- t2. The reasoning behind a suggestion is visible in plain language, not buried in a tooltip or absent. *Good: a short "why" visible by default. Red flag: reasoning only available via a support ticket or engineering log.*
- t3. A user can trace an output back to the source data or logic that produced it. *Good: "Flagged because Workday shows a pay band mismatch." Red flag: an unexplained flag with no link to its source.*

**Honesty: limits are disclosed.** What the system doesn't know is as important as what it does.
- h1. **[Gate]** The system has an explicit "can't determine this" state, rather than guessing with false confidence. *Good: a distinct, visible "needs human review" state. Red flag: every case gets a confident-looking answer, even low-quality ones.*
- h2. Edge cases and low-confidence outputs are flagged distinctly from high-confidence ones, not blended in the same visual treatment. *Good: visually and structurally different treatment for uncertain results.*
- h3. Product or marketing copy around this feature doesn't oversell what the AI can reliably do. *Good: "AI-assisted suggestions, reviewed by you." Red flag: language implying full automation or guaranteed accuracy.*

**Equity: works across different users.** One AI experience rarely fits every user or context equally well.
- e1. The design was tested with assistive technology (screen reader, keyboard-only, voice control), not just visually reviewed. *Good: a real screen-reader pass on the AI-specific UI, not just the base component library.*
- e2. The system accounts for different user contexts (expert vs. novice, high-stakes vs. routine) rather than one path for everyone. *Good: a simplified plain-language view for the most vulnerable users. Red flag: identical experience regardless of stakes or literacy.*
- e3. Output has been checked for systematic bias against any user group, language, region, or edge-case identity. *Good: documented testing across diverse names, languages, and data patterns.*

**Real reduction: not hidden complexity.** Speed that just moves the work somewhere less visible isn't a win.
- f1. The AI measurably reduces steps, tools, or time, not just visual clutter while the underlying complexity remains. *Good: 7 steps across 5 tools becomes 3 steps in 2. Red flag: the same steps in a nicer UI.*
- f2. Automation is reversible: a user can undo, edit, or override without starting the whole task over. *Good: inline accept/reject per item. Red flag: an all-or-nothing batch action.*
- f3. The feature has been validated with real task-timing or usage data, not only a demo or stakeholder walkthrough. *Good: server-side start/end timing on the actual task, before and after.*

**Failure design: graceful degradation.** Every AI feature will be wrong sometimes. This is about what happens next.
- fd1. **[Gate]** There's a clear, designed path for what happens when the AI is wrong, not just a generic error state. *Good: a specific recovery flow for AI mistakes. Red flag: a blank error toast shared with every other failure.*
- fd2. Unfixable or ambiguous cases are flagged explicitly and don't silently block or corrupt unrelated work. *Good: one flagged row doesn't hold up the other 99 in a batch.*
- fd3. **[Gate]** A human reviewer can always intervene without needing engineering support. *Good: an admin-facing override control. Red flag: fixing a bad AI call requires a bug ticket.*

## Verdict

Percentage = points earned ÷ (2 × scored, non-N/A criteria).

1. Any gate scored 0 → **Do not ship, gate failed** (list the failed gates).
2. Otherwise ≥ 80% → **Ready to ship**
3. 50-79% → **Needs revision**
4. Below 50% → **Not ready**

## Output

```markdown
AI Design Evaluation Rubric: <feature>
Company/Team: <if known>
Reviewer: Claude, for <Joseph or whoever asked>
Date: <today>

Gut-check: <n>/5 clear. <which ones failed, if any>

Verdict: <verdict> (<earned>/<possible> points, <pct>%)
<Gate criteria scored 0: ... , if any>

## Agency: surface, don't decide (<earned>/<possible>)
- [2] a1 ... (evidence: <where you saw it>)
- [0] a3 ... (missing: <what would satisfy it>)
...
```

End with the three changes that would move the score most, gates first. No closing summary beyond that.
