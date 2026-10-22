#!/usr/bin/env python3
"""PreToolUse guard for Bash commands.

- Denies pattern-based and bulk process killing: pkill, killall, kill fed by
  pgrep, pidof or ps | grep, xargs kill, and kill -1 or a process group.
  Stop processes by exact PID instead (rules/kill-by-pid.md).
- Asks for confirmation before any git push that targets main or master
  (rules/git-branch-workflow.md).
- Denies deletes (rm, rmdir, unlink, shred, find -delete, xargs rm, git rm) and
  tells Claude to move the files into _archive/ instead (rules/archive-dont-delete.md).
  Temp paths and regenerable folders (node_modules, dist, build, caches) can still
  be deleted. Add more with GUARDRAILS_DELETE_ALLOW, colon-separated: entries with
  a slash are path prefixes, anything else is a folder name.
- Denies git commands that throw away uncommitted work or stashes: git clean,
  reset --hard, checkout -- / . / -f, restore (worktree), switch -f, stash drop/clear.

Commands wrapped in bash -c, sh -c, zsh -c or eval are checked as if run directly.

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

SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
MAX_DEPTH = 5

KILL_REASON = (
    "Blocked: pattern-based or bulk process killing (pkill, killall, pgrep or ps | grep feeding kill, "
    "xargs kill, kill -1 or a process group) can take down unrelated processes. Find the exact PID with "
    "`lsof -nP -iTCP:<port> -sTCP:LISTEN` and run `kill <PID>`, then restart with the server's usual "
    "command and env vars."
)

GIT_DISCARD_FIX = {
    "clean": "List the files with `git clean -n`, then move the ones that should go into _archive/.",
    "reset": "Save the work first with `git stash push -u -m \"<why>\"`, or use `git reset --keep`, "
             "which refuses to drop local changes.",
    "checkout": "Save the work first with `git stash push -u -m \"<why>\"`; it stays recoverable in `git stash list`.",
    "restore": "Save the work first with `git stash push -u -m \"<why>\"`; it stays recoverable in `git stash list`.",
    "switch": "Save the work first with `git stash push -u -m \"<why>\"`, then switch without forcing.",
    "stash": "Leave the stash where it is; it costs nothing.",
}


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


def wrapped_command(word, args):
    """The command string run by `bash -c '...'`, `sh -lc '...'` or `eval ...`, or None."""
    if word == "eval":
        return " ".join(args) or None
    if word in SHELLS:
        has_c = False
        for a in args:
            if a.startswith("-") and not a.startswith("--"):
                has_c = has_c or "c" in a[1:]
            elif not a.startswith("-"):
                return a if has_c else None
    return None


def expand(command, depth=0):
    """Segments of the command, with the body of each shell wrapper split into segments of its own."""
    for seg in segments(command):
        inner = wrapped_command(*command_word(seg))
        if inner is None or depth >= MAX_DEPTH:
            yield seg
            continue
        try:
            inner_segs = list(expand(inner, depth + 1))
        except ValueError:
            inner_segs = [seg]
        yield from inner_segs


def broad_kill(args):
    """True when kill targets every process (-1), a process group (-<pgid>) or its own group (0)."""
    i = 0
    if args and args[0] in ("-s", "-n"):
        i = 2
    elif args and args[0].startswith("-") and args[0] != "--":
        i = 1
    targets = [a for a in args[i:] if a != "--"]
    return any(re.match(r"^-\d+$", t) or t == "0" for t in targets)


def kill_blocked(command, segs):
    words = [command_word(s)[0] for s in segs]
    if any(w in ("pkill", "killall") for w in words):
        return True
    for seg in segs:
        word, args = command_word(seg)
        if word == "kill" and broad_kill(args):
            return True
        if word == "xargs" and any(os.path.basename(a) == "kill" for a in args):
            return True
    lookup = re.search(r"\b(pgrep|pidof)\b", command) or ("ps" in words and ("grep" in words or "awk" in words))
    return bool(lookup and "kill" in words)


def git_subcommand(args):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in ("-C", "-c") else 1
    return (args[i], args[i + 1:]) if i < len(args) else (None, [])


def git_discard(args):
    """The git subcommand if this call throws away uncommitted work or stashes, else None."""
    sub, rest = git_subcommand(args)
    flags = lambda *names: any(a in names for a in rest)
    if sub == "clean":
        dry = any(a == "--dry-run" or (a.startswith("-") and not a.startswith("--") and "n" in a[1:]) for a in rest)
        return None if dry else sub
    if sub == "reset" and flags("--hard"):
        return sub
    if sub == "checkout" and flags("--", ".", "-f", "--force"):
        return sub
    if sub == "restore" and not (flags("--staged", "-S") and not flags("--worktree", "-W")):
        return sub
    if sub == "switch" and flags("-f", "--force", "--discard-changes"):
        return sub
    if sub == "stash" and rest[:1] in (["drop"], ["clear"]):
        return sub
    return None


def git_discard_reason(sub):
    return (f"Blocked: `git {sub}` here throws away work that may not be committed or stashed, "
            f"and it can't be undone. {GIT_DISCARD_FIX[sub]} If discarding is really what's wanted, "
            "ask the user to run it.")


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
        sub, rest = git_subcommand(args)
        if sub == "rm" and "--cached" not in rest:
            return True, [a for a in rest if not a.startswith("-")]
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
        segs = list(expand(command))
    except Exception:
        return

    if kill_blocked(command, segs):
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
            discarded = git_discard(args)
            if discarded:
                decide("deny", git_discard_reason(discarded))
            target = push_target(args, cwd)
            if target:
                decide("ask", f"This pushes to {target}, which may deploy to production. "
                              "Confirm only if you asked for this push.")


if __name__ == "__main__":
    main()
