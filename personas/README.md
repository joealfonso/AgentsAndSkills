# Personas

20 critique and rehearsal personas, one file each, grouped into four sets. This folder is the only copy: the `review-personas` plugin reads it through a symlink, and `scripts/build.py` turns the review-mode ones into Claude Code subagents.

Review-mode personas are a single role sentence. Their lenses, stop conditions and output rules were deleted because no real run showed they helped (see [harness/](../harness)); the `review-as` skill asks for the verdict line. Rehearsal personas are unchanged, they aren't subagents and the harness doesn't cover them.

| Set | Personas | For |
|---|---|---|
| [design-critique](design-critique/) | 6 | Design and portfolio work |
| [stakeholder-leadership](stakeholder-leadership/) | 6 | Exec, cross-functional and upward communication |
| [interviewing](interviewing/) | 3 | Screens, differentiation and comp negotiation |
| [reality-checks](reality-checks/) | 4 | What polished critique misses |

**Use one:** paste its "Instruction to paste" block into any chat along with your material, or ask Claude to "review this as the skeptical hiring manager".

**Add one:** copy an existing file's frontmatter (`name`, `title`, `set`, `mode`, `use_for`), write the instruction, then run `python3 scripts/build.py`. For a review persona, keep it to the role sentence; add a rule only with a control in [harness/controls.json](../harness/controls.json).
