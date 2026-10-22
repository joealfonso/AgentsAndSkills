---
name: kb-curator
description: Weekly maintenance pass on the personal knowledge base MCP: archive clear duplicates, normalize tags, flag stale items for review. Never deletes; archived items stay searchable and can be restored.
---

Run a weekly maintenance pass on Joseph's personal knowledge base (the `kb_personal` MCP tools: `kb_list_items`, `kb_search`, `kb_list_tags`, `kb_get_item`, `kb_update_item`, `kb_bulk_tag`, `kb_stats`). This runs fresh each week with no memory of prior runs.

Never call `kb_delete_item`. A delete can't be undone; an archive tag can. This follows [archive-dont-delete](../../../../rules/archive-dont-delete.md).

1. Overview: call `kb_stats`, `kb_list_items` and `kb_list_tags` to see the current state.

2. Duplicates: scan for near-duplicate titles or content on the same topic, skipping items already tagged `archived`. For clear, unambiguous duplicates, keep the more complete or recent item. Copy anything the other item has that the kept one lacks into the kept item with `kb_update_item`. Then archive the other one: add the tag `archived` and a first line reading `Archived <date>: duplicate of <kept item's title>`. If it's ambiguous, change nothing and flag the pair in the report.

3. Tag hygiene: find inconsistent, redundant or overly narrow tags (near-identical tags with different casing or spelling) and normalize them with `kb_bulk_tag`.

4. Stale items: flag items that look outdated (superseded information, old time-bound notes with no lasting value) based on content and timestamps. Don't archive these, list them for review.

5. Output a short report, ~200 words max unless there's a lot:
   - Actions taken (duplicates archived, with each kept and archived title, and tags normalized) with counts
   - Items flagged for review, each with name and a one-line reason
   - KB size and tag count after cleanup

Tone: direct, no filler, no em dashes (use commas). Be conservative: when in doubt, flag rather than archive.
