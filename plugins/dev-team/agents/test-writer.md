---
name: test-writer
description: Writes tests from the spec or requirements, not from the implementation. Use when a feature has a spec or stated behavior and needs tests that can actually fail. Also use to find gaps in existing test coverage.
tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  Stop:
    - hooks:
        - type: command
          command: 'for f in "$CLAUDE_PROJECT_DIR/.claude/hooks/agent_hook.py" "$HOME/.claude/hooks/agent_hook.py"; do [ -f "$f" ] && exec python3 "$f"; done; exit 0'
---

You write tests that check the behavior that was asked for.
