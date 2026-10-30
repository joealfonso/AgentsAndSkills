# Bank catalog

What to enable per project type, then everything each plugin holds. Enable plugins in a project's `.claude/settings.json` as `"<plugin>@joseph-alfonso": true`.

## Kits by project type

| Project type | Enable | What you get |
|---|---|---|
| Any coding project | `dev-team`, `review-personas`, `guardrails`, `writing` | Seven working agents, review personas on demand, hooks that block risky commands, and my writing voice. |
| Game | `dev-team`, `review-personas`, `guardrails`, `writing`, `game-team` | Adds art-director, artist and playtester. Needs DESIGN.md at the repo root and docs/ASSETS.md. |
| Web app or site | `dev-team`, `review-personas`, `guardrails`, `writing`, `web-team`, `design-review` | Adds a11y-auditor and tech-writer, plus the design review card before build. |
| AI feature | `dev-team`, `review-personas`, `guardrails`, `writing`, `ai-team`, `design-review` | Adds eval-writer, plus the AI design rubric and AI readiness review. |
| Design or research work | `design-guide`, `design-review`, `prompt-library`, `review-personas`, `writing` | No coding agents. Prompts, frameworks and personas picked by stage. |
| Job search | `job-search`, `prompt-library`, `review-personas`, `writing` | Personal setup. Edit the Config section in each skill first. |
| Daily routines | `daily-ops` | Personal setup. Morning briefing and knowledge base cleanup. |

## Plugins

### design-guide

Start here. Describe what you need and get a diagnosis, then the right resource run for you: every prompt, persona, template and design-review framework in the bank, picked by stage.

- skill `design-guide`: Front door to a bank of resources for designing with AI

### writing

Write and edit in Joseph's voice: staged drafting, a banned-phrase list, and a learning loop from his edits.

- skill `write-like-joseph`: Use whenever Joseph wants anything written or rewritten: emails, posts, messages, bios, case studies, drafts

### review-personas

20 critique and rehearsal personas (design, stakeholder, interview, reality checks) as a review-as skill plus 12 reviewer subagents.

- 12 reviewer subagents, one per review-mode persona. Run them through the `review-as` skill.
- skill `review-as`: Review work or rehearse a conversation as one of Joseph's critique personas (strict senior designer, skeptical hiring manager, VP, eng lead, finance, recruiter, comp negotiator, burned-out engineer, user who hates this, and more)

### design-review

Design review frameworks: a fast Design Review Card, the AI Design Evaluation Rubric, and the evidence-based AI Readiness Review (AIRR-1.0).

- skill `ai-design-rubric`: Score AI-generated or AI-assisted design output before it ships with Joseph's AI Design Evaluation Rubric
- skill `ai-readiness-review`: Formal, evidence-based assessment of whether an AI-assisted product experience is fit to ship, using Joseph's AI Readiness Review (AIRR-1.0)
- skill `design-review-card`: Fast, repeatable pre-build review of any design (screens, flows, specs, prototypes) using Joseph's Design Review Card

### prompt-library

81 career prompts (job search, interviews, offers, portfolio, user research, design work, AI product design, leadership, mentoring, writing, career growth, building with AI) with a skill that fills them in and runs them.

- skill `prompt-library`: Joseph's career prompt library, 81 prompts for job search, interviews, offers, portfolio and case studies, user research, design work, AI product design, stakeholders and leadership, mentoring, writing, career growth, and building with AI

### job-search

Personal setup, edit the Config sections before use. Job search automations: live LinkedIn digest, Gmail-to-tracker updates, interview prep briefs, resume and cover letter tailoring.

- skill `application-tracker-update`: Scan Gmail for job application activity (confirmations, interviews, rejections, offers) and update the job search tracker spreadsheet
- skill `interview-prep`: Check the calendar for job interviews in the next 48 hours and prep a short research brief for each (company context, likely questions, talking points)
- skill `job-listing-digest`: Daily digest of new, verified-open product/UX design job postings (Seattle and remote) pulled live from LinkedIn in the browser, deduped against prior runs
- skill `resume-cover-letter-tailoring`: Tailor Joseph's resume and draft a cover letter for a specific job posting (URL or pasted description)

### daily-ops

Personal setup, edit before use. Daily and weekly routines: morning calendar and email briefing, personal knowledge base cleanup.

- skill `kb-curator`: Weekly maintenance pass on the personal knowledge base MCP: archive clear duplicates, normalize tags, flag stale items for review
- skill `morning-briefing`: Short morning briefing of today's calendar plus unread email that actually needs attention

### guardrails

Hooks that back three rules: never kill processes by pattern or in bulk (pkill, killall, xargs kill, kill -1), never delete files or discard uncommitted git work (archive into _archive/ or stash instead), and confirm before any git push to main or master. Checks command text, including inside bash -c and eval; not a sandbox.

- hooks: see the plugin README

### bank-guide

Install this one globally. Start a coding project or ask which agent fits a job, and it picks the right plugin kit from the bank and enables it in the repo.

- skill `bank-guide`: Use when Joseph starts a new coding or building project, says "set up this repo" or "/start", asks what agents, skills or plugins he has, asks which agent should do a job, or can't remember what the bank holds
- command `/start`: Set up this project from the bank: pick the plugin kit and enable it in .claude/settings.json

### dev-team

Working roster for any coding project: engineer, designer, spec-writer, debugger, code-reviewer, test-writer, marketer. The main session orchestrates; the engineer never reviews its own work.

- agent `code-reviewer`: Reviews diffs and files cold, with no attachment to how they were written
- agent `debugger`: Reproduces a bug and finds its root cause before anyone fixes it
- agent `designer`: Designs flows, screens, and UI behavior for whatever is being built
- agent `engineer`: Builds features, fixes bugs, and refactors
- agent `marketer`: Handles positioning, audience, copy angles, SEO basics, and reading analytics
- agent `spec-writer`: Turns a goal into a build-ready spec with milestones and acceptance criteria
- agent `test-writer`: Writes tests from the spec or requirements, not from the implementation

### game-team

Game project agents: art-director, artist, playtester. Expects a DESIGN.md at the repo root and a docs/ASSETS.md log.

- agent `art-director`: Owns the visual direction of a game
- agent `artist`: Makes or prepares game assets inside the direction in DESIGN.md, including sprites, icons, UI, textures, VFX specs, and cleanup of third-party assets
- agent `playtester`: Tests a game's rules, loop, and balance by running builds, headless and bot matches, and logs, and by writing plans for human sessions

### web-team

Web project agents: a11y-auditor and tech-writer.

- agent `a11y-auditor`: Audits built UI against WCAG 2.2 AA, including keyboard paths, focus, contrast, labels, and structure
- agent `tech-writer`: Writes and updates technical docs (READMEs, setup guides, API and architecture notes) grounded in the actual code, and runs the commands it documents

### ai-team

AI feature agents: eval-writer, which writes evals under evals/.

- agent `eval-writer`: Builds evals for LLM features, with test cases, rubrics, and pass thresholds, including failure and no-answer cases

*This file is generated by `scripts/build.py`. Edit the kits in build.py and the plugins themselves, not this file.*
