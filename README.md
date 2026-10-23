# Agents and Skills

My bank of AI skills, personas, agents and working rules. Everything here is plain Markdown, so it works in Claude Code, Claude Desktop/Cowork, claude.ai, or pasted into any other assistant.

## What's in here

| Folder | What it is | How to use it |
|---|---|---|
| [`plugins/`](plugins) | Skills and subagents, packaged as Claude Code plugins | Install a plugin, link a skill, or zip one for claude.ai |
| [`personas/`](personas) | 19 critique and rehearsal personas, one file each | Paste one into any chat, or use the `review-as` skill |
| [`rules/`](rules) | Reusable CLAUDE.md snippets learned the hard way | Copy the block into a project's CLAUDE.md |
| [`claude-code/`](claude-code) | Notes and patterns for running Claude Code, and how my setup compares | Read before changing hooks, memory or workflow |
| [`templates/`](templates) | CLAUDE.md starter, notes on writing specs, a service blueprint, and a rainbow spreadsheet for usability studies | Copy into a new project or doc |
| [`prompts/`](prompts) | 81 career prompts across 13 areas, plus a context block about me | Fill in the brackets and paste, or use the `prompt-library` skill |
| [`examples/`](examples) | Sample outputs from a review skill and a persona, on two made-up specs | See what you get before installing anything |
| [`tools/`](tools) | Interactive HTML versions of the design review frameworks | Use them live at [josephalfonso.com/AgentsAndSkills/tools](https://josephalfonso.com/AgentsAndSkills/tools/), or browse the whole bank by stage: [STAGES.md](STAGES.md) |

## Catalog

To find things by where you are in the work instead of by file type, see [STAGES.md](STAGES.md).

### Skills

| Skill | Plugin | What it does |
|---|---|---|
| [write-like-joseph](plugins/writing/skills/write-like-joseph/SKILL.md) | writing | Writes and edits in my voice: staged drafting, banned phrases, learns from my edits |
| [review-as](plugins/review-personas/skills/review-as/SKILL.md) | review-personas | Runs any persona below as a one-shot review or a live rehearsal |
| [design-review-card](plugins/design-review/skills/design-review-card/SKILL.md) | design-review | 10-15 minute pre-build pass, 26 checks plus an optional AI check, outputs a follow-up list |
| [ai-design-rubric](plugins/design-review/skills/ai-design-rubric/SKILL.md) | design-review | Gut-check plus 18 scored criteria across six pillars, with gates and a ship verdict |
| [ai-readiness-review](plugins/design-review/skills/ai-readiness-review/SKILL.md) | design-review | AIRR-1.0: risk tiers, 27 evidence-backed criteria mapped to NIST, EU AI Act, HAX, PAIR, ISO 42001, WCAG |
| [job-listing-digest](plugins/job-search/skills/job-listing-digest/SKILL.md) | job-search | Daily list of new, verified-open design jobs from LinkedIn (Seattle + remote) |
| [application-tracker-update](plugins/job-search/skills/application-tracker-update/SKILL.md) | job-search | Reads Gmail for application activity and updates the tracker spreadsheet |
| [interview-prep](plugins/job-search/skills/interview-prep/SKILL.md) | job-search | Finds interviews in the next 48 hours and writes a brief for each |
| [resume-cover-letter-tailoring](plugins/job-search/skills/resume-cover-letter-tailoring/SKILL.md) | job-search | Tailors my resume and drafts a cover letter for one posting, as .docx |
| [morning-briefing](plugins/daily-ops/skills/morning-briefing/SKILL.md) | daily-ops | Today's calendar plus the unread email that needs attention |
| [kb-curator](plugins/daily-ops/skills/kb-curator/SKILL.md) | daily-ops | Weekly cleanup of the personal knowledge base: duplicates, tags, stale items |

The three design-review skills go from light to heavy: the card for any design, the rubric for AI features, AIRR for high-consequence AI features or a launch gate. The card points to AIRR when 3 or more of its AI questions come back open. Interactive versions of all three are live at [josephalfonso.com/AgentsAndSkills/tools](https://josephalfonso.com/AgentsAndSkills/tools/).

The job-search and daily-ops skills are my personal setup, published as examples to adapt. They expect Gmail, Google Calendar, Chrome or my knowledge base MCP (not in this repo) to be connected, and they're written for my search (Seattle and remote design roles, my file paths). Each has a **Config** section at the top with the values to change.

### Personas

Every persona has stop conditions (when to say nothing) and a fixed verdict line, so it reviews what's actually there instead of inventing problems. [examples/](examples) shows the same persona flagging an incomplete spec and passing a complete one. **Review** personas do one pass and return a verdict. **Rehearsal** personas stay in character for a practice conversation. Review personas also ship as Claude Code subagents.

| Persona | Mode | Use for |
|---|---|---|
| **Design critique** | | |
| [Strict Senior Product Designer](personas/design-critique/strict-senior-product-designer.md) | review | Case studies, portfolio decks, design rationale |
| [Skeptical Hiring Manager](personas/design-critique/skeptical-hiring-manager.md) | review | Resume review, portfolio walkthroughs, interview answers |
| [Junior Designer You're Mentoring](personas/design-critique/junior-designer-youre-mentoring.md) | rehearsal | Checking you can teach a concept, not just do it |
| [Enterprise Stakeholder (Non-Design)](personas/design-critique/enterprise-stakeholder-non-design.md) | review | Translating design decisions into business language |
| [Research-First Partner](personas/design-critique/research-first-partner.md) | rehearsal | Problem framing before any UI |
| [AI/ML Product Specialist](personas/design-critique/ai-ml-product-specialist.md) | review | AI features beyond the happy path |
| **Stakeholder and leadership** | | |
| [Skeptical VP / Exec Sponsor](personas/stakeholder-leadership/skeptical-vp-exec-sponsor.md) | rehearsal | Roadmap defense, exec decks |
| [Cross-functional Eng Lead](personas/stakeholder-leadership/cross-functional-eng-lead.md) | review | Pressure-testing a spec before engineering |
| [Finance / Ops Stakeholder](personas/stakeholder-leadership/finance-ops-stakeholder.md) | review | Cost and risk framing |
| [Skip-Level Manager](personas/stakeholder-leadership/skip-level-manager.md) | rehearsal | Upward communication |
| [The New Manager You're Coaching](personas/stakeholder-leadership/the-new-manager-youre-coaching.md) | rehearsal | Coaching instead of solving |
| [Board-Level Narrative Partner](personas/stakeholder-leadership/board-level-narrative-partner.md) | review | A quarter of work in three slides |
| **Interviewing** | | |
| [Skeptical Recruiter (Screen-stage)](personas/interviewing/skeptical-recruiter-screen-stage.md) | rehearsal | Phone screen practice |
| [Competing Candidate](personas/interviewing/competing-candidate.md) | rehearsal | Finding real differentiators |
| [Compensation Negotiator](personas/interviewing/compensation-negotiator.md) | rehearsal | Holding a number under pushback |
| **Reality checks** | | |
| [The Burned-Out Engineer](personas/reality-checks/the-burned-out-engineer.md) | review | Does the spec survive implementation |
| [The User Who Hates This](personas/reality-checks/the-user-who-hates-this.md) | review | The emotional read heuristics miss |
| [Your Own Portfolio Reviewer, Six Months Later](personas/reality-checks/your-own-portfolio-reviewer-six-months-later.md) | review | Decisions made for speed, not quality |
| [The Silent Skeptic](personas/reality-checks/the-silent-skeptic.md) | review | Where a presentation loses people |

### Prompt library

81 paste-ready prompts for recurring career work, indexed in [prompts/README.md](prompts/README.md):

| Area | Prompts | Examples |
|---|---|---|
| Job search | 8 | Job posting decoder, resume bullet rewrite, referral ask |
| Interviewing | 7 | Story bank builder, portfolio presentation script, mock interview |
| Offers and negotiation | 4 | Offer comparison, counter-offer script, resignation plan |
| Portfolio and case studies | 6 | Case study from raw notes, NDA-safe rewrite, impact metric finder |
| User research | 9 | Research plan, usability test plan, rainbow spreadsheet, synthesis, anomaly review |
| Design work | 10 | Problem framing brief, service blueprints, edge case sweep, accessibility review |
| AI product design | 6 | AI failure modes, eval plan, human-in-the-loop design |
| Stakeholders and leadership | 8 | Exec summary, decision memo, difficult conversation prep |
| Mentoring and teaching | 5 | Feedback on junior work, workshop outline, learning plan |
| Writing and visibility | 6 | LinkedIn post, talk proposal, claim checker |
| Career growth | 6 | Brag doc entry, promotion case, first 90 days |
| Building with AI | 5 | Brief to SPEC.md, CLAUDE.md draft, subagent brief |
| Claude Projects | 1 | Visual inspiration assistant |

Paste [prompts/about-me.md](prompts/about-me.md) above any prompt so the assistant knows my background and how I want answers. The `prompt-library` skill does that and fills in the brackets for you.

### Rules

| Rule | When to add it |
|---|---|
| [git-branch-workflow](rules/git-branch-workflow.md) | `main` deploys to production |
| [responsive-overlap-check](rules/responsive-overlap-check.md) | Any front-end project |
| [model-by-task](rules/model-by-task.md) | Projects that use subagents |
| [kill-by-pid](rules/kill-by-pid.md) | Projects with dev servers |
| [remove-unreliable-features](rules/remove-unreliable-features.md) | Data-driven products |
| [archive-dont-delete](rules/archive-dont-delete.md) | Losing a file would hurt |

Three of these are also backed by the `guardrails` plugin, since a rule in CLAUDE.md can be forgotten and a hook can't. It blocks pattern and bulk process kills (`pkill`, `killall`, `pgrep | kill`, `xargs kill`, `kill -1`), blocks deletes and replies with the `mv` into `_archive/` to run instead, blocks git commands that throw away uncommitted work (`git clean`, `reset --hard`, `checkout -- .`, `restore`, `stash drop`), and asks you to confirm any `git push` that would update `main` or `master` (including a bare `git push` while on `main`). It also checks inside `bash -c` and `eval`. It reads command text, so it catches mistakes, not a determined workaround; the [plugin README](plugins/guardrails/README.md#guardrails) lists what gets through.

## Using it

### Claude Code: install as plugins

```
/plugin marketplace add joealfonso/AgentsAndSkills
/plugin install review-personas@joseph-alfonso
```

Plugins: `writing`, `review-personas`, `design-review`, `prompt-library`, `job-search`, `daily-ops`, `guardrails`. Install only what a machine needs. `/plugin marketplace update joseph-alfonso` pulls new changes. When you change a plugin, bump the `version` in its `plugin.json`, or machines that already installed it may keep the cached copy.

### Claude Code: link straight from this checkout

Symlinks mean edits in the repo are live immediately.

```bash
scripts/skills.sh list
scripts/skills.sh link write-like-joseph
scripts/skills.sh link all
scripts/skills.sh unlink all
```

### claude.ai and Claude Desktop

Zip a skill and upload it in Settings > Capabilities > Skills:

```bash
scripts/skills.sh zip review-as
```

The zip lands in `dist/`. For a scheduled task in Cowork, point the task at the skill or paste the SKILL.md body as its prompt.

### Anywhere else

Open a persona or prompt file, copy the instruction or prompt block, and paste it into a new conversation with your material.

## Adding to the bank

- **New persona:** add `personas/<set>/<name>.md` with the same frontmatter as the others (`name`, `title`, `set`, `mode`, `use_for`), then run `python3 scripts/build.py`. That makes a subagent if it's review mode and updates the skill's index. The `review-as` skill reads `personas/` through a symlink, so there's no copy to update. Add a row to the table above.
- **New skill:** add `plugins/<plugin>/skills/<name>/SKILL.md` with `name` and `description` frontmatter. A new plugin also needs `.claude-plugin/plugin.json` and an entry in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).
- **New rule:** add `rules/<name>.md` with the paste-ready block and a one-line why.

Every push runs [CI](.github/workflows/check.yml): generated agents and indexes up to date, the plugin symlinks in place, no broken links, the guardrail hook tests, valid JSON, and `claude plugin validate` on the marketplace and every plugin. To run the same checks locally:

```bash
python3 scripts/build.py --check
python3 scripts/check_links.py
python3 scripts/test_guard.py
```

## License

Written content (personas, skills, prompts, rules, templates, the review frameworks) is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use and adapt it freely with credit. Scripts and hook code are MIT. Details in [LICENSE](LICENSE).
