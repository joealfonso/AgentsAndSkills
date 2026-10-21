# Service blueprint template

A blank current-state blueprint to copy into a doc, a spreadsheet, or a whiteboard tool. It uses the same lanes and markers as the [service blueprint prompts](../prompts/design-work/), so a blueprint started here can be handed to the review or future-state prompts as-is.

## Scope

- **Service and scenario:**
- **Customer (which version of them):**
- **Starts when:**
- **Ends when:**
- **Evidence used:** research, tickets, process docs, staff interviews, system diagrams
- **Who was in the room:**

## Blueprint

Columns are the customer's steps, left to right. Add columns as needed, and add branch columns for exception paths (rejected, wrong data, someone out, the customer does something unexpected).

| Lane | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 |
|---|---|---|---|---|---|
| **Physical evidence** | | | | | |
| **Customer actions** | | | | | |
| **Frontstage** | | | | | |
| *line of interaction* | | | | | |
| **Backstage** | | | | | |
| *line of visibility* | | | | | |
| **Support processes** | | | | | |
| *line of internal interaction* | | | | | |
| **Fail points (F)** | | | | | |
| **Wait points (W)** | | | | | |
| **Handoffs (owner after)** | | | | | |
| **Customer feeling** | | | | | |

## What goes in each lane

| Lane | Contains | Ask |
|---|---|---|
| Physical evidence | Screens, emails, documents, places, anything the customer sees or touches | What tells them this step happened? |
| Customer actions | What the customer does, in their words | What are they trying to get done here? |
| Frontstage | What staff or the interface do in view of the customer | What do they see us do? |
| Backstage | What staff do out of view | Who does what, and how do they know to do it? |
| Support processes | Systems, policies, vendors, other teams | What has to be true for the backstage to work? |

The three lines matter as much as the lanes. Every arrow that crosses the **line of visibility** is work the customer depends on but can't see, which is where most fail points hide. Every crossing of the **line of internal interaction** is a dependency on another team or system.

## Markers

- **F** fail point: where it breaks or could break. Note what the customer experiences and the backstage cause.
- **W** wait point: how long, and whether the customer knows why.
- **Handoff:** work changes hands. Record the owner afterwards; a handoff with no owner is a finding.
- **OBSERVED / ASSUMED / UNKNOWN:** tag every cell. A blueprint built only from process docs shows the intended service, not the real one.
- **Anomaly:** a one-off story or behavior that doesn't fit. Keep it on the board with a distinct marker instead of averaging it away.

## Before you call it done

- [ ] Every step has something in every lane, or is marked UNKNOWN with a name to ask.
- [ ] At least one exception path is drawn.
- [ ] Frontline staff checked the backstage lanes.
- [ ] Fail points are ranked by customer impact.
- [ ] Every handoff has an owner, or is flagged.
