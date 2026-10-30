#!/usr/bin/env python3
"""Sync the source folders into their plugins.

personas/ and prompts/ are the only copies of the personas and prompts. The plugins reach them
through two symlinks, which Claude Code resolves into real files when it installs a plugin:
  plugins/review-personas/skills/review-as/personas  -> ../../../../personas
  plugins/prompt-library/skills/prompt-library/prompts -> ../../../../prompts
The design-guide skill links to personas/, prompts/, templates/, rules/ and the design-review skills the same way.

From personas/<set>/<name>.md this script:
  1. writes a subagent to plugins/review-personas/agents/ for each review-mode persona
  2. regenerates the persona index table inside the review-as SKILL.md and each set's README.md

From prompts/<category>/<name>.md it:
  3. regenerates the prompt index in prompts/README.md, the prompt-library SKILL.md, and each category's README.md

From the SECTIONS list in tools/stages.html it:
  4. regenerates STAGES.md, the same stage map as a table GitHub can show
  5. regenerates catalog.md in the design-guide skill: every resource by stage, with when to use it,
     plus everything not placed in a stage, so the skill can diagnose a request and pick one

It also checks the plugin symlinks are in place.

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
                       "Reviewers that catch what polished critique misses: the engineer who has rebuilt this twice, the user who hates it, your future self, the audience member who stopped listening, and the calibration committee reading your self-review."),
}

PROMPTS = ROOT / "prompts"
PROMPT_SKILL = ROOT / "plugins" / "prompt-library" / "skills" / "prompt-library"
PROMPT_ABOUT = {
    "job-search": "Finding roles worth applying to and getting in the door: decoding postings, rewriting resume bullets, outreach, referrals, follow-ups and company research.",
    "interviewing": "Preparing for and recovering from interviews: a story bank, tighter answers, portfolio presentations, design exercises, questions to ask, debriefs and mock rounds.",
    "offers-and-negotiation": "From offer to first day: comparing offers, negotiating, accepting or declining, and resigning well.",
    "portfolio-and-case-studies": "Turning real projects into evidence: case studies from raw notes, impact metrics, cutting length, NDA-safe rewrites, one-liners and a portfolio review.",
    "user-research": "Planning, running and making sense of user research: research plans, interview guides, field notes, usability tests, surveys, the rainbow spreadsheet, synthesis, and an anomaly review so outliers aren't lost.",
    "design-work": "Day-to-day design work: framing problems, service blueprints for digital products (build, review, future state, workshops), documenting rationale, crit prep, edge cases, copy and accessibility.",
    "ai-product-design": "Designing AI features that hold up: failure modes, uncertainty and trust, evaluation plans, behavior specs, human oversight, and reality-checking AI pitches.",
    "stakeholders-and-leadership": "Working with people who decide things: exec summaries, decision memos, disagreeing well, status updates, meetings, 1:1s, hard conversations and stakeholder maps.",
    "mentoring-and-teaching": "Helping others grow: plain explanations, feedback on junior work, career conversations, workshops and learning plans.",
    "writing-and-visibility": "Being known for your thinking: LinkedIn posts, talk proposals, article outlines, fact-checking, bios and newsletters.",
    "career-growth": "Steering your own career: weekly brag docs, self-reviews, promotion cases, the first 90 days, quarterly check-ins and skill gap audits.",
    "building-with-ai": "Getting good work out of coding agents: specs, CLAUDE.md files, delegation briefs, bug reports and critiquing what they build.",
    "projects": "Longer system prompts that set up a Claude Project or a custom assistant for an ongoing job.",
}

PROMPT_EXTRA = {
    "user-research": "**Template:** the [rainbow spreadsheet](../../templates/rainbow-spreadsheet/), my usability study sheet as importable tabs. The setup and analysis prompts below work with it.",
}

PROMPT_ORDER = {
    "job-search": "Job search",
    "interviewing": "Interviewing",
    "offers-and-negotiation": "Offers and negotiation",
    "portfolio-and-case-studies": "Portfolio and case studies",
    "user-research": "User research",
    "design-work": "Design work",
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
    return wanted, [AGENTS_DIR]


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
            + (PROMPT_EXTRA[cat] + "\n\n" if cat in PROMPT_EXTRA else "") +
            "Fill in the `[BRACKETS]` and paste a prompt into any assistant, with [about-me.md](../about-me.md) above it, "
            "or ask Claude to use it by name through the `prompt-library` skill.\n\n"
            "| Prompt | Use when |\n|---|---|\n" + rows + "\n\n"
            "*This file is generated by `scripts/build.py` from the prompts' frontmatter.*\n")
    readme = PROMPTS / "README.md"
    wanted[readme] = replace_index(readme.read_text(), prompt_index(entries, ""))
    skill_md = PROMPT_SKILL / "SKILL.md"
    wanted[skill_md] = replace_index(skill_md.read_text(), prompt_index(entries, "prompts/"))
    return wanted, []


# ---- stages ----

STAGES_HTML = ROOT / "tools" / "stages.html"
STAGE_ITEM = {
    "p": ("prompts/{}.md", "{}"),
    "s": ("plugins/{}/SKILL.md", "{} (skill)"),
    "r": ("personas/{}.md", "*{}* (persona)"),
    "t": ("tools/{}", "{} (browser tool)"),
    "m": ("templates/{}", "{} (template)"),
}


def parse_stages():
    """The SECTIONS list in tools/stages.html as [{title, sub, stages: [{title, hi, items: [(kind, name, path)]}]}]."""
    src = STAGES_HTML.read_text().split("const SECTIONS = [", 1)[1].split("\n  ];", 1)[0]
    tokens = re.finditer(r'^      title: "([^"]+)",\n      sub: "([^"]+)"'
                         r'|\{ title: "([^"]+)",( hi: true,)?'
                         r'|\b([psrtm])\("([^"]+)", "([^"]+)"\)', src, re.M)
    sections = []
    for t in tokens:
        if t.group(1):
            sections.append({"title": t.group(1), "sub": t.group(2), "stages": []})
        elif t.group(3):
            sections[-1]["stages"].append({"title": t.group(3), "hi": bool(t.group(4)), "items": []})
        else:
            sections[-1]["stages"][-1]["items"].append((t.group(5), t.group(6), t.group(7)))
    return sections


def stages_wanted():
    """STAGES.md, so the stage map in tools/stages.html also reads on GitHub."""
    out = ["# Stage by stage", "",
           "Everything in this repo, grouped by the stage of the work where it helps. "
           "Stages marked ★ have an interactive [browser tool](tools/). "
           "The same map as cards: [tools/stages.html](https://josephalfonso.com/AgentsAndSkills/tools/stages.html).", ""]
    for sec in parse_stages():
        out += [f"## {sec['title']}", "", sec["sub"], "", "| # | Stage | What's in it |", "|---|---|---|"]
        for i, st in enumerate(sec["stages"], 1):
            items = []
            for kind, name, path in st["items"]:
                link, label = STAGE_ITEM[kind]
                items.append(f"[{label.format(name)}]({link.format(path)})")
            out.append(f"| {i:02d} | **{st['title']}**{' ★' if st['hi'] else ''} | {' · '.join(items)} |")
        out.append("")
    out.append("*This file is generated by `scripts/build.py` from the `SECTIONS` list in tools/stages.html.*\n")
    return {ROOT / "STAGES.md": "\n".join(out)}, []


# ---- design guide catalog ----

GUIDE_SKILL = ROOT / "plugins" / "design-guide" / "skills" / "design-guide"
TOOLS_URL = "https://josephalfonso.com/AgentsAndSkills/tools/"
TOOL_FRAMEWORK = {
    "design-review-card.html": "design-review-card",
    "ai-design-evaluation-rubric.html": "ai-design-rubric",
    "ai-readiness-review.html": "ai-readiness-review",
}
TEMPLATE_USE = {
    "service-blueprint.md": "you're mapping a service by hand and want the blank structure the blueprint prompts use",
    "CLAUDE.md": "a new project needs agent instructions and you want a short starting point",
    "rainbow-spreadsheet/": "you're running a usability study and want one sheet for goals, participants, tasks and observations",
    "self-evaluation-log.md": "you review your own work with personas and want a record of which flags keep coming back",
}


def first_sentence(text):
    return re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0].rstrip(".")


def catalog_wanted():
    """catalog.md for the design-guide skill. Paths are relative to the skill folder, through its symlinks."""
    plugin_skills = {d.name: (d.parent.parent.name, frontmatter(d.joinpath("SKILL.md").read_text()))
                     for d in (ROOT / "plugins").glob("*/skills/*") if d.joinpath("SKILL.md").exists()}

    def entry(kind, name, path):
        if kind == "p":
            meta = frontmatter((PROMPTS / f"{path}.md").read_text())
            return f"[{name}](prompts/{path}.md) · prompt · {meta['use_when']}"
        if kind == "r":
            meta = frontmatter((PERSONAS / f"{path}.md").read_text())
            return f"[{name}](personas/{path}.md) · {meta['mode']} persona · {meta['use_for'].rstrip('.')}"
        if kind == "t":
            skill = TOOL_FRAMEWORK[path]
            desc = first_sentence(plugin_skills[skill][1]["description"])
            return (f"[{name}](frameworks/{skill}/SKILL.md) · review framework · {desc}. "
                    f"Interactive version: {TOOLS_URL}{path}")
        if kind == "m":
            if path not in TEMPLATE_USE:
                sys.exit(f"add templates/{path} to TEMPLATE_USE in scripts/build.py")
            return f"[{name}](templates/{path}) · template · {TEMPLATE_USE[path]}"
        skill = path.rsplit("/", 1)[1]
        plugin, meta = plugin_skills[skill]
        return (f"{name} · installed skill `{skill}` from the `{plugin}` plugin, personal setup · "
                f"{first_sentence(meta['description'])}")

    placed = set()
    out = ["# Catalog", "",
           "Every resource in the bank, by the stage of the work where it helps. "
           "Each line: link · kind · when to use it. Search this file for words from the request.", ""]
    for sec in parse_stages():
        out += [f"## {sec['title']}", "", sec["sub"], ""]
        for i, st in enumerate(sec["stages"], 1):
            out += [f"### {i:02d} {st['title']}", ""]
            for kind, name, path in st["items"]:
                placed.add((kind, path))
                out.append(f"- {entry(kind, name, path)}")
            out.append("")

    out += ["## Also in the bank", "", "Not placed in a stage, still worth matching.", ""]
    rest = []
    for p in sorted(PROMPTS.rglob("*.md")):
        rel = p.relative_to(PROMPTS)
        if rel.name == "README.md" or rel.parent == Path(".") or ("p", rel.with_suffix("").as_posix()) in placed:
            continue
        meta = frontmatter(p.read_text())
        rest.append(f"- [{meta['title']}](prompts/{rel.as_posix()}) · prompt · {meta['use_when']}")
    for p in sorted(PERSONAS.rglob("*.md")):
        rel = p.relative_to(PERSONAS)
        if rel.name == "README.md" or ("r", rel.with_suffix("").as_posix()) in placed:
            continue
        meta = frontmatter(p.read_text())
        rest.append(f"- [{meta['title']}](personas/{rel.as_posix()}) · {meta['mode']} persona · {meta['use_for'].rstrip('.')}")
    for skill, (plugin, meta) in sorted(plugin_skills.items()):
        if plugin in ("design-guide", "design-review", "prompt-library", "review-personas", "bank-guide") \
                or ("s", f"{plugin}/skills/{skill}") in placed:
            continue
        rest.append(f"- {skill} · installed skill `{skill}` from the `{plugin}` plugin, personal setup · "
                    f"{first_sentence(meta['description'])}")
    for p in sorted((ROOT / "rules").glob("*.md")):
        if p.name == "README.md":
            continue
        lines = p.read_text().splitlines()
        title = lines[0].lstrip("# ")
        why = next(l for l in lines[1:] if l.strip())
        rest.append(f"- [{title}](rules/{p.name}) · CLAUDE.md rule · {why.rstrip('.')}")
    out += rest
    out += ["", "*This file is generated by `scripts/build.py`. Edit the sources, not this file.*", ""]
    return {GUIDE_SKILL / "catalog.md": "\n".join(out)}, []


# ---- coding bank catalog ----

BANK_SKILL = ROOT / "plugins" / "bank-guide" / "skills" / "bank-guide"
# Project type -> plugins to enable in that project's .claude/settings.json. Edit here, then run build.py.
BASE_KIT = ["dev-team", "review-personas", "guardrails", "writing"]
PROJECT_KITS = [
    ("Any coding project", BASE_KIT, "Seven working agents, review personas on demand, hooks that block risky commands, and my writing voice."),
    ("Game", BASE_KIT + ["game-team"], "Adds art-director, artist and playtester. Needs DESIGN.md at the repo root and docs/ASSETS.md."),
    ("Web app or site", BASE_KIT + ["web-team", "design-review"], "Adds a11y-auditor and tech-writer, plus the design review card before build."),
    ("AI feature", BASE_KIT + ["ai-team", "design-review"], "Adds eval-writer, plus the AI design rubric and AI readiness review."),
    ("Design or research work", ["design-guide", "design-review", "prompt-library", "review-personas", "writing"], "No coding agents. Prompts, frameworks and personas picked by stage."),
    ("Job search", ["job-search", "prompt-library", "review-personas", "writing"], "Personal setup. Edit the Config section in each skill first."),
    ("Daily routines", ["daily-ops"], "Personal setup. Morning briefing and knowledge base cleanup."),
]


def loose_front(path):
    """Frontmatter as a dict, tolerant of values that aren't quoted."""
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    out = {}
    for line in m.group(1).splitlines() if m else []:
        k, sep, v = line.partition(":")
        if sep:
            v = v.strip()
            out[k.strip()] = json.loads(v) if v.startswith('"') else v
    return out


def bank_catalog_wanted():
    """catalog.md for the bank-guide skill: project kits, then every plugin with its agents and skills."""
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    listed = {p["name"] for p in market["plugins"]}
    on_disk = {d.name for d in (ROOT / "plugins").iterdir() if d.joinpath(".claude-plugin", "plugin.json").exists()}
    if listed != on_disk:
        sys.exit(f"marketplace.json and plugins/ disagree: {sorted(listed ^ on_disk)}")
    for ptype, kit, _ in PROJECT_KITS:
        missing = [k for k in kit if k not in listed]
        if missing:
            sys.exit(f"kit '{ptype}' names plugins that don't exist: {missing}")

    out = ["# Bank catalog", "",
           "What to enable per project type, then everything each plugin holds. "
           "Enable plugins in a project's `.claude/settings.json` as `\"<plugin>@joseph-alfonso\": true`.", "",
           "## Kits by project type", "", "| Project type | Enable | What you get |", "|---|---|---|"]
    out += [f"| {t} | {', '.join(f'`{k}`' for k in kit)} | {why} |" for t, kit, why in PROJECT_KITS]
    out += ["", "## Plugins", ""]
    for plugin in market["plugins"]:
        d = ROOT / "plugins" / plugin["name"]
        out += [f"### {plugin['name']}", "", plugin["description"], ""]
        agents = sorted((d / "agents").glob("*.md")) if (d / "agents").exists() else []
        if len(agents) > 8:
            out.append(f"- {len(agents)} reviewer subagents, one per review-mode persona. Run them through the `review-as` skill.")
        for a in agents if len(agents) <= 8 else []:
            meta = loose_front(a)
            if meta.get("name") != a.stem:
                sys.exit(f"{a.relative_to(ROOT)}: name does not match file name")
            out.append(f"- agent `{a.stem}`: {first_sentence(meta['description'])}")
        for sk in sorted((d / "skills").glob("*/SKILL.md")) if (d / "skills").exists() else []:
            out.append(f"- skill `{sk.parent.name}`: {first_sentence(loose_front(sk)['description'])}")
        for c in sorted((d / "commands").glob("*.md")) if (d / "commands").exists() else []:
            out.append(f"- command `/{c.stem}`: {loose_front(c).get('description', '')}")
        if (d / "hooks" / "hooks.json").exists():
            out.append("- hooks: see the plugin README")
        out.append("")
    out.append("*This file is generated by `scripts/build.py`. Edit the kits in build.py and the plugins themselves, not this file.*\n")
    return {BANK_SKILL / "catalog.md": "\n".join(out)}, []


LINKS = {
    BANK_SKILL / "templates": "../../../../templates",
    PERSONA_SKILL / "personas": "../../../../personas",
    PROMPT_SKILL / "prompts": "../../../../prompts",
    GUIDE_SKILL / "personas": "../../../../personas",
    GUIDE_SKILL / "prompts": "../../../../prompts",
    GUIDE_SKILL / "templates": "../../../../templates",
    GUIDE_SKILL / "rules": "../../../../rules",
    GUIDE_SKILL / "frameworks": "../../../design-review/skills",
}


def check_links():
    """Problems with the plugin symlinks, as messages. Missing links are created."""
    problems = []
    for link, target in LINKS.items():
        if link.is_symlink() and str(link.readlink()) == target:
            continue
        if not link.exists() and not link.is_symlink() and "--check" not in sys.argv:
            link.symlink_to(target)
            print(f"linked {link.relative_to(ROOT)} -> {target}")
            continue
        problems.append(f"{link.relative_to(ROOT)} should be a symlink to {target}")
    return problems


def main():
    check = "--check" in sys.argv
    problems = check_links()
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    wanted, managed = {}, []
    for fn in (personas_wanted, prompts_wanted, stages_wanted, catalog_wanted, bank_catalog_wanted):
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
