# The Burned-Out Engineer: suggested replies spec

*Output of the [burned-out engineer](../personas/reality-checks/the-burned-out-engineer.md) persona (`review as the burned-out engineer`) on [the suggested replies spec](input-suggested-replies-spec.md). Compare the card's 12 follow-ups: the persona flags only 3, and only where it can name what would force a rebuild.*

---

Is this actually final, or is this the version before the version we'll actually build?

1. **Panel placement is locked, but "No match: TBD" decides whether the panel exists at all.** (Status line; States, No match.) If no-match turns out to mean hiding the panel, the composer reflows on most tickets, since most tickets aren't repeat questions. That's a layout rebuild, not a copy tweak. Settle no-match before calling placement locked.

2. **"Text inserted into the composer is not marked."** (AI labeling.) If anyone later asks for sent replies to say they were AI-assisted, for audit or for the CSAT comparison in Success, the composer has to track which text came from a draft through every edit. That's a change to the composer's data, and it's cheap now and expensive after launch. Decide now, even if the answer is "never."

3. **"Agent opens a ticket. A panel… shows up to 3 drafts."** (Flow, step 1.) The spec doesn't say whether drafts are generated once per ticket and stored, or again on every open. If it's every open, the drafts change under an agent who comes back to a ticket, and at 50% rollout that's three model calls per ticket view. Which one we build changes the storage and the 3-second budget in Loading.

FLAGS
