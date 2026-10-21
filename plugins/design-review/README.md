# design-review

Three review frameworks, from fast to formal. The interactive versions are in [tools](../../tools/) and live at [josephalfonso.com/AgentsAndSkills/tools](https://josephalfonso.com/AgentsAndSkills/tools/).

| Skill | Use for | Output |
|---|---|---|
| [design-review-card](skills/design-review-card/SKILL.md) | Any design before build, 10-15 minutes | A follow-up list, no grade |
| [ai-design-rubric](skills/ai-design-rubric/SKILL.md) | AI features | Gut-check, 18 scored criteria with gates, a ship verdict |
| [ai-readiness-review](skills/ai-readiness-review/SKILL.md) | High-consequence AI features, launch gates | Risk tier, 27 evidence-backed criteria, Ready / Conditional / Not ready / Blocked |

The card suggests the readiness review when 3 or more of its AI questions come back open. AIRR's full criteria and regulatory sources are in `skills/ai-readiness-review/references/`.
