# Personas

20 critique and rehearsal personas, one file each, grouped into four sets. This folder is the only copy: the `review-personas` plugin reads it through a symlink, and `scripts/build.py` turns the review-mode ones into Claude Code subagents.

What makes them different from "pretend to be a hiring manager": every persona has **stop conditions** (when to say nothing) and a fixed **verdict line**, so it reviews what's actually on the page instead of inventing problems to look useful.

| Set | Personas | For |
|---|---|---|
| [design-critique](design-critique/) | 6 | Design and portfolio work |
| [stakeholder-leadership](stakeholder-leadership/) | 6 | Exec, cross-functional and upward communication |
| [interviewing](interviewing/) | 3 | Screens, differentiation and comp negotiation |
| [reality-checks](reality-checks/) | 4 | What polished critique misses |

**Use one:** paste its "Instruction to paste" block into any chat along with your material, or ask Claude to "review this as the skeptical hiring manager".

**Add one:** copy an existing file's frontmatter (`name`, `title`, `set`, `mode`, `use_for`), write the instruction with stop conditions and output rules, then run `python3 scripts/build.py`.
