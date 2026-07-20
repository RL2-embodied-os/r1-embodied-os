"""Mock AudioResolver for the Week 1 audio perception chain.

Resolves already-validated AudioChunkMetadata to an opaque, test-owned
fixture handle, or an explicit media_unavailable error. Performs no file,
network, device, or Base64 operations -- the fixture catalogue and clock
are both injected by the caller, never read from disk or the system clock
implicitly, so resolution stays deterministic and side-effect free.

Owns the transport reference expiry check (see
docs/week01/architecture_and_interfaces.md: "expired/unavailable reference
returns resolver error"); AudioChunkMetadataValidator does not check expiry.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Mapping

from interfaces.models import AudioChunkMetadataDraft
from interfaces.week01_models import (
    AudioAvailable,
    AudioHandle,
    AudioResolution,
    MediaUnavailable,
    ResolutionError,
    SourceMediaReference,
)


def _parse_rfc3339(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone offset")
    return parsed.astimezone(timezone.utc)


def _unavailable(message: str, *, retryable: bool) -> MediaUnavailable:
    return MediaUnavailable(
        status="media_unavailable",
        error=ResolutionError(code="media_unavailable", message=message, retryable=retryable),
    )


class MockAudioResolver:
    """Resolves metadata to a test-owned fixture handle; performs no I/O.

    `fixtures` maps sensor_id -> opaque fixture_id and is injected by the
    caller so each test/scenario controls its own Mock media catalogue.
    `clock` is injected for deterministic expiry checks; defaults to the
    real UTC clock outside of tests.
    """

    def __init__(
        self,
        fixtures: Mapping[str, str],
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self._fixtures = dict(fixtures)
        self._clock = clock

    async def resolve(self, metadata: AudioChunkMetadataDraft) -> AudioResolution:
        expires_at = metadata["transport"]["expires_at"]
        if expires_at is not None and _parse_rfc3339(expires_at) <= self._clock():
            return _unavailable("transport reference has expired", retryable=False)

        fixture_id = self._fixtures.get(metadata["sensor_id"])
        if fixture_id is None:
            return _unavailable(
                f"no fixture registered for sensor_id {metadata['sensor_id']!r}",
                retryable=False,
            )

        handle = AudioHandle(
            media_kind="audio",
            fixture_id=fixture_id,
            source=SourceMediaReference(
                robot_id=metadata["robot_id"],
                sensor_id=metadata["sensor_id"],
                sequence=metadata["sequence"],
            ),
        )
        return AudioAvailable(status="media_available", handle=handle)
