# Design review: Suggested replies in the support inbox (v0.3)

*Output of the [design-review-card](../plugins/design-review/skills/design-review-card/SKILL.md) skill on [the suggested replies spec](input-suggested-replies-spec.md).*

Designer: not given
Reviewers: not given
Date: 2026-10-21
Material reviewed: written spec v0.3, no screens

24 of 31 marked · 12 ✓ · 12 open · 7 not reviewed

## Follow-ups (12)

1. Who outside the team has read this spec, and what did they question? (01 Purpose · p3)
2. What does the panel show when no help center article matches? "No match" is TBD, and it's the state agents will hit on every ticket that isn't a repeat question. (02 States · s1)
3. What shows when only one or two drafts come back, or a cited article has been unpublished since the draft was made? (02 States · s4)
4. How does a long draft fit the side panel: truncated with expand, or scrolling? (02 States · s5)
5. How does an agent learn what the panel is the first time, and does that go away for returning agents? (02 States · s6)
6. What happens on a ticket thread with 200 messages, and for a customer whose help center has zero articles? (03 Edges · e2)
7. Does **Use this** replace what the agent already typed or insert at the cursor? The label doesn't say. (05 Words · w1)
8. "Smart replies, written for you" promises finished replies. The flow says they're drafts to check. Can the header say that? (05 Words · w3)
9. Who gets the ticket when suggestions are wrong or broken: support tooling, the ML team, or the help center owner? (06 When it goes wrong · r3)
10. Once a draft is in the composer it isn't marked as AI-generated, and that's the point where the agent relies on it, at Send. Should it stay marked until edited? (07 AI check · ai1)
11. Can the system say it isn't sure, or does it always return up to 3 drafts at the same confidence? (07 AI check · ai3)
12. What's the designed path when a draft is confidently wrong, for example citing an outdated billing article? Thumbs-down records it but doesn't help the agent in the moment. (07 AI check · ai5)

3 of 5 AI questions are open. Worth running a full AI Readiness Review before this goes to build.

## Not reviewed today (7)

- 03 Edges: e1 longest realistic string (no screens)
- 03 Edges: e5 small screen and largest text size (no screens)
- 04 Access: a1 keyboard, a2 screen reader, a3 contrast, a4 color alone, a5 target size and motion (no screens)

<details>
<summary>Every line, for checking the counts</summary>

| Line | Mark | Where |
|---|---|---|
| p1 | ✓ | Problem section |
| p2 | ✓ | Success: handle time −20%, CSAT flat or better |
| p3 | ? | Not mentioned |
| s1 | ? | No match: TBD |
| s2 | ✓ | Loading: skeleton, then "Still working…" |
| s3 | ✓ | Error copy says to reply as usual |
| s4 | ? | Not covered |
| s5 | ? | Not covered |
| s6 | ? | Not covered |
| e1 | – | No screens |
| e2 | ? | Not covered |
| e3 | ✓ | Loading state keeps the composer usable |
| e4 | ✓ | Data: public help center only |
| e5 | – | No screens |
| a1–a5 | – | No screens |
| w1 | ? | "Use this" |
| w2 | ✓ | Error copy |
| w3 | ? | "written for you" |
| r1 | ✓ | Draft is editable, nothing sends without Send |
| r2 | ✓ | No destructive actions in the flow |
| r3 | ? | No owner named |
| r4 | ✓ | Error leaves the composer unaffected |
| ai1 | ? | Badge on the panel only |
| ai2 | ✓ | Each draft cites its article |
| ai3 | ? | No confidence or "not sure" path |
| ai4 | ✓ | Editable, thumbs-down |
| ai5 | ? | No path beyond thumbs-down |

</details>
