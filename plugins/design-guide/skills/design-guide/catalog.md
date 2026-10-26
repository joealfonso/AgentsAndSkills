# Catalog

Every resource in the bank, by the stage of the work where it helps. Each line: link · kind · when to use it. Search this file for words from the request.

## Design work

From a fuzzy request to a shipped, defended decision.

### 01 Frame the problem

- [Problem Framing Brief](prompts/design-work/problem-framing-brief.md) · prompt · a new project lands, often as a solution request, and you need to frame the actual problem
- [AI Pitch Reality Check](prompts/ai-product-design/ai-pitch-reality-check.md) · prompt · someone (or you) is proposing an AI feature and you want to test it before roadmap commitment
- [Stakeholder Map](prompts/stakeholders-and-leadership/stakeholder-map.md) · prompt · starting a project with many people who can help or block it
- [Research-First Partner](personas/design-critique/research-first-partner.md) · rehearsal persona · early-stage problem framing, before any UI gets discussed

### 02 Research users

- [Lean Research Plan](prompts/user-research/research-plan.md) · prompt · you need evidence before a decision and have limited time
- [User Interview Guide](prompts/user-research/interview-guide.md) · prompt · you're about to run user or stakeholder interviews
- [Survey Design](prompts/user-research/survey-design.md) · prompt · you need answers from more people than you can interview
- [Field Notes Template](prompts/user-research/field-notes-template.md) · prompt · before each research session, so every note-taker captures the same things, surprises included
- [Research Synthesis](prompts/user-research/research-synthesis.md) · prompt · you have interview notes, test results or transcripts and need findings
- [Anomaly Review](prompts/user-research/anomaly-review.md) · prompt · after synthesis, before sharing findings, to catch what got left out

### 03 Map the service

- [Service Blueprint](prompts/design-work/service-blueprint.md) · prompt · you need to see how a service works end to end, front of house and back, before designing any part of it
- [Service Blueprint Template](templates/service-blueprint.md) · template · you're mapping a service by hand and want the blank structure the blueprint prompts use
- [Blueprint Workshop](prompts/design-work/blueprint-workshop.md) · prompt · you're bringing people together to map a service, and need the right people and a plan that gets the backstage truth
- [Service Blueprint Review](prompts/design-work/service-blueprint-review.md) · prompt · you have a blueprint (yours or someone else's) and want to find what it reveals or hides
- [Future-State Blueprint](prompts/design-work/future-state-blueprint.md) · prompt · you have a current-state blueprint and need to design and justify the improved service

### 04 Design the AI behavior

- [AI Failure Modes](prompts/ai-product-design/ai-failure-modes.md) · prompt · early in designing any AI feature, before the happy path hardens
- [AI Behavior Spec](prompts/ai-product-design/ai-behavior-spec.md) · prompt · you need to tell engineering and the model exactly how an AI feature should behave
- [Human-in-the-Loop Design](prompts/ai-product-design/human-in-the-loop-design.md) · prompt · an AI feature takes or recommends actions with real consequences
- [Uncertainty and Trust](prompts/ai-product-design/uncertainty-and-trust-patterns.md) · prompt · you need to decide how the UI shows confidence, sources and reasoning
- [AI/ML Product Specialist](personas/design-critique/ai-ml-product-specialist.md) · review persona · pressure-testing AI feature design beyond the happy path

### 05 Build with agents

- [Project Brief to SPEC.md](prompts/building-with-ai/project-brief-to-spec.md) · prompt · starting a side project or prototype with a coding agent
- [CLAUDE.md Draft](prompts/building-with-ai/claude-md-draft.md) · prompt · a repo needs agent instructions, or the existing ones are bloated
- [CLAUDE.md Starter](templates/CLAUDE.md) · template · a new project needs agent instructions and you want a short starting point
- [Subagent Brief](prompts/building-with-ai/subagent-brief.md) · prompt · handing a task to another agent or session that starts with no context
- [Prototype Critique](prompts/building-with-ai/prototype-critique.md) · prompt · an agent built something and you need to judge it before iterating
- [Bug Report for an Agent](prompts/building-with-ai/bug-report-for-agent.md) · prompt · something is broken and you want an agent (or engineer) to fix it in one pass

### 06 Critique and quality

- [Design Review Card](frameworks/design-review-card/SKILL.md) · review framework · Fast, repeatable pre-build review of any design (screens, flows, specs, prototypes) using Joseph's Design Review Card. Interactive version: https://josephalfonso.com/AgentsAndSkills/tools/design-review-card.html
- [AI Design Rubric](frameworks/ai-design-rubric/SKILL.md) · review framework · Score AI-generated or AI-assisted design output before it ships with Joseph's AI Design Evaluation Rubric. Interactive version: https://josephalfonso.com/AgentsAndSkills/tools/ai-design-evaluation-rubric.html
- [Edge Case Sweep](prompts/design-work/edge-case-sweep.md) · prompt · before handoff, to find the states and cases nobody designed
- [Accessibility Review](prompts/design-work/accessibility-review.md) · prompt · before handoff or as a QA pass on a built screen
- [UX Copy Pass](prompts/design-work/ux-copy-pass.md) · prompt · screens are designed but the words are placeholder, internal or vague
- [Critique Prep](prompts/design-work/critique-prep.md) · prompt · before you bring work to crit, so you get useful feedback instead of opinions
- [The User Who Hates This](personas/reality-checks/the-user-who-hates-this.md) · review persona · catching the emotional read a usability heuristic would miss

### 07 Test with real users

- [Usability Test Plan](prompts/user-research/usability-test-plan.md) · prompt · you need to see whether people can actually complete tasks in a design or product
- [Rainbow Spreadsheet Setup](prompts/user-research/rainbow-spreadsheet-setup.md) · prompt · you're about to run a usability study and want the rainbow spreadsheet ready before the first session
- [Rainbow Spreadsheet](templates/rainbow-spreadsheet/) · template · you're running a usability study and want one sheet for goals, participants, tasks and observations
- [Rainbow Spreadsheet Analysis](prompts/user-research/rainbow-spreadsheet-analysis.md) · prompt · during a study to log sessions, or after it to turn a filled rainbow spreadsheet into findings

### 08 Ship and defend

- [AI Readiness Review](frameworks/ai-readiness-review/SKILL.md) · review framework · Formal, evidence-based assessment of whether an AI-assisted product experience is fit to ship, using Joseph's AI Readiness Review (AIRR-1.0). Interactive version: https://josephalfonso.com/AgentsAndSkills/tools/ai-readiness-review.html
- [AI Eval Plan](prompts/ai-product-design/ai-eval-plan.md) · prompt · before launch, or when someone claims an AI feature 'works'
- [Design Rationale Doc](prompts/design-work/design-rationale-doc.md) · prompt · you need to document why a design is the way it is, for engineers, stakeholders, or future you
- [Decision Memo](prompts/stakeholders-and-leadership/decision-memo.md) · prompt · a decision is contested or will be questioned later, and you want it written down properly
- [Executive Summary](prompts/stakeholders-and-leadership/exec-summary.md) · prompt · you need to turn a long doc, thread or project into something an exec reads in 60 seconds
- [Cross-functional Eng Lead](personas/stakeholder-leadership/cross-functional-eng-lead.md) · review persona · pressure-testing a spec before it goes to engineering
- [The Burned-Out Engineer](personas/reality-checks/the-burned-out-engineer.md) · review persona · pressure-testing whether a spec actually holds up to implementation reality

## Career

From spotting a role to growing once you're in it.

### 01 Find the right roles

- Job Listing Digest · installed skill `job-listing-digest` from the `job-search` plugin, personal setup · Daily digest of new, verified-open product/UX design job postings (Seattle and remote) pulled live from LinkedIn in the browser, deduped against prior runs
- [Job Posting Decoder](prompts/job-search/job-posting-decoder.md) · prompt · you find a posting and want to know what they actually want before deciding to apply
- [Should I Apply? Scorecard](prompts/job-search/should-i-apply-scorecard.md) · prompt · you have several open roles and limited time, and need to decide where to spend it
- [Company Research Brief](prompts/job-search/company-research-brief.md) · prompt · before an application, a first call, or any interview

### 02 Apply and follow up

- Resume and Cover Letter Tailoring · installed skill `resume-cover-letter-tailoring` from the `job-search` plugin, personal setup · Tailor Joseph's resume and draft a cover letter for a specific job posting (URL or pasted description)
- [Resume Bullet Rewrite](prompts/job-search/resume-bullet-rewrite.md) · prompt · your resume describes what you did instead of what changed because of it
- [Recruiter Outreach](prompts/job-search/recruiter-outreach.md) · prompt · you want to reach out cold or warm about a specific role
- [Referral Ask](prompts/job-search/referral-ask.md) · prompt · someone you know works at a company you're applying to
- Application Tracker Update · installed skill `application-tracker-update` from the `job-search` plugin, personal setup · Scan Gmail for job application activity (confirmations, interviews, rejections, offers) and update the job search tracker spreadsheet
- [Application Follow-Up](prompts/job-search/application-follow-up.md) · prompt · it's been 1-2 weeks since you applied or interviewed with no word

### 03 Tell the story

- [Case Study from Raw Notes](prompts/portfolio-and-case-studies/case-study-from-raw-notes.md) · prompt · you have a project in your head, Slack, and old files, and need a case study outline
- [Impact Metric Finder](prompts/portfolio-and-case-studies/impact-metric-finder.md) · prompt · you know a project mattered but don't have the numbers ready
- [Cut a Case Study in Half](prompts/portfolio-and-case-studies/case-study-cut.md) · prompt · your case study is too long, too process-heavy, or buries the point
- [NDA-Safe Rewrite](prompts/portfolio-and-case-studies/nda-safe-rewrite.md) · prompt · you want to show work covered by confidentiality
- [Project One-Liners](prompts/portfolio-and-case-studies/project-one-liner.md) · prompt · you need a crisp line for a portfolio grid, resume, intro or bio
- [Portfolio Site Review](prompts/portfolio-and-case-studies/portfolio-site-review.md) · prompt · before sending your portfolio to anyone important
- [Strict Senior Product Designer](personas/design-critique/strict-senior-product-designer.md) · review persona · case studies, portfolio decks, design rationale, anything going external

### 04 Interview

- Interview Prep · installed skill `interview-prep` from the `job-search` plugin, personal setup · Check the calendar for job interviews in the next 48 hours and prep a short research brief for each (company context, likely questions, talking points)
- [Story Bank Builder](prompts/interviewing/story-bank-builder.md) · prompt · you're preparing for interviews and want 8-10 reusable stories ready to go
- [Portfolio Presentation Script](prompts/interviewing/portfolio-presentation-script.md) · prompt · you have a 45-60 minute portfolio review and need a structure and talk track
- [Design Exercise Prep](prompts/interviewing/design-exercise-prep.md) · prompt · you have a live design challenge or take-home coming up
- [Mock Interview](prompts/interviewing/mock-interview.md) · prompt · you want a realistic practice round with honest scoring
- [Questions to Ask](prompts/interviewing/questions-to-ask.md) · prompt · the end of any interview round
- [Skeptical Hiring Manager](personas/design-critique/skeptical-hiring-manager.md) · review persona · resume review, portfolio walkthroughs, interview answer prep

### 05 Negotiate the offer

- [Offer Comparison](prompts/offers-and-negotiation/offer-comparison.md) · prompt · you have one or more offers (or an offer versus staying) and need to compare them honestly
- [Counter-Offer](prompts/offers-and-negotiation/counter-offer.md) · prompt · you have an offer and want to negotiate it
- [Compensation Negotiator](personas/interviewing/compensation-negotiator.md) · rehearsal persona · offer conversations, practicing holding a number under pushback
- [Accept or Decline](prompts/offers-and-negotiation/accept-or-decline.md) · prompt · you've decided and need to tell them, or tell the other companies
- [Resignation Plan](prompts/offers-and-negotiation/resignation.md) · prompt · you're leaving a job and want to leave it well

### 06 Grow in the role

- [First 90 Days](prompts/career-growth/first-90-days.md) · prompt · you've accepted a new role and want to start well
- [Brag Doc Entry](prompts/career-growth/brag-doc-entry.md) · prompt · end of each week, 5 minutes, so review season isn't archaeology
- [Career Check-In](prompts/career-growth/career-check-in.md) · prompt · every quarter, to make sure your work is going where you want
- [Self-Review](prompts/career-growth/self-review.md) · prompt · review season
- [Promotion Case](prompts/career-growth/promotion-case.md) · prompt · you're aiming for the next level and need to make the case, or help your manager make it
- [Skill Gap Audit](prompts/career-growth/skill-gap-audit.md) · prompt · you're aiming at a type of role (e.g. AI design lead, design director) and want to know what's missing

### 07 Lead and teach

- [Feedback on Junior Work](prompts/mentoring-and-teaching/feedback-on-junior-work.md) · prompt · reviewing a mentee's or report's work and you want feedback that teaches
- [Explain It Plainly](prompts/mentoring-and-teaching/explain-plainly.md) · prompt · teaching a junior designer, a stakeholder, or a class something you know well
- [Learning Plan](prompts/mentoring-and-teaching/learning-plan.md) · prompt · you or a mentee need to get competent at something new, fast
- [Workshop Outline](prompts/mentoring-and-teaching/workshop-outline.md) · prompt · teaching a session, running a team workshop, or giving a lunch-and-learn
- [The New Manager You're Coaching](personas/stakeholder-leadership/the-new-manager-youre-coaching.md) · rehearsal persona · practicing coaching rather than solving, fits an educator-for-junior-staff role

### 08 Be visible

- Write Like Joseph · installed skill `write-like-joseph` from the `writing` plugin, personal setup · Use whenever Joseph wants anything written or rewritten: emails, posts, messages, bios, case studies, drafts
- [LinkedIn Post](prompts/writing-and-visibility/linkedin-post.md) · prompt · you learned or shipped something worth sharing and want a post that doesn't sound like LinkedIn
- [Article Outline](prompts/writing-and-visibility/article-outline.md) · prompt · you have an argument to write up, for your site, Medium, or a publication
- [Talk Proposal](prompts/writing-and-visibility/talk-proposal.md) · prompt · submitting to a design, AI or product conference
- [Bio Variants](prompts/writing-and-visibility/bio-variants.md) · prompt · you need a bio for a talk, a podcast, a site, or an intro
- [Claim Checker](prompts/writing-and-visibility/claim-checker.md) · prompt · before publishing anything with factual claims, numbers or citations

## Also in the bank

Not placed in a stage, still worth matching.

- [Behavioral answer tightener](prompts/interviewing/answer-tightener.md) · prompt · you've drafted or recorded an answer and it runs long or wanders
- [Post-interview debrief](prompts/interviewing/post-interview-debrief.md) · prompt · right after an interview, while it's fresh
- [Replying to a rejection](prompts/job-search/rejection-reply.md) · prompt · you got a no and want to keep the door open or learn something
- [Career conversation with a mentee](prompts/mentoring-and-teaching/career-conversation.md) · prompt · a mentee or report wants to talk about where they're headed
- [Visual inspiration assistant](prompts/projects/visual-inspiration-assistant.md) · prompt · setting up a Claude Project that captures, tags and searches design inspiration
- [Difficult conversation prep](prompts/stakeholders-and-leadership/difficult-conversation.md) · prompt · conflict, delivering hard feedback, or a conversation you've been avoiding
- [Disagreeing with a stakeholder productively](prompts/stakeholders-and-leadership/disagree-and-redirect.md) · prompt · a stakeholder wants something you think is wrong, and you need to say so without losing them
- [Meeting prep](prompts/stakeholders-and-leadership/meeting-prep.md) · prompt · an important meeting where you need an outcome, not just attendance
- [1:1 with my manager](prompts/stakeholders-and-leadership/one-on-one-prep.md) · prompt · regular 1:1s, so they cover what matters instead of status
- [Status update](prompts/stakeholders-and-leadership/status-update.md) · prompt · weekly or project updates that people actually read
- [Newsletter issue](prompts/writing-and-visibility/newsletter-issue.md) · prompt · writing a recurring note to your audience
- [Enterprise Stakeholder (Non-Design)](personas/design-critique/enterprise-stakeholder-non-design.md) · review persona · translating design decisions into business language before an exec review
- [Junior Designer You're Mentoring](personas/design-critique/junior-designer-youre-mentoring.md) · rehearsal persona · stress-testing whether you can actually teach a concept, not just do it
- [Competing Candidate](personas/interviewing/competing-candidate.md) · rehearsal persona · sharpening what's actually differentiated before a final round
- [Skeptical Recruiter (Screen-stage)](personas/interviewing/skeptical-recruiter-screen-stage.md) · rehearsal persona · practicing the initial phone screen, "walk me through your background."
- [The Silent Skeptic](personas/reality-checks/the-silent-skeptic.md) · review persona · finding where a presentation or narrative loses people before they even ask a question
- [Your Own Portfolio Reviewer, Six Months Later](personas/reality-checks/your-own-portfolio-reviewer-six-months-later.md) · review persona · catching decisions you made for expedience that you're not actually proud of
- [Board-Level Narrative Partner](personas/stakeholder-leadership/board-level-narrative-partner.md) · review persona · compressing a quarter of work into a short, decision-relevant story
- [Finance / Ops Stakeholder](personas/stakeholder-leadership/finance-ops-stakeholder.md) · review persona · framing design work in terms leadership tracks at scale
- [Skeptical VP / Exec Sponsor](personas/stakeholder-leadership/skeptical-vp-exec-sponsor.md) · rehearsal persona · roadmap defense, exec-facing decks, anything that needs to land in one breath
- [Skip-Level Manager](personas/stakeholder-leadership/skip-level-manager.md) · rehearsal persona · practicing upward communication above your direct manager
- kb-curator · installed skill `kb-curator` from the `daily-ops` plugin, personal setup · Weekly maintenance pass on the personal knowledge base MCP: archive clear duplicates, normalize tags, flag stale items for review
- morning-briefing · installed skill `morning-briefing` from the `daily-ops` plugin, personal setup · Short morning briefing of today's calendar plus unread email that actually needs attention
- [Files: archive, don't delete](rules/archive-dont-delete.md) · CLAUDE.md rule · Paste into CLAUDE.md for any project where losing a file would hurt
- [Git: branches and PRs, never straight to main](rules/git-branch-workflow.md) · CLAUDE.md rule · Paste into a project's CLAUDE.md when `main` deploys to production
- [Processes: stop by exact PID, never by pattern](rules/kill-by-pid.md) · CLAUDE.md rule · Paste into CLAUDE.md for any project with dev servers, and repeat it in every subagent brief that might restart one
- [Agents: pick the model by the job](rules/model-by-task.md) · CLAUDE.md rule · Paste into CLAUDE.md for any project that uses subagents or background sessions
- [Data: remove features you can't make reliable](rules/remove-unreliable-features.md) · CLAUDE.md rule · Paste into CLAUDE.md for data-driven products
- [UI: check layouts at every width before calling it done](rules/responsive-overlap-check.md) · CLAUDE.md rule · Paste into a front-end project's CLAUDE.md

*This file is generated by `scripts/build.py`. Edit the sources, not this file.*
