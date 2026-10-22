# Spec: CSV export on the Reports page (v1.0)

*Fictional input for the examples in this folder. A small spec that's ready to build.*

**Status.** Final: everything below. Open: nothing. Column order follows the table and changes with it.

## What

An **Export CSV** button above the Reports table exports exactly the rows and columns the user sees, with current filters and sort applied.

## Rules

- The export runs the same query as the table, so it follows the same row-level permissions. No separate permission check.
- Up to 50,000 rows: the file downloads directly.
- Over 50,000 rows: the button reads "Email me the CSV." The file is built in the background and a link is emailed to the user, valid for 7 days.
- Dates are ISO 8601 in the user's time zone, which is named in the header row. Numbers are unformatted.

## States

- **Empty table:** button disabled, tooltip "Nothing to export with these filters."
- **Building (direct download):** button shows a spinner and stays disabled until the download starts.
- **Error:** toast "Export failed. Try again, or narrow the filters." Nothing is emailed.
- **Background export failed:** email says it failed and links back to the report with the same filters.

## Out of scope

Excel format, scheduled exports, choosing columns.
