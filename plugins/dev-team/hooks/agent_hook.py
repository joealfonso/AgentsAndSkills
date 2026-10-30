#!/usr/bin/env python3
"""SubagentStop hook for the agents in this repo.

1. Logs every run (agent, verdict, whether it was blocked) to ~/.claude/agent-harness/usage.jsonl,
   or $AGENT_HARNESS_LOG, so scripts/agent_harness.py --usage can show how the agents are really used.
2. For agents in ENFORCE, blocks the stop once if the report's last line isn't the verdict.
   Each entry is a control in harness/controls.json, with the failure it came from and when it expires.

Never fails loudly: bad input or a logging error exits 0 with no output.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path

VERDICTS = {
    "code-reviewer": ("FLAGS", "CLEAN FROM THIS SEAT", "CAN'T JUDGE"),
    "a11y-auditor": ("FLAGS", "CLEAN FROM THIS SEAT", "CAN'T JUDGE"),
    "playtester": ("FINDINGS", "CLEAN FROM THIS SEAT", "CAN'T JUDGE"),
    "debugger": ("CONFIRMED", "LIKELY", "CAN'T REPRODUCE"),
}
ENFORCE = {"code-reviewer", "a11y-auditor"}


def verdict_of(agent, text):
    """(verdict found anywhere, whether the last line is the verdict)."""
    tokens = VERDICTS.get(agent)
    if not tokens:
        return None, None
    text = text.replace("’", "'")
    pat = r"^[\s*#>`_\-]*(" + "|".join(re.escape(t) for t in tokens) + r")\b"
    lines = [ln for ln in text.splitlines() if ln.strip()]
    last = re.match(pat, lines[-1]) if lines else None
    if last:
        return last.group(1), True
    anywhere = next((m.group(1) for ln in lines if (m := re.match(pat, ln))), None)
    return anywhere, False


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    agent = str(data.get("agent_type") or "").split(":")[-1]
    text = data.get("last_assistant_message") or ""
    retry = bool(data.get("stop_hook_active"))
    verdict, last = verdict_of(agent, text)
    block = agent in ENFORCE and last is False and not retry

    record = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "agent": agent, "agent_id": data.get("agent_id"), "session_id": data.get("session_id"),
              "project": Path(data.get("cwd") or ".").name, "verdict": verdict, "verdict_last": last,
              "blocked": block, "retry": retry, "chars": len(text)}
    try:
        log = Path(os.environ.get("AGENT_HARNESS_LOG") or Path.home() / ".claude" / "agent-harness" / "usage.jsonl")
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass

    if block:
        tokens = VERDICTS[agent]
        print(json.dumps({"decision": "block", "reason":
              f"Make the last line of your report the verdict: {tokens[0]} (how many), "
              f"{tokens[1]} (one sentence on what you checked) or {tokens[2]} (what's missing). "
              "Add only that line. Don't repeat the report."}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
