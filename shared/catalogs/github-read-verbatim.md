# GitHub Read actions — verbatim connector catalog

```yaml
catalog_kind: read
entry_count: 56
payload_sha256: 610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e
normalization: forbidden
deduplication: forbidden
paraphrase: forbidden
correction: forbidden
```

The content below is authoritative and must remain byte-for-byte identical. Availability in a specific session must be discovered independently and must not rewrite this catalog.

<!-- VERBATIM_CATALOG_BEGIN -->
Check whether a GitHub repository has been set up. You must populate exactly one of `repository_full_name`, `repository_id`, or `repository_url` to select the repository.

Compare two commits/refs and return per-file stats plus compare metadata. This is a thin wrapper around `GithubPlugin.compare_commits` to provide a stable, compact response shape to connector consumers.

Download a GitHub private user image attachment URL. Use this only for private-user-images.githubusercontent.com URLs, such as GitHub issue or pull request image uploads. Use fetch or fetch_file for repository files.

Download a GitHub Actions workflow artifact ZIP archive. GitHub serves this endpoint through a temporary redirect; the underlying client follows that redirect before returning a reusable file reference for the ZIP bytes. Docs: https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28#download-an-artifact

Fetch a UTF-8 text file from GitHub by URL. When the repository and path are known, prefer fetch_file; its optional ref defaults to the repository's default branch. Use a file URL such as https://github.com/owner/repo/blob/branch/path/to/file.py. raw.githubusercontent.com file URLs and api.github.com/repos/.../contents/... URLs with a ref query parameter are also accepted.

Fetch blob content by SHA from the given repository.

Fetch a commit with its metadata, diff, and canonical URL.

Fetch GitHub Actions workflow runs associated with a commit SHA. This wrapper currently filters to pull-request-triggered runs and returns the first page only. Docs: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-repository (este es muy importante, tiene que ser verificado por el propio conector asi yo no tengo que mandar el link del flow, osea debe esperar a que termine el flow si es despues de un push y si el prompt lo pide verificar y entregal el output segun sea requerido)

Fetch file content by repository path, using the default branch when ref is omitted.

Fetch a GitHub issue. You must populate exactly one of `repository_full_name`, `repository_id`, or `repository_url` to select the issue's repository.

Fetch comments for a GitHub issue across all pages.

Fetch a pull request with its diff, metadata, and optionally comments.

Fetch a merged PR discussion timeline. The returned list combines issue comments, inline review comments, and review submissions into one normalized array. Docs: https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28 Docs: https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28 Docs: https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28

Fetch the patch for one validated changed file in an accessible pull request. Call `list_pr_changed_filenames` first, then pass an exact returned path. A valid pull request that does not contain the path returns `patch=null`. A 404 means GitHub could not resolve the repository or pull request; do not retry other paths.

Fetch the patch for a GitHub pull request across all changed-file pages.

Fetch decoded logs for a GitHub Actions workflow job. GitHub serves this endpoint through a temporary redirect; the underlying client follows that redirect before decoding the bytes. Docs: https://docs.github.com/en/rest/actions/workflow-jobs?apiVersion=2022-11-28#download-job-logs-for-a-workflow-run-job

Fetch steps for a GitHub Actions workflow job. Returns only step summaries, not the full job payload. Docs: https://docs.github.com/en/rest/actions/workflow-jobs?apiVersion=2022-11-28#get-a-job-for-a-workflow-run

Fetch artifacts for a GitHub Actions workflow run. This wrapper returns the first page only. Docs: https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28#list-workflow-run-artifacts

Fetch jobs for a GitHub Actions workflow run. This wrapper returns the latest attempt's jobs from the first page only. Docs: https://docs.github.com/en/rest/actions/workflow-jobs?apiVersion=2022-11-28#list-jobs-for-a-workflow-run

Fetch the combined CI status and individual status checks for a commit.

Fetch a raw commit diff or patch.

Fetch reactions for an issue comment.

Fetch just the diff or patch text for a pull request.

Get metadata (title, description, refs, and status) for a pull request. This action does *not* include the actual code changes. If you need the diff or per-file patches, call `fetch_pr_patch` instead (or use `get_users_recent_prs_in_repo` with include_diff=True when listing the user's own PRs).

Fetch reactions for a GitHub pull request.

Fetch reactions for a pull request review comment.

Retrieve the GitHub profile for the authenticated user.

Retrieve metadata for a GitHub repository. You must populate exactly one of `repository_full_name`, `repository_id`, or `repository_url`: - `repository_full_name`: `owner/name`, such as `openai/openai`. Maps to GitHub REST `owner` and `repo` path parameters. - `repository_id`: numeric GitHub repository ID, such as `1296269`. - `repository_url`: repository URL or nested repository URL, such as a PR, issue, branch, file, REST API, GitHub Enterprise Server `/api/v3`, or GHE.com API URL. GitHub REST repository docs: https://docs.github.com/en/rest/repos/repos#get-a-repository GitHub Enterprise Server REST docs: https://docs.github.com/en/enterprise-server@latest/rest/using-the-rest-api/

Return the collaborator permission level for a user on a repository.

Get the GitHub App installation ID for a repository visible to the linked account.

Return the GitHub login for the authenticated user

List the user's recent GitHub pull requests in a repository. `limit` is the final number of PRs returned. The connector paginates the underlying GitHub search endpoint to satisfy larger limits.

List commits for a repository in newest-first GitHub API order.

List entries in a repository directory, using the default branch when ref is omitted.

List all organizations the authenticated user has installed this GitHub App on.

List all accounts that the user has installed our GitHub app on.

List changed filenames for a PR across all paginated file-list pages.

List inline review threads on a pull request, including resolved state. Returns GraphQL review thread nodes, including comment bodies and resolution metadata. Docs: https://docs.github.com/en/graphql/reference/objects#pullrequestreviewthread

List review submissions on a pull request. Returns GraphQL review nodes normalized into the connector's review model. Docs: https://docs.github.com/en/graphql/reference/objects#pullrequestreview

Return the most recent GitHub issues the user can access. `top_k` is the final result limit. The connector transparently paginates GitHub's issues API until that limit is reached or no more pages exist.

List repositories accessible to the authenticated user.

List repositories accessible to the authenticated user filtered by affiliation.

List repositories accessible to the authenticated user.

List the authenticated user's organization memberships.

List organizations the authenticated user is a member of.

Uses mfetch to perform document fetch for link following and citations.

Uses synced RAG index to perform semantic search against query. The index is refreshed until (now - 2h). Additional query syntax: - Include +() boosts for significant entities (people, teams, products, projects, key terms). Example: +(John Doe). - Whenever required, set freshness explicitly with the --QDF= (Query Deserved Freshness) parameter according to temporal requirements. Infer and expand relative dates clearly in queries utilizing conversation_start_date, which refers to the absolute current date. QDF Reference: --QDF=0: stable/historic info (10+ yrs OK) --QDF=1: general info (<=18mo boost) --QDF=2: slow-changing info (<=6mo) --QDF=3: moderate 

Resolve a branch, tag, or commit-ish ref to a commit SHA.

Search files within a specific GitHub repository. Provide a plain string query, avoid GitHub query flags such as is:pr. Include keywords that match file names, functions, or error messages. repository_name or org can narrow the search scope. Example: query="tokenizer bug" repository_name="tiktoken". topn is the number of results to return. No results are returned if the query is empty.

Search GitHub branches within a repository.

Search GitHub commits globally, by organization, or optionally by repository. Include at least one non-qualifier search term in the query. To list recent commits without matching text, pass an empty query with `repository_full_name` and use the default descending order.

Search for a repository (not a file) by name or description. To search for a file, use `search`.

Search repositories within the user's installations using GitHub search.

Search GitHub issues. You must populate exactly one of `repository_full_name`, `repository_id`, or `repository_url` to select the repository or repositories to search.

Search GitHub pull requests globally, by organization, or optionally by repository.

Search for a repository (not a file) by name or description. To search for a file, use `search`.
<!-- VERBATIM_CATALOG_END -->
