#!/usr/bin/env python3
"""Tests for the agent harness: the SubagentStop hook (what it blocks, what it lets through, what it
logs) and scripts/agent_harness.py (cutting rules, checking controls, expiry). No model calls.
Run: python3 scripts/test_agent_harness.py"""
import copy
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_harness as h  # noqa: E402

FAILS = []


def expect(name, got, want):
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def hook(payload, log):
    env = {**os.environ, "AGENT_HARNESS_LOG": str(log)}
    out = subprocess.run([sys.executable, str(h.HOOK)], input=payload, capture_output=True, text=True, env=env)
    return out.returncode, out.stdout.strip()


def stop(agent, msg, retry=False):
    return json.dumps({"agent_type": agent, "last_assistant_message": msg, "stop_hook_active": retry,
                       "agent_id": "a1", "session_id": "s1", "cwd": "/home/dev/shop"})


def test_hook():
    log = Path(tempfile.mkdtemp()) / "usage.jsonl"
    controls = h.load()

    # every block and allow case in controls.json, through the real script
    for c in controls:
        if c["agent"] == "*":
            continue
        for msg in c["block"]:
            expect(f"{c['id']} blocks {msg[-40:]!r}", h.run_hook(c["agent"], msg), "block")
        for msg in c["allow"]:
            expect(f"{c['id']} allows {msg[-40:]!r}", h.run_hook(c["agent"], msg), "allow")

    no_verdict = "1. Missing null check (a.py:3).\n\nOtherwise fine."
    cases = [
        ("plugin-scoped name is still enforced", stop("dev-team:code-reviewer", no_verdict), "block"),
        ("second stop after a block is let through", stop("code-reviewer", no_verdict, retry=True), "allow"),
        ("agents outside ENFORCE are never blocked", stop("engineer", "Built it. Didn't run it."), "allow"),
        ("debugger has verdicts but isn't enforced", stop("debugger", "Cause unclear."), "allow"),
        ("a verdict word mid-sentence isn't a verdict line", stop("code-reviewer", "No FLAGS from me, all good."), "block"),
        ("empty report is blocked", stop("code-reviewer", ""), "block"),
        ("verdict last behind markdown is fine", stop("a11y-auditor", "...\n\n> **FLAGS**: 2"), "allow"),
    ]
    for name, payload, want in cases:
        code, out = hook(payload, log)
        expect(f"{name} (exit code)", code, 0)
        expect(name, "block" if out and json.loads(out)["decision"] == "block" else "allow", want)

    code, out = hook("not json", log)
    expect("bad input exits 0", code, 0)
    expect("bad input prints nothing", out, "")
    code, out = hook(stop("code-reviewer", no_verdict), "/dev/null/cannot/write.jsonl")
    expect("unwritable log still exits 0", code, 0)
    expect("unwritable log still blocks", json.loads(out)["decision"] if out else None, "block")

    # the usage log: one record per stop, with the verdict and whether it came last
    log2 = Path(tempfile.mkdtemp()) / "usage.jsonl"
    hook(stop("dev-team:code-reviewer", "FLAGS\n1. x (a.py:1)\nChecked: y"), log2)
    hook(stop("code-reviewer", "FLAGS\n1. x (a.py:1)\nChecked: y\nFLAGS: 1", retry=True), log2)
    hook(stop("engineer", "Changed a.py. Ran the tests."), log2)
    recs = [json.loads(x) for x in log2.read_text().splitlines()]
    expect("log has one record per stop", len(recs), 3)
    expect("log strips the plugin prefix", recs[0]["agent"], "code-reviewer")
    expect("log keeps a verdict that isn't last", (recs[0]["verdict"], recs[0]["verdict_last"], recs[0]["blocked"]),
           ("FLAGS", False, True))
    expect("log marks the retry", (recs[1]["retry"], recs[1]["verdict_last"], recs[1]["blocked"]), (True, True, False))
    expect("log records agents with no verdict", (recs[2]["verdict"], recs[2]["blocked"]), (None, False))
    expect("log stores the project name, not the path", recs[0]["project"], "shop")
    expect("log stores no report text", any("a.py" in json.dumps(r) for r in recs), False)

    usage = h.usage(recs)
    expect("usage skips retries", usage["code-reviewer"]["runs"], 1)
    expect("usage counts blocks", usage["code-reviewer"]["blocked"], 1)


def test_remove_rule():
    body = "You work.\n\nHow you work:\n\n- Keep it small.\n- Run it.\n\nReport: what changed. Then stop.\n"
    expect("whole bullet goes", h.remove_rule(body, "Keep it small."),
           "You work.\n\nHow you work:\n\n- Run it.\n\nReport: what changed. Then stop.\n")
    expect("sentence inside a line goes", h.remove_rule(body, "Then stop."),
           "You work.\n\nHow you work:\n\n- Keep it small.\n- Run it.\n\nReport: what changed.\n")
    expect("lead-in with nothing under it goes",
           h.remove_rule(h.remove_rule(body, "Keep it small."), "Run it."),
           "You work.\n\nReport: what changed. Then stop.\n")
    agent_file = "---\nname: x\nhooks:\n  Stop:\n    - hooks:\n        - type: command\n---\n\nYou work.\n\nRules:\n\n- Run it.\n"
    expect("cutting from a file leaves the frontmatter alone", h.cut_from_file(agent_file, "Run it."),
           "---\nname: x\nhooks:\n  Stop:\n    - hooks:\n        - type: command\n---\n\nYou work.\n")
    persona = "---\nname: p\n---\n\n# P\n\n**Use for:** x.\n\n## Instruction to paste\n\nYou are P. Be blunt.\n"
    expect("cutting from a persona touches only the instruction", h.cut_from_file(persona, "Be blunt."),
           "---\nname: p\n---\n\n# P\n\n**Use for:** x.\n\n## Instruction to paste\n\nYou are P.\n")
    nums = "Steps:\n\n1. One.\n2. Two.\n3. Three.\n"
    expect("numbered lists renumber", h.remove_rule(nums, "Two."), "Steps:\n\n1. One.\n2. Three.\n")
    for bad in ("Run", "Keep it small.\n- Run it."):
        try:
            h.remove_rule(body + "- Run again.\n", bad)
            FAILS.append(f"remove_rule should refuse {bad!r}")
        except ValueError:
            pass


def test_controls():
    controls, agents = h.load(), h.agents()
    expect("controls.json passes --check", h.check(controls, agents), [])
    for c in controls:
        if c["agent"] == "*":
            continue
        body = agents[c["agent"]]["body"]
        if c.get("baseline"):
            alt = h.ablated(c, body)
            expect(f"{c['id']}: the baseline run has the old wording, not the rule",
                   (c["baseline"] in alt, c["rule"] in alt), (True, False))
        cut = h.remove_rule(body, c["rule"])
        expect(f"{c['id']}: the cut prompt lacks the rule", c["rule"] in cut, False)
        expect(f"{c['id']}: the cut adds nothing", all(ln in body for ln in cut.splitlines()), True)

    def broken(**change):
        bad = copy.deepcopy(controls)
        bad[0].update(change)
        return h.check(bad, agents)

    expect("a rule not in the prompt fails --check", bool(broken(rule="Always be nice.")), True)
    expect("a control with no expiry fails --check", bool(broken(expires={})), True)
    expect("a control with no failure on record fails --check", bool(broken(failure="")), True)
    expect("an allow case the hook blocks fails --check", bool(broken(allow=["no verdict here"])), True)
    expect("a block case the hook allows fails --check", bool(broken(block=["FLAGS: 1"])), True)
    expect("prose with no eval case fails --check", bool(broken(backed_by="prose", block={}, allow={})), True)

    loose = h.audit(controls, agents)
    backed = {c["rule"] for c in controls}
    expect("audit never lists a backed rule", any(r in backed for rules in loose.values() for r in rules), False)
    expect("audit skips the role sentence", any(ln.startswith("You review code") for ln in loose.get("code-reviewer", [])), False)
    expect("after --prune nothing is unbacked", loose, {})


def test_expiry():
    c = next(x for x in h.load() if x["id"] == "code-reviewer.verdict-last")
    run = {"agent": "code-reviewer", "verdict_last": True, "retry": False}
    expect("19 clean runs isn't enough", h.expired(c, [run] * 19, "sonnet"), None)
    expect("20 clean runs expire the hook", h.expired(c, [run] * 20, "sonnet") is not None, True)
    blocked = {**run, "verdict_last": False}
    expect("one blocked run in the last 20 keeps it", h.expired(c, [run] * 19 + [blocked], "sonnet"), None)
    expect("retries don't count as runs", h.expired(c, [run] * 19 + [{**run, "retry": True}], "sonnet"), None)
    c2 = {**c, "proven": {"verdict": "PROVEN", "model": "sonnet", "cases": {
        "block": {"with": 4, "without": 0, "n": 4}, "allow": {"with": 4, "without": 0, "n": 4}}}}
    expect("a passing eval alone doesn't expire a hook", h.expired(c2, [], "sonnet"), None)
    log_c = next(x for x in h.load() if x["id"] == "usage-log")
    expect("the log control is live before its date", h.expired(log_c, [], "sonnet"), None)
    past = {**log_c, "expires": {**log_c["expires"], "date": datetime.date.today().isoformat()}}
    expect("the log control expires on its date", h.expired(past, [], "sonnet") is not None, True)
    prose = {"id": "x", "backed_by": "prose", "expires": {"when": "x", "model_changed": True},
             "proven": {"verdict": "PROVEN", "model": "claude-sonnet-4-5", "cases": {}}}
    expect("a model upgrade expires a prose proof", h.expired(prose, [], "sonnet") is not None, True)


def main():
    for t in (test_hook, test_remove_rule, test_controls, test_expiry):
        t()
    if FAILS:
        print("\n".join(FAILS))
        print(f"{len(FAILS)} failed")
        sys.exit(1)
    print("all agent harness tests pass")


if __name__ == "__main__":
    main()
