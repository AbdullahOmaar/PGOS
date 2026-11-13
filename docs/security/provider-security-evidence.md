# PGOS Repository Security Evidence

**Evidence date:** 2026-11-13  
**Repository:** `AbdullahOmaar/PGOS`  
**Visibility:** PUBLIC  
**Default branch:** `main`  
**Exact main revision observed:** `33f88e71ea15a85e2c90cf16e1c31311b1a1c9ff`  
**Disposition:** PARTIAL — current-tree scan and exact-main CI/CodeQL passed; fresh provider alert inventories and runtime authorization evidence remain unavailable

This page records a bounded provider-state snapshot. It is not a security certification, penetration test, complete secret-history scan, or proof that PGOS enforces authorization at runtime.

## Verified GitHub branch ruleset

Ruleset [27170450](https://github.com/AbdullahOmaar/PGOS/rules/27170450), **PGOS main — Pull Request and CI Enforcement**, was read back as active for `refs/heads/main` at the evidence revision.

Verified rules:
- Pull requests are required before changes reach `main`.
- The required status check is `validate`, with strict up-to-date checking.
- Non-fast-forward updates and branch deletion are blocked.
- Linear history is required.
- Allowed merge methods are squash and rebase.
- No bypass actors are configured; the connected GitHub principal reports it cannot bypass the ruleset.

The latest ruleset readback reports:
- `required_approving_review_count: 0`
- `required_reviewers: []`
- `require_last_push_approval: false`
- `required_review_thread_resolution: false`
- `require_code_owner_review: false`
- `require_extra_approval_for_unattributed_changes: false`

The Project Owner explicitly instructed that GitHub PR reviewer gates remain removed and must not be re-enabled. The current provider readback matches that direction. This is limited to GitHub PR approval/latest-push/review-thread enforcement; it does **not** waive independent verification, security/privacy review, or named Release Authority for high-impact operational work. No provider setting mutation was performed in this evidence capture.

## Exact-revision automation evidence

At exact main SHA `33f88e71ea15a85e2c90cf16e1c31311b1a1c9ff`:
- GitHub Actions validation run [43365868829](https://github.com/AbdullahOmaar/PGOS/actions/runs/43365868829) completed SUCCESS. Its `validate` job completed core synthetic-record validation (4 JSON), extended-record validation (1 JSON), and **20/20 unit tests** successfully.
- CodeQL run [43365868563](https://github.com/AbdullahOmaar/PGOS/actions/runs/43365868563) completed SUCCESS; `Analyze (python)` succeeded.

These are CI/static-analysis signals, not proof of runtime authorization, complete dependency coverage, or absence of every vulnerability.

## Secret scanning and dependency coverage

- A fresh bounded scan of the exact current main tree retrieved all **44/44 tracked file blobs** as UTF-8 text. The ten documented pattern groups were checked: private-key headers, GitHub tokens, AWS access keys, Google API keys, OpenAI key formats, Slack tokens, Stripe secret-key formats, credential-bearing PostgreSQL/MySQL/MongoDB URIs, literal password/client-secret/access-token/API-key assignments, and JWT-like tokens. Result: **zero matches** across all groups.
- The bounded tree scan does not cover unreachable/dangling Git objects, hidden server-side objects, unenumerated refs/tags, binaries or formats outside the patterns. It is not an absolute guarantee that no secret exists.
- The recorded reachable-history scan covered 50 commits and 78 changed-file diffs using the same ten bounded pattern groups; zero matches were recorded. It does not cover unreachable objects or unenumerated refs.
- The last recorded provider readback reported GitHub Secret Scanning and Push Protection enabled with zero open alerts at that checkpoint. A fresh provider-settings and alert-inventory readback was not available in the current connector scope. Current state is therefore **NOT FRESHLY VERIFIED**.
- The last recorded provider readback had `secret_scanning_non_provider_patterns` disabled. Generic/non-provider-pattern secret coverage is **NOT ESTABLISHED**.
- Dependabot enablement is Owner-reported, but a fresh provider readback and alert inventory were blocked by the available connector surface. Status: **OWNER-REPORTED / PROVIDER READBACK BLOCKED**.
- The current repository tree has no supported dependency manifest or lockfile (for example `requirements.txt`, `pyproject.toml`, `package.json`, `poetry.lock`, `Pipfile`, `uv.lock`, `go.mod`, or `Cargo.toml`). A dependency inventory or vulnerability audit cannot be demonstrated from this tree.

## Runtime and authorization limitations

The repository validators check record structure and selected invariants. Connected Notion, Linear and GitHub tools expose record operations but no PGOS policy runtime or authorization/transition API. The synthetic cross-tool exercise proved record creation and Linear state synchronization only. Default-deny, wrong-project, expired-permission and principal-mismatch enforcement remain **NOT TESTABLE** with the available runtime/tool surface.

## Required follow-up

1. Obtain supported provider access to re-read Secret Scanning, Push Protection, generic-pattern coverage, Dependabot settings and alert inventories.
2. Add an appropriate dependency manifest only when the project intentionally adopts runtime dependencies; then enable and verify dependency auditing.
3. Build or expose a real policy-enforcement runtime and execute negative authorization tests against isolated synthetic data before claiming behavioral governance enforcement.

No provider setting, secret, production record, deployment, or paid resource was changed by this evidence capture.
