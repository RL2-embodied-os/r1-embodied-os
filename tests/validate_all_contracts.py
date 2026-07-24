"""Validate the shared contract baseline and Week 1 semantic rules.

This module is intentionally pure and side-effect free on import. Run it with:

    python -m tests.validate_all_contracts
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from jsonschema import Draft202012Validator, FormatChecker

from tests.contract_path import CONTRACTS_DIR, EXAMPLES_DIR, require_contract_baseline


SemanticChecker = Callable[[Mapping[str, Any], datetime], List[str]]


@dataclass(frozen=True)
class CaseSpec:
    case_id: str
    document_path: Path
    schema_path: Path
    expected_schema: str
    expected_semantic: Optional[str]
    semantic_checker: Optional[SemanticChecker] = None


@dataclass(frozen=True)
class ValidationCaseResult:
    case_id: str
    document: Dict[str, Any]
    schema_status: str
    semantic_status: Optional[str]
    errors: Tuple[str, ...]
    expected_schema: str
    expected_semantic: Optional[str]

    @property
    def matches_expectation(self) -> bool:
        return (
            self.schema_status == self.expected_schema
            and self.semantic_status == self.expected_semantic
        )


SKILL_SCHEMA = CONTRACTS_DIR / "skill-command.schema.json"
TELEMETRY_SCHEMA = CONTRACTS_DIR / "telemetry.schema.json"
ROBOT_STATE_SCHEMA = CONTRACTS_DIR / "robot-state.schema.json"
CAPABILITY_SCHEMA = CONTRACTS_DIR / "capability.schema.json"
CAMERA_SCHEMA = CONTRACTS_DIR / "camera-frame-metadata.schema.json"
AUDIO_SCHEMA = CONTRACTS_DIR / "audio-chunk-metadata.schema.json"
DETECTION_SCHEMA = CONTRACTS_DIR / "week01" / "detection-frame-result.schema.json"
ASR_SCHEMA = CONTRACTS_DIR / "week01" / "asr-result.schema.json"


def _parse_rfc3339(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone offset")
    return parsed.astimezone(timezone.utc)


def _validate_command(document: Mapping[str, Any], now: datetime) -> List[str]:
    issued_at = _parse_rfc3339(str(document["issued_at"]))
    expires_at = _parse_rfc3339(str(document["expires_at"]))
    ttl_ms = int(document["ttl_ms"])
    errors: List[str] = []

    if expires_at <= issued_at:
        errors.append("invalid_time_window: expires_at must be after issued_at")
    validity_ms = int((expires_at - issued_at).total_seconds() * 1000)
    if validity_ms > ttl_ms:
        errors.append("invalid_time_window: expires_at exceeds ttl_ms")
    if expires_at <= now.astimezone(timezone.utc):
        errors.append("expired: expires_at is not later than receive time")
    return errors


def _validate_detection(document: Mapping[str, Any], now: datetime) -> List[str]:
    del now
    image_width = float(document["image_width"])
    image_height = float(document["image_height"])
    errors: List[str] = []

    for detection in document["detections"]:
        x1, y1, x2, y2 = detection["bbox_xyxy"]
        detection_id = detection["detection_id"]
        if x1 >= x2 or y1 >= y2:
            errors.append(
                f"invalid_bbox: {detection_id} requires x1 < x2 and y1 < y2"
            )
        elif x2 > image_width or y2 > image_height:
            errors.append(
                f"image_size_mismatch: {detection_id} exceeds image dimensions"
            )
    return errors


def _validate_camera_for_detection(
    document: Mapping[str, Any], now: datetime
) -> List[str]:
    errors: List[str] = []
    if document["width_px"] is None or document["height_px"] is None:
        errors.append("image_size_unavailable: width_px and height_px are required")

    expires_at = document["transport"]["expires_at"]
    if expires_at is not None and _parse_rfc3339(str(expires_at)) <= now:
        errors.append("media_unavailable: transport reference has expired")
    return errors


def capability_is_supported(
    report: Mapping[str, Any], capability_name: str
) -> bool:
    """Return True only for an explicitly supported capability with evidence."""

    capability = report["capabilities"][capability_name]
    return bool(
        capability["status"] == "supported"
        and capability["evidence"]
        and capability["verified_at"]
    )


CASE_SPECS: Sequence[CaseSpec] = (
    CaseSpec("valid_stop_without_lease", EXAMPLES_DIR / "valid-stop-without-lease.json", SKILL_SCHEMA, "schema_valid", "semantic_valid", _validate_command),
    CaseSpec("valid_stand_command", EXAMPLES_DIR / "valid-stand-command.json", SKILL_SCHEMA, "schema_valid", "semantic_valid", _validate_command),
    CaseSpec("valid_move_command", EXAMPLES_DIR / "valid-move-command.json", SKILL_SCHEMA, "schema_valid", "semantic_valid", _validate_command),
    CaseSpec("invalid_motion_without_lease", EXAMPLES_DIR / "invalid-motion-without-lease.json", SKILL_SCHEMA, "schema_invalid", None, _validate_command),
    CaseSpec("invalid_expired_command", EXAMPLES_DIR / "invalid-expired-command.json", SKILL_SCHEMA, "schema_valid", "semantic_invalid", _validate_command),
    CaseSpec("telemetry_unknown_safety", EXAMPLES_DIR / "telemetry.json", TELEMETRY_SCHEMA, "schema_valid", None),
    CaseSpec("robot_state", EXAMPLES_DIR / "robot-state.json", ROBOT_STATE_SCHEMA, "schema_valid", None),
    CaseSpec("capability_unverified", EXAMPLES_DIR / "capability-report.json", CAPABILITY_SCHEMA, "schema_valid", None),
    CaseSpec("camera_metadata_draft", EXAMPLES_DIR / "camera-frame-metadata.json", CAMERA_SCHEMA, "schema_valid", None),
    CaseSpec("audio_metadata_draft", EXAMPLES_DIR / "audio-chunk-metadata.json", AUDIO_SCHEMA, "schema_valid", None),
    CaseSpec("detection_frame_result", EXAMPLES_DIR / "week01" / "detection-frame-result.json", DETECTION_SCHEMA, "schema_valid", "semantic_valid", _validate_detection),
    CaseSpec("invalid_detection_bbox", EXAMPLES_DIR / "week01" / "invalid-detection-bbox.json", DETECTION_SCHEMA, "schema_valid", "semantic_invalid", _validate_detection),
    CaseSpec("invalid_detection_image_size", EXAMPLES_DIR / "week01" / "invalid-detection-image-size.json", DETECTION_SCHEMA, "schema_valid", "semantic_invalid", _validate_detection),
    CaseSpec("asr_result", EXAMPLES_DIR / "week01" / "asr-result.json", ASR_SCHEMA, "schema_valid", None),
    CaseSpec("asr_no_speech", EXAMPLES_DIR / "week01" / "asr-no-speech.json", ASR_SCHEMA, "schema_valid", None),
    CaseSpec("invalid_asr_confidence", EXAMPLES_DIR / "week01" / "invalid-asr-confidence.json", ASR_SCHEMA, "schema_invalid", None),
    CaseSpec("invalid_telemetry_timestamp", EXAMPLES_DIR / "week01" / "invalid-telemetry-timestamp.json", TELEMETRY_SCHEMA, "schema_invalid", None),
    CaseSpec("camera_missing_size", EXAMPLES_DIR / "week01" / "camera-frame-missing-size.json", CAMERA_SCHEMA, "schema_valid", "semantic_invalid", _validate_camera_for_detection),
    CaseSpec("camera_expired_transport", EXAMPLES_DIR / "week01" / "camera-frame-expired-transport.json", CAMERA_SCHEMA, "schema_valid", "semantic_invalid", _validate_camera_for_detection),
    CaseSpec("valid_camera_complete", EXAMPLES_DIR / "week01" / "valid-camera-frame.json", CAMERA_SCHEMA, "schema_valid", "semantic_valid", _validate_camera_for_detection),
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object in {path}")
    return value


def _assert_strict_objects(node: Any, location: str = "$") -> None:
    """Require additionalProperties:false on every declared object schema."""

    if isinstance(node, dict):
        if node.get("type") == "object" and node.get("additionalProperties") is not False:
            raise ValueError(
                f"{location}: object schema must set additionalProperties to false"
            )
        for key, value in node.items():
            _assert_strict_objects(value, f"{location}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _assert_strict_objects(value, f"{location}[{index}]")


def _format_schema_error(error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "$"
    return f"{location}: {error.message}"


def run_validation(
    now: Optional[datetime] = None,
) -> List[ValidationCaseResult]:
    """Validate every registered example against schema and semantic rules."""

    require_contract_baseline()
    receive_time = now or datetime.now(timezone.utc)
    if receive_time.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    schema_cache: Dict[Path, Dict[str, Any]] = {}
    results: List[ValidationCaseResult] = []
    for spec in CASE_SPECS:
        schema = schema_cache.get(spec.schema_path)
        if schema is None:
            schema = _load_json(spec.schema_path)
            Draft202012Validator.check_schema(schema)
            _assert_strict_objects(schema)
            schema_cache[spec.schema_path] = schema

        document = _load_json(spec.document_path)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        schema_errors = sorted(validator.iter_errors(document), key=str)
        if schema_errors:
            results.append(
                ValidationCaseResult(
                    case_id=spec.case_id,
                    document=document,
                    schema_status="schema_invalid",
                    semantic_status=None,
                    errors=tuple(_format_schema_error(error) for error in schema_errors),
                    expected_schema=spec.expected_schema,
                    expected_semantic=spec.expected_semantic,
                )
            )
            continue

        semantic_errors = (
            spec.semantic_checker(document, receive_time)
            if spec.semantic_checker is not None
            else None
        )
        results.append(
            ValidationCaseResult(
                case_id=spec.case_id,
                document=document,
                schema_status="schema_valid",
                semantic_status=(
                    None
                    if semantic_errors is None
                    else "semantic_invalid"
                    if semantic_errors
                    else "semantic_valid"
                ),
                errors=tuple(semantic_errors or ()),
                expected_schema=spec.expected_schema,
                expected_semantic=spec.expected_semantic,
            )
        )
    return results


def main() -> int:
    results = run_validation()
    for result in results:
        semantic = result.semantic_status or "not_run"
        expectation = "PASS" if result.matches_expectation else "MISMATCH"
        print(
            f"{expectation:8} {result.case_id:32} "
            f"{result.schema_status:16} {semantic}"
        )
        for error in result.errors:
            print(f"         - {error}")
    return 0 if all(result.matches_expectation for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
