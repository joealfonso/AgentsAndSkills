# Processes: stop by exact PID, never by pattern

Paste into CLAUDE.md for any project with dev servers, and repeat it in every subagent brief that might restart one.

```markdown
## Stopping processes

Stop processes only by exact PID, never with `pkill -f` or `killall` patterns.

- Find the PID: `lsof -nP -iTCP:<port> -sTCP:LISTEN`
- Kill that PID, then restart the server with its usual command and env vars.
```

**Why:** a subagent ran `pkill -f "src/main.ts" -U <uid> -f`. macOS pkill read the extra words as more patterns and killed the dev server, the game server, another worktree's Vite, Chrome helpers and an MCP server. The restarted server also lost its env flags.
