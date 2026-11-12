import unittest
from scripts.validate_records import validate_record

class ValidatorTests(unittest.TestCase):
    def test_valid_project(self):
        record = {
            "record_type":"Project","id":"PRJ-TEST-001","name":"Test","revision":1,
            "status":"GOVERNANCE_SETUP","owner":{"id":"owner-1","verified":True},
            "problem":"Problem","outcomes":["Outcome"],"scope":["Scope"],"non_goals":[],
            "risk_tier":"LOW","data_classes":["INTERNAL"],
            "canonical_sources":{"notion":"NOT_APPLICABLE","linear":"NOT_APPLICABLE","github":"NOT_APPLICABLE","runtime":"NOT_APPLICABLE"}
        }
        self.assertEqual(validate_record(record), [])

    def test_high_impact_requires_a4(self):
        record = {
            "record_type":"WorkOrder","id":"WO-TEST-001","project_id":"PRJ-TEST-001","revision":1,
            "title":"Test","status":"DRAFT","objective":"Test objective","scope":["docs/**"],"non_goals":[],
            "owner_id":"owner-1","assignee":{"id":"agent-1","verified":False},
            "permission":{"level":"A1","actions":["production_deploy"],"resources":["**"],"environment":"local","expires_at":"2026-12-01T00:00:00Z"},
            "acceptance_criteria":[{"id":"AC-1","given":"x","when":"y","then":"z","evidence_required":"test"}],
            "verification_plan":{"checks":["unit"],"verifier_id":"reviewer"},"risk_tier":"HIGH"
        }
        self.assertTrue(any("high-impact action requires A4" in e for e in validate_record(record)))

    def test_unknown_record_type_fails(self):
        self.assertTrue(validate_record({"record_type":"Unknown"}))

if __name__ == "__main__":
    unittest.main()
