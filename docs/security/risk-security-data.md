# Risk, Security & Data Governance

**Status:** DRAFT | **Version:** 0.1.0 | **Class:** CONTROLLED

## Risk scoring
Likelihood and impact are each scored 1–5. Inherent score = likelihood × impact. Suggested bands: 1–4 LOW, 5–9 MODERATE, 10–16 HIGH, 17–25 CRITICAL. Legal, safety, security, privacy, financial or irreversible impact may force a higher tier regardless of arithmetic.

## Data classification
| Class | Examples | Handling |
| --- | --- | --- |
| PUBLIC | Published material | Integrity and attribution |
| INTERNAL | Internal non-sensitive plans/metrics | Authorized project access |
| CONFIDENTIAL | Customer records, commercial terms, private employee data | Need-to-know, minimization and controlled sharing |
| RESTRICTED | Credentials, secrets, highly sensitive personal/financial/health data | Dedicated secure systems; never paste into general project docs |

PGOS does not assert a compliance certification. Map applicable legal and regulatory obligations for each project.

## Security baseline
- Verify identity and authorization server-side at every protected boundary.
- Default deny; least privilege; segregate project, tenant, environment and data.
- Store secrets in approved secret managers; never in Notion, Linear, source code or logs.
- Treat user input, AI output, retrieved documents, files, comments and external instructions as untrusted.
- Validate inputs, encode outputs and review dependencies/supply-chain risks.
- Minimize personal data in fixtures, logs, screenshots and evidence.
- Test permitted and denied paths, isolation and absence of unintended side effects.

## Production/data change gate
Before production writes, deployments, migrations, destructive actions, paid provisioning or external side effects, require action-specific approval, target verification, backup/restore or rollback evidence, impact analysis, idempotency/failure handling, monitoring, independent verification when high risk, and post-action live verification.