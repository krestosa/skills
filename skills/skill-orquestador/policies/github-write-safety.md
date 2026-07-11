# GitHub write safety

All connector write actions require explicit scope and post-write verification.

Before a write, resolve:

- exact `repository_full_name`;
- target issue, PR, branch, ref, comment, review, job, run, or file;
- current remote SHA or object ID when applicable;
- whether the action is additive, replacing, state-changing, destructive, or irreversible;
- authorization for that specific write category;
- expected result and rollback path.

For connector-native code publication, prefer one atomic Git Data API commit:

```text
verified remote parent/tree
→ create_blob
→ create_tree
→ create_commit
→ create_branch or fast-forward update_ref
→ fetch_commit
→ compare_commits
→ byte verification
```

Do not use force ref updates unless destructive authorization is explicit and the expected remote SHA is revalidated immediately before the write.

Do not silently write to the default branch. Do not reply, resolve threads, submit reviews, rerun CI, enable auto-merge, or merge unless the user authorized that category.
