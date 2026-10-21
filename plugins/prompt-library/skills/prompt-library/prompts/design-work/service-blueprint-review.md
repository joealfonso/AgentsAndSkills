---
title: "Service blueprint review"
category: design-work
use_when: "you have a blueprint (yours or someone else's) and want to find what it reveals or hides"
inputs: "the blueprint (table, text, or a description of the board), the goal of the work"
---

# Service blueprint review

**Use when:** you have a blueprint (yours or someone else's) and want to find what it reveals or hides

**You'll need:** the blueprint (table, text, or a description of the board), the goal of the work

## Prompt

```text
Review this service blueprint.

Blueprint: [PASTE TABLE, or describe the board lane by lane]
Goal of the work it's informing: [e.g. "cut time-to-answer in half", "reduce support tickets"]

Check, in order:
1. Provenance: is it clear what came from the source and what is a Proposal, Assumed or Open? Untagged guesses are the most dangerous cells on the board. Quote them.
2. Personas: is there a lead persona with a tier, and is everyone who touches the flow in the strip with a role specific to this flow? Name anyone missing, especially teams that own data, policy, wording or hardware.
3. Phases: do they cover the whole service, including the end (reset, follow-up, feedback), not just the happy middle?
4. Lanes: does every phase have something in every lane? Empty backstage or support cells usually mean nobody asked. Name who would know.
5. Support systems: are owners, vendors, dependencies and lead times named, or just system names?
6. Risks and open questions: is there one per phase, and does each come with a fallback, a proposal, or an owner and a deadline? A risk with no next step is a worry, not a finding.
7. Exceptions and constraints: are edge states (empty, error, offline, no permission, missing data, an item that disappears mid-flow, someone needing an accommodation) written into the cells where they happen?
8. Sensitive data: where personal or sensitive data flows, does the blueprint say who can and can't see it?
9. Opportunities: the 3 changes that would most improve the service, each tied to a specific cell or risk.

If the blueprint is solid for its purpose, say so and keep the list short.
```
