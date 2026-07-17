"""Behavioral tests for schema and semantic contract validation."""

from datetime import datetime, timezone

from tests.contract_path import CONTRACTS_DIR, EXAMPLES_DIR
from tests.validate_all_contracts import (
    CASE_SPECS,
    capability_is_supported,
    run_validation,
)


REFERENCE_NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def test_contract_report_matches_each_case_expectation() -> None:
    report = run_validation(now=REFERENCE_NOW)
    mismatches = [result for result in report if not result.matches_expectation]
    assert mismatches == []


def test_report_distinguishes_schema_and_semantic_failures() -> None:
    report = {result.case_id: result for result in run_validation(now=REFERENCE_NOW)}

    assert report["invalid_motion_without_lease"].schema_status == "schema_invalid"
    assert report["invalid_motion_without_lease"].semantic_status is None
    assert report["invalid_expired_command"].schema_status == "schema_valid"
    assert report["invalid_expired_command"].semantic_status == "semantic_invalid"
    assert report["invalid_detection_bbox"].schema_status == "schema_valid"
    assert report["invalid_detection_bbox"].semantic_status == "semantic_invalid"
    assert report["invalid_asr_confidence"].schema_status == "schema_invalid"
    assert report["asr_result"].semantic_status is None


def test_unknown_safety_values_remain_null_and_capability_is_not_injected() -> None:
    report = {result.case_id: result for result in run_validation(now=REFERENCE_NOW)}
    telemetry = report["telemetry_unknown_safety"].document

    assert telemetry["safety"]["armed"] is None
    assert telemetry["safety"]["estopped"] is None
    assert "capability" not in telemetry
    assert "capability_status" not in telemetry


def test_unverified_capability_is_not_available() -> None:
    report = {result.case_id: result for result in run_validation(now=REFERENCE_NOW)}
    capability_report = report["capability_unverified"].document
    assert capability_is_supported(capability_report, "camera") is False


def test_every_contract_and_example_is_registered() -> None:
    registered_schemas = {spec.schema_path.resolve() for spec in CASE_SPECS}
    registered_examples = {spec.document_path.resolve() for spec in CASE_SPECS}

    assert registered_schemas == {
        path.resolve() for path in CONTRACTS_DIR.rglob("*.schema.json")
    }
    assert registered_examples == {
        path.resolve() for path in EXAMPLES_DIR.rglob("*.json")
    }


def test_semantic_failures_report_stable_reason_codes() -> None:
    report = {result.case_id: result for result in run_validation(now=REFERENCE_NOW)}

    assert report["invalid_detection_bbox"].errors[0].startswith("invalid_bbox:")
    assert report["invalid_detection_image_size"].errors[0].startswith(
        "image_size_mismatch:"
    )
    assert report["camera_missing_size"].errors[0].startswith(
        "image_size_unavailable:"
    )
    assert report["camera_expired_transport"].errors[0].startswith(
        "media_unavailable:"
    )
