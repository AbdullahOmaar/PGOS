"""Validation helpers for PGOS ChangeRequest, Handoff and Incident records.

This extends the core structural validator without claiming provider-enforced
identity, authentic approval, or runtime policy enforcement.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXTRA_TYPES = {"ChangeRequest", "Handoff", "Incident"}
REQUIRED = {
    "ChangeRequest": (
        "id", "project_id", "revision", "title", "status", "trigger", "reason",
        "current_state", "proposed_state", "scope_impact", "timeline_impact",
        "budget_impact", "technical_impact", "data_impact", "security_impact",
        "privacy_impact", "migration_plan", "compatibility_plan", "rollback_plan",
        "test_evidence_impact", "risk_classification", "required_approvers",
    ),
    "Handoff": (
        "id", "project_id", "work_order_id", "revision", "status",
        "from_identity", "to_identity", "scope_summary", "acceptance_status",
        "branch", "base_sha", "head_sha", "changed_files", "tests",
        "review_ci_runtime_evidence", "not_run_checks", "blockers",
        "remaining_work", "next_action", "created_at",
    ),
    "Incident": (
        "id", "project_id", "revision", "severity", "status", "start_at",
        "detected_at", "affected_scope", "affected_data", "detection", "impact",
        "containment", "recovery", "owner_id",
    ),
}
RISK_LEVELS = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
CHANGE_STATUSES = {"PROPOSED", "UNDER_REVIEW", "APPROVED", "REJECTED",
                   "DEFERRED", "SUPERSEDED", "CANCELLED"}
HANDOFF_STATUSES = {"DRAFT", "PREPARED", "SUBMITTED", "ACKNOWLEDGED",
                    "ACCEPTED", "REJECTED", "BLOCKED"}
INCIDENT_SEVERITIES = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
INCIDENT_STATUSES = {"OPEN", "INVESTIGATING", "CONTAINED", "RESOLVED", "CLOSED"}


def _iso(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except ValueError:
        return False


def _parse_dt(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc)


def validate_record(record: Any, path: str = "<memory>") -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return [f"{path}: record must be a JSON object"]

    record_type = record.get("record_type")
    if record_type not in EXTRA_TYPES:
        return [f"{path}: unsupported extended record_type: {record_type!r}"]

    for field in REQUIRED[record_type]:
        if field not in record or record[field] is None or record[field] == "":
            errors.append(f"{path}: missing or empty required field '{field}'")
    if errors:
        return errors

    if not isinstance(record["id"], str) or not re.fullmatch(
        r"[A-Z][A-Z0-9-]{2,63}", record["id"]
    ):
        errors.append(f"{path}: id must be an immutable uppercase identifier")
    if not isinstance(record["revision"], int) or record["revision"] < 1:
        errors.append(f"{path}: revision must be a positive integer")
    if not isinstance(record["project_id"], str) or not record["project_id"].strip():
        errors.append(f"{path}: project_id must be non-empty")

    if record_type == "ChangeRequest":
        if record["status"] not in CHANGE_STATUSES:
            errors.append(f"{path}: invalid ChangeRequest status")
        if record["risk_classification"] not in RISK_LEVELS:
            errors.append(f"{path}: invalid risk_classification")
        if not isinstance(record["required_approvers"], list):
            errors.append(f"{path}: required_approvers must be an array")
        if record["status"] == "APPROVED":
            if not record.get("decision_ref"):
                errors.append(f"{path}: APPROVED ChangeRequest requires decision_ref")
            if not isinstance(record["required_approvers"], list) or not record["required_approvers"]:
                errors.append(f"{path}: APPROVED ChangeRequest requires approvers")
        expires_at = record.get("expires_at")
        if expires_at is not None and not _iso(expires_at):
            errors.append(f"{path}: expires_at must be timezone-aware ISO-8601 or null")

    elif record_type == "Handoff":
        if record["status"] not in HANDOFF_STATUSES:
            errors.append(f"{path}: invalid Handoff status")
        for field in ("from_identity", "to_identity"):
            identity = record[field]
            if not isinstance(identity, dict) or not identity.get("id") or not isinstance(identity.get("verified"), bool):
                errors.append(f"{path}: {field} must contain id and boolean verified")
            elif record["status"] == "ACCEPTED" and identity["verified"] is not True:
                errors.append(f"{path}: ACCEPTED Handoff requires verified {field}")
        for field in ("changed_files", "tests", "review_ci_runtime_evidence",
                      "not_run_checks", "blockers", "remaining_work"):
            if not isinstance(record[field], list):
                errors.append(f"{path}: {field} must be an array")
        if record["status"] == "ACCEPTED":
            if not record["tests"] or not record["review_ci_runtime_evidence"]:
                errors.append(f"{path}: ACCEPTED Handoff requires test and review evidence")
            sha_pattern = r"(?:[0-9a-f]{40}|[0-9a-f]{64})"
            if not re.fullmatch(sha_pattern, str(record["base_sha"])) or not re.fullmatch(sha_pattern, str(record["head_sha"])):
                errors.append(f"{path}: ACCEPTED Handoff requires exact base_sha and head_sha")
            if record["acceptance_status"] not in {"ACCEPTED", "VERIFIED_COMPLETE"}:
                errors.append(f"{path}: ACCEPTED Handoff requires accepted acceptance_status")
            if record["not_run_checks"] or record["blockers"]:
                errors.append(f"{path}: Handoff with not_run_checks or blockers cannot be ACCEPTED")
        if not _iso(record["created_at"]):
            errors.append(f"{path}: created_at must be timezone-aware ISO-8601")

    elif record_type == "Incident":
        if record["severity"] not in INCIDENT_SEVERITIES:
            errors.append(f"{path}: invalid Incident severity")
        if record["status"] not in INCIDENT_STATUSES:
            errors.append(f"{path}: invalid Incident status")
        for field in ("affected_scope", "affected_data"):
            if not isinstance(record[field], list):
                errors.append(f"{path}: {field} must be an array")
        for field in ("start_at", "detected_at"):
            if not _iso(record[field]):
                errors.append(f"{path}: {field} must be timezone-aware ISO-8601")
        for field in ("contained_at", "resolved_at"):
            if record.get(field) is not None and not _iso(record[field]):
                errors.append(f"{path}: {field} must be timezone-aware ISO-8601 or null")
        if _iso(record["start_at"]) and _iso(record["detected_at"]):
            if _parse_dt(record["detected_at"]) < _parse_dt(record["start_at"]):
                errors.append(f"{path}: detected_at cannot precede start_at")
        if record.get("contained_at") and _iso(record["detected_at"]):
            if _parse_dt(record["contained_at"]) < _parse_dt(record["detected_at"]):
                errors.append(f"{path}: contained_at cannot precede detected_at")
        if record.get("resolved_at") and record.get("contained_at") and _iso(record["contained_at"]):
            if _parse_dt(record["resolved_at"]) < _parse_dt(record["contained_at"]):
                errors.append(f"{path}: resolved_at cannot precede contained_at")
        if record["status"] in {"CONTAINED", "RESOLVED", "CLOSED"} and not record.get("contained_at"):
            errors.append(f"{path}: CONTAINED/RESOLVED/CLOSED Incident requires contained_at")
        if any(value not in {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"} for value in record["affected_data"]):
            errors.append(f"{path}: affected_data must use PGOS data classification values")
        if record["status"] in {"RESOLVED", "CLOSED"}:
            if not record.get("resolved_at") or not record.get("recovery") or not record.get("root_cause"):
                errors.append(f"{path}: RESOLVED/CLOSED Incident requires resolved_at, recovery and root_cause")

    return errors


def validate_records(records: list[dict[str, Any]]) -> list[str]:
    """Validate extended records plus IDs and references in a mixed record set."""
    errors: list[str] = []
    seen: dict[str, int] = {}
    projects = {
        r.get("id") for r in records
        if isinstance(r, dict) and r.get("record_type") == "Project"
    }
    work_orders = {
        r.get("id"): r for r in records
        if isinstance(r, dict) and r.get("record_type") == "WorkOrder"
    }
    decisions = {
        r.get("id") for r in records
        if isinstance(r, dict) and r.get("record_type") == "Decision"
    }

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record[{index}]: record must be a JSON object")
            continue
        record_id = record.get("id")
        if record_id:
            if record_id in seen:
                errors.append(f"record[{index}]: duplicate id '{record_id}'")
            else:
                seen[record_id] = index

        record_type = record.get("record_type")
        if record_type in EXTRA_TYPES:
            errors.extend(validate_record(record, f"record[{index}]"))
            project_id = record.get("project_id")
            if projects and project_id not in projects:
                errors.append(f"record[{index}]: project_id '{project_id}' does not resolve")
            elif not projects:
                errors.append("record set must include its Project record")
            if record_type == "Handoff":
                work_order = work_orders.get(record.get("work_order_id"))
                if work_order is None:
                    errors.append(f"record[{index}]: work_order_id '{record.get('work_order_id')}' does not resolve")
                elif work_order.get("project_id") != project_id:
                    errors.append(f"record[{index}]: Handoff and WorkOrder belong to different projects")
            if record_type == "ChangeRequest" and record.get("decision_ref"):
                if record["decision_ref"] not in decisions:
                    errors.append(f"record[{index}]: decision_ref '{record['decision_ref']}' does not resolve")

    for work_order in work_orders.values():
        if projects and work_order.get("project_id") not in projects:
            errors.append(f"WorkOrder '{work_order.get('id')}': project_id does not resolve")
    return errors


def validate_directory(directory: Path) -> tuple[list[str], int]:
    files = sorted(directory.rglob("*.json"))
    if not files:
        return [f"{directory}: no JSON records found"], 0
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in files:
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        if isinstance(parsed, dict):
            records.append(parsed)
        elif isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
            records.extend(parsed)
        else:
            errors.append(f"{path}: JSON must contain an object or an array of objects")
    errors.extend(validate_records(records))
    return errors, len(files)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate PGOS ChangeRequest, Handoff and Incident records")
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    if not args.directory.exists() or not args.directory.is_dir():
        parser.error(f"directory does not exist: {args.directory}")
    errors, count = validate_directory(args.directory)
    if errors:
        print(f"PGOS extended-record validation FAILED: {len(errors)} finding(s) across {count} file(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PGOS extended-record validation PASSED: {count} JSON file(s); structural/cross-reference checks only")
    print("NOTE: does not prove identity, approval authenticity, provider enforcement or runtime behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
