# GitHub Write actions — verbatim connector catalog

```yaml
catalog_kind: write
entry_count: 41
payload_sha256: 499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d
normalization: forbidden
deduplication: forbidden
paraphrase: forbidden
correction: forbidden
```

The content below is authoritative and must remain byte-for-byte identical. Availability in a specific session must be discovered independently and must not rewrite this catalog.

<!-- VERBATIM_CATALOG_BEGIN -->
Create a top-level PR Conversation comment (Issue comment).

Add assignees to an issue or pull request. Returns a normalized issue snapshot after the mutation. Docs: https://docs.github.com/en/rest/issues/assignees?apiVersion=2022-11-28#add-assignees-to-an-issue

Add labels to an issue or pull request. Returns a normalized issue snapshot after the mutation. Docs: https://docs.github.com/en/rest/issues/labels?apiVersion=2022-11-28#add-labels-to-an-issue

Add a reaction to an issue comment.

Add a reaction to a GitHub pull request.

Add a reaction to a pull request review comment.

Add a review to a GitHub pull request. review is required for REQUEST_CHANGES and COMMENT events.

Convert an open pull request back to draft state. Returns the connector's normalized PR snapshot after the transition. Docs: https://docs.github.com/en/graphql/reference/mutations#convertpullrequesttodraft

Create a blob in the repository and return its SHA.

Create a new branch from exactly one existing commit SHA or base ref.

Create a commit pointing to tree_sha with one or more parents.

Create a UTF-8 text file through GitHub's contents API. Returns only the resulting commit SHA, not GitHub's full content/commit payload. Docs: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents

Create a GitHub issue. Returns a normalized issue snapshot, not GitHub's raw REST payload. Docs: https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#create-an-issue

Open a pull request in the repository. Returns the connector's normalized PR snapshot, not the full REST response payload. Docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request

Create a tree object in the repository from the given elements.

Delete a file through GitHub's contents API. Returns only the resulting commit SHA. Docs: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#delete-a-file

Dismiss a submitted pull request review. Returns the normalized review snapshot after dismissal. Docs: https://docs.github.com/en/graphql/reference/mutations#dismisspullrequestreview

Enable auto-merge for a pull request. This wrapper infers the merge method from repository settings and returns only `success`. Docs: https://docs.github.com/en/graphql/reference/mutations#enablepullrequestautomerge

Label a pull request.

Lock an issue or pull request conversation. Allowed `lock_reason` values are `off-topic`, `too heated`, `resolved`, and `spam`. Docs: https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#lock-an-issue

Mark a draft pull request as ready for review. Returns the connector's normalized PR snapshot after the transition. Docs: https://docs.github.com/en/graphql/reference/mutations#markpullrequestreadyforreview

Merge a pull request immediately. Returns GitHub's merge result payload (`sha`, `merged`, `message`). Docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#merge-a-pull-request

Remove assignees from an issue or pull request. Returns a normalized issue snapshot after the mutation. Docs: https://docs.github.com/en/rest/issues/assignees?apiVersion=2022-11-28#remove-assignees-from-an-issue

Remove one label from an issue or pull request. Returns a normalized issue snapshot after the mutation. Docs: https://docs.github.com/en/rest/issues/labels?apiVersion=2022-11-28#remove-a-label-from-an-issue

Remove individual or team reviewer requests from a pull request. Returns the connector's normalized PR snapshot after the mutation. Docs: https://docs.github.com/en/rest/pulls/review-requests?apiVersion=2022-11-28#remove-requested-reviewers-from-a-pull-request

Remove a reaction from an issue comment.

Remove a reaction from a GitHub pull request.

Remove a reaction from a pull request review comment.

Reply to an inline review comment on a PR (Files changed thread). comment_id must be the ID of the thread’s top-level inline review comment (replies-to-replies are not supported by the API)

Request individual or team reviewers on a pull request. Returns the connector's normalized PR snapshot after the review request mutation. Docs: https://docs.github.com/en/rest/pulls/review-requests?apiVersion=2022-11-28#request-reviewers-for-a-pull-request

Re-run all failed jobs in a GitHub Actions workflow run. Use this to retry only the failed jobs from a workflow run, instead of starting a full new attempt for successful jobs too. The linked GitHub app or token must have GitHub Actions write permission for the repository. Docs: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#re-run-failed-jobs-from-a-workflow-run

Re-run one GitHub Actions workflow job. Use this when a specific failed or cancelled job should be retried without re-running every failed job in the workflow run. The linked GitHub app or token must have GitHub Actions write permission for the repository. Docs: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#re-run-a-job-for-a-workflow-run

Resolve an inline pull request review thread. Docs: https://docs.github.com/en/graphql/reference/mutations#resolvereviewthread

Unlock an issue or pull request conversation. Docs: https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#unlock-an-issue

Mark an inline pull request review thread as unresolved. Docs: https://docs.github.com/en/graphql/reference/mutations#unresolvereviewthread

Replace a UTF-8 text file through GitHub's contents API. Returns the resulting commit SHA and content blob SHA. Use `content_sha` for a subsequent sequential update. Do not run update/delete writes for the same path in parallel. Docs: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents

Update a GitHub issue, including title/body, state, labels, assignees, or milestone. Returns a normalized issue snapshot after the patch. Docs: https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#update-an-issue

Update a top-level PR Conversation comment (Issue comment).

Update PR metadata, base branch, or open/closed state. Returns the connector's normalized PR snapshot. Docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#update-a-pull-request

Move branch ref to the given commit SHA.

Update an inline review comment (or a reply) on a PR.
<!-- VERBATIM_CATALOG_END -->
