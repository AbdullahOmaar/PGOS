# Open-Source Foundation Evaluation

**Status:** PROPOSED / DRAFT — evaluation only  
**Review date:** 2026-11-12  
**Related Linear document:** https://linear.app/3a-agent/document/pgos-open-source-foundation-evaluation-and-workflow-poc-plan-v010-c15d2b6e8bb7  
**Related Notion record:** https://app.notion.com/p/4169320b90fb818aa180e8c3fa3d4026

## Purpose and boundary

Evaluate mature open-source tools that can supply commodity project-management, policy-decision and workflow-orchestration capabilities. PGOS should retain its distinctive governance responsibilities: project and Work Order identity, bounded authorization, policy gates, attributable human approvals, evidence, review, change control and audit traceability.

This document does not select or approve a production component. No installation, provisioning, migration, production integration, paid hosting or replacement of the current Notion / Linear / GitHub authority model is authorized here.

## Candidate matrix

| Component | License / edition | PGOS fit | Limitation and disposition |
|---|---|---|---|
| OpenProject Community | GPLv3; self-managed Community edition is free of charge with unlimited users and projects. | Potential self-hosted project-management foundation. | Overlaps Linear. Keep Linear and Notion unchanged; consider only as an alternative after an explicit migration decision. Operator still owns hosting, backup, upgrades and security. |
| Open Policy Agent (OPA) | Open-source general-purpose policy engine; graduated CNCF project. | Strong candidate for policy-as-code and decision evaluation using actor, Work Order, action, resource, environment, revision and approval attributes. | OPA is a Policy Decision Point, not an identity provider. PGOS must authenticate actors and enforce allow/deny decisions in its own Policy Enforcement Point. |
| Conductor OSS | Apache 2.0; self-hostable. Documents durable workflows, human approval, MCP tool discovery/calls, retry, pause/resume and execution history. Orkes is identified as primary maintainer. | Strong fit for human-in-loop Work Order and AI-agent orchestration. | Test operational footprint, persistence/broker options, audit retention, identity and enforcement boundaries. **Candidate A for POC only.** |
| Temporal | MIT; durable-execution platform with recorded workflow event history and recovery after failures. | Strong general-purpose durable workflow engine. | Code-first workflow orchestration; compare the effort to implement and maintain human approval, evidence and audit mapping. **Candidate B for POC.** |
| Flowable OSS | Apache 2.0; BPMN/CMMN/DMN engines, Java-based, supporting human and system activities. | Good fit for modeled business processes and human task flows; Java/Spring-friendly. | Assess operational complexity and whether BPMN/CMMN modeling is justified for PGOS. **Candidate C for POC.** |
| Kestra OSS | Apache 2.0. Current edition documentation says OSS uses one shared Basic Auth account; individual accounts, SSO and fine-grained RBAC are Enterprise features. | Useful for automation and data workflows. | Not suitable as PGOS's primary identity or approval enforcement layer under the free edition. |

## Proposed architecture boundary

- Notion remains canonical for project scope, owners, priorities, decisions, approvals and Work Orders.
- Linear remains execution tracking; GitHub remains engineering source and exact-revision evidence; runtime providers remain runtime truth.
- A future PGOS control plane authenticates identity, resolves project/Work Order context, requests policy decisions and enforces them before protected side effects.
- OPA may evaluate policy; it does not authenticate a person/agent and does not enforce anything unless a PGOS service acts as the PEP.
- A workflow engine may coordinate lifecycle states, retries and human waits; it must not grant permissions on its own. Re-check authoritative approval and policy immediately before every protected tool action.
- Do not migrate or duplicate canonical Notion/Linear/GitHub records during evaluation.

## Comparable workflow POC

Use an isolated synthetic Work Order; never use the current DRAFT sample Work Order as authority to implement a real feature.

1. Validate a synthetic Work Order and its project reference.
2. Resolve a synthetic actor identity and project binding. Unknown, expired or mismatched identity must fail closed.
3. Classify risk and calculate the required approval.
4. Evaluate a deterministic/mock policy decision first; OPA can be integrated in a later, separately approved stage.
5. Pause for named human approval. Test approve, reject, timeout/expiry, reassignment and resume.
6. Execute only a harmless local/mock worker after a fresh authorization check.
7. Capture exact workflow version, actor, approval decision, timestamps, tool inputs/outputs, retries and evidence.
8. Produce a handoff/closeout record; never claim business acceptance without its acceptance evidence.

## Scorecard

Score each engine 1–5 and attach raw evidence for:
- durability after process/worker restart while waiting for approval;
- approve/reject/expire/reassign and revision-specific approval;
- denial at the enforcement boundary for unknown or stale identity, cross-project resource, expired authorization and wrong revision;
- audit trail, event history, input/output capture and retention;
- retry, timeout, idempotency and duplicate-effect prevention;
- active workflow versioning and safe upgrades;
- Java/Python worker, HTTP/API, MCP, Notion/Linear/GitHub integration;
- OIDC/service identity, least privilege and secrets handling;
- minimum services, persistence, broker, backup/restore, monitoring and resource footprint;
- license, active maintenance, security response and paid-feature boundaries.

## Recommendation to carry forward

- Keep the current Notion + Linear + GitHub authority arrangement.
- Evaluate OPA as the policy-decision component, with authentication and enforcement implemented by PGOS.
- Compare Conductor OSS, Temporal and Flowable on the same synthetic workflow. Conductor is first to prototype because its documented human-approval and native MCP tasks directly match the intended use case; it is not selected until all candidates are scored.
- Keep OpenProject as an alternative project-management option only; no Linear migration.
- Do not use Kestra OSS as the primary identity/approval control boundary while OSS provides only a shared Basic Auth account.

## Approval gates

A runnable POC requires a separate bounded Work Order identifying runtime, exact resources, permitted actions, expiry, test cases, acceptance criteria and independent reviewer. No paid provisioning, public exposure, secrets transfer, production data, production integration, deployment or release is included.

Runtime identity binding for the current assistant session remains NOT VERIFIED. This evaluation is a proposal, not an approved ADR or adoption decision.

## Official references

- OpenProject Community: https://www.openproject.org/community-edition/
- OpenProject GPLv3 and edition FAQ: https://www.openproject.org/docs/faq/
- OPA documentation: https://www.openpolicyagent.org/docs
- OPA deployment / PDP and PEP: https://www.openpolicyagent.org/docs/deploy
- Conductor OSS repository: https://github.com/conductor-oss/conductor
- Conductor MCP guide: https://docs.conductor-oss.org/devguide/ai/mcp-guide.html
- Temporal repository / MIT: https://github.com/temporalio/temporal
- Temporal durable execution: https://docs.temporal.io/temporal
- Flowable Open Source: https://www.flowable.com/open-source-code
- Flowable OSS downloads: https://www.flowable.com/open-source-download
- Kestra OSS versus Enterprise: https://kestra.io/docs/oss-vs-paid
