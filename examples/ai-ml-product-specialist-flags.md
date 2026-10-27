# AI/ML Product Specialist: suggested replies spec

*Output of the [AI/ML product specialist](../personas/design-critique/ai-ml-product-specialist.md) persona (`review as the AI/ML specialist`) on [the suggested replies spec](input-suggested-replies-spec.md). Compare [the burned-out engineer](burned-out-engineer-flags.md): two flags land on the same lines, but this persona asks what the user sees when the model is wrong, not what would force a rebuild.*

---

What does this look like when the model gets it wrong three times in a row?

1. **"No match: TBD."** (States.) For a model that only reads the help center, no matching article is the most common way to be wrong, and it's the one state left undefined. If the model drafts anyway and cites the closest article, an ungrounded answer looks exactly like a good one, and agents will use it. Define what the panel shows when nothing fits before anything else.

2. **"…up to 3 drafts, each citing the help center article it came from."** (Flow, step 1.) All three drafts look equally sure, and nothing tells the agent when a draft strays from its article or the match is weak. Then "Text inserted into the composer is not marked" (AI labeling) drops even the badge once a draft is used, so a wrong answer goes out looking like the agent wrote it.

3. **"Agent can thumbs-down a suggestion, with an optional reason."** (Flow, step 3.) The spec doesn't say what a thumbs-down changes. If the same bad draft comes back on the next password-reset ticket, agents stop rating, then stop reading the panel, and the 20% handle-time drop in Success never shows up. Say what the agent sees change after they reject a draft.

FLAGS
