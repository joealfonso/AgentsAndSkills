---
name: ai-readiness-review
description: Formal, evidence-based assessment of whether an AI-assisted product experience is fit to ship, using Joseph's AI Readiness Review (AIRR-1.0). Risk-tier screening, 27 criteria across 7 dimensions mapped to NIST AI RMF, the EU AI Act, Microsoft HAX, Google PAIR, ISO/IEC 42001 and WCAG, and a three-condition verdict (Ready, Conditional, Not ready, Blocked). Use for launch gates, high-stakes AI features, "AI readiness review", "AIRR", or when compliance, legal or risk partners need to see design coverage.
---

# AI Readiness Review (AIRR-1.0)

A structured instrument for judging whether an AI-assisted experience is fit to ship, scored against published human-AI interaction research and regulatory requirements. Author: Joseph Alfonso.

Most AI governance frameworks work at the organizational or model layer. Very few turn into decisions a designer makes about a specific screen. This instrument sits in that gap: it takes obligations and findings from NIST AI RMF, the EU AI Act, Microsoft HAX, Google PAIR, ISO/IEC 42001 and WCAG, and expresses them as reviewable properties of an interface.

**Scope.** Design layer only. It does not assess model performance, data governance, or legal compliance, and it is not a substitute for a formal conformity assessment or legal review. Say so in every report.

For a quicker pass use `ai-design-rubric` or `design-review-card`.

## 0. Review record

Collect: feature under review, organization/team, lifecycle stage (concept, design in progress, pre-handoff, pre-launch gate, post-launch audit), reviewer, date, and the artifact assessed (which screens, spec version, prototype link). Ask for anything missing that changes the review; otherwise note it as unknown.

## 1. Risk tier

Rigor scales with consequence. Answer all five yes/no, from the material or by asking:

1. Does the output influence a decision about a person's employment, finances, health, housing, legal status, education, or benefits?
2. Can the system take an action, or commit a result, without a human confirming it first?
3. Does the feature process personal, sensitive, or identifiable data?
4. Will non-expert, vulnerable, or unsupported users rely on the output without a specialist intermediary?
5. Are the effects of a wrong output slow, costly, or impossible to reverse?

- **Tier 3, Consequential:** 3 or more yes, or both Q1 and Q2 yes. The output materially affects a person's rights, livelihood or wellbeing, or is hard to reverse. Treat the review as a launch gate, not a critique. Composite ≥ 90%, dimension floor 67%, every gate must score 2.
- **Tier 2, Elevated:** 1-2 yes. The output shapes a meaningful decision or the system acts with partial autonomy. Composite ≥ 80%, floor 50%, T2+ gates must score at least 1.
- **Tier 1, Routine:** 0 yes. Low-consequence assistive feature, errors visible, cheap and reversible. Composite ≥ 70%, floor 40%, gates recorded but not enforced.

Don't issue a verdict until the tier is set.

## 2. Scoring method

Score each of the 27 criteria in [references/criteria.md](references/criteria.md): **0** not met, **1** partially met, **2** met with evidence, or **N/A** (removed from numerator and denominator, but counts as reviewed).

**A 2 requires stated evidence**: a specific screen, spec line, test result or observation you can cite. Reviewer impression is not evidence. If the material doesn't show it, score 1 at most and say what evidence would earn the 2. This is the main control on drift between reviewers.

Gates:
- **T2+ gates** are active at Tier 2 (fail if 0) and Tier 3 (fail if below 2).
- **T3 gates** are active only at Tier 3 (fail if below 2).

## 3. Verdict

Three independent conditions must all hold for Ready, because one aggregate percentage can hide a systemic failure inside a good average:

1. **Composite threshold:** total points ÷ possible points meets the tier minimum.
2. **Dimension floor:** no single dimension falls below the tier floor.
3. **Gate clearance:** every gate active at this tier is satisfied. Gates encode obligations that can't be traded off, largely from EU AI Act Articles 13, 14 and 50.

Apply in this order:
- Any active gate failed → **Blocked**, regardless of composite.
- Composite below threshold → **Not ready**.
- A dimension below the floor, or criteria left unscored → **Conditional**. Re-review after remediation.
- Everything holds and all 27 are scored → **Ready**.

Also list every criterion scored 2 without evidence.

## 4. Output

```markdown
# AI Readiness Review: <feature>

Instrument: AIRR-1.0 · Design-layer review
Organization/team: <...> · Lifecycle stage: <...>
Reviewer: <...> · Date: <...>
Artifact assessed: <...>

## Tier
<Tier n, name>. Screening: Q1 <yes/no> · Q2 ... · Q5 ...
Thresholds: composite <x>% · dimension floor <y>% · <gate rule>

## Verdict: <Ready / Conditional / Not ready / Blocked>
Composite <pct>% (<earned>/<possible>), <scored>/27 criteria reviewed
- <each reason: gate failures, composite gap, floor failures, unscored count, evidence gaps>

## Dimensions
| Dimension | Score | Floor met |
|---|---|---|
| D1 Capability disclosure | <e>/<p> · <pct>% | ✓ / ✗ |
...

## Criteria
### D1 Capability disclosure
- **D1.1** [2] <criterion> · Evidence: <cite> · Sources: AI Act Art. 50, HAX
- **D1.2** [1] <criterion> · Gap: <what's missing> · Sources: ...
...

## Remediation, in order
1. <failed gates first, then floor failures, then the cheapest composite gains>

*Design-layer review only. Not legal advice and not a conformity assessment. Verify current obligations with qualified counsel.*
```

When Joseph needs to show a compliance, legal or risk partner what the design review already covers, add the crosswalk: a table of criterion ID, criterion, and source references, taken from [references/criteria.md](references/criteria.md). Full citations are in [references/sources.md](references/sources.md).
