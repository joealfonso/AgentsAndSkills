---
title: "Service blueprint"
category: design-work
use_when: "you need to see how a service works end to end, front of house and back, before designing any part of it"
inputs: "the source (brief, research, process docs), the journey, the personas involved"
---

# Service blueprint

**Use when:** you need to see how a service works end to end, front of house and back, before designing any part of it

**You'll need:** the source (brief, research, process docs), the journey, the personas involved

## Prompt

```text
Build a service blueprint.

Source material: [PASTE BRIEF, research notes, process docs]
Journey to blueprint: [WHICH JOURNEY, e.g. "core journey 2 in the brief"]
Personas: [WHO IS INVOLVED, with their tier if known: primary / secondary / tertiary]

Structure each blueprint like this:

1. Context line, one or two sentences: the lead persona and their tier, the source ("Source: core journey 2 in the brief"), anything I extended beyond the source and why, and this rule: "Items marked Proposal, Assumed or Open are additions; everything else comes from the source."

2. Persona strip: the lead persona first, then everyone involved in this flow. For each: tier (primary / secondary / tertiary), name, and one line on their role in this flow specifically ("Approves the request from a notification", not a generic job description). Include easily forgotten contributors, such as the team that writes the interface text or the team that owns the data.

3. Phases: 4-6 numbered phases, left to right, each named in two to four words starting with a verb ("Find", "Compare and choose", "Confirm and track").

Lanes, top to bottom. These blueprints are for digital products, so the defaults assume an app or web product. Each lane gets a short plain-language subtitle under its name:
- [LEAD PERSONA] actions (What they do): what the lead persona does in each phase. Name the lane after them, e.g. "Employee actions", "Admin actions".
(line of interaction)
- Evidence and frontstage (What the app, staff and spaces show): the screens, states, notifications, messages and content the persona sees, and anything a person does in view. Write what the interface actually shows and decides ("Available times and a plain summary before confirming", "Saved filters apply on their own"), not just the screen name.
  Only if the product has real physical touchpoints (signs, devices, printed items, a counter): split this into "Physical evidence (What they see and touch)" above the line of interaction and "Frontstage (What staff do in view)" below it.
(line of visibility)
- Backstage (What the team does unseen): the services, jobs, rules and people working out of view. Name each one by what it does: a service that picks who to notify and when, a job that runs every morning, a timer that releases a hold, validation that blocks publishing, a queue that routes orders.
- Support systems (Data, vendors, owners): APIs, data feeds, third-party vendors, identity and sign-on, analytics, policies, and the teams that own each (IT, Legal and Privacy, Content, Data, a vendor). Call out dependencies that aren't confirmed and integrations with long lead times.
- Risks and open questions (What could break this): one per phase. Each states the risk or question and what to do about it: a fallback ("Fallback: ..."), a proposal ("Proposal: ..."), or who decides and when ("Ask at kickoff."). Include data that might not exist, integrations that might slip, adoption risks (a step that adds friction, a notification that becomes noise), and edge states (empty, error, offline, no permission).

How to write cells:
- One or two plain, concrete sentences. Name the actual thing (the screen, the service, the team), not a category.
- Put design decisions and constraints in the cell where they apply: "No offline mode in this release." "Preferences stay private to the user."
- Put exceptions and edge states in the cell too: "If nobody confirms by the hold time, the slot is released." Empty, error, offline and no-permission states belong where they happen. Don't drop a step's edge cases because they're uncommon.
- Untagged means it comes from the source. Tag everything else inline at the start of the sentence:
  "Proposal:" for my design additions, "Assumed:" for things believed but unconfirmed, "Open:" for decisions or facts nobody has yet.
- Use numbers when the source has them (targets, durations, baselines). Never invent one.
- Flag privacy and sensitive data where it flows, and say who can and can't see it.

Output each blueprint as a table: lanes as rows, phases as columns, the line of interaction and line of visibility as their own labeled rows. Then one short list: the Open items, each with who can answer it.

If the source has several journeys, offer to blueprint each one as a set, with every persona leading at least one blueprint. When a persona has a role in the source but no journey, draft theirs from the role description and say in the context line that it needs confirming with that persona.
```
