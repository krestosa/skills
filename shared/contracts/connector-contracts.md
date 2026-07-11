# Connector contracts

The exact connector descriptions are stored in:

- `../catalogs/github-read-verbatim.md`
- `../catalogs/github-write-verbatim.md`

Those files are immutable catalogs. They document 56 Read entries and 41 Write entries exactly as supplied. Do not substitute inferred tool names for the supplied text.

At runtime:

1. discover which connector actions are actually loaded;
2. map the requested operation to an available action;
3. preserve the verbatim catalog unchanged;
4. report missing capability rather than using remote `git` or `gh`;
5. require action-specific authorization for writes.

The authorization envelope is defined in `authorization-envelope.schema.json`.
