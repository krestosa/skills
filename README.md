# Skills

A hierarchical, repository-agnostic skill system for software delivery.

```text
SKILL.md
└── skills/main
    └── skills/orchestrator
        └── skills/individual/*
```

## Layers

- `skills/main/`: global prompt and directives. It defines outcome, personality, collaboration style, authorization, tool boundaries, output priorities, and stop rules.
- `skills/orchestrator/`: selects and coordinates only the individual skills required by the current request. It can operate in the current chat or emit bounded prompts for separate chats.
- `skills/individual/`: specialized skills. Each `SKILL.md` includes its role, personality, collaboration style, success criteria, tools, output, and stop rules.
- `skills/skill-orquestador/`: lossless canonical engineering source library and verbatim GitHub connector catalogs used by the hierarchy.

## Invariants

- No repository, owner, branch, framework, product, or organization is a built-in default.
- Remote GitHub reads and writes use the GitHub connector.
- Local `git` is limited to local workspace operations.
- GitHub Read and Write connector catalogs remain verbatim.
- No GitHub workflows are included.
- The orchestrator loads only the skills required by the current task.
- Canonical source texts are referenced, not duplicated or rewritten.

## Validate

```bash
python skills/main/scripts/validate_hierarchy.py
python skills/skill-orquestador/scripts/validate_skill.py
```
