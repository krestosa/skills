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
Razonamiento: [Instant|Medium|High]

The reasoning line is outside the prompt block, appears immediately after it, and is the final element of that prompt delivery. It is not copied into the target chat. It contains no model recommendation and no explanation. The target model remains the latest available model as internal policy.

When several workstreams require separate prompts, repeat the prompt-block-plus-directive pair for each workstream. Do not insert prose between pairs. The final response element is the reasoning directive for the final prompt.

## Internal design record

This optional diagnostic is for prompt construction or requested audits only. It is not emitted in ordinary prompt delivery.

```text
Reasoning classification:
- residual ambiguity: [closed | bounded | open]
- adaptation burden: [low | moderate | high]
- risk floor: [low | moderate | high plus any hard trigger]
- prompt closure adjustment: [none | High→Medium | Medium→Instant]
- selected level: [Instant | Medium | High]
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
