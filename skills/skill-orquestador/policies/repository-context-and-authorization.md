# Repository context and authorization

The skill has no built-in repository. Resolve the target repository for every task.

Required context:

```yaml
repository_full_name: {{repository_full_name}}
repository_url: optional canonical URL
default_branch: connector-resolved branch
base_sha: exact verified SHA
working_branch: explicit branch or null
```

Resolution order:

1. explicit repository in the current user request;
2. explicit GitHub URL in the current request;
3. repository identified by the current project or local workspace;
4. connector metadata;
5. ask for the missing `owner/name` only when ambiguity remains.

Authorization statement for generated prompts:

```text
The user states that {{repository_full_name}} is owned by them or under their legitimate control. The task is limited to authorized software development, maintenance, validation, documentation, and Git/GitHub operations on that repository. No authority is inferred for other repositories, accounts, or infrastructure.
```

Authorization is repository-specific and action-specific. It does not automatically authorize remote writes, force updates, review actions, CI reruns, auto-merge, merge, deletion, or destructive recovery.
