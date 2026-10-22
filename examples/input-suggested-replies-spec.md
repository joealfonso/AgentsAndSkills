# Spec: Suggested replies in the support inbox (v0.3)

*Fictional input for the examples in this folder.*

**Status.** Locked: panel placement, model provider. Open: copy, rollout percentages.

## Problem

Tier-1 support agents at mid-size SaaS customers spend about 40% of handle time typing answers to repeat questions: password resets, billing dates, how to export data. Suggested replies give the agent a drafted answer built from the customer's help center, so they edit instead of write.

**Users:** support agents in the Helpdesk app. End customers never see a suggestion unless an agent sends it.

**Success:** median handle time on tickets tagged "how-to" drops 20% within six weeks, with CSAT on those tickets flat or better. Tracked per agent team.

## Flow

1. Agent opens a ticket. A panel on the right shows "Suggested reply" with up to 3 drafts, each citing the help center article it came from.
2. Agent clicks **Use this** to put the draft into the composer. The draft is editable, and nothing sends until the agent clicks Send.
3. Agent can thumbs-down a suggestion, with an optional reason.

## States

- **Loading:** skeleton for up to 3 seconds, then "Still working…" The composer stays usable the whole time.
- **Error:** "Suggestions aren't available right now. You can reply as usual." Composer unaffected.
- **No match:** TBD.

## Data

The model reads the ticket thread and the customer's public help center only. No access to billing, other tickets, or internal articles.

## Copy (draft)

- Panel header: "Smart replies, written for you"
- Button: "Use this"

## AI labeling

The panel carries an "AI-generated" badge. Text inserted into the composer is not marked.

## Rollout

10% of agent teams, then 50%. Out of scope for v1: auto-send, languages other than English.
