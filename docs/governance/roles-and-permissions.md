# Roles & Permission Boundaries

**Status:** DRAFT | **Version:** 0.1.0

Roles describe accountability, not automatic permissions.

- **Project Owner:** accountable for outcomes, scope, priority, risk acceptance and action-specific approvals.
- **Project Master / Governance Lead:** maintains governance integrity, dependencies, decision traceability and cross-tool consistency.
- **Delivery Lead:** coordinates approved batches and dependencies.
- **Implementer:** executes only the assigned Work Order within its path, environment and expiry limits.
- **Independent Verifier:** evaluates acceptance evidence without being the sole author of the change for high-risk work.
- **Release Authority:** grants separate release approval.
- **Security / Data Owner:** reviews applicable security, privacy, data and access risks.

Verify human or agent identity independently of role labels. Enforce permissions at the provider/application boundary. Default deny and least privilege. Role assignment never grants merge, production, financial, destructive or external-communication permission by itself.