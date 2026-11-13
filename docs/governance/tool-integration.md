# Notion, Linear & GitHub Integration Standard

**Status:** DRAFT | **Version:** 0.2.1 | **Class:** CONTROLLED

## Notion
Canonical for project charter, outcomes, scope, priorities, ownership, dependencies, Work Orders, decisions, approvals, risks, exceptions, acceptance and handoffs. Prefer one canonical record/database per record class and immutable IDs.

## Linear
Execution tracker: Initiative (optional program), Project (bounded delivery program), Milestone (outcome/release checkpoint), Issue (approved Work Order or implementation unit), Sub-issue (separately owned/verifiable unit), Cycle (capacity window, not scope approval).

Every issue links Project ID, Outcome ID, Work Order ID, decision references, Notion canonical source and GitHub PR/commit when applicable. Status never implies Owner approval or release permission.

## GitHub
Use AGENTS.md, README.md, docs/architecture, docs/adr, docs/security, docs/runbooks, issue/PR templates, tests and scripts as appropriate. Configure branch protection, required PR review, exact-head required checks, secret scanning and deployment environments in provider settings. Documentation alone does not enforce settings.

## Adoption sequence
1. Create project profile and source map.
2. Confirm Notion access and canonical record location.
3. Create Linear project only after outcomes/scope are approved.
4. Link the correct GitHub repository and verify settings.
5. Add project-specific AGENTS.md, templates, checks and ADR baseline.
6. Test a full Work Order flow.
7. Record deviations and maturity level.

If a provider capability is unavailable, document the limitation and approved equivalent; do not claim an integration works until verified.