"""DESIGN: Deterministic FakeDetector implementing the DetectorBackend seam.

Consumes only an opaque ImageHandle plus a DetectionContext; it never sees
CameraFrameMetadata and never resolves media itself. Same fixture + context
always produces the same result. No I/O of any kind.

A future YoloV5Adapter implements the same Protocol; swapping backends
requires no change to the resolver, pipeline, or consumers.
"""

from typing import List, Mapping, Sequence, Tuple, TypedDict

from interfaces.week01_models import (
    Detection2D,
    DetectionBackendResult,
    DetectionContext,
    DetectionFrameResult,
    ImageHandle,
)


class FixtureDetection(TypedDict):
    """One scripted detection inside a fixture (test-harness managed)."""

    class_id: int
    class_name: str
    confidence: float
    bbox_xyxy: Tuple[float, float, float, float]


class FakeDetector:
    """Deterministic scripted detector over an injected fixture table."""

    def __init__(self, fixtures: Mapping[str, Sequence[FixtureDetection]]):
        # {fixture_id: [FixtureDetection, ...]} — empty list means the
        # detector "succeeds and finds no targets" for that fixture.
        self._fixtures = {key: list(value) for key, value in fixtures.items()}

    async def detect(
        self, media: ImageHandle, context: DetectionContext
    ) -> DetectionBackendResult:
        scripted = self._fixtures.get(media["fixture_id"])
        if scripted is None:
            return {
                "status": "failed",
                "error": {
                    "code": "detector_unavailable",
                    "message": f"unknown fixture {media['fixture_id']!r}",
                    "retryable": False,
                },
            }

        # Semantic self-check: reject rather than emit contract-violating boxes.
        width = float(context["image_width"])
        height = float(context["image_height"])
        for index, entry in enumerate(scripted):
            x1, y1, x2, y2 = entry["bbox_xyxy"]
            if x1 >= x2 or y1 >= y2:
                return {
                    "status": "failed",
                    "error": {
                        "code": "invalid_bbox",
                        "message": (
                            f"fixture {media['fixture_id']!r} entry {index} "
                            "requires x1 < x2 and y1 < y2"
                        ),
                        "retryable": False,
                    },
                }
            if x2 > width or y2 > height:
                return {
                    "status": "failed",
                    "error": {
                        "code": "image_size_mismatch",
                        "message": (
                            f"fixture {media['fixture_id']!r} entry {index} "
                            "exceeds image dimensions"
                        ),
                        "retryable": False,
                    },
                }

        detections: List[Detection2D] = [
            {
                "detection_id": f"det-{media['fixture_id']}-{index:04d}",
                "class_id": entry["class_id"],
                "class_name": entry["class_name"],
                "confidence": entry["confidence"],
                "bbox_xyxy": entry["bbox_xyxy"],
                "observed_at": context["observed_at"],
            }
            for index, entry in enumerate(scripted)
        ]
        result: DetectionFrameResult = {
            "schema_version": "0.1",
            "source_frame": context["source_frame"],
            "detector": "fake",
            "image_width": context["image_width"],
            "image_height": context["image_height"],
            "processed_at": context["processed_at"],
            "detections": detections,
        }
        return {"status": "succeeded", "result": result}