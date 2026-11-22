# Claude API: keep the prompt prefix stable

Paste into CLAUDE.md for any project that builds requests to the Claude API: an agent, a chat feature, a long-running loop.

```markdown
## Prompt caching

The prompt cache is a prefix match: one changed byte invalidates everything after it. When you touch code that builds a request to Claude:

- Order content by how often it changes: tools and the base system prompt first, then per-project context, then per-session context, then messages.
- Nothing that varies per request goes in the system prompt or tool definitions. No timestamps, IDs, user names or sections added by a flag. Serialize tools in a fixed order.
- New information mid-conversation (the date, a changed file, a mode switch) is appended as a message. Never edit the system prompt to deliver it.
- One tool set and one model per conversation. A mode is a tool the model calls plus a message, not a different tool list. Rarely used tools are deferred (`defer_loading`), not removed. A cheaper model gets the job as a subagent with a written brief.
- Side calls (summaries, compaction) copy the parent's system prompt, tools and model exactly, then append their own instruction as the last message.
- After any change to prompt assembly, send the same request twice and check `usage.cache_read_input_tokens` on the second. Zero means the prefix broke.
```

**Why:** cost and speed. These mistakes are the Claude Code team's, not mine: a timestamp in the static system prompt, tool definitions sent in a different order each request, and a tool parameter that changed mid-session each broke their cache. From [their post on prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/); my notes are in [claude-code/prompt-caching.md](https://github.com/joealfonso/AgentsAndSkills/blob/main/claude-code/prompt-caching.md).
