import copy
import json
import unittest
from pathlib import Path

from scripts.extended_records import validate_record, validate_records, validate_directory

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "extended-adoption" / "records.json"

def load_records():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))

def get_record(record_type):
    return next(copy.deepcopy(r) for r in load_records() if r["record_type"] == record_type)

class ExtendedRecordTests(unittest.TestCase):
    def test_valid_change_request(self):
        self.assertEqual(validate_record(get_record("ChangeRequest")), [])

    def test_approved_change_requires_decision_and_approvers(self):
        record = get_record("ChangeRequest")
        record["status"] = "APPROVED"
        record["required_approvers"] = []
        errors = validate_record(record)
        self.assertTrue(any("requires decision_ref" in e for e in errors))
        self.assertTrue(any("requires approvers" in e for e in errors))

    def test_valid_draft_handoff(self):
        self.assertEqual(validate_record(get_record("Handoff")), [])

    def test_accepted_handoff_requires_verified_identities(self):
        record = get_record("Handoff")
        record["status"] = "ACCEPTED"
        record["acceptance_status"] = "ACCEPTED"
        record["base_sha"] = "a"*40
        record["head_sha"] = "b"*40
        record["tests"] = ["PASS"]
        record["review_ci_runtime_evidence"] = ["Independent review PASS"]
        record["not_run_checks"] = []
        record["blockers"] = []
        errors = validate_record(record)
        self.assertTrue(any("verified from_identity" in e for e in errors))
        self.assertTrue(any("verified to_identity" in e for e in errors))

    def test_accepted_handoff_requires_exact_revisions(self):
        record = get_record("Handoff")
        record["status"] = "ACCEPTED"
        record["acceptance_status"] = "ACCEPTED"
        record["from_identity"]["verified"] = True
        record["to_identity"]["verified"] = True
        record["tests"] = ["PASS"]
        record["review_ci_runtime_evidence"] = ["Independent review PASS"]
        record["not_run_checks"] = []
        record["blockers"] = []
        errors = validate_record(record)
        self.assertTrue(any("exact base_sha and head_sha" in e for e in errors))

    def test_accepted_handoff_requires_test_and_review_evidence(self):
        record = get_record("Handoff")
        record["status"] = "ACCEPTED"
        record["acceptance_status"] = "ACCEPTED"
        record["from_identity"]["verified"] = True
        record["to_identity"]["verified"] = True
        record["base_sha"] = "a"*40
        record["head_sha"] = "b"*40
        record["not_run_checks"] = []
        record["blockers"] = []
        errors = validate_record(record)
        self.assertTrue(any("requires test and review evidence" in e for e in errors))

    def test_accepted_handoff_cannot_hide_not_run_checks_or_blockers(self):
        record = get_record("Handoff")
        record["status"] = "ACCEPTED"
        record["acceptance_status"] = "ACCEPTED"
        record["from_identity"]["verified"] = True
        record["to_identity"]["verified"] = True
        record["base_sha"] = "a"*40
        record["head_sha"] = "b"*40
        record["tests"] = ["PASS"]
        record["review_ci_runtime_evidence"] = ["Independent review PASS"]
        record["not_run_checks"] = []
        record["blockers"] = ["Unresolved blocker"]
        errors = validate_record(record)
        self.assertTrue(any("cannot be ACCEPTED" in e for e in errors))

    def test_valid_open_incident(self):
        self.assertEqual(validate_record(get_record("Incident")), [])

    def test_incident_timeline_must_be_chronological(self):
        record = get_record("Incident")
        record["detected_at"] = "2026-11-11T23:00:00Z"
        self.assertTrue(any("detected_at cannot precede start_at" in e for e in validate_record(record)))

    def test_closed_incident_requires_recovery_and_root_cause(self):
        record = get_record("Incident")
        record.update({"status":"CLOSED","contained_at":"2026-11-12T00:10:00Z","resolved_at":"2026-11-12T00:20:00Z"})
        self.assertTrue(any("requires resolved_at, recovery and root_cause" in e for e in validate_record(record)))

    def test_contained_incident_requires_contained_timestamp(self):
        record = get_record("Incident")
        record["status"] = "CONTAINED"
        self.assertTrue(any("requires contained_at" in e for e in validate_record(record)))

    def test_duplicate_ids_are_rejected(self):
        records = load_records()
        records.append(copy.deepcopy(records[-1]))
        self.assertTrue(any("duplicate id" in e for e in validate_records(records)))

    def test_missing_project_reference_is_rejected(self):
        records = load_records()
        next(r for r in records if r["record_type"] == "ChangeRequest")["project_id"] = "PRJ-DOES-NOT-EXIST"
        self.assertTrue(any("does not resolve" in e for e in validate_records(records)))

    def test_handoff_requires_existing_work_order(self):
        records = load_records()
        next(r for r in records if r["record_type"] == "Handoff")["work_order_id"] = "WO-MISSING"
        self.assertTrue(any("does not resolve" in e for e in validate_records(records)))

    def test_change_request_decision_reference_must_resolve(self):
        records = load_records()
        next(r for r in records if r["record_type"] == "ChangeRequest")["decision_ref"] = "DEC-MISSING"
        self.assertTrue(any("decision_ref" in e and "does not resolve" in e for e in validate_records(records)))

    def test_extended_adoption_fixture_passes(self):
        errors, count = validate_directory(EXAMPLE.parent)
        self.assertEqual(count, 1)
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()
