# skill-orquestador

A modular senior-engineering orchestration skill for arbitrary software repositories.

The skill resolves repository identity at runtime and never embeds a default repository. Remote GitHub operations are connector-only. Local Git remains available for local workspace operations.

Use `SKILL.md` as the entrypoint. `manifests/modules.json` defines route loading. Exact GitHub connector descriptions live in `catalogs/` and are byte-validated.

Run local validation:

```bash
python scripts/validate_skill.py
```

Build the standalone compiled artifact:

```bash
python scripts/build_compiled.py
```
