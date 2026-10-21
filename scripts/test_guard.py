#!/usr/bin/env python3
"""Tests for plugins/guardrails/hooks/guard.py. Run: python3 scripts/test_guard.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent / "plugins" / "guardrails" / "hooks" / "guard.py"


def repo(branch, commit=False):
    d = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", "-b", branch, d], check=True)
    if commit:
        subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return d


def decision(command, cwd):
    payload = json.dumps({"tool_input": {"command": command}, "cwd": cwd})
    out = subprocess.run([sys.executable, str(GUARD)], input=payload,
                         capture_output=True, text=True).stdout.strip()
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"


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
    ]
    failed = 0
    for command, cwd, want in cases:
        got = decision(command, cwd)
        if got != want:
            failed += 1
            print(f"FAIL want {want}, got {got}: {command}")
    print(f"{len(cases) - failed}/{len(cases)} guard cases passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
