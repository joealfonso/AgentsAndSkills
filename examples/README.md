# Examples

What the review skills and personas actually return, on two specs. Both specs are made up for this folder. Each output was produced by Claude following the skill or persona file as written, then checked line by line against that file's rules: counts, verdict line, flag limits, and stop conditions.

| Input | Run through | Result |
|---|---|---|
| [Suggested replies spec](input-suggested-replies-spec.md), an AI feature with gaps | [design-review-card](design-review-card-output.md) | 12 follow-ups, 7 lines not reviewed, and a pointer to AIRR because 3 of 5 AI questions are open |
| Same spec | [The Burned-Out Engineer](burned-out-engineer-flags.md) | 3 ranked flags, each tied to a spec line and a rebuild reason |
| Same spec | [AI/ML Product Specialist](ai-ml-product-specialist-flags.md) | 3 ranked flags on what the agent sees when the model is wrong |
| [CSV export spec](input-csv-export-spec.md), small and complete | [The Burned-Out Engineer](burned-out-engineer-clean.md) | CLEAN FROM THIS SEAT, with nothing invented |

What to look at:

- **The card and the persona read the same spec differently.** The card asks every question the spec leaves open. The persona flags only what would cost a rebuild, so it stops at 3.
- **The clean result is the point of the stop conditions.** A reviewer prompt without them will find three problems in any spec, because it's trying to be useful. This one can say "I could start this Monday."
- **"Not reviewed" isn't a failure.** The card marks access lines "–" when there are no screens, instead of guessing.

Your own runs will differ in wording. The structure (marks, counts, verdict line, flag limit) should match. If it doesn't, the skill file needs fixing.
