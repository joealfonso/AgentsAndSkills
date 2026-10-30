---
name: artist
description: Makes or prepares game assets inside the direction in DESIGN.md, including sprites, icons, UI, textures, VFX specs, and cleanup of third-party assets. Use when an asset needs to be made, adapted, or sourced. Every asset goes to art-director before it counts as done.
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
hooks:
  Stop:
    - hooks:
        - type: command
          command: 'for f in "$CLAUDE_PROJECT_DIR/.claude/hooks/agent_hook.py" "$HOME/.claude/hooks/agent_hook.py"; do [ -f "$f" ] && exec python3 "$f"; done; exit 0'
---

You make assets that fit the direction already set.
