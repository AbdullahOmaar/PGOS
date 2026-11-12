# Decisions, Change & Approval Control

**Status:** DRAFT | **Version:** 0.2.0 | **Class:** CONTROLLED

Each material decision contains Decision ID, Project ID, title, status, revision, context, options (including do nothing), chosen option and rationale, consequences, affected scope/contracts/systems, risks, decision owner, approvers, independent reviewer where needed, effective version, review date and supersession links.

Statuses: PROPOSED, UNDER_REVIEW, APPROVED, REJECTED, DEFERRED, SUPERSEDED, REVOKED.

## Approval provenance

Approval must be explicit, attributable, scoped and version-specific. Record the canonical decision/work-order reference and, where the project uses a mapped Owner chat channel, the Owner conversation source/date and exact scope approved. Do not require a separate Owner token/password/manual session ID solely to recognize the mapped Owner instruction.

Conversational attribution is not a cryptographic signature or independently verified platform session identity unless the platform exposes that evidence. Keep the human Owner, agent/worker runtime and connected-tool account as separate principals. A chat Owner instruction does not authenticate an agent, prove dispatch/acknowledgement, or grant provider permissions.

Approval must identify the exact action, resource, environment, scope and validity window. Never infer approval from silence, status labels, issue assignment or a prior unrelated approval.

## Change classes
| Class | Typical change | Minimum control |
| --- | --- | --- |
| Editorial | Typo/formatting without semantic change | Maintainer review |
| Minor | Backward-compatible low-risk behavior | Work Order + relevant test/review |
| Major | Scope, API, schema, architecture, access or breaking change | Decision + impact analysis + migration/rollback + Owner approval |
| High impact | Production, privacy/security, financial/legal or irreversible effect | Action-specific approval, independent verification and release controls |

Controlled/security/architecture policy changes require independent review by a non-author and explicit Owner approval before adoption.