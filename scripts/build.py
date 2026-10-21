#!/usr/bin/env python3
"""Sync the source folders into their plugins.

personas/<set>/<name>.md is the source of truth for the review-personas plugin:
  1. copies every persona into plugins/review-personas/skills/review-as/personas/
  2. writes a subagent to plugins/review-personas/agents/ for each review-mode persona
  3. regenerates the persona index table inside the review-as SKILL.md and each set's README.md

prompts/<category>/<name>.md is the source of truth for the prompt-library plugin:
  4. copies every prompt (and about-me.md) into plugins/prompt-library/skills/prompt-library/prompts/
  5. regenerates the prompt index in prompts/README.md, the prompt-library SKILL.md, and each category's README.md

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
PERSONA_SETS = {
    "design-critique": ("Design critique personas",
                        "Reviewers for design and portfolio work: the senior designer, hiring manager, junior mentee, business stakeholder, research partner and AI specialist who find gaps before someone else does."),
    "stakeholder-leadership": ("Stakeholder and leadership personas",
                               "Practice and review for upward and cross-functional communication: execs, engineering leads, finance, skip-levels, a new manager you're coaching, and a board-level narrative editor."),
    "interviewing": ("Interviewing personas",
                     "Rehearsal partners for job search stages beyond the portfolio review: the phone screen, a competing candidate, and the compensation conversation."),
    "reality-checks": ("Reality-check personas",
                       "Reviewers that catch what polished critique misses: the engineer who has rebuilt this twice, the user who hates it, your future self, and the audience member who stopped listening."),
}

PROMPTS = ROOT / "prompts"
PROMPT_SKILL = ROOT / "plugins" / "prompt-library" / "skills" / "prompt-library"
PROMPT_ABOUT = {
    "job-search": "Finding roles worth applying to and getting in the door: decoding postings, rewriting resume bullets, outreach, referrals, follow-ups and company research.",
    "interviewing": "Preparing for and recovering from interviews: a story bank, tighter answers, portfolio presentations, design exercises, questions to ask, debriefs and mock rounds.",
    "offers-and-negotiation": "From offer to first day: comparing offers, negotiating, accepting or declining, and resigning well.",
    "portfolio-and-case-studies": "Turning real projects into evidence: case studies from raw notes, impact metrics, cutting length, NDA-safe rewrites, one-liners and a portfolio review.",
    "design-work": "Day-to-day design and research: framing problems; planning, collecting and synthesizing research (interviews, field notes, usability tests with a rainbow spreadsheet, surveys) with an anomaly review so outliers aren't lost; service blueprints for digital products (build, review, future state, workshops); documenting rationale, crit prep, edge cases, copy and accessibility.",
    "ai-product-design": "Designing AI features that hold up: failure modes, uncertainty and trust, evaluation plans, behavior specs, human oversight, and reality-checking AI pitches.",
    "stakeholders-and-leadership": "Working with people who decide things: exec summaries, decision memos, disagreeing well, status updates, meetings, 1:1s, hard conversations and stakeholder maps.",
    "mentoring-and-teaching": "Helping others grow: plain explanations, feedback on junior work, career conversations, workshops and learning plans.",
    "writing-and-visibility": "Being known for your thinking: LinkedIn posts, talk proposals, article outlines, fact-checking, bios and newsletters.",
    "career-growth": "Steering your own career: weekly brag docs, self-reviews, promotion cases, the first 90 days, quarterly check-ins and skill gap audits.",
    "building-with-ai": "Getting good work out of coding agents: specs, CLAUDE.md files, delegation briefs, bug reports and critiquing what they build.",
    "projects": "Longer system prompts that set up a Claude Project or a custom assistant for an ongoing job.",
}

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
        set_rows = []
        for p in sorted(x for x in d.glob("*.md") if x.name != "README.md"):
            text = p.read_text()
            meta = frontmatter(text)
            instruction = text.split("## Instruction to paste\n\n", 1)[1].strip()
            wanted[PERSONA_SKILL / "personas" / meta["set"] / p.name] = text
            if meta["mode"] == "review":
                wanted[AGENTS_DIR / p.name] = persona_agent(meta, instruction)
            rows.append(f"| {meta['set']} | {meta['name']} | {meta['mode']} | {meta['use_for'].rstrip('.')} |")
            set_rows.append(f"| [{meta['title']}]({p.name}) | {meta['mode']} | {meta['use_for'].rstrip('.')} |")
        title, about = PERSONA_SETS.get(d.name, (d.name, ""))
        wanted[d / "README.md"] = (
            f"# {title}\n\n{about}\n\n"
            "Each file is one persona: paste its instruction block into any chat with your material, "
            "or ask Claude to \"review this as ...\" with the `review-as` skill. **Review** personas do one pass "
            "and return a verdict; **rehearsal** personas stay in character for a practice conversation.\n\n"
            "| Persona | Mode | Use for |\n|---|---|---|\n" + "\n".join(set_rows) + "\n\n"
            "*This file is generated by `scripts/build.py` from the personas' frontmatter.*\n")
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
    for cat, title in PROMPT_ORDER.items():
        items = [e for e in entries if e["category"] == cat]
        if not items:
            continue
        rows = "\n".join(f"| [{e['title']}]({Path(e['path']).name}) | {e['use_when']} |" for e in items)
        wanted[PROMPTS / cat / "README.md"] = (
            f"# {title}\n\n{PROMPT_ABOUT.get(cat, '')}\n\n"
            "Fill in the `[BRACKETS]` and paste a prompt into any assistant, with [about-me.md](../about-me.md) above it, "
            "or ask Claude to use it by name through the `prompt-library` skill.\n\n"
            "| Prompt | Use when |\n|---|---|\n" + rows + "\n\n"
            "*This file is generated by `scripts/build.py` from the prompts' frontmatter.*\n")
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
