# Roles & Permission Boundaries

**Status:** DRAFT | **Version:** 0.2.1

Roles describe accountability, not automatic permissions.

- **Project Owner:** accountable for outcomes, scope, priority, risk acceptance and action-specific approvals.
- **Project Master / Governance Lead:** maintains governance integrity, dependencies, decision traceability and cross-tool consistency.
- **Delivery Lead:** coordinates approved batches and dependencies.
- **Implementer:** executes only the assigned Work Order within its path, environment and expiry limits.
- **Independent Verifier:** evaluates acceptance evidence without being the sole author of the change for high-risk work.
- **Release Authority:** grants separate release approval.
- **Security / Data Owner:** reviews applicable security, privacy, data and access risks.

## Human Owner identity

A project may explicitly map its Project Owner to an authenticated conversation channel. When that mapping is recorded in the project's canonical governance decision, the human sending messages through that established authenticated Owner conversation is treated as the Project Owner for conversational decisions and instructions. Do not require a separate framework account, password, token, or manually supplied session ID solely to recognize that mapped Owner instruction.

Record the decision reference and the available conversation source/date. Do not claim that the framework independently verified a stable platform session ID, cryptographic signature, or signed principal assertion unless the platform actually exposes such evidence.

This rule is limited to the established Owner channel. Shared or ambiguous accounts, forwarded/pasted messages without provenance, conflicting project context, or unbound channels remain UNKNOWN until resolved.

## Separate principals

- **Agent / worker runtime:** the AI or delegated worker is a separate principal. Its runtime identity, assignment, dispatch, acknowledgement, claim, and handoff require their own evidence. An Owner message does not prove a worker exists or has acknowledged a task.
- **Connected tool account:** GitHub, Notion, Linear, database, and other integrations use their own linked identities. Verify the actual connected account and the permission required for each operation. Owner authority in chat does not grant provider permissions.
- **Application actor:** where the governed application has users/tenants, authenticate and authorize those actors at the server-side application boundary. Do not conflate application users with the Project Owner or integration account.

## Permission enforcement

Bind every capability to the actor, Work Order ID and approved revision, allowed action, resource/path/record, environment, time window/expiry, approval reference, and preconditions. Enforce permissions at the provider/application boundary. Default deny and least privilege.

A valid Owner instruction may establish a decision or authorize a bounded Work Order; it does not grant blanket permission for undeclared scope or A4 actions. Role assignment never grants merge, production, financial, destructive, or external-communication permission by itself.

## Review responsibility

For the PGOS governance-document package only, a documented Project Master / maintainer self-review may satisfy the governance-document review gate under [DEC-PGOS-003 — Master Self-Review for PGOS Governance Package](https://app.notion.com/p/4179320b90fb81b88be4fcdaf4154618). The self-review must identify the exact candidate, changed paths, review criteria, findings/dispositions and result.

This exception does not remove independent verification, security/privacy review, or separate Release Authority requirements for high-impact work, nor does it permit the Project Master to approve their own A4 actions. Provider-enforced review rules remain in force.

**Decision references:** [DEC-PGOS-001](https://app.notion.com/p/4169320b90fb8121a870dfea96b2135f) (Owner identity) and [DEC-PGOS-003](https://app.notion.com/p/4179320b90fb81b88be4fcdaf4154618) (PGOS governance-document review).