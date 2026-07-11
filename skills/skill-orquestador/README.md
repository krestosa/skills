# skill-orquestador

A modular senior-engineering orchestration skill for arbitrary software repositories, adapted for GPT-5.6 Sol.

The skill is outcome-first, loads the smallest relevant route and stack profile, preserves the canonical engineering sources byte-for-byte, and keeps the full supplied GPT-5.6 guidance as reference rather than injecting it into every task. Remote GitHub operations are connector-only; local Git remains available for local workspace operations.

Key files:

- `SKILL.md`: lean entrypoint and completion contract.
- `policies/gpt-5.6-sol.md`: compact operational model policy.
- `models/gpt-5.6-sol.json`: machine-readable defaults and routing behavior.
- `templates/gpt-5.6-prompt-contract.md`: outcome-first prompt structure.
- `evals/gpt-5.6-sol.json`: representative migration and regression cases.
- `references/gpt-5.6-sol-prompting-guidance.md`: full supplied guidance.
- `manifests/modules.json`: route loading.
- `catalogs/`: exact connector descriptions, byte-validated.

Run local validation:

```bash
python scripts/validate_skill.py
```

Build the standalone compiled artifact:

```bash
python scripts/build_compiled.py
```

Build the ChatGPT Project package:

```bash
python scripts/build_chatgpt_flat.py
```
