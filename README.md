# PGOS — Project Governance OS

**Version:** 0.1.0  
**Status:** DRAFT — Owner review required before adoption  
**Purpose:** A portable, project-agnostic governance operating system for software, product, business, research, and automation projects.

PGOS defines how work is authorized, planned, executed, verified, changed, released, and learned. It does **not** define a project's product strategy, domain rules, technical stack, or regulatory obligations.

## Independence

PGOS is a new standalone framework. It does not inherit approvals, policies, records, repository structure, permissions, or architecture from AIBA, MWOS, Aureon, Nuvio, or any other existing project.

## Authority model

| System | Canonical responsibility |
| --- | --- |
| Notion | Project charter, scope, ownership, priorities, dependencies, decisions, approvals, work orders, risks, acceptance and handoffs |
| Linear | Execution planning and tracking: initiatives, projects, outcomes, batches, issues, cycles and blockers |
| GitHub | Source code, engineering standards, ADRs, branches, commits, PRs, reviews, tests, CI and release artefacts |
| Runtime providers | Actual deployment, infrastructure, database and production-state evidence |

See [`docs/governance/authority-model.md`](docs/governance/authority-model.md).

## Package contents

- `docs/governance/` — charter, authority, roles, work orders, decisions, evidence and integrations.
- `docs/security/` — risk, identity, data classification and security baseline.
- `docs/release/` — release gates, rollback and live verification.
- `docs/architecture/` — reusable architecture decision record standard.
- `templates/` — machine-readable JSON starter records, including Project, WorkOrder, Decision, ChangeRequest, Handoff, Risk, Evidence, Incident and Release.
- `scripts/validate_records.py` — dependency-free core record and cross-reference validator.
- `scripts/extended_records.py` — extended ChangeRequest, Handoff and Incident preflight validator and CLI, including identity-state, approval-state, timeline and cross-reference checks.
- `tests/` — unit and synthetic adoption tests.
- `examples/` — synthetic project profiles and extended governance records.

## Quick start

Requires Python 3.10+; no third-party package is required.

```bash
python scripts/validate_records.py examples/sample-project
python -m scripts.extended_records examples/extended-adoption
python -m unittest discover -s tests -v
```

The sample projects are synthetic and intentionally contain no real customer data, credentials, or production identifiers.

## Project adoption sequence

1. Register a project and appoint its accountable owner.
2. Create its charter and define outcomes, scope and non-goals.
3. Classify risk and data; select the project governance profile.
4. Map canonical sources and tool links.
5. Approve a bounded Work Order before execution.
6. Track execution in the selected work-management tool.
7. Link source changes and exact-revision evidence.
8. Independently verify acceptance criteria where required.
9. Obtain action-specific release approval before production or external side effects.
10. Record acceptance, residual risks, handoff and closeout.

## Identity and approval boundary

A project may map its human Project Owner to an authenticated conversation channel through a canonical governance decision. The sender in that established Owner conversation may then provide attributable Owner instructions without a separate PGOS account, password, token or manual session ID. This is conversational attribution, not a cryptographic signature or a stable session identifier that PGOS can independently verify unless the platform exposes such evidence.

The AI/worker runtime identity and each connected tool account remain separate principals. Their identities and permissions must be checked through their own runtime/provider evidence. A chat Owner instruction does not grant provider permissions or blanket A4 authority.

## Important limitations

- The validators check record structure and selected governance invariants. They are not a policy engine, identity provider, access-control gateway, cryptographic signature verifier, or proof of tool configuration.
- The extended-record validator checks handoff identity flags and approval-state consistency as record data only; it does not authenticate the named actors or the human author of a chat instruction.
- Repository branch protection, required checks, secret scanning, permissions, and deployment gates must be configured and tested in the provider.
- A JSON record marked `APPROVED` is only a claim unless the approval reference is verifiable in the project's canonical approval system.
- PGOS remains DRAFT until independently reviewed and explicitly adopted by its Owner.

## Governance links

- Notion canonical root: https://app.notion.com/p/4169320b90fb81eda52cd8fd8915faa3
- Owner identity decision: https://app.notion.com/p/4169320b90fb8121a870dfea96b2135f
- Linear project: https://linear.app/3a-agent/project/pgos-project-governance-os-v010-2ec77b5f295f
- Linear foundation issue: https://linear.app/3a-agent/issue/3A-223/complete-pgos-foundation-v010

These links are the current PGOS workspace references; they do not imply overall project approval or successful provider enforcement.