# Prompt caching

Prompt caching is what makes a long Claude Code session affordable and fast: each request reuses the work done for the one before it. The Claude Code team alerts on their cache hit rate and treats a drop as an incident. These are my notes from their post, [Lessons from building Claude Code: Prompt caching is everything](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/) (Thariq Shihipar, April 30, 2026), split into what it changes about how I run a session and what to check when I build something on the Claude API.

Everything here is from the post unless it's marked. **(docs)** is from Anthropic's [prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). **(mine)** is my reading of what the post means for running Claude Code, which the post doesn't say in those words.

## The one rule

The cache is a prefix match. The API caches everything from the start of the request up to each `cache_control` breakpoint, so one change anywhere invalidates everything after it. Content that never changes goes first and content that changes goes last.

Claude Code orders every request this way:

| Layer | What's in it | Shared by |
|---|---|---|
| 1 | Base system prompt and tool definitions | Every session |
| 2 | CLAUDE.md and memory | Every session in the project |
| 3 | Session state: environment, MCP, output style | One session |
| 4 | Conversation messages | Grows each turn |

The team has broken this three ways: a detailed timestamp in the static system prompt, tool definitions sent in a different order each request, and a tool parameter that changed mid-session (which agents the Agent tool could call).

## What it changes in a session

**Don't switch models mid-session.** Caches are per model. The post's example: about 100k tokens into an Opus conversation, a simple question costs more on Haiku than on Opus, because Haiku has to rebuild the whole cache. The cheaper model gets the job as a subagent, with a hand-off message the current model writes. Claude Code's Explore agents run on Haiku this way. This is why [model-by-task](../rules/model-by-task.md) sets the model on the subagent and leaves the main session alone, and the [subagent brief](../prompts/building-with-ai/subagent-brief.md) prompt writes the hand-off.

**Say what changed, don't edit the instructions.** When a fact goes stale (the date, a file I changed), the harness doesn't touch the system prompt. It adds a `<system-reminder>` to the next user message or tool result. CLAUDE.md gets the same treatment from me: it sits in layer 2, ahead of the whole conversation, so it holds what stays true. Status, today's date and the current task go in the chat or a separate file. **(mine)**

**Plan mode and MCP tools are already cache-safe.** Plan mode doesn't swap in a read-only tool list. Every tool stays in every request, `EnterPlanMode` and `ExitPlanMode` are tools themselves, and the mode is described in a message. MCP tools are sent as stubs with only a name and `defer_loading: true`, and the full schema loads when the model finds it through tool search. Nothing for me to do here, except not build the naive version when it's my own agent.

**Compaction is cheap for the same reason.** When the context window fills, a forked call summarizes the conversation. The fork reuses the parent's exact system prompt, context and tools, puts the parent's messages in front, and adds the compaction prompt as one new user message, so it reads the parent's cache. The post's figure puts that read at a tenth of the normal input price and the summary at about 20k tokens.

## When I build on the API

The paste-ready version of this list is the [stable-prompt-prefix](../rules/stable-prompt-prefix.md) rule. The detail behind it:

**Order and breakpoints.** The API renders `tools`, then `system`, then `messages`, and a request takes at most 4 `cache_control` breakpoints. A prefix under the model's minimum length isn't cached and there's no error. **(docs)**

**Things that break the cache without an error.**

| In the prefix | Why it breaks |
|---|---|
| A timestamp, or a request or random ID **(docs)** | Every request is different |
| Tools or JSON serialized in no fixed order **(docs)** | Same content, different bytes |
| A user or session ID in the system prompt **(docs)** | No two users share a prefix |
| System prompt sections added by a flag **(docs)** | Every flag combination is its own prefix |
| A tool list that varies by user or by mode | Tools come first, so nothing after them is shared |

**Updates go in messages.** Mid-conversation, new information is appended to `messages`, in a `<system-reminder>` inside a user message or tool result. On models that support it, a `{"role": "system"}` message appended to `messages` does the same job and can't be forged by user content. **(docs)**

**One tool set and one model per conversation.** A mode is a tool the model calls plus a message describing the mode. A side benefit of plan mode being a tool: the model can enter it on its own when it hits a hard problem. Tools that are rarely needed are deferred, not removed. A cheaper model gets a subagent.

**Forks copy the parent.** Compaction, summaries and skill runs use the parent's system prompt, tools and model exactly, then append their own instruction at the end. A separate "summarize this" call with its own system prompt and no tools shares nothing with the parent from the first token, so the whole conversation is billed at the uncached rate. Leave room in the context window for the compaction message and the summary it writes. The API has [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) built in now, based on this work.

**Watch the hit rate.** The post says a few percentage points of cache misses noticeably change cost and latency. The numbers are in every response's `usage`: `cache_read_input_tokens` (read from cache), `cache_creation_input_tokens` (written to cache) and `input_tokens` (the uncached rest). The full prompt is the sum of the three. In a healthy loop the read number grows each turn and the write number stays small. If reads are zero on a second identical request, something in the prefix changed, and diffing two consecutive request bodies finds it. **(docs)**

**Price and lifetime.** A cache read costs about a tenth of normal input, less on the newest models. A write costs 1.25x normal input for the default 5-minute lifetime and 2x for the 1-hour one, and every read resets the timer. Check the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) for current numbers. **(docs)**
