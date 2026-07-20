"""Behavioral tests for MockAudioResolver."""

import asyncio
import copy
import json
from datetime import datetime, timezone

from implementations.audio.audio_resolver import MockAudioResolver
from tests.contract_path import EXAMPLES_DIR


REFERENCE_NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def _load_valid_metadata() -> dict:
    with (EXAMPLES_DIR / "audio-chunk-metadata.json").open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _resolve(resolver: MockAudioResolver, metadata: dict):
    return asyncio.run(resolver.resolve(metadata))


def test_registered_sensor_with_valid_transport_resolves_to_a_handle() -> None:
    metadata = _load_valid_metadata()
    resolver = MockAudioResolver(
        fixtures={metadata["sensor_id"]: "normal_speech_01"},
        clock=lambda: REFERENCE_NOW,
    )

    resolution = _resolve(resolver, metadata)

    assert resolution["status"] == "media_available"
    handle = resolution["handle"]
    assert handle["media_kind"] == "audio"
    assert handle["fixture_id"] == "normal_speech_01"
    assert handle["source"] == {
        "robot_id": metadata["robot_id"],
        "sensor_id": metadata["sensor_id"],
        "sequence": metadata["sequence"],
    }


def test_unregistered_sensor_id_is_media_unavailable() -> None:
    metadata = _load_valid_metadata()
    resolver = MockAudioResolver(fixtures={}, clock=lambda: REFERENCE_NOW)

    resolution = _resolve(resolver, metadata)

    assert resolution["status"] == "media_unavailable"
    assert resolution["error"]["code"] == "media_unavailable"
    assert resolution["error"]["retryable"] is False


def test_expired_transport_reference_is_media_unavailable() -> None:
    metadata = copy.deepcopy(_load_valid_metadata())
    metadata["transport"]["expires_at"] = "2026-07-01T00:00:00Z"
    resolver = MockAudioResolver(
        fixtures={metadata["sensor_id"]: "normal_speech_01"},
        clock=lambda: REFERENCE_NOW,
    )

    resolution = _resolve(resolver, metadata)

    assert resolution["status"] == "media_unavailable"
    assert "expired" in resolution["error"]["message"]


def test_transport_expiring_exactly_now_counts_as_expired() -> None:
    metadata = copy.deepcopy(_load_valid_metadata())
    metadata["transport"]["expires_at"] = REFERENCE_NOW.isoformat().replace("+00:00", "Z")
    resolver = MockAudioResolver(
        fixtures={metadata["sensor_id"]: "normal_speech_01"},
        clock=lambda: REFERENCE_NOW,
    )

    resolution = _resolve(resolver, metadata)

    assert resolution["status"] == "media_unavailable"


def test_null_expires_at_never_expires() -> None:
    metadata = copy.deepcopy(_load_valid_metadata())
    metadata["transport"]["expires_at"] = None
    resolver = MockAudioResolver(
        fixtures={metadata["sensor_id"]: "normal_speech_01"},
        clock=lambda: REFERENCE_NOW,
    )

    resolution = _resolve(resolver, metadata)

    assert resolution["status"] == "media_available"
