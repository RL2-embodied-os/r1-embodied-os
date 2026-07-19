"""DESIGN: Mock MediaResolver for the Week 1 visual perception chain.

Maps CameraFrameMetadata identity (robot_id, sensor_id, sequence) to an
opaque fixture handle. Performs no I/O, no Base64, no file or network
access, and never mutates or extends the metadata object.

`media_unavailable` is produced by this layer, per the Week 1 contract.
"""

from typing import Mapping, Tuple

from interfaces.models import CameraFrameMetadataDraft
from interfaces.week01_models import ImageHandle, ImageResolution

FrameKey = Tuple[str, str, int]


class MockMediaResolver:
    """Deterministic, dependency-injected resolver over a fixture table."""

    def __init__(self, fixtures: Mapping[FrameKey, str]):
        # {(robot_id, sensor_id, sequence): fixture_id} — injected by tests.
        self._fixtures = dict(fixtures)

    async def resolve(self, metadata: CameraFrameMetadataDraft) -> ImageResolution:
        key: FrameKey = (
            metadata["robot_id"],
            metadata["sensor_id"],
            metadata["sequence"],
        )
        fixture_id = self._fixtures.get(key)
        if fixture_id is None:
            return {
                "status": "media_unavailable",
                "error": {
                    "code": "media_unavailable",
                    "message": (
                        "no fixture registered for frame "
                        f"{key[0]}/{key[1]}/{key[2]}"
                    ),
                    "retryable": False,
                },
            }
        handle: ImageHandle = {
            "media_kind": "image",
            "fixture_id": fixture_id,
            "source": {
                "robot_id": metadata["robot_id"],
                "sensor_id": metadata["sensor_id"],
                "sequence": metadata["sequence"],
            },
        }
        return {"status": "media_available", "handle": handle}