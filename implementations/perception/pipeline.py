"""DESIGN: Week 1 visual perception pipeline (Mock main line).

Chain: CameraFrameMetadata -> MediaResolver -> DetectorBackend
       -> DetectionFrameResult (or a structured error).

Responsibilities:
- On `media_unavailable` from the resolver, stop and return it without
  calling the detector (contract requirement).
- On null `width_px`/`height_px`, return `image_size_unavailable` and do
  not emit detections claiming verification.
- Build DetectionContext from validated metadata plus an injected clock;
  the pipeline itself never reads wall-clock time.

Transport-expiry semantics are enforced by the shared contract validators
(`media_unavailable: transport reference has expired`); this pipeline does
not duplicate that check. Fake vs. real YOLO switching happens purely by
injecting a different DetectorBackend; nothing here changes.
"""
import pytest

from typing import Callable, Union

from interfaces.models import CameraFrameMetadataDraft
from interfaces.week01_interfaces import DetectorBackend, MediaResolver
from interfaces.week01_models import (
    DetectionBackendResult,
    DetectionContext,
    MediaUnavailable,
)

Clock = Callable[[], str]  # returns an RFC 3339 UTC timestamp string

PerceptionOutcome = Union[MediaUnavailable, DetectionBackendResult]


class PerceptionPipeline:
    """Deterministic, dependency-injected Mock perception chain."""

    def __init__(
        self,
        resolver: MediaResolver,
        detector: DetectorBackend,
        clock: Clock,
    ):
        self._resolver = resolver
        self._detector = detector
        self._clock = clock

    async def run(self, metadata: CameraFrameMetadataDraft) -> PerceptionOutcome:
        resolution = await self._resolver.resolve(metadata)
        if resolution["status"] == "media_unavailable":
            # Contract: do not call the detector when media is unavailable.
            return resolution

        width = metadata["width_px"]
        height = metadata["height_px"]
        if width is None or height is None:
            return {
                "status": "failed",
                "error": {
                    "code": "image_size_unavailable",
                    "message": "width_px and height_px are required",
                    "retryable": False,
                },
            }

        context: DetectionContext = {
            "source_frame": resolution["handle"]["source"],
            "image_width": width,
            "image_height": height,
            "observed_at": metadata["captured_at"],
            "processed_at": self._clock(),
        }
        return await self._detector.detect(resolution["handle"], context)