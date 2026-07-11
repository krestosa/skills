# GPT-5.6 Sol prompt contract

Use this template for complex tasks. Omit a section only when it would add no behavioral information.

```text
Role:
[Function and relevant context.]

Personality:
[Brief tone and collaboration choices.]

Goal:
[User-visible outcome.]

Success criteria:
- [Observable completion condition]
- [Required evidence or validation]
- [Required action or artifact]

Constraints:
- [Safety, authorization, scope, preservation, cost, or business limits]

Tools:
- [Relevant tools and routing decisions]
- [Prerequisites, fallback budget, and prohibited routes]

Output:
[Required fields, sections, format, language, and task-specific detail.]

Stop rules:
- [When to answer, retry, fallback, ask, block, or stop]
```

## Coding delta

Add only what changes behavior:

```text
Repository and verified base:
Owned files and non-scope:
Required behavior:
Validation:
External-write authorization:
```

## Research delta

```text
Question and scope:
Required source quality:
Claims requiring citations:
Coverage or comparison requirement:
Missing-evidence behavior:
```

## Visual delta

```text
Product context and design system:
Required states and responsive behavior:
Visual constraints:
Render-and-inspect checks:
```

## Prompt migration delta

```text
Baseline model and reasoning effort:
Representative eval set:
One change under test:
Pass criteria:
Token, latency, cost, call, and retry measurements:
Rollback condition:
```
