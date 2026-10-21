---
name: job-listing-digest
description: Daily digest of new, verified-open product/UX design job postings (Seattle and remote) pulled live from LinkedIn in the browser, deduped against prior runs. Built to run as a daily scheduled task.
---

Search for new design job postings for Joseph, a product/UX designer. This runs fresh daily with no memory of prior runs.

## Config

- Target roles: Senior Product Designer, Product Designer, UX/UI Designer.
- Adjacent titles worth surfacing on a strong match: Product Design Lead, UX Designer, Design Systems Designer, Service Designer, Interaction Designer.
- Locations: Seattle WA and fully remote.
- Dedupe file: `Job_Digest_Seen.txt` next to this skill's scheduled task folder (one URL per line).

## Steps

Do NOT use web search for this. It returns stale, cached job board snippets, and many listings turn out closed. Use the browser tools, which load the live page and let you confirm a listing still accepts applications.

1. Load the Chrome browser tools if they're deferred (`tabs_context_mcp`, `navigate`, `computer`, `read_page`, `browser_batch`, `get_page_text`) and get a tab.

2. Run LinkedIn Jobs searches (the logged-out view is fine) with URLs like:
   - `https://www.linkedin.com/jobs/search/?keywords=Senior%20Product%20Designer&location=Seattle%2C%20Washington%2C%20United%20States&f_TPR=r604800&sortBy=DD`
   - `https://www.linkedin.com/jobs/search/?keywords=Product%20Designer&location=United%20States&f_TPR=r604800&f_WT=2&sortBy=DD` (`f_WT=2` = remote)
   - Vary keywords across target and adjacent titles. `f_TPR=r86400` = past 24 hours (try first), `r604800` = past week (widen if too few).
   - `sortBy=DD` sorts by most recent.

3. For each candidate card, note the "posted X ago" or "Reposted X ago" timestamp as the freshness signal. Use `read_page` (filter: interactive) to pull `/jobs/view/<id>/` links, scrolling the list as needed.

4. Before including a listing, open its clean `https://www.linkedin.com/jobs/view/<id>/` URL and confirm an active "Apply" or "Easy Apply" button and no "no longer accepting applications" notice. Include only listings verified this way.

5. Dedupe: read the dedupe file if it exists and skip postings already in it. After compiling today's list, append the new clean URLs (create the file if needed). If that path isn't reachable from the session, write it to the session's outputs folder and say so.

6. Output new postings only (skip the section if nothing is new). For each: Company, Role, Location, one line on why it fits, and the clean link. Cap at 10, closest matches and freshest first.

Tone: direct, no filler, no em dashes (use commas).
