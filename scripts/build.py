#!/usr/bin/env python3
"""Sync the source folders into their plugins.

personas/<set>/<name>.md is the source of truth for the review-personas plugin:
  1. copies every persona into plugins/review-personas/skills/review-as/personas/
  2. writes a subagent to plugins/review-personas/agents/ for each review-mode persona
  3. regenerates the persona index table inside the review-as SKILL.md

prompts/<category>/<name>.md is the source of truth for the prompt-library plugin:
  4. copies every prompt (and about-me.md) into plugins/prompt-library/skills/prompt-library/prompts/
  5. regenerates the prompt index in prompts/README.md and in the prompt-library SKILL.md

Run it after adding or editing a persona or prompt:  python3 scripts/build.py
Pass --check to fail (exit 1) if anything is out of date, without writing.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PERSONAS = ROOT / "personas"
PERSONA_PLUGIN = ROOT / "plugins" / "review-personas"
PERSONA_SKILL = PERSONA_PLUGIN / "skills" / "review-as"
AGENTS_DIR = PERSONA_PLUGIN / "agents"
PERSONA_ORDER = ["design-critique", "stakeholder-leadership", "interviewing", "reality-checks"]

PROMPTS = ROOT / "prompts"
PROMPT_SKILL = ROOT / "plugins" / "prompt-library" / "skills" / "prompt-library"
PROMPT_ORDER = {
    "job-search": "Job search",
    "interviewing": "Interviewing",
    "offers-and-negotiation": "Offers and negotiation",
    "portfolio-and-case-studies": "Portfolio and case studies",
    "design-work": "Design and research work",
    "ai-product-design": "AI product design",
    "stakeholders-and-leadership": "Stakeholders and leadership",
    "mentoring-and-teaching": "Mentoring and teaching",
    "writing-and-visibility": "Writing and visibility",
    "career-growth": "Career growth",
    "building-with-ai": "Building with AI",
    "projects": "System prompts for Claude Projects",
}

AGENT_PREAMBLE = """You are running as a subagent. In the instructions below, "I", "me" and "my" mean the person whose material you were handed. Read every file path or URL you were given before judging. If the material isn't there, answer CAN'T JUDGE and name what's missing.

"""


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        v = v.strip()
        meta[k.strip()] = json.loads(v) if v.startswith('"') else v
    return meta


def replace_index(text, table):
    return re.sub(r"(<!-- index:start[^>]*-->\n).*?(<!-- index:end -->)",
                  lambda m: m.group(1) + table + m.group(2), text, flags=re.S)


# ---- personas ----

def persona_agent(meta, instruction):
    use = meta["use_for"].rstrip(".")
    desc = f"{meta['title']} review persona. Use for {use}. Returns ranked flags or a clean verdict."
    return (f"---\nname: {meta['name']}\ndescription: {json.dumps(desc)}\n"
            f"tools: Read, Glob, Grep, WebFetch\nmodel: sonnet\n---\n\n"
            + AGENT_PREAMBLE + instruction + "\n")


def personas_wanted():
    sets = sorted((d for d in PERSONAS.iterdir() if d.is_dir()),
                  key=lambda d: (PERSONA_ORDER.index(d.name) if d.name in PERSONA_ORDER else 99, d.name))
    wanted, rows = {}, ["| Set | Persona | Mode | Use for |", "|---|---|---|---|"]
    for d in sets:
        for p in sorted(d.glob("*.md")):
            text = p.read_text()
            meta = frontmatter(text)
            instruction = text.split("## Instruction to paste\n\n", 1)[1].strip()
            wanted[PERSONA_SKILL / "personas" / meta["set"] / p.name] = text
            if meta["mode"] == "review":
                wanted[AGENTS_DIR / p.name] = persona_agent(meta, instruction)
            rows.append(f"| {meta['set']} | {meta['name']} | {meta['mode']} | {meta['use_for'].rstrip('.')} |")
    skill_md = PERSONA_SKILL / "SKILL.md"
    wanted[skill_md] = replace_index(skill_md.read_text(), "\n".join(rows) + "\n")
    return wanted, [PERSONA_SKILL / "personas", AGENTS_DIR]


# ---- prompts ----

def prompt_index(entries, link_prefix):
    out = []
    for cat, title in PROMPT_ORDER.items():
        items = [e for e in entries if e["category"] == cat]
        if not items:
            continue
        out += [f"### {title}", "", "| Prompt | Use when |", "|---|---|"]
        out += [f"| [{e['title']}]({link_prefix}{e['path']}) | {e['use_when']} |" for e in items]
        out.append("")
    unknown = {e["category"] for e in entries} - set(PROMPT_ORDER)
    if unknown:
        sys.exit(f"add these categories to PROMPT_ORDER in scripts/build.py: {', '.join(sorted(unknown))}")
    return "\n".join(out)


def prompts_wanted():
    wanted, entries = {}, []
    for p in sorted(PROMPTS.rglob("*.md")):
        rel = p.relative_to(PROMPTS)
        if rel.name == "README.md":
            continue
        text = p.read_text()
        wanted[PROMPT_SKILL / "prompts" / rel] = text
        if rel.parent != Path("."):
            meta = frontmatter(text)
            entries.append({**meta, "path": rel.as_posix()})
    readme = PROMPTS / "README.md"
    wanted[readme] = replace_index(readme.read_text(), prompt_index(entries, ""))
    skill_md = PROMPT_SKILL / "SKILL.md"
    wanted[skill_md] = replace_index(skill_md.read_text(), prompt_index(entries, "prompts/"))
    return wanted, [PROMPT_SKILL / "prompts"]


def main():
    check = "--check" in sys.argv
    wanted, managed = {}, []
    for fn in (personas_wanted, prompts_wanted):
        w, m = fn()
        wanted.update(w)
        managed += m

    existing = {p for d in managed if d.exists() for p in d.rglob("*.md")}
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
    for d in managed:
        for sub in sorted(d.rglob("*"), reverse=True) if d.exists() else []:
            if sub.is_dir() and not any(sub.iterdir()):
                shutil.rmtree(sub)
    print(f"{len(changed)} files written, {len(stale)} removed")


if __name__ == "__main__":
    main()
