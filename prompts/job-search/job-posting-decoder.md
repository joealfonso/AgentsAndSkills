---
title: "Job posting decoder"
category: job-search
use_when: "you find a posting and want to know what they actually want before deciding to apply"
inputs: "the full job posting, your resume"
---

# Job posting decoder

**Use when:** you find a posting and want to know what they actually want before deciding to apply

**You'll need:** the full job posting, your resume

## Prompt

```text
Read this job posting the way a hiring manager wrote it, not the way HR polished it.

Job posting:
[PASTE POSTING]

My resume:
[PASTE RESUME]

Tell me:
1. The real job in two sentences: what problem this hire exists to solve, and what the first six months probably look like.
2. The top 3 requirements that will actually decide the hire, ranked. Separate them from boilerplate and wish-list items.
3. Signals about the team and company: level of design maturity, whether design reports into product or engineering, whether this is a new or backfill role, anything that suggests a mess I'd be hired to clean up. Quote the line each signal comes from.
4. Red flags, only ones you can tie to a specific line (scope far beyond the level, "fast-paced" plus a huge list, unclear ownership). If there are none, say none.
5. My fit: where my resume clearly matches, where it's thin, and what I'd need to show to close the gap.
6. Verdict: APPLY, APPLY WITH A REFERRAL FIRST, or SKIP, with one sentence of reasoning.

Don't pad the fit section. If I'm a strong match, say so plainly.
```
