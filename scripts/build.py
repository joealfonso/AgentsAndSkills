#!/usr/bin/env python3
"""Sync personas/ into the review-personas plugin.

personas/<set>/<name>.md is the source of truth. This script:
  1. copies every persona into plugins/review-personas/skills/review-as/personas/
  2. writes a subagent to plugins/review-personas/agents/ for each review-mode persona
  3. regenerates the persona index table inside the review-as SKILL.md

Run it after adding or editing a persona:  python3 scripts/build.py
Pass --check to fail (exit 1) if anything is out of date, without writing.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "personas"
PLUGIN = ROOT / "plugins" / "review-personas"
SKILL_DIR = PLUGIN / "skills" / "review-as"
AGENTS_DIR = PLUGIN / "agents"

AGENT_PREAMBLE = """You are running as a subagent. In the instructions below, "I", "me" and "my" mean the person whose material you were handed. Read every file path or URL you were given before judging. If the material isn't there, answer CAN'T JUDGE and name what's missing.

"""


def parse(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n\n(.*)", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    instruction = text.split("## Instruction to paste\n\n", 1)[1].strip()
    return meta, text, instruction


def agent_doc(meta, instruction):
    use = meta["use_for"].rstrip(".")
    desc = f"{meta['title']} review persona. Use for {use}. Returns ranked flags or a clean verdict."
    return (
        f"---\nname: {meta['name']}\ndescription: {json.dumps(desc)}\n"
        f"tools: Read, Glob, Grep, WebFetch\nmodel: sonnet\n---\n\n"
        + AGENT_PREAMBLE
        + instruction
        + "\n"
    )


def index_table(personas):
    rows = ["| Set | Persona | Mode | Use for |", "|---|---|---|---|"]
    for meta, _, _ in personas:
        rows.append(f"| {meta['set']} | {meta['name']} | {meta['mode']} | {meta['use_for'].rstrip('.')} |")
    return "\n".join(rows) + "\n"


def main():
    check = "--check" in sys.argv
    order = ["design-critique", "stakeholder-leadership", "interviewing", "reality-checks"]
    sets = sorted((d for d in SRC.iterdir() if d.is_dir()),
                  key=lambda d: (order.index(d.name) if d.name in order else 99, d.name))
    personas = [parse(p) for d in sets for p in sorted(d.glob("*.md"))]

    wanted = {}
    for meta, text, instruction in personas:
        wanted[SKILL_DIR / "personas" / meta["set"] / f"{meta['name']}.md"] = text
        if meta["mode"] == "review":
            wanted[AGENTS_DIR / f"{meta['name']}.md"] = agent_doc(meta, instruction)

    skill_md = SKILL_DIR / "SKILL.md"
    skill_text = re.sub(
        r"(<!-- index:start[^>]*-->\n).*?(<!-- index:end -->)",
        lambda m: m.group(1) + index_table(personas) + m.group(2),
        skill_md.read_text(), flags=re.S)
    wanted[skill_md] = skill_text

    existing = set((SKILL_DIR / "personas").rglob("*.md")) | set(AGENTS_DIR.glob("*.md"))
    stale = sorted(existing - set(wanted))
    changed = sorted(p for p, t in wanted.items() if not p.exists() or p.read_text() != t)

    if check:
        for p in changed + stale:
            print(f"out of date: {p.relative_to(ROOT)}")
        sys.exit(1 if changed or stale else 0)

    for p in stale:
        p.unlink()
    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(wanted[p])
    for d in (SKILL_DIR / "personas").iterdir() if (SKILL_DIR / "personas").exists() else []:
        if d.is_dir() and not any(d.iterdir()):
            shutil.rmtree(d)
    print(f"{len(personas)} personas, {sum(m['mode'] == 'review' for m, _, _ in personas)} agents, "
          f"{len(changed)} files written, {len(stale)} removed")


if __name__ == "__main__":
    main()
