# job-search

Job search automations, written to run as scheduled tasks in Claude Desktop/Cowork or on demand.

**This is my setup, not a general tool.** The skills are written for me: Seattle and remote product design roles, my tracker at `~/Documents/JobSearch`, my resume and portfolio links. To use them yourself, edit each skill's **Config** section, and replace "Joseph" with your name in the skill text. Install it as a starting point to adapt, not something that works as-is.

| Skill | Runs | Needs |
|---|---|---|
| [job-listing-digest](skills/job-listing-digest/SKILL.md) | Daily | Chrome browser tools |
| [application-tracker-update](skills/application-tracker-update/SKILL.md) | Daily | Gmail, the tracker spreadsheet |
| [interview-prep](skills/interview-prep/SKILL.md) | Daily | Google Calendar, web search |
| [resume-cover-letter-tailoring](skills/resume-cover-letter-tailoring/SKILL.md) | On demand | Your base resume, a job posting |

For one-off job search tasks (decoding a posting, outreach, follow-ups), use the [job-search prompts](../../prompts/job-search/) instead.
