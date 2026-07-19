"""DESIGN: Week 1 perception chain tests (six required behaviors).

Covers: normal detection, empty detection, invalid bbox, image-size
mismatch, media unavailable, detector unavailable — plus determinism and
schema conformance of the produced DetectionFrameResult.

Async note: Protocols are async; tests wrap calls in asyncio.run() to keep
requirements-dev.txt unchanged (no pytest-asyncio dependency).
"""

from typing import Optional

from interfaces.models import CameraFrameMetadataDraft

import asyncio
import json
from datetime import datetime, timezone

import jsonschema

from week01_contracts import CONTRACTS_DIR, EXAMPLES_DIR
from implementations.perception.fake_detector import FakeDetector
from implementations.perception.media_resolver import MockMediaResolver
from implementations.perception.pipeline import PerceptionPipeline
from tests.validate_all_contracts import _validate_detection

FRAME_KEY = ("research-unit-01", "camera-mock-01", 7)
FIXED_PROCESSED_AT = "2026-07-19T10:00:00Z"


def fixed_clock() -> str:
    return FIXED_PROCESSED_AT


def make_metadata(
    width: Optional[int] = 640,
    height: Optional[int] = 480,
    sequence: int = FRAME_KEY[2],
    ) -> CameraFrameMetadataDraft:
    """Valid CameraFrameMetadata draft (shape mirrors examples/)."""
    return {
        "schema_version": "0.1",
        "contract_status": "draft",
        "robot_id": FRAME_KEY[0],
        "sensor_id": FRAME_KEY[1],
        "captured_at": "2026-07-19T09:59:58Z",
        "sequence": sequence,
        "timestamp_source": "unknown",
        "content_type": "image/unknown",
        "encoding": None,
        "width_px": width,
        "height_px": height,
        "calibration_version": None,
        "verification_status": "unverified",
        "transport": {
            "type": "object_storage",
            "reference": "object:00000000-0000-4000-8000-00000000fe07",
            "expires_at": "2099-01-01T00:01:00Z",
        },
    }


FIXTURES_DETECTIONS = {
    "fixture-normal": [
        {
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.92,
            "bbox_xyxy": (50.5, 60.0, 248.75, 400.25),
        },
        {
            "class_id": 5,
            "class_name": "bus",
            "confidence": 0.58,
            "bbox_xyxy": (300.0, 100.0, 620.0, 470.0),
        },
    ],
    "fixture-empty": [],
    "fixture-bad-order": [
        {
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.88,
            "bbox_xyxy": (200.0, 50.0, 100.0, 300.0),  # x1 >= x2
        }
    ],
    "fixture-out-of-bounds": [
        {
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.90,
            "bbox_xyxy": (10.0, 10.0, 9000.0, 400.0),  # exceeds width
        }
    ],
}


def make_pipeline(resolver_fixtures=None):
    resolver = MockMediaResolver(
        resolver_fixtures
        if resolver_fixtures is not None
        else {FRAME_KEY: "fixture-normal"}
    )
    detector = FakeDetector(FIXTURES_DETECTIONS)
    return PerceptionPipeline(resolver, detector, fixed_clock)


def load_detection_schema():
    path = CONTRACTS_DIR / "week01" / "detection-frame-result.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def as_json_document(document):
    """Serialize as it would cross the wire (tuples become JSON arrays)."""
    return json.loads(json.dumps(document))


def assert_schema_valid(document):
    jsonschema.validate(
        as_json_document(document),
        load_detection_schema(),
        format_checker=jsonschema.FormatChecker(),
    )


# 1. Normal detection ------------------------------------------------------

def test_normal_detection_succeeds_and_conforms():
    outcome = asyncio.run(make_pipeline().run(make_metadata()))
    assert outcome["status"] == "succeeded"
    result = outcome["result"]
    assert_schema_valid(result)
    now = datetime(2026, 7, 19, tzinfo=timezone.utc)
    assert _validate_detection(result, now) == []  # semantic_valid
    assert result["detector"] == "fake"
    assert result["source_frame"] == {
        "robot_id": FRAME_KEY[0],
        "sensor_id": FRAME_KEY[1],
        "sequence": FRAME_KEY[2],
    }
    assert result["processed_at"] == FIXED_PROCESSED_AT
    assert [d["class_name"] for d in result["detections"]] == ["person", "bus"]


def test_normal_detection_is_deterministic():
    first = asyncio.run(make_pipeline().run(make_metadata()))
    second = asyncio.run(make_pipeline().run(make_metadata()))
    assert first == second


# 2. Empty detection -------------------------------------------------------

def test_empty_detection_is_success_with_empty_array():
    pipeline = make_pipeline({FRAME_KEY: "fixture-empty"})
    outcome = asyncio.run(pipeline.run(make_metadata()))
    assert outcome["status"] == "succeeded"
    assert outcome["result"]["detections"] == []
    assert_schema_valid(outcome["result"])


# 3. Invalid bbox ----------------------------------------------------------

def test_invalid_bbox_is_rejected_not_emitted():
    pipeline = make_pipeline({FRAME_KEY: "fixture-bad-order"})
    outcome = asyncio.run(pipeline.run(make_metadata()))
    assert outcome == {
        "status": "failed",
        "error": {
            "code": "invalid_bbox",
            "message": (
                "fixture 'fixture-bad-order' entry 0 requires x1 < x2 and y1 < y2"
            ),
            "retryable": False,
        },
    }


def test_shared_validator_flags_invalid_bbox_example():
    document = json.loads(
        (EXAMPLES_DIR / "week01" / "invalid-detection-bbox.json").read_text(
            encoding="utf-8"
        )
    )
    now = datetime(2026, 7, 19, tzinfo=timezone.utc)
    errors = _validate_detection(document, now)
    assert any(error.startswith("invalid_bbox") for error in errors)


# 4. Image-size mismatch ---------------------------------------------------

def test_out_of_bounds_bbox_is_image_size_mismatch():
    pipeline = make_pipeline({FRAME_KEY: "fixture-out-of-bounds"})
    outcome = asyncio.run(pipeline.run(make_metadata()))
    assert outcome["status"] == "failed"
    assert outcome["error"]["code"] == "image_size_mismatch"


# 5. Media unavailable -----------------------------------------------------

class CountingDetector:
    """Wrapper proving the detector is never called on media_unavailable."""

    def __init__(self, inner):
        self.inner = inner
        self.calls = 0

    async def detect(self, media, context):
        self.calls += 1
        return await self.inner.detect(media, context)


def test_unknown_frame_is_media_unavailable_and_detector_not_called():
    resolver = MockMediaResolver({})  # no fixtures registered
    detector = CountingDetector(FakeDetector(FIXTURES_DETECTIONS))
    pipeline = PerceptionPipeline(resolver, detector, fixed_clock)
    outcome = asyncio.run(pipeline.run(make_metadata()))
    assert outcome["status"] == "media_unavailable"
    assert outcome["error"]["code"] == "media_unavailable"
    assert detector.calls == 0


# 5b. Missing image size ---------------------------------------------------

def test_null_dimensions_yield_image_size_unavailable():
    outcome = asyncio.run(
        make_pipeline().run(make_metadata(width=None, height=None))
    )
    assert outcome == {
        "status": "failed",
        "error": {
            "code": "image_size_unavailable",
            "message": "width_px and height_px are required",
            "retryable": False,
        },
    }


# 6. Detector unavailable --------------------------------------------------

def test_unknown_fixture_is_detector_unavailable_not_fake_success():
    pipeline = make_pipeline({FRAME_KEY: "fixture-not-scripted"})
    outcome = asyncio.run(pipeline.run(make_metadata()))
    assert outcome["status"] == "failed"
    assert outcome["error"]["code"] == "detector_unavailable"