# Decisions, Change & Approval Control

**Status:** DRAFT | **Version:** 0.1.0 | **Class:** CONTROLLED

Each material decision contains Decision ID, Project ID, title, status, revision, context, options (including do nothing), chosen option and rationale, consequences, affected scope/contracts/systems, risks, decision owner, approvers, independent reviewer where needed, effective version, review date and supersession links.

Statuses: PROPOSED, UNDER_REVIEW, APPROVED, REJECTED, DEFERRED, SUPERSEDED, REVOKED.

## Change classes
| Class | Typical change | Minimum control |
| --- | --- | --- |
| Editorial | Typo/formatting without semantic change | Maintainer review |
| Minor | Backward-compatible low-risk behavior | Work Order + relevant test/review |
| Major | Scope, API, schema, architecture, access or breaking change | Decision + impact analysis + migration/rollback + Owner approval |
| High impact | Production, privacy/security, financial/legal or irreversible effect | Action-specific approval, independent verification and release controls |

Approval must identify the exact action, resource, environment, scope and validity window. Never infer approval from silence, status labels, issue assignment or a prior unrelated approval.