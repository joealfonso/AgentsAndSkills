#!/usr/bin/env python3
"""Tests for plugins/guardrails/hooks/guard.py. Run: python3 scripts/test_guard.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent / "plugins" / "guardrails" / "hooks" / "guard.py"
PROJ = "/home/dev/project"  # never touched on disk; delete checks only compute paths


def repo(branch, commit=False):
    d = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", "-b", branch, d], check=True)
    if commit:
        subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return d


def run_guard(command, cwd, env=None):
    payload = json.dumps({"tool_input": {"command": command}, "cwd": cwd})
    out = subprocess.run([sys.executable, str(GUARD)], input=payload, capture_output=True, text=True,
                         env={**os.environ, **(env or {})}).stdout.strip()
    if not out:
        return "allow", ""
    spec = json.loads(out)["hookSpecificOutput"]
    return spec["permissionDecision"], spec["permissionDecisionReason"]


def decision(command, cwd, env=None):
    return run_guard(command, cwd, env)[0]


def main():
    feat, main_, main_c = repo("feature"), repo("main"), repo("main", commit=True)
    cases = [
        ('pkill -f "src/main.ts" -U 501 -f', feat, "deny"),
        ("sudo killall node", feat, "deny"),
        ("kill $(pgrep -f vite)", feat, "deny"),
        ("pgrep -f vite | xargs kill", feat, "deny"),
        ("lsof -nP -iTCP:8080 -sTCP:LISTEN", feat, "allow"),
        ("kill 4242", feat, "allow"),
        ('git commit -m "never use pkill or killall"', feat, "allow"),
        ("pgrep -f vite", feat, "allow"),
        ("git push", main_, "ask"),
        ("git push origin", main_, "ask"),
        ("git push", main_c, "ask"),
        ("git push origin HEAD", main_c, "ask"),
        ("git push", feat, "allow"),
        ("git push -u origin feature", main_, "allow"),
        ("git push origin main", feat, "ask"),
        ("git push origin HEAD:main", feat, "ask"),
        ("git push origin +refs/heads/master", feat, "ask"),
        ("git push --all", feat, "ask"),
        (f"cd {main_} && git push", feat, "ask"),
        (f"git -C {main_} push", feat, "ask"),
        ("git push origin feature:feature", feat, "allow"),
        ("git status && git log", main_, "allow"),
        ('echo "unterminated', main_, "allow"),
        ("git push", "/nonexistent", "allow"),
        # deletes: a project path outside temp folders, so the temp allowance doesn't apply
        ("rm notes.md", PROJ, "deny"),
        ("rm -rf src/old", PROJ, "deny"),
        ("sudo rm -f a.txt", PROJ, "deny"),
        ("rmdir empty-dir", PROJ, "deny"),
        ("unlink old-link", PROJ, "deny"),
        ("shred -u secrets.txt", PROJ, "deny"),
        ("find . -name '*.bak' -delete", PROJ, "deny"),
        ("find . -name x -exec rm {} \\;", PROJ, "deny"),
        ("ls *.log | xargs rm", PROJ, "deny"),
        ("git rm old.md", PROJ, "deny"),
        ("git -C sub rm -r legacy", PROJ, "deny"),
        ("cd docs && rm a.md", PROJ, "deny"),
        ("rm -rf node_modules src", PROJ, "deny"),
        ("rm -- -weird-name", PROJ, "deny"),
        ("rm -rf $BUILD_DIR", PROJ, "deny"),
        ("rm -rf node_modules", PROJ, "allow"),
        ("rm -rf dist build .next", PROJ, "allow"),
        ("rm -rf packages/web/node_modules", PROJ, "allow"),
        ("find . -name __pycache__ -exec rm -rf {} +", PROJ, "deny"),
        ("find node_modules -name '*.map' -delete", PROJ, "allow"),
        ("rm -rf /tmp/scratch", PROJ, "allow"),
        ("rm -f /private/tmp/claude/out.png", PROJ, "allow"),
        ("git rm --cached secrets.env", PROJ, "allow"),
        ('echo "rm -rf /"', PROJ, "allow"),
        ('git commit -m "stop using rm"', PROJ, "allow"),
        ("mkdir -p _archive && mv notes.md _archive/notes.md", PROJ, "allow"),
        ("find . -name '*.py'", PROJ, "allow"),
        ("trash notes.md", PROJ, "allow"),
    ]
    env_cases = [
        ("rm -rf .drafts", PROJ, {"GUARDRAILS_DELETE_ALLOW": ".drafts"}, "allow"),
        ("rm -rf /data/exports/old", PROJ, {"GUARDRAILS_DELETE_ALLOW": "/data/exports"}, "allow"),
        ("rm -rf /data/other", PROJ, {"GUARDRAILS_DELETE_ALLOW": "/data/exports"}, "deny"),
    ]
    reason_cases = [
        ("rm notes.md", PROJ, "mkdir -p _archive && mv notes.md _archive/notes.md"),
        ("rm -r src/old", PROJ, "mkdir -p _archive/src && mv src/old _archive/src/old"),
        ("cd docs && rm a.md", PROJ, "mkdir -p _archive/docs && mv docs/a.md _archive/docs/a.md"),
        ("rm /elsewhere/x.txt", PROJ, "mkdir -p /elsewhere/_archive && mv /elsewhere/x.txt /elsewhere/_archive/"),
        ("rm -rf node_modules src", PROJ, "mv src _archive/src"),
    ]
    failed = 0
    for command, cwd, want in cases:
        got = decision(command, cwd)
        if got != want:
            failed += 1
            print(f"FAIL want {want}, got {got}: {command}")
    for command, cwd, env, want in env_cases:
        got = decision(command, cwd, env)
        if got != want:
            failed += 1
            print(f"FAIL want {want}, got {got}: {command} with {env}")
    for command, cwd, snippet in reason_cases:
        got, reason = run_guard(command, cwd)
        if got != "deny" or snippet not in reason:
            failed += 1
            print(f"FAIL reason for {command!r} should include {snippet!r}, got: {reason!r}")
    if "node_modules" in run_guard("rm -rf node_modules src", PROJ)[1].split("Temp paths")[0]:
        failed += 1
        print("FAIL archive suggestion should skip the regenerable folder")
    total = len(cases) + len(env_cases) + len(reason_cases) + 1
    print(f"{total - failed}/{total} guard cases passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
