---
name: skills-main
description: Repository-wide entrypoint for the hierarchical skill system. Loads the global main contract, then delegates routing to the orchestrator.
---

# Skills repository entrypoint

Load `skills/main/SKILL.md`.

Then load `skills/orchestrator/SKILL.md`.

Do not load individual skills directly from this entrypoint. The orchestrator selects the smallest sufficient skill set for the current request.
