---
title: "Service blueprint"
category: design-work
use_when: "you need to see how a service actually works end to end, front of house and back, before redesigning any part of it"
inputs: "the service and scenario, who the customer is, research notes, what you know about staff, systems and policies"
---

# Service blueprint

**Use when:** you need to see how a service actually works end to end, front of house and back, before redesigning any part of it

**You'll need:** the service and scenario, who the customer is, research notes, what you know about staff, systems and policies

## Prompt

```text
Build a current-state service blueprint.

Service and scenario: [e.g. "an employee requests time off and gets an answer"]
Customer: [WHO, and which version of them this blueprint follows]
Start and end points: [WHERE THE SCENARIO BEGINS AND ENDS]
Evidence: [research notes, support tickets, process docs, system diagrams, staff interviews]
What I know about backstage: [teams, tools, policies, handoffs]

Use the steps the customer takes as columns, in order. For each step, fill these rows:
- Physical evidence: what the customer sees or touches (screens, emails, documents, places).
- Customer actions.
- Frontstage: what staff or the interface do that the customer can see.
(line of interaction)
- Backstage: what staff do that the customer can't see.
(line of visibility)
- Support processes: systems, policies, vendors and other teams that make the backstage possible.
(line of internal interaction)

Then add, per step where they apply:
- Fail points (F): where it breaks or could break, and what the customer experiences when it does.
- Wait points (W): how long, and whether the customer knows why.
- Handoffs: every time work changes hands, and who owns it after.
- Customer feeling, in a word, only where the evidence shows it.

Rules:
- Tag every cell OBSERVED (from the evidence, with the source) or ASSUMED. Don't fill a cell with a plausible guess and no tag; leave it [UNKNOWN] and ask who would know.
- Include exception paths, not just the happy path: what happens when a request is rejected, data is wrong, someone is out, or the customer does something unexpected. Add them as branch columns.

Output the blueprint as a table (rows are the lanes, columns are the steps), then:
1. Fail points ranked by impact on the customer, with the backstage cause of each.
2. Handoffs with no clear owner.
3. The ASSUMED and UNKNOWN cells that matter most, and who to ask.
```
