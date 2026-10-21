# AI Readiness Review criteria (AIRR-1.0)

27 criteria across 7 dimensions. Score each 0 (not met), 1 (partially met), 2 (met, with evidence), or N/A.

**Gate T2+** is enforced at Tier 2 (must score at least 1) and Tier 3 (must score 2). **Gate T3** is enforced at Tier 3 only (must score 2). Gates are recorded but not enforced at Tier 1.

Reference keys are defined in [sources.md](sources.md).

## D1 Capability disclosure

Whether the user knows an AI is involved, what it is for, and how well it performs, before they rely on it.

**D1.1** **[Gate T2+]** Users are told they are interacting with an AI system, clearly and at or before first interaction.
- Met: a persistent, legible indicator at the point of interaction.
- Not met: disclosure buried in a terms page, a settings screen, or a one-time dismissed modal.
- Sources: AI Act Art. 50 · HAX G1–G18

**D1.2** Expected reliability is communicated in terms the user can act on, not as an unqualified capability claim.
- Met: "correct on roughly 4 of 5 standard cases, less reliable on multi-entity documents."
- Not met: silence, or marketing language implying near-perfect accuracy.
- Sources: HAX G1–G18 · AI Act Art. 13 · NIST AI 100-1

**D1.3** Scope boundaries are stated: the interface communicates what the system is not for.
- Met: explicit out-of-scope statement near the point of use.
- Not met: boundaries known internally but never surfaced, leaving users to discover them through failure.
- Sources: HAX G1–G18 · PAIR Guidebook · AI Act Art. 13

**D1.4** Expectation-setting is staged across the experience rather than front-loaded into a single disclaimer.
- Met: onboarding introduces capability progressively and reinforces limits in context.
- Not met: a wall of caveats at signup that no one reads and nothing thereafter.
- Sources: PAIR Guidebook

## D2 Output legibility

Whether a user can tell why the system produced this result and how much to trust it.

**D2.1** Uncertainty is expressed per output and reflects actual model confidence rather than a fixed decorative label.
- Met: a confidence signal that meaningfully varies and has been checked against real output distribution.
- Not met: every result labelled "High confidence," or confidence shown as an unexplained bare number.
- Sources: NIST AI 100-1 · HAX G1–G18 · NIST AI 600-1

**D2.2** **[Gate T2+]** The reason for a given output is available at the point of decision, in plain language.
- Met: a short, specific rationale visible or one interaction away, where the user acts.
- Not met: rationale accessible only through support escalation, engineering logs, or a separate documentation site.
- Sources: HAX G1–G18 · AI Act Art. 13 · NIST AI 100-1

**D2.3** Output is traceable to the inputs, records, or rules that produced it.
- Met: "flagged because the record in System B shows a conflicting value."
- Not met: an unattributed flag the user cannot investigate or contest.
- Sources: NIST AI 100-1 · ISO/IEC 42001 · AI Act Art. 13

**D2.4** **[Gate T2+]** Confidence signals and explanations are conveyed non-visually as well as visually.
- Met: uncertainty and rationale are exposed to assistive technology, verified by test, not by inspecting markup.
- Not met: confidence encoded only in color, icon, or position.
- Sources: WCAG 2.2 · AI Act Art. 50 · W3C AI-A11y

## D3 Human agency and oversight

Whether a person remains genuinely in control, and whether the design supports rather than erodes their judgment.

**D3.1** **[Gate T2+]** The user can see what the system proposes to do before it takes effect.
- Met: a distinct proposal or preview state preceding commitment.
- Not met: the action completes and an undo affordance appears afterwards.
- Sources: AI Act Art. 14 · HAX G1–G18

**D3.2** **[Gate T2+]** A person can disregard, override, or reverse the output without engineering assistance.
- Met: an in-product override control available to the operating role.
- Not met: correcting a wrong output requires a bug ticket, a data fix, or a support request.
- Sources: AI Act Art. 14 · HAX G1–G18

**D3.3** **[Gate T2+]** Consequential actions require explicit human confirmation; the system does not execute them silently.
- Met: an affirmative approve or reject step for anything with material effect on a person.
- Not met: automatic execution with notification after the fact.
- Sources: AI Act Art. 14

**D3.4** **[Gate T3]** The design actively counters automation bias rather than encouraging uncritical acceptance.
- Met: the interface makes independent verification easy and does not pre-select or visually privilege the AI's answer.
- Not met: a pre-checked recommendation, or a review flow where accepting is one click and disagreeing is six.
- Sources: AI Act Art. 14 · Parasuraman 1997 · Mosier 1996 · NIST AI 600-1

## D4 Uncertainty and failure design

What the experience does when the system is unsure, wrong, or outside its competence. Every AI feature will be here eventually.

**D4.1** **[Gate T2+]** An explicit "cannot determine" state exists and is structurally distinct from a confident answer.
- Met: a designed abstention state that routes to human review.
- Not met: every input receives a confident-looking answer regardless of input quality, the classic confabulation failure.
- Sources: PAIR Guidebook · HAX G1–G18 · NIST AI 600-1

**D4.2** Low-confidence output receives different visual and interaction treatment from high-confidence output.
- Met: uncertain results are visibly and behaviorally distinct, for example requiring an extra confirmation.
- Not met: identical presentation, leaving the user to guess.
- Sources: HAX G1–G18 · PAIR Guidebook

**D4.3** **[Gate T2+]** A designed recovery path exists for AI-specific errors, separate from generic system error handling.
- Met: a flow addressing what the user does when the AI is confidently wrong, including how to correct it and what happens to the correction.
- Not met: AI failures fall through to the same toast as a network timeout.
- Sources: PAIR Guidebook · HAX G1–G18

**D4.4** Failure is contained: one bad output does not block, corrupt, or silently alter unrelated work.
- Met: in a batch, a flagged item is isolated while the rest proceed.
- Not met: an all-or-nothing operation where one unresolvable row halts the set.
- Sources: NIST AI 100-1 · PAIR Guidebook

## D5 Equity and accessibility

Whether the experience holds up across the full user population, not the reference user it was designed against.

**D5.1** **[Gate T2+]** The AI-specific interface has been tested with assistive technology, not only reviewed visually or inherited from a component library.
- Met: a screen reader and keyboard-only pass on the AI surfaces themselves, with findings recorded.
- Not met: "our design system is accessible" offered as the answer.
- Sources: WCAG 2.2 · W3C AI-A11y

**D5.2** **[Gate T3]** Performance disparities across user subgroups, languages, or regions have been measured rather than assumed absent.
- Met: documented evaluation across representative name, language, and data patterns.
- Not met: no subgroup testing, or testing on a single locale generalized to all.
- Sources: NIST AI 100-1 · NIST AI 600-1 · AI Act Art. 13 · HAX G1–G18

**D5.3** AI-generated accessibility content is human-reviewed before it is relied upon.
- Met: machine-generated alt text, captions, or plain-language summaries are treated as complementary to curated content and reviewed before being relied on.
- Not met: raw model output shipped as a standalone accessibility feature, which W3C's draft finds inadequate for both automated alt text and ASR captioning.
- Sources: W3C AI-A11y · WCAG 2.2

**D5.4** The experience adapts to user context and stakes rather than offering one undifferentiated path.
- Met: a plain-language or simplified path for users facing the highest consequences and the least support.
- Not met: an expert-oriented interface presented identically to every audience.
- Sources: HAX G1–G18 · PAIR Guidebook

## D6 Demonstrated value

Whether the AI actually improves the work, measured against a baseline, rather than relocating complexity somewhere less visible.

**D6.1** The efficiency or quality claim is measured against a real pre-AI baseline, not estimated.
- Met: instrumented task timing or error rates with defined start and end points, before and after.
- Not met: a stakeholder demo, or a percentage derived from an assumption.
- Sources: NIST AI 100-1 · ISO/IEC 42001

**D6.2** Complexity is genuinely removed rather than displaced into a downstream step, another team, or a later moment.
- Met: an end-to-end step and tool count that falls.
- Not met: the front end looks simpler while a support team absorbs the reconciliation.
- Sources: NIST AI 100-1 · PAIR Guidebook

**D6.3** A granular feedback mechanism exists and demonstrably routes into system improvement.
- Met: per-output feedback with a defined owner and review cadence.
- Not met: a thumbs-up control whose data nobody reads.
- Sources: HAX G1–G18 · PAIR Guidebook

**D6.4** Post-deployment monitoring is defined, with a named owner and a threshold that triggers action.
- Met: a documented metric, threshold, owner, and escalation path.
- Not met: monitoring described as an intention with no trigger condition.
- Sources: NIST AI 100-1 · ISO/IEC 42001

## D7 Accountability record

Whether the decisions behind this experience are documented well enough to be defended, inherited, or audited later.

**D7.1** **[Gate T2+]** Known limitations are documented in a form that actually reaches the people who deploy and use the system.
- Met: limitations expressed in operator-facing documentation and reflected in the interface.
- Not met: limitations known only to the build team.
- Sources: AI Act Art. 13 · ISO/IEC 42001

**D7.2** A named human owner is accountable for this feature's behavior in production.
- Met: a specific person or role, not a team alias, answerable for the AI's output.
- Not met: distributed ownership with no one designated.
- Sources: NIST AI 100-1 · ISO/IEC 42001

**D7.3** **[Gate T3]** An impact assessment covering affected individuals and groups was completed before launch.
- Met: a documented assessment identifying who is affected and how, including those who are not direct users.
- Not met: impact considered informally or only for the primary persona.
- Sources: ISO/IEC 42001 · NIST AI 100-1
