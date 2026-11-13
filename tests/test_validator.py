import json
import re
import unittest
from pathlib import Path
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


    def test_package_version_is_consistent_across_governance_documents(self):
        root = Path(__file__).resolve().parents[1]
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        release = re.search(
            r"^## (\\d+\\.\\d+\\.\\d+) — .* \\(DRAFT; not adopted\\)$",
            changelog,
            re.MULTILINE,
        )
        self.assertIsNotNone(release, "CHANGELOG must declare a draft package version")
        version = release.group(1)

        versioned_documents = [
            "README.md",
            "docs/architecture/adr-standard.md",
            "docs/governance/adoption-guide.md",
            "docs/governance/authority-model.md",
            "docs/governance/charter-and-intake.md",
            "docs/governance/decisions-and-change-control.md",
            "docs/governance/roles-and-permissions.md",
            "docs/governance/tool-integration.md",
            "docs/governance/work-order-lifecycle.md",
            "docs/security/risk-security-data.md",
            "docs/release/release-and-closeout.md",
        ]
        for relative_path in versioned_documents:
            content = (root / relative_path).read_text(encoding="utf-8")
            match = re.search(r"^\\*\\*Version:\\*\\* (\\d+\\.\\d+\\.\\d+)", content, re.MULTILINE)
            self.assertIsNotNone(match, f"{relative_path} must declare a version")
            self.assertEqual(version, match.group(1), relative_path)

        sample_project = json.loads(
            (root / "examples" / "sample-project" / "project.json").read_text(encoding="utf-8")
        )
        self.assertEqual(version, sample_project["governance_profile_version"])

if __name__ == "__main__":
    unittest.main()
