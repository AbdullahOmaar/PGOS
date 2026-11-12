# Work Order & Delivery Lifecycle Standard

**Status:** DRAFT | **Version:** 0.2.0 | **Class:** CONTROLLED

## Mandatory Work Order fields
- Work Order ID, Project ID, title, revision and status.
- Objective / Outcome ID and measurable value.
- Scope and explicit non-goals.
- Accountable human Owner, Owner instruction source/decision reference, delivery lead and verified assignee identity.
- Separate agent/worker runtime identity and binding evidence; do not infer it from the Owner conversation.
- Permission grant: autonomy level, tools, actions, resources, environment and expiry.
- Connected-tool principal and operation permission evidence where relevant.
- Dependencies and prerequisite Decision IDs.
- Measurable acceptance criteria and negative/failure behavior.
- Verification plan, verifier and evidence source.
- Risk level and security/privacy/data impact.
- Rollback or compensating action where relevant.
- Budget/effort limits where applicable.
- Approval reference, created time and change history.

## Owner channel

Where a canonical project decision maps the human Owner to an authenticated conversation channel, instructions from the sender in that established channel are attributable to the human Owner. Do not demand a separate framework account, password, token or manual session ID solely for Owner recognition. Record the decision and available conversation source/date; do not claim cryptographic session proof unless exposed by the platform.

The agent/worker runtime and each connected provider account are separate principals. Verify their identity and permissions independently. Owner authority does not expand the Work Order's scope or grant provider permissions.

## Lifecycle
DRAFT → SUBMITTED → APPROVED → ASSIGNED → CLAIMED → IN_PROGRESS → SUBMITTED_FOR_REVIEW → VERIFYING → ACCEPTED → CLOSED

Exceptional states: BLOCKED, WAITING_APPROVAL, PAUSED, REWORK, REJECTED, CANCELLED, EXPIRED.

Approval is not assignment; assignment is not dispatch; dispatch is not acknowledgement; submission is not acceptance.

## Decomposition
Project Goal → Outcome → Batch → Work Order → Linear Issue(s) → GitHub Change(s) → Verification Evidence.

Batch around coherent results. One accountable owner and one primary writer per shared boundary. Define interfaces and dependencies before parallel implementation.

Linear Done or a merged PR is not by itself outcome acceptance or deployment verification.

**Decision reference:** [DEC-PGOS-001 — Chat-Based Owner Authority & Principal Separation](https://app.notion.com/p/4169320b90fb8121a870dfea96b2135f) — approved for the identity principle only.