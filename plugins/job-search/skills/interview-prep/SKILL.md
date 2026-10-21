---
name: interview-prep
description: Check the calendar for job interviews in the next 48 hours and prep a short research brief for each (company context, likely questions, talking points). Built to run as a daily scheduled task.
---

Check whether Joseph has job interviews coming up and prep him for them. This runs fresh daily with no memory of prior runs.

## Config

- Resume folder (optional): `~/Documents/JobSearch` (any file with "Resume" in the name)

## Steps

1. Use the calendar tools (`list_events` or `search_events`) to look at events in the next 48 hours. Identify any that look like job interviews (title or description containing "interview", a company name plus "chat"/"call"/"screen", or similar signals).

2. If none are found, say so briefly and stop.

3. For each interview, research the company and role with web search: what the company does, recent news, the role's likely focus, and 2-3 questions they're likely to ask given the role. Keep research proportional, a few searches per interview.

4. Optionally personalize: if a resume exists in the resume folder, read it and tie 1-2 talking points to Joseph's actual background. If not, skip this step.

5. Output, for each interview: company/role, interview time, 3-4 bullets of company/role context, 2-3 likely questions, and 1-2 suggested talking points. Under ~150 words each. Direct tone, no em dashes (use commas), no filler.
