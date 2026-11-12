# Contributing to PGOS

PGOS is a reusable governance framework. Changes must preserve project-agnostic behavior and must not import another project's private policy or approval state.

## Before changing
- Read README.md and AGENTS.md.
- Link an approved Work Order and relevant Decision record.
- State scope, non-goals, risk and acceptance criteria.
- Keep changes focused and preserve unrelated work.

## Validation
Run:
```bash
python scripts/validate_records.py examples/sample-project
python -m unittest discover -s tests -v
```

Add tests for new validation rules, including negative cases. Never use real credentials, personal data or production identifiers in examples.

## Pull requests
Use the PR template. Report exact candidate SHA and checks; mark unrun checks explicitly. A passing CI run is not Owner acceptance or release approval.

## Governance
Do not weaken security, approval, identity or release gates without a documented Decision and explicit Owner approval. Independent review requirements cannot be satisfied by the change author.