---
name: application-tracker-update
description: Scan Gmail for job application activity (confirmations, interviews, rejections, offers) and update the job search tracker spreadsheet. Built to run as a daily scheduled task.
---

Keep Joseph's job search tracker up to date. This runs fresh daily with no memory of prior runs.

## Config

- Tracker file: `~/Documents/JobSearch/Job_Search_Tracker.xlsx`
- "Tracker" sheet columns: Company, Role, Location, Date Applied, Status, Last Update, Source / Link, Next Step, Notes (headers on row 2, data starts row 3).
- Status must be one of: Applied, Screening, Interviewing, Offer, Rejected, Withdrawn.
- A "Dashboard" sheet holds COUNTIF formulas that reference the Tracker sheet. Don't edit those formulas.

## Steps

1. Use the Gmail tools (`search_threads`, `get_thread`, `get_message`) to search recent mail (roughly `newer_than:2d`) for job application activity: new application confirmations, interview invitations or scheduling, rejections, and offers. Look for sender and subject patterns like "application received", "interview", "next steps", "unfortunately", "offer".

2. Load the `xlsx` skill before touching the file, since the dashboard formulas must keep working.

3. Open the tracker with openpyxl. For each relevant email:
   - New company/role not in the sheet: add a row (Company, Role, Location if known, Date Applied if this is a confirmation, Status "Applied", Last Update = today, Source/Link if available, Notes with brief context).
   - Matches an existing row (same company and role): update Status and set Last Update to today. Add a one-line note about what changed.
   - Never delete rows or overwrite Notes. Append to them.

4. Save with openpyxl, then recalculate the Dashboard formulas. The xlsx skill's macro-based `recalc.py` has repeatedly timed out (40s+) in sandboxes. Use this instead:
   ```
   mkdir -p /tmp/loprofile /tmp/converted
   soffice --headless --norestore -env:UserInstallation=file:///tmp/loprofile --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir /tmp/converted "<path to xlsx>"
   ```
   This recalculates and caches values while keeping the formulas. Verify with openpyxl `data_only=False` that formulas are intact and `data_only=True` that Dashboard values are populated with no `#VALUE!`, `#DIV/0!`, `#REF!`, `#NAME?`, `#NULL!`, `#NUM!` or `#N/A`. Then copy the converted file over the original. A stale `.~lock.Job_Search_Tracker.xlsx#` file may refuse to delete; ignore it, it doesn't block reads or writes.

5. Output a short summary of what changed today (rows added, statuses updated), or "no new activity". No em dashes (use commas), direct tone.
