# Authority & Source-of-Truth Model

**Status:** DRAFT | **Version:** 0.1.0 | **Class:** CONTROLLED

| Information class | Canonical authority | Downstream references |
| --- | --- | --- |
| Mission, scope, outcomes, priorities | Approved Notion charter/decision | Linear project/issues link back |
| Ownership, dependencies, Work Orders | Notion records | Linear assignee/project references |
| Architecture and engineering standards | Accepted GitHub docs and ADRs | Notion decision links to ADR |
| Source code and version history | GitHub | Linear issues and Notion Work Orders link to PR/commit |
| Reviews, CI and test evidence | Exact-head GitHub/provider evidence | Notion acceptance points to exact revision |
| Approvals and exceptions | Notion approval/decision records | Linear/GitHub carry reference IDs |
| Deployment and runtime | Actual runtime provider | GitHub release and Notion evidence links |
| Database schema and live data state | Owning database/provider | GitHub migration and Notion change record |

## Selection rules
1. Identify the information class before choosing a source.
2. Prefer the designated authority, not the most recently edited copy.
3. Check approval state, revision, owner, timestamp and explicit supersession.
4. DRAFT, proposed, copied or stale material is non-authoritative.
5. Record material conflict resolution as a versioned Decision Record.
6. When authority is UNKNOWN or CONFLICTED, block the dependent consequential action.

## No silent mirroring
- Store decisions once in Notion; link their IDs elsewhere.
- Store code and ADRs in GitHub; link them from Notion.
- Store execution state in Linear; summarize decision-relevant milestones in Notion.
- Store runtime truth with its provider; do not substitute CI green or HTTP 200 for live acceptance.
- Do not copy secrets, personal data or full sensitive logs into governance records.

Evidence is stale when its commit, artifact, configuration, environment, test scope, permission model or source decision changes materially.