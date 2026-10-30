---
name: design-guide
description: Front door to a bank of resources for designing with AI. Use whenever someone describes a design, research, AI product or design career need in their own words without naming a tool, for example "I need to...", "how do I...", "where do I start with...", "what should I use for...", "is this ready?", or "help me with my AI feature / spec / research / prototype / portfolio / interview". Works out where they are in the work and what's actually missing, tells them, then runs the right prompt, review framework, persona or template.
---

# Design guide

Someone describes what they need in their own words. Work out what's really going on, tell them plainly, then do the work with the right resource from this bank. They should never have to browse the repo or know what's in it.

Next to this file:

- `catalog.md`: every resource, by stage, with when to use it. Search it for words from the request.
- `prompts/`, `personas/`, `templates/`, `rules/`: the resources themselves.
- `frameworks/`: the three design-review skills (Design Review Card, AI Design Rubric, AI Readiness Review).

If they name a resource ("run the edge case sweep", "review this as the eng lead"), skip the diagnosis and run it.

## 1. Diagnose

Read the request and anything attached. Decide three things:

- **Stage.** Where the work really is. It's often earlier than the ask: "review my AI feature" with no stated problem or user is a framing problem, not a critique. Use the signals below.
- **What they have.** Nothing yet, notes, a spec or screens, a built thing, a launch date. This decides the resource more than the wording of the ask.
- **What's at stake.** A throwaway prototype, an everyday feature, or AI that acts on people's money, health, access, safety or reputation. Higher stakes call for a heavier review.

Ask one question only when two stages fit and would lead to different work. Otherwise state your read and keep going.

### Signals

| They say or have | Stage | Start with |
|---|---|---|
| A solution with no problem: "we've been asked to build X", "add AI to..." | Frame the problem | Problem Framing Brief, plus AI Pitch Reality Check when AI is the proposed answer |
| Guesses about users, a decision with no evidence behind it | Research users | Lean Research Plan |
| Notes, transcripts or test results piling up | Research users | Research Synthesis, then Anomaly Review |
| Each screen works, but handoffs between people or teams break | Map the service | Service Blueprint |
| An AI feature: "what if it's wrong", trust, confidence, people over-relying on it | Design the AI behavior | AI Failure Modes, then Uncertainty and Trust |
| AI that takes or recommends actions with real consequences | Design the AI behavior | Human-in-the-Loop Design |
| Building a prototype with a coding agent | Build with agents | Project Brief to SPEC.md, then Prototype Critique once something exists |
| "Is this ready?", "review my design", screens or a spec before build | Critique and quality | Design Review Card |
| The same, for a feature that uses AI | Critique and quality | AI Design Rubric (the card first if the basics aren't covered) |
| "Can people actually use it?" with a prototype and access to users | Test with real users | Usability Test Plan with the Rainbow Spreadsheet |
| Launch coming, sign-off needed, "defend this decision" | Ship and defend | AI Readiness Review for high-consequence AI, otherwise Decision Memo or Design Rationale Doc |
| "Check my own work before anyone sees it", a self-review | Self-evaluation | The matching Self-evaluation stage in `catalog.md`, with the verdict added to the Self-Evaluation Log |
| Portfolio, resume, interviews, offers, promotion, mentoring, being visible | Career | The matching Career stage in `catalog.md` |

For anything the table doesn't cover, search `catalog.md`. For "where do I start?" with nothing else, list the eight Design work stages in one line each and ask what they're working on.

**Review weight goes card → rubric → AIRR.** The card suits any design and takes 10-15 minutes. The rubric is for AI features. The AI Readiness Review is for high-consequence AI or a launch gate, and for any design where 3 or more of the card's AI questions come back open.

## 2. Inform

Before running anything, tell them in five lines or fewer:

- **Where you are:** the stage, and what in their request made you read it that way.
- **What's missing:** the one thing standing between them and progress. One thing, not a list.
- **Do this:** the resource, and what they'll have when it's done.
- **Then:** the next one or two resources, so they can see the path.

If their stage is earlier than their ask, say so and name what skipping it will cost, then let them choose. Don't refuse what they asked for.

If they only wanted to know what to use ("what should I use for...", "is there something for..."), stop here.

## 3. Run it

- **Prompt** (`prompts/<category>/<name>.md`): read it, fill every `[BRACKET]` from the conversation, and ask once, in one message, for anything essential that's missing. Then follow it as written, including its output format and stop conditions. `prompts/about-me.md` is the repo author's background (Joseph Alfonso). Apply it only when the person you're helping is Joseph.
- **Persona** (`personas/<set>/<name>.md`): follow its instruction block. Review personas do one pass and end with a verdict line: FLAGS, CLEAN FROM THIS SEAT or CAN'T JUDGE. Rehearsal personas stay in character until their own rules end the exercise.
- **Framework** (`frameworks/<name>/SKILL.md`): follow that skill file. If they'd rather fill it in themselves, give the interactive version's link from `catalog.md`.
- **Template** (`templates/...`): hand it back pre-filled with what's already known, with the gaps marked.
- **Rule** (`rules/<name>.md`): give them the paste-ready block for their project's CLAUDE.md, and say the `guardrails` plugin enforces the archive, kill-by-PID and git rules as hooks.
- **Installed skill** (job search, writing, daily ops): these depend on their own plugin and personal setup. Name it and say what it needs. Don't run it from here.

If nothing in the bank fits, say so in one line and help directly. A near-miss resource is worse than none.

## Rules

- One main recommendation, two follow-ons at most.
- Tie every part of the diagnosis to something they said or showed. No general lectures on process.
- Keep the diagnosis short. The work is the point.
