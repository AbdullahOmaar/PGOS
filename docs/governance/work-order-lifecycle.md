# Work Order & Delivery Lifecycle Standard

**Status:** DRAFT | **Version:** 0.1.0 | **Class:** CONTROLLED

## Mandatory Work Order fields
- Work Order ID, Project ID, title, revision and status.
- Objective / Outcome ID and measurable value.
- Scope and explicit non-goals.
- Accountable owner, delivery lead and verified assignee identity.
- Permission grant: autonomy level, tools, actions, resources, environment and expiry.
- Dependencies and prerequisite Decision IDs.
- Measurable acceptance criteria and negative/failure behavior.
- Verification plan, verifier and evidence source.
- Risk level and security/privacy/data impact.
- Rollback or compensating action where relevant.
- Budget/effort limits where applicable.
- Approval reference, created time and change history.

## Lifecycle
DRAFT → SUBMITTED → APPROVED → ASSIGNED → CLAIMED → IN_PROGRESS → SUBMITTED_FOR_REVIEW → VERIFYING → ACCEPTED → CLOSED

Exceptional states: BLOCKED, WAITING_APPROVAL, PAUSED, REWORK, REJECTED, CANCELLED, EXPIRED.

Approval is not assignment; assignment is not dispatch; dispatch is not acknowledgement; submission is not acceptance.

## Decomposition
Project Goal → Outcome → Batch → Work Order → Linear Issue(s) → GitHub Change(s) → Verification Evidence.

Batch around coherent results. One accountable owner and one primary writer per shared boundary. Define interfaces and dependencies before parallel implementation.

Linear Done or a merged PR is not by itself outcome acceptance or deployment verification.