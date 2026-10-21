---
name: design-review-card
description: Fast, repeatable pre-build review of any design (screens, flows, specs, prototypes) using Joseph's Design Review Card. 26 checks across purpose, states, edges, access, words and failure recovery, plus a 5-question AI check when the feature uses AI. Produces a follow-up list, not a grade. Use for "review this design", "design review", "is this ready for build", "what are we missing".
---

# Design Review Card

A fast pass over a design before it goes to build. The point is not to score the work, it's to find the questions nobody has asked yet. The output is the follow-up list.

## How to run it

1. Get the material: screens, a prototype link, a spec, or a description. Note what you were given in the header.
2. Decide whether the feature uses AI or ML. If it does, add section 07. If unclear, ask once.
3. Walk every line and mark it:
   - **✓ Looks good**: you can point to where the material handles it.
   - **? Open question**: it's not handled, or you can't tell from the material. Write the actual question.
   - **– Not reviewed**: the material doesn't cover this area at all (no mobile screens, no copy yet). Not a failure, just out of view today.
4. Mark generously and move fast. A "?" is a question, not an accusation. Don't invent problems: if the material plainly handles a line, it's ✓.

## The card

**01 Purpose.** If these are shaky, stop here. Everything downstream inherits the problem.
- p1. We can say in one sentence what problem this solves, and for whom.
- p2. We know how we will tell whether it worked. (A number, a behavior, or an observation. Not "users will love it.")
- p3. Someone who is not on this team has looked at it. (Fresh eyes catch what familiarity hides.)

**02 States.** The happy path is always designed. These are the ones that get discovered in QA.
- s1. Empty, before there is any content.
- s2. Loading, including slow loading.
- s3. Error, and it says what to do next.
- s4. Partial, some of it worked and some did not.
- s5. Full, more content than fits comfortably.
- s6. First time versus returning. (Onboarding affordances that never go away become clutter.)

**03 Edges.** Cheap to check now, expensive to find later.
- e1. Longest realistic name, title, or string. (Including languages that run longer than English.)
- e2. Zero items, and thousands of items.
- e3. Slow or intermittent connection.
- e4. Someone who lacks permission to see part of this.
- e5. Small screen, and largest supported text size.

**04 Access.** Test it, do not assume the design system covers it.
- a1. Reachable and operable by keyboard alone, in a sensible order.
- a2. Makes sense to a screen reader, verified by listening. (Reading the markup is not the same as hearing it.)
- a3. Contrast holds for text and for meaningful non-text.
- a4. Nothing important is carried by color, position, or shape alone.
- a5. Targets are big enough, and motion can be reduced.

**05 Words.** Copy is design. Review it like design.
- w1. Labels say what will happen, not what the system is called internally.
- w2. Errors say what went wrong and what to do about it.
- w3. Nothing here overpromises what the product actually does.

**06 When it goes wrong.** Assume it will. Design that path deliberately.
- r1. A person can undo, edit, or back out.
- r2. Destructive or irreversible actions are clearly marked as such.
- r3. We know who receives the support ticket when this breaks.
- r4. One thing failing does not take unrelated things down with it.

**07 AI check** (only if the feature uses AI). The short form. Any "?" here is worth resolving before build, not after.
- ai1. The user can tell an AI is involved, at the point they rely on it.
- ai2. The user can see why it produced this result, in plain language.
- ai3. The system can say "I'm not sure" instead of guessing confidently. (The single most common gap. Confident wrong answers are worse than no answer.)
- ai4. A person can override or reverse it without filing a ticket.
- ai5. There is a designed path for when the AI is confidently wrong. (Distinct from a generic error state.)

## Output

```markdown
# Design review: <what we're reviewing>

Designer: <if known>
Reviewers: <if known>
Date: <today>
Material reviewed: <screens / spec / prototype>

<marked> of <total> marked · <n> ✓ · <n> open · <n> not reviewed

## Follow-ups (<n>)

1. <the question> (<section> · <line>)
2. ...

## Not reviewed today (<n>)

- <section>: <line>
```

- Phrase each follow-up as the question someone needs to answer, tied to a specific screen or spec line where possible.
- If 3 or more of the 5 AI questions are open, add: "<n> of 5 AI questions are open. Worth running a full AI Readiness Review before this goes to build." and offer the `ai-readiness-review` skill.
- No score and no verdict. That's by design.
