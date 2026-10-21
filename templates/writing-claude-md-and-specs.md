# Writing CLAUDE.md files and specs

Notes on what makes agent instructions work.

## CLAUDE.md

Models follow roughly 150-200 instructions reliably. Spend them on what the agent can't work out by reading the code.

**Always include**
- Project overview (1-2 sentences)
- Tech stack and key dependencies
- Essential commands (build, test, run)
- Directory structure (key folders only)
- Conventions that cause bugs if missed

**Include if it applies everywhere**
- Branch naming, commit message format
- Testing requirements
- Deployment process

**Never include**
- Secrets (API keys, credentials, connection strings)
- Detailed code style (use a linter)
- Task-specific instructions (use separate files)
- Anything the agent could figure out from the code

**Move to separate files**
- Database schema details
- Complex workflow procedures
- Architecture deep-dives
- Onboarding docs

**Subagent guidance** is worth a short section:

```markdown
## Subagent Guidelines
- Security reviews: fresh subagent, no implementation context carried over
- Code exploration: read docs/index.md first
- Documentation: free access to docs/
```

## Specs

1. **Start high-level, let the agent draft the details.** Write a short product brief, have the agent expand it into a `SPEC.md`, and treat that as the source of truth. Use plan mode (read-only) and refine until there's no room for misreading.
2. **Structure it like a PRD.** Good specs cover six areas: commands (with real flags), testing, project structure, code style (show examples), git workflow, and boundaries. Version it with the code.
3. **Break work into modular prompts.** The more requirements in one prompt, the worse each one is followed. Split by domain (`SPEC_backend.md`, `SPEC_frontend.md`), refresh context per major task, and use subagents for specialties.
4. **Build in self-checks and your expertise.** Use three tiers: ✅ Always / ⚠️ Ask first / 🚫 Never. "Never commit secrets" is the most common constraint across thousands of real agent configs. Add verification steps, conformance tests, and the pitfalls only you know.
5. **Test, iterate, evolve.** Run tests after each milestone, update the spec when something goes wrong or requirements change, and re-sync the agent with the new spec.
