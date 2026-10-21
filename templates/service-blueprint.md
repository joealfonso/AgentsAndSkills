# Service blueprint template

A blank service blueprint for a digital product, to copy into a doc, a spreadsheet, or a whiteboard tool. It uses the same structure and tags as the [service blueprint prompts](../prompts/design-work/), so a blueprint started here can go straight into the review or future-state prompt.

Make one blueprint per core journey. Across the set, every persona should lead at least one.

## Context line

One or two sentences under the title:

> [Lead persona], [tier] persona. Source: [where this journey comes from, e.g. core journey 2 in the brief]. [Anything extended beyond the source, and why.] Items marked Proposal, Assumed or Open are additions; everything else comes from the source.

If a persona has a role in the source but no journey, draft theirs from the role description and say it needs confirming with them.

## Persona strip

| | Tier | Persona | Role in this flow |
|---|---|---|---|
| **Lead** | Primary / Secondary / Tertiary | | One line, specific to this journey |
| Involved | | | |
| Involved | | | |
| Involved | | | |

Include the contributors people forget: whoever writes the interface text, owns the data, or approves policy.

## Blueprint

Phases are numbered, left to right, named in two to four words starting with a verb. Four to six is typical.

| Lane | 1 [Phase] | 2 [Phase] | 3 [Phase] | 4 [Phase] | 5 [Phase] |
|---|---|---|---|---|---|
| **[Lead persona] actions**<br>What they do | | | | | |
| *Line of interaction* | | | | | |
| **Evidence and frontstage**<br>What the app, staff and spaces show | | | | | |
| *Line of visibility* | | | | | |
| **Backstage**<br>What the team does unseen | | | | | |
| **Support systems**<br>Data, vendors, owners | | | | | |
| **Risks and open questions**<br>What could break this | | | | | |

**Physical touchpoints?** If the product involves real physical things (signs, devices, printed items, a counter), split the evidence lane into **Physical evidence** (what they see and touch) above the line of interaction and **Frontstage** (what staff do in view) below it.

## What goes in each lane

| Lane | Contains | Ask |
|---|---|---|
| Actions | What the lead persona does, in their terms | What are they trying to get done here? |
| Evidence and frontstage | Screens, states, notifications, messages, content, and anything a person does in view | What does the product actually show and decide at this moment? |
| Backstage | Services, scheduled jobs, rules, queues, timers, and people working out of view | What runs, and what triggers it? |
| Support systems | APIs, data feeds, vendors, sign-on, analytics, policies, and the team that owns each | What has to exist, and who owns it? Is it confirmed? |
| Risks and open questions | One per phase, each with a fallback, a proposal, or who decides and when | What breaks this, and what do we do then? |

## Writing cells

- One or two plain, concrete sentences. Name the actual screen, service or team.
- Write decisions and constraints where they apply: "No offline mode in this release." "Preferences stay private to the user."
- Write edge states where they happen: empty, error, offline, no permission, data missing, an item gone mid-flow.
- Use numbers only when the source has them.
- Say who can and can't see sensitive data wherever it flows.

## Tags

Untagged means it came from the source. Start a sentence with a tag for anything else:

- **Proposal:** a design addition.
- **Assumed:** believed but unconfirmed.
- **Open:** a decision or fact nobody has yet. List every Open item under the blueprint with who can answer it.

## Before you call it done

- [ ] Context line names the source and the tagging rule.
- [ ] Every persona involved in the flow is in the strip with a role specific to this journey.
- [ ] Every phase has something in every lane, or an Open item saying who would know.
- [ ] Every risk has a fallback, a proposal, or an owner and a deadline.
- [ ] Edge states are written into the phases where they happen.
- [ ] Every Open item has someone to ask.
