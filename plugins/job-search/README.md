# job-search

Job search automations, written to run as scheduled tasks in Claude Desktop/Cowork or on demand. Each skill has a **Config** section at the top with the paths and targets to change.

| Skill | Runs | Needs |
|---|---|---|
| [job-listing-digest](skills/job-listing-digest/SKILL.md) | Daily | Chrome browser tools |
| [application-tracker-update](skills/application-tracker-update/SKILL.md) | Daily | Gmail, the tracker spreadsheet |
| [interview-prep](skills/interview-prep/SKILL.md) | Daily | Google Calendar, web search |
| [resume-cover-letter-tailoring](skills/resume-cover-letter-tailoring/SKILL.md) | On demand | Your base resume, a job posting |

For one-off job search tasks (decoding a posting, outreach, follow-ups), use the [job-search prompts](../../prompts/job-search/) instead.
