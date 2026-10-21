#!/usr/bin/env python3
"""PreToolUse guard for Bash commands.

- Denies pattern-based process killing: pkill, killall, and kill fed by pgrep.
  Stop processes by exact PID instead (rules/kill-by-pid.md).
- Asks for confirmation before any git push that targets main or master
  (rules/git-branch-workflow.md).

Reads the hook payload on stdin and prints a permission decision as JSON.
Prints nothing (allow) for every other command, and never fails closed on
input it can't parse.
"""
import json
import os
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "master"}
OPERATORS = re.compile(r"^[;&|()]+$")
PREFIXES = {"sudo", "env", "time", "exec", "nohup", "command"}

KILL_REASON = (
    "Blocked: pattern-based process killing (pkill, killall, pgrep | kill) can take down "
    "unrelated processes. Find the exact PID with `lsof -nP -iTCP:<port> -sTCP:LISTEN` "
    "and run `kill <PID>`, then restart with the server's usual command and env vars."
)


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


def segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    seg = []
    for tok in lexer:
        if OPERATORS.match(tok):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def command_word(seg):
    i = 0
    while i < len(seg) and (seg[i] in PREFIXES or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[i])):
        i += 1
    return (os.path.basename(seg[i]), seg[i + 1:]) if i < len(seg) else (None, [])


def current_branch(cwd):
    try:
        out = subprocess.run(["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except Exception:
        return ""


def push_target(args, cwd):
    """Return the protected branch a `git ... push` would update, or None."""
    while args and args[0] != "push":
        if args[0] == "-C" and len(args) > 1:
            cwd = os.path.join(cwd, os.path.expanduser(args[1]))
            args = args[2:]
        else:
            args = args[1:]
    if not args:
        return None
    rest = args[1:]
    if "--all" in rest or "--mirror" in rest:
        return "every branch"
    positional = []
    skip = False
    for a in rest:
        if skip:
            skip = False
        elif a in ("-o", "--push-option", "--repo", "--receive-pack", "--exec"):
            skip = True
        elif not a.startswith("-"):
            positional.append(a)
    refspecs = positional[1:]
    for ref in refspecs:
        dst = ref.lstrip("+").split(":")[-1]
        dst = dst[len("refs/heads/"):] if dst.startswith("refs/heads/") else dst
        if dst in PROTECTED:
            return dst
        if dst == "HEAD" and current_branch(cwd) in PROTECTED:
            return current_branch(cwd)
    if not refspecs:
        branch = current_branch(cwd)
        if branch in PROTECTED:
            return branch
    return None


def main():
    try:
        payload = json.load(sys.stdin)
        command = payload.get("tool_input", {}).get("command", "")
        cwd = payload.get("cwd") or os.getcwd()
        segs = list(segments(command))
    except Exception:
        return

    words = [command_word(s)[0] for s in segs]
    if any(w in ("pkill", "killall") for w in words):
        decide("deny", KILL_REASON)
    if "pgrep" in command and ("kill" in words or "xargs" in words and "kill" in command):
        decide("deny", KILL_REASON)

    for seg in segs:
        word, args = command_word(seg)
        if word == "cd" and args:
            cwd = os.path.join(cwd, os.path.expanduser(args[0]))
        elif word == "git":
            target = push_target(args, cwd)
            if target:
                decide("ask", f"This pushes to {target}, which may deploy to production. "
                              "Confirm only if you asked for this push.")


if __name__ == "__main__":
    main()
