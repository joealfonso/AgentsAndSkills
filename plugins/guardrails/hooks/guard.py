#!/usr/bin/env python3
"""PreToolUse guard for Bash commands.

- Denies pattern-based process killing: pkill, killall, and kill fed by pgrep.
  Stop processes by exact PID instead (rules/kill-by-pid.md).
- Asks for confirmation before any git push that targets main or master
  (rules/git-branch-workflow.md).
- Denies deletes (rm, rmdir, unlink, shred, find -delete, xargs rm, git rm) and
  tells Claude to move the files into _archive/ instead (rules/archive-dont-delete.md).
  Temp paths and regenerable folders (node_modules, dist, build, caches) can still
  be deleted. Add more with GUARDRAILS_DELETE_ALLOW, colon-separated: entries with
  a slash are path prefixes, anything else is a folder name.

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

DELETE_WORDS = {"rm", "rmdir", "unlink", "shred", "srm"}
TEMP_PREFIXES = ("/tmp/", "/private/tmp/", "/var/folders/")
REGENERABLE = {"node_modules", "dist", "build", "__pycache__", ".pytest_cache", ".mypy_cache",
               ".next", ".nuxt", ".turbo", ".cache", ".parcel-cache", "coverage", ".venv"}

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


def delete_allowed(path, cwd):
    """True for temp paths and regenerable folders, which can be deleted outright."""
    extra = [e for e in os.environ.get("GUARDRAILS_DELETE_ALLOW", "").split(":") if e]
    full = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
    prefixes = TEMP_PREFIXES + tuple(os.path.normpath(os.path.expanduser(e)) + "/" for e in extra if "/" in e)
    names = REGENERABLE | {e for e in extra if "/" not in e}
    if (full + "/").startswith(prefixes):
        return True
    return any(part in names for part in full.split(os.sep))


def archive_command(path, cwd, root):
    """The mkdir + mv that archives `path` instead of deleting it."""
    full = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
    rel = os.path.relpath(full, root)
    if rel.startswith(".."):
        dest_dir = os.path.join(os.path.dirname(full), "_archive")
        return f"mkdir -p {shlex.quote(dest_dir)} && mv {shlex.quote(full)} {shlex.quote(dest_dir)}/"
    dest = os.path.join("_archive", rel)
    return f"mkdir -p {shlex.quote(os.path.dirname(dest))} && mv {shlex.quote(rel)} {shlex.quote(dest)}"


def delete_reason(targets, cwd, root):
    lines = ["Blocked: nothing gets deleted. Move it into an _archive/ folder instead, keeping its path:"]
    if targets:
        lines += [f"  {archive_command(t, cwd, root)}" for t in targets]
    else:
        lines.append("  mkdir -p _archive/<dir> && mv <path> _archive/<path>")
        lines.append("List the files this command would remove, then archive each one.")
    lines.append("Temp paths and regenerable folders (node_modules, dist, build, caches) can still be deleted. "
                 "If a real delete is needed, ask the user to run it.")
    return "\n".join(lines)


def delete_targets(word, args):
    """For a delete command, return (is_delete, targets). Empty targets means unknown."""
    if word in DELETE_WORDS:
        targets, after_dashdash = [], False
        for a in args:
            if after_dashdash or not a.startswith("-"):
                targets.append(a)
            elif a == "--":
                after_dashdash = True
        return True, targets
    if word == "find":
        if "-delete" in args:
            return True, [a for a in args[:1] if not a.startswith("-")]
        for i, a in enumerate(args):
            if a in ("-exec", "-execdir", "-ok") and i + 1 < len(args) and os.path.basename(args[i + 1]) in DELETE_WORDS:
                return True, [a for a in args[:1] if not a.startswith("-")]
    if word == "xargs" and any(os.path.basename(a) in DELETE_WORDS for a in args):
        return True, []
    if word == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            i += 2 if args[i] in ("-C", "-c") else 1
        if i < len(args) and args[i] == "rm" and "--cached" not in args[i + 1:]:
            return True, [a for a in args[i + 1:] if not a.startswith("-")]
    return False, []


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
        root = cwd
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
        is_delete, targets = delete_targets(word, args)
        if is_delete:
            blocked = [t for t in targets if not delete_allowed(t, cwd)]
            if not targets or (word == "find" and blocked):
                # find and xargs: the files aren't known until the command runs
                decide("deny", delete_reason([], cwd, root))
            if blocked:
                decide("deny", delete_reason(blocked, cwd, root))
        if word == "cd" and args:
            cwd = os.path.join(cwd, os.path.expanduser(args[0]))
        elif word == "git":
            target = push_target(args, cwd)
            if target:
                decide("ask", f"This pushes to {target}, which may deploy to production. "
                              "Confirm only if you asked for this push.")


if __name__ == "__main__":
    main()
