# PGOS Adoption Guide

**Status:** DRAFT | **Version:** 0.2.1

PGOS is a framework, not a universal preset of every control for every project. Each adopting project must create its own profile.

## Minimum adoption package
- Project charter and named Owner.
- Risk/data classification and security baseline.
- Source-of-truth map for the actual tools used.
- Named roles and approval matrix.
- Work Order template and lifecycle.
- Decision/change/exception register.
- Verification and release requirements.
- Explicit deviations and their approvers.

## Risk tiers
- LOW: reversible, low-impact, non-sensitive work.
- MODERATE: user-visible behavior, integrations and non-sensitive data changes.
- HIGH: authentication, authorization, personal data, critical infrastructure, money, legal obligations, production writes or irreversible effects.

A project may strengthen controls. It may not silently weaken a mandatory high-risk control.

## Readiness test
A new project is ready only when its Owner can answer: what outcome is authorized, who may act, against which resources/environment, under what expiry, how success and failure are verified, who independently accepts, and who approves release/side effects.