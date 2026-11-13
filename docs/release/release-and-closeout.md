# Release, Verification & Closeout Standard

**Status:** DRAFT | **Version:** 0.1.0 | **Class:** CONTROLLED

## Release Candidate packet
- Exact source revision and artifact digest.
- Approved scope and Decision versions.
- Required automated/manual checks with PASS, FAIL, NOT RUN, STALE or UNKNOWN.
- Applicable review disposition (including a documented PGOS maintainer self-review only where DEC-PGOS-003 applies).
- Security/privacy/data migration review.
- Known issues, residual risks and approved exceptions.
- Backup/rollback/restore plan.
- Named Release Authority approval.
- Deployment receipt and live functional verification.

READY_FOR_APPROVAL is not permission to deploy.

## Evidence quality
Every evidence item identifies Evidence ID, Project/Work Order, criterion, source URL, exact commit/artifact/schema revision, environment, configuration and test scope, command/procedure, result, timestamp, producer, reviewer and invalidation triggers.

## Review and separation of duties
For the PGOS governance-document package, a documented Project Master / maintainer self-review may satisfy the document-review gate under [DEC-PGOS-003](https://app.notion.com/p/4179320b90fb81b88be4fcdaf4154618). Owner adoption and any release approval remain separate.

For high-impact operational changes, preserve independent verification, designated security/privacy review and named Release Authority approval as required by the applicable risk policy. This decision does not waive those controls or provider-enforced PR rules.

## Distinct completion states
- IMPLEMENTED — change exists.
- TESTED — required checks passed on the relevant exact candidate.
- REVIEWED — required review accepted that candidate.
- ACCEPTED — outcome owner/verifier accepted criteria.
- MERGED — integrated into target branch.
- DEPLOYED — provider reports deployment of artifact.
- LIVE_VERIFIED — intended live environment/behavior checked.

A build pass is not product acceptance. HTTP 200 is not journey verification.