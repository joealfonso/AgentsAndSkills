#!/usr/bin/env python3
"""The agent harness: controls for the subagents in plugins/*/agents/, each one earned by a real failure.

harness/controls.json is the whole harness. A control is one rule plus what backs it:
  failure    the real run where an agent got it wrong (no failure on record, no control)
  backed_by  "prose" (only the prompt), or the hook/script that enforces it
  block      a case the control must catch
  allow      a case it must let through, so it can't pass by blocking everything
  proven     the last eval: model, date, pass rate with the rule and with it cut
  expires    the condition that makes it dead weight, checked by --expired. A hook expires on real logged
             runs, never on --eval: short eval cases pass where long real runs fail

  python3 scripts/agent_harness.py --check     static, no model: every control is well formed, its rule is
                                               in the prompt word for word, hook controls block what they
                                               should and allow what they should
  python3 scripts/agent_harness.py --audit     prompt lines no control backs: rules nobody has proven
  python3 scripts/agent_harness.py --prune     delete those lines from their source files, then run build.py
  python3 scripts/agent_harness.py --eval [ID] [-n 4]
                                               run each control's block and allow case n times with the rule
                                               and n times with it cut; writes the result into "proven"
  python3 scripts/agent_harness.py --smoke     one run of every block and allow case that last passed;
                                               fails on a regression (use after a model upgrade)
  python3 scripts/agent_harness.py --usage     what the agents did in real sessions, from the hook's log
  python3 scripts/agent_harness.py --sessions  the same from past session transcripts, including runs from
                                               before the hook: final reports and the tools each agent used
  python3 scripts/agent_harness.py --expired   controls whose expiry condition now holds
  python3 scripts/agent_harness.py --garden    all of the above in one pass; run it every few weeks

--eval and --smoke call `claude -p` in safe mode, so your CLAUDE.md, plugins, hooks and MCP servers
stay out of the results. They need a logged-in `claude`.
"""
import argparse
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = ROOT / "harness" / "controls.json"
BUILD = ROOT / "scripts" / "build.py"
PERSONAS = ROOT / "personas"
HOOK = ROOT / "plugins" / "dev-team" / "hooks" / "agent_hook.py"
SESSIONS = Path.home() / ".claude" / "projects"
LOG = Path(os.environ.get("AGENT_HARNESS_LOG") or Path.home() / ".claude" / "agent-harness" / "usage.jsonl")

PASS_WITH = 0.75   # follows the rule in at least this share of runs with it in the prompt
MARGIN = 0.5       # and at least this much more often than with the rule cut

LIST_ITEM = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
JUDGE_SYSTEM = """You grade one output from an AI agent against one yes/no question. Answer it strictly and
literally; don't grade overall quality. Reply with only JSON: {"pass": true or false, "why": "one sentence"}"""


# ---- prompts and rules ----

def split_front(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith(" "):
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[m.end():]


def agents():
    out = {}
    for f in sorted(ROOT.glob("plugins/*/agents/*.md")):
        meta, body = split_front(f.read_text())
        out[meta["name"]] = {"file": f, "meta": meta, "body": body.strip() + "\n",
                             "generated": f.parent.parent.name == "review-personas"}
    return out


def preamble():
    return re.search(r'AGENT_PREAMBLE = """(.*?)\n', BUILD.read_text()).group(1)


def remove_rule(text, rule):
    """Cut one rule (a whole list item or a sentence inside a line) and tidy what's left."""
    if "\n" in rule or text.count(rule) != 1:
        raise ValueError(f"rule must appear exactly once on one line: {rule[:60]!r}")
    lines = text.split("\n")
    i = next(i for i, ln in enumerate(lines) if rule in ln)
    if LIST_ITEM.sub("", lines[i]).strip() == rule.strip():
        del lines[i]
    else:
        rest = re.sub(r" {2,}", " ", lines[i].replace(rule, "")).rstrip()
        if re.fullmatch(r"\s*(?:[-*]|\d+\.)?\s*", rest):
            del lines[i]
        else:
            lines[i] = rest
    out, n = [], 0
    for ln in lines:  # renumber numbered lists
        m = re.match(r"^(\s*)\d+\.\s+", ln)
        if m:
            n += 1
            ln = f"{m.group(1)}{n}. " + ln[m.end():]
        elif ln.strip():
            n = 0
        out.append(ln)
    keep = []
    for j, ln in enumerate(out):  # a lead-in like "How you work:" with no list left under it goes too
        if ln.rstrip().endswith(":") and not LIST_ITEM.match(ln):
            nxt = next((x for x in out[j + 1:] if x.strip()), "")
            if not LIST_ITEM.match(nxt):
                ln = " ".join(re.split(r"(?<=[.!?]) ", ln.rstrip())[:-1])  # keep any sentences before it
                if not ln:
                    continue
        keep.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(keep)).rstrip("\n") + "\n"


def cut_from_file(text, rule):
    """remove_rule on a source file's prompt only: never the frontmatter, and in a persona file only
    the instruction block."""
    marker = "## Instruction to paste\n\n"
    if marker in text:
        head, body = text.split(marker, 1)
        return head + marker + remove_rule(body, rule)
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    split = m.end() if m else 0
    return text[:split] + remove_rule(text[split:], rule)


def prompt_lines(a):
    """The rule-bearing lines of an agent prompt: every list item and instruction paragraph after the
    opening role sentence. The preamble build.py adds to persona agents is audited once, separately."""
    lines = [ln.strip() for ln in a["body"].split("\n") if ln.strip()]
    if a["generated"]:
        lines = [ln for ln in lines if ln != preamble()]
    out = []
    for k, ln in enumerate(lines):
        if k == 0:
            out += [s for s in re.split(r"(?<=\.) ", ln)[1:] if not s.endswith(":")]  # the role sentence stays
            continue
        if ln.endswith(":") and not LIST_ITEM.match(ln):
            continue
        out.append(LIST_ITEM.sub("", ln))
    return out


def source_of(a):
    if not a["generated"]:
        return a["file"]
    return next(PERSONAS.rglob(f"{a['meta']['name']}.md"))


# ---- the hook, loaded in-process for block/allow checks ----

def hook_module():
    spec = importlib.util.spec_from_file_location("agent_hook", HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_hook(agent, message, retry=False, log=None):
    payload = json.dumps({"agent_type": agent, "last_assistant_message": message, "stop_hook_active": retry,
                          "agent_id": "test", "session_id": "test", "cwd": "/tmp/project"})
    env = {**os.environ, "AGENT_HARNESS_LOG": str(log or Path(tempfile.mkdtemp()) / "log.jsonl")}
    out = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True, env=env)
    return "block" if out.stdout.strip() and json.loads(out.stdout)["decision"] == "block" else "allow"


# ---- static check ----

def load():
    return json.loads(CONTROLS.read_text())["controls"]


def check(controls, all_agents):
    errors = []
    ids = set()
    for c in controls:
        cid = c.get("id", "?")
        if cid in ids:
            errors.append(f"{cid}: duplicate id")
        ids.add(cid)
        for k in ("agent", "rule", "failure", "backed_by", "block", "allow", "expires"):
            if not c.get(k):
                errors.append(f"{cid}: missing {k}")
        if not isinstance(c.get("expires"), dict) or not c["expires"].get("when"):
            errors.append(f"{cid}: expires needs a 'when' sentence")
        if c.get("agent") == "*":  # harness plumbing, not a prompt rule; its tests live in test_agent_harness.py
            continue
        a = all_agents.get(c.get("agent"))
        if not a:
            errors.append(f"{cid}: no agent {c.get('agent')!r}")
            continue
        if a["body"].count(c.get("rule", "\0")) != 1:
            errors.append(f"{cid}: rule not in {a['file'].relative_to(ROOT)} exactly once")
        if c.get("backed_by") == "prose":
            for side in ("block", "allow"):
                case = c.get(side) or {}
                if not case.get("prompt") or not case.get("check"):
                    errors.append(f"{cid}: prose {side} case needs a prompt and a check")
        elif c.get("backed_by"):
            if not (ROOT / c["backed_by"]).exists():
                errors.append(f"{cid}: {c['backed_by']} doesn't exist")
            for side, want in (("block", "block"), ("allow", "allow")):
                for msg in c.get(side) or []:
                    got = run_hook(c["agent"], msg)
                    if got != want:
                        errors.append(f"{cid}: hook should {want} but did {got}: {msg[-80:]!r}")
    hook = hook_module()
    for c in controls:
        if c.get("agent") != "*" and c.get("backed_by", "").endswith("agent_hook.py") and c["agent"] not in hook.ENFORCE:
            errors.append(f"{c['id']}: agent_hook.py doesn't enforce {c['agent']}")
    for name in hook.ENFORCE:
        if not any(c["agent"] == name and c["backed_by"].endswith("agent_hook.py") for c in controls):
            errors.append(f"agent_hook.py enforces {name} with no control in controls.json")
    return errors


def audit(controls, all_agents):
    """Prompt lines no control backs, per agent."""
    backed = {}
    for c in controls:
        backed.setdefault(c["agent"], []).append(c["rule"])
    out = {}
    for name, a in all_agents.items():
        rules = backed.get(name, [])
        loose = []
        for ln in prompt_lines(a):
            hit = [r for r in rules if r in ln]
            if not hit:
                if not any(ln in r for r in rules):
                    loose.append(ln)
                continue
            rest = ln  # a line that holds a backed rule can still hold unbacked sentences around it
            for r in hit:
                rest = rest.replace(r, " ")
            rest = re.sub(r"^\s*[A-Z][\w ]*:\s*", "", rest.strip())  # a label like "Output rules:"
            loose += [s.strip() for s in re.split(r"(?<=[.!?]) ", rest) if s.strip()]
        if loose:
            out[name] = loose
    pre = preamble()
    pre_rules = re.split(r"(?<=\.) ", pre)[2:]  # the first two sentences set up "I" and "my", they aren't rules
    if pre_rules and not any(c["rule"] in pre for c in controls):
        out["_preamble (scripts/build.py)"] = pre_rules
    return out


def prune(controls, all_agents):
    gone = 0
    for name, lines in audit(controls, all_agents).items():
        if name.startswith("_preamble"):
            src = BUILD
            text = src.read_text()
            for r in lines:
                text = text.replace(" " + r, "")
        else:
            a = all_agents[name]
            src = source_of(a)
            text = src.read_text()
            for r in lines:
                text = cut_from_file(text, r)
        src.write_text(text)
        gone += len(lines)
        print(f"{src.relative_to(ROOT)}: deleted {len(lines)} unproven rules")
    subprocess.run([sys.executable, str(BUILD)], check=True)
    print(f"{gone} rules deleted")


# ---- model runs ----

def claude(system, prompt, model, tools=None, cwd=None):
    cmd = ["claude", "-p", "--model", model, "--system-prompt", system, "--safe-mode", "--strict-mcp-config",
           "--no-session-persistence", "--output-format", "json"]
    if tools:
        cmd += ["--restricted", "--tools", ",".join(tools), "--allowedTools", ",".join(tools),
                "--settings", json.dumps({"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True}})]
    else:
        cmd += ["--tools", ""]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd or tempfile.gettempdir(),
                       timeout=900)
    try:
        res = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude gave no JSON: {(p.stderr or p.stdout)[-300:]}")
    if res.get("is_error"):
        raise RuntimeError(f"claude failed: {res.get('result')}")
    return res.get("result") or ""


def grade(check_, prompt, text, judge_model):
    for key, val in check_.items():
        if key == "regex":
            ok = re.search(val, text, re.I | re.M) is not None
        elif key == "not_regex":
            ok = re.search(val, text, re.I | re.M) is None
        elif key == "last_line":
            lines = [ln for ln in text.strip().split("\n") if ln.strip()]
            ok = bool(lines) and re.search(val, lines[-1], re.I) is not None
        elif key == "max_count":
            ok = len(re.findall(val[0], text, re.I | re.M)) <= val[1]
        elif key == "judge":
            out = claude(JUDGE_SYSTEM, f"## Task\n{prompt}\n\n## Output\n{text}\n\n## Question\n{val}", judge_model)
            m = re.search(r'"pass"\s*:\s*(true|false)', out)
            if not m:
                raise RuntimeError(f"judge gave no verdict: {out[:200]}")
            ok = m.group(1) == "true"
        else:
            raise ValueError(f"unknown check {key}")
        if not ok:
            return False
    return True


def eval_control(c, a, n, model, judge_model, cases=("block", "allow")):
    """Pass counts per case, with the rule and with it cut. Hook controls are evaluated on their prose:
    the hook isn't running here, so this measures whether the model still needs it."""
    model = a["meta"].get("model") or model
    full, cut = a["body"], remove_rule(a["body"], c["rule"])
    case_specs = c.get("eval") or {k: c[k] for k in cases}
    out = {}
    for side, case in case_specs.items():
        w = sum(grade(case["check"], case["prompt"], claude(full, case["prompt"], model), judge_model) for _ in range(n))
        wo = sum(grade(case["check"], case["prompt"], claude(cut, case["prompt"], model), judge_model) for _ in range(n))
        out[side] = {"with": w, "without": wo, "n": n}
    rates = [(v["with"] / n, v["without"] / n) for v in out.values()]
    if min(r[0] for r in rates) < PASS_WITH:
        verdict = "IGNORED"
    elif max(r[0] - r[1] for r in rates) < MARGIN:
        verdict = "REDUNDANT"
    else:
        verdict = "PROVEN"
    return {"verdict": verdict, "model": model, "date": datetime.date.today().isoformat(), "cases": out}


# ---- usage log and expiry ----

def read_log():
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def usage(log):
    by = {}
    for r in log:
        s = by.setdefault(r["agent"], {"runs": 0, "blocked": 0, "verdicts": {}, "projects": set(), "last": ""})
        if r.get("retry"):
            continue
        s["runs"] += 1
        s["blocked"] += bool(r.get("blocked"))
        s["verdicts"][r.get("verdict") or "-"] = s["verdicts"].get(r.get("verdict") or "-", 0) + 1
        s["projects"].add(r.get("project"))
        s["last"] = max(s["last"], r.get("ts", ""))
    return by


def sessions(names):
    """Runs of these agents in past session transcripts: (agent, project, final report, tools used)."""
    out = []
    for meta_f in sorted(SESSIONS.glob("*/*/subagents/agent-*.meta.json")):
        try:
            agent = json.loads(meta_f.read_text()).get("agentType", "").split(":")[-1]
        except (json.JSONDecodeError, OSError):
            continue
        if agent not in names:
            continue
        report, tools = "", {}
        for line in meta_f.with_name(meta_f.name.replace(".meta.json", ".jsonl")).read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = e.get("message")
            if e.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("content"), list):
                continue
            for b in m["content"]:
                if b.get("type") == "tool_use":
                    if "Handback" in b["name"]:
                        report = b["input"].get("message", report)
                    else:
                        tools[b["name"]] = tools.get(b["name"], 0) + 1
                elif b.get("type") == "text" and b.get("text", "").strip():
                    report = b["text"]
        out.append({"agent": agent, "project": meta_f.parent.parent.parent.name, "report": report, "tools": tools})
    return out


def print_sessions(all_agents):
    hook = hook_module()
    runs = sessions(set(all_agents))
    print(f"{SESSIONS}: {len(runs)} runs of these agents")
    by = {}
    for r in runs:
        by.setdefault(r["agent"], []).append(r)
    for name, rs in sorted(by.items()):
        used = {}
        for r in rs:
            for k, v in r["tools"].items():
                used[k] = used.get(k, 0) + v
        granted = [x.strip() for x in all_agents[name]["meta"].get("tools", "").split(",") if x.strip()]
        unused = [x for x in granted if x not in used]
        line = f"  {name:32} {len(rs)} runs  tools used {used}"
        if name in hook.VERDICTS:
            last = sum(bool(hook.verdict_of(name, r["report"])[1]) for r in rs)
            line += f"  verdict last {last}/{len(rs)}"
        print(line + (f"  never used: {', '.join(unused)}" if unused else ""))


def expired(c, log, model):
    """The reason this control is now dead weight, or None."""
    e = c["expires"]
    if e.get("date") and datetime.date.today().isoformat() >= e["date"]:
        return f"date {e['date']} reached: {e['when']}"
    if e.get("clean_runs"):
        runs = [r for r in log if r["agent"] == c["agent"] and not r.get("retry")]
        tail = runs[-e["clean_runs"]:]
        if len(tail) == e["clean_runs"] and all(r.get("verdict_last") for r in tail):
            return f"last {e['clean_runs']} logged runs had the verdict last without a block"
    p = c.get("proven")
    if e.get("model_changed") and p and p.get("model") != model:
        return f"proven on {p['model']}, now running {model}: re-run --eval {c['id']}"
    if p and p.get("verdict") in ("REDUNDANT", "IGNORED") and c["backed_by"] == "prose":
        return f"last eval said {p['verdict']}"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for flag in ("check", "audit", "prune", "smoke", "usage", "sessions", "expired", "garden"):
        ap.add_argument(f"--{flag}", action="store_true")
    ap.add_argument("--eval", nargs="*", metavar="ID")
    ap.add_argument("-n", type=int, default=4)
    ap.add_argument("--model", default="sonnet", help="for agents whose frontmatter names no model")
    ap.add_argument("--judge-model", default="sonnet")
    args = ap.parse_args()

    controls, all_agents = load(), agents()
    errors = check(controls, all_agents)
    if errors:
        print("\n".join(errors))
        sys.exit(1)

    if args.garden:
        print_sessions(all_agents)
        print()
        args.usage = args.expired = True
        loose = audit(controls, all_agents)
        print(f"{sum(len(v) for v in loose.values())} rules with no control (--audit lists them, --prune deletes them)\n")
    if args.sessions:
        print_sessions(all_agents)
    if args.audit:
        loose = audit(controls, all_agents)
        total = sum(len(v) for v in loose.values())
        for name, lines in loose.items():
            print(f"{name}:")
            for ln in lines:
                print(f"  - {ln[:110]}")
        print(f"\n{total} rules with no control: no real failure on record and no eval behind them. "
              f"--prune deletes them.")
    elif args.prune:
        prune(controls, all_agents)
    if args.usage:
        log = read_log()
        print(f"{LOG}: {len(log)} records")
        for name, s in sorted(usage(log).items(), key=lambda x: -x[1]["runs"]):
            v = ", ".join(f"{k} {n}" for k, n in s["verdicts"].items())
            print(f"  {name:32} {s['runs']:4} runs  {s['blocked']} blocked  [{v}]  "
                  f"{len(s['projects'])} projects  last {s['last'][:10]}")
    if args.expired:
        log, hits = read_log(), 0
        for c in controls:
            why = expired(c, log, args.model)
            if why:
                hits += 1
                print(f"{c['id']}: {why}")
        print(f"{hits} of {len(controls)} controls expired")
    if args.eval is not None or args.smoke:
        if not shutil.which("claude"):
            sys.exit("needs the claude CLI on PATH")
        data = json.loads(CONTROLS.read_text())
        failed = 0
        for c in data["controls"]:
            if c["agent"] == "*" or args.eval and c["id"] not in args.eval:
                continue
            if args.smoke and (c.get("proven") or {}).get("verdict") != "PROVEN":
                continue
            a = all_agents[c["agent"]]
            if args.smoke:
                res = eval_control(c, a, 1, args.model, args.judge_model)
                ok = all(v["with"] == 1 for v in res["cases"].values())
                failed += not ok
                print(f"{'ok  ' if ok else 'FAIL'} {c['id']}")
                continue
            res = eval_control(c, a, args.n, args.model, args.judge_model)
            c["proven"] = res
            cases = "  ".join(f"{k} {v['with']}/{v['n']} vs {v['without']}/{v['n']}" for k, v in res["cases"].items())
            print(f"{res['verdict']:9} {c['id']}  {cases}")
        if not args.smoke:
            CONTROLS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        sys.exit(1 if failed else 0)
    if not any((args.audit, args.prune, args.usage, args.sessions, args.expired, args.smoke, args.eval is not None)):
        print(f"ok: {len(controls)} controls, every one well formed, hook block/allow cases pass")


if __name__ == "__main__":
    main()
