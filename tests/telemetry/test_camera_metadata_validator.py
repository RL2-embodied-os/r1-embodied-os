""""Deterministic tests for the CameraFrameMetadata semantic validator"""

import json
from datetime import datetime, timezone
import pytest
from jsonschema import Draft202012Validator, FormatChecker
from implementations.telemetry.camera_metadata_validator import CameraMetadataValidationError, image_size_status, validate_camera_frame_metadata
from tests.contract_path import CONTRACTS_DIR, EXAMPLES_DIR

CAMERA_SCHEMA = json.loads((CONTRACTS_DIR / 'camera-frame-metadata.schema.json').read_text())
_validator = Draft202012Validator(CAMERA_SCHEMA, format_checker=FormatChecker())

def _load_example(name:str) -> dict:
    return json.loads((EXAMPLES_DIR / 'week01' / name).read_text())

def assert_schema_valid(document: dict ) -> None:
    errors = list(_validator.iter_errors(document))
    assert errors == [], [e.message for e in errors]

def test_valid_example_passes_schema_and_semantic_validation() -> None:
    metadata = _load_example('camera-frame-missing-size.json') #missing size exmaple is schema valid as both width and height are null, but it flags image_size_unavailable at semantic layer
    assert_schema_valid(metadata)
    validate_camera_frame_metadata(metadata, now=datetime(2026, 7, 17, 8, 0, 0, tzinfo=timezone.utc))
    assert image_size_status(metadata) == 'image_size_unavailable'

def test_expired_transport_raises_expired_transport() -> None:
    metadata = _load_example('camera-frame-expired-transport.json')
    assert_schema_valid(metadata)
    with pytest.raises(CameraMetadataValidationError, match='^expired_transport'):
        validate_camera_frame_metadata(metadata, now=datetime(2026, 7, 17, tzinfo=timezone.utc))


def test_present_dimensions_report_ok_status() -> None:
    metadata = _load_example('camera-frame-expired-transport.json')
    assert image_size_status(metadata) == 'ok'

def test_mismatched_dimensions_raise_invalid_field() -> None:
    metadata = _load_example('camera-frame-missing-size.json').copy()
    metadata['width_px'] = 10
    with pytest.raises(CameraMetadataValidationError, match='^invalid_field'):
        validate_camera_frame_metadata(metadata, now=datetime(2026, 7, 17, tzinfo=timezone.utc))



