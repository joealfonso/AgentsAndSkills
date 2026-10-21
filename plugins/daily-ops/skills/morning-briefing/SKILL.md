---
name: morning-briefing
description: Short morning briefing of today's calendar plus unread email that actually needs attention. Built to run as a daily 7am scheduled task.
---

Produce a concise morning briefing for Joseph. This runs fresh each day with no memory of prior runs, so gather everything live.

1. Calendar: use the calendar tools (`list_events` or `search_events`) to pull today's events across all calendars, midnight to midnight local time. List them chronologically with time and title. If there are none, say so.

2. Email: use the Gmail tools (`search_threads`) to find unread threads from roughly the last 24 hours (`is:unread newer_than:1d`). Skim subjects and senders and flag only what looks time-sensitive or important (real people, meeting-related, deadlines). Skip newsletters and promos. Give each flagged thread one line: sender, subject, why it matters.

3. Output: a short, scannable briefing, no more than ~150 words unless a lot is going on.
   - Today's schedule (chronological)
   - Email that needs attention (only the flagged ones)
   - Skip a section entirely if there's nothing in it.

Tone: direct, no filler, no em dashes (use commas). Present the briefing as the response text, no file needed.
