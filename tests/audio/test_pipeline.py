"""End-to-end tests for the Week 1 Mock audio chain: all 8 required scenarios.

Validator -> Resolver -> FakeASR -> Normalizer -> ASRResult, with the final
result checked against the real, frozen asr-result.schema.json each time.
"""

import asyncio
import copy
import json
from datetime import datetime, timezone

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from implementations.audio.audio_resolver import MockAudioResolver
from implementations.audio.fake_asr import FakeASR
from implementations.audio.pipeline import AudioPipeline
from tests.contract_path import CONTRACTS_DIR, EXAMPLES_DIR


REFERENCE_NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)
ASR_SCHEMA_PATH = CONTRACTS_DIR / "week01" / "asr-result.schema.json"


def _load_valid_metadata() -> dict:
    with (EXAMPLES_DIR / "audio-chunk-metadata.json").open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _schema_validator() -> Draft202012Validator:
    with ASR_SCHEMA_PATH.open("r", encoding="utf-8") as stream:
        schema = json.load(stream)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _assert_schema_valid(result: dict) -> None:
    errors = list(_schema_validator().iter_errors(result))
    assert errors == [], [str(error) for error in errors]


def _pipeline(resolver_fixtures: dict, asr_fixtures: dict) -> AudioPipeline:
    resolver = MockAudioResolver(fixtures=resolver_fixtures, clock=lambda: REFERENCE_NOW)
    asr = FakeASR(fixtures=asr_fixtures)
    return AudioPipeline(resolver=resolver, asr=asr)


def _process(pipeline: AudioPipeline, metadata: dict, result_id: str = "asr-result-e2e"):
    return asyncio.run(pipeline.process(metadata, result_id, "2026-07-17T08:09:01Z"))


def test_scenario_normal_transcription() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "normal_speech_01"},
        asr_fixtures={
            "normal_speech_01": {
                "status": "succeeded",
                "text": "Please inspect the workbench.",
                "language": "en",
                "confidence": 0.95,
                "error": None,
            }
        },
    )

    result = _process(pipeline, metadata)

    assert result["status"] == "succeeded"
    assert result["text"] == "Please inspect the workbench."
    _assert_schema_valid(result)


def test_scenario_no_speech() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "silence_01"},
        asr_fixtures={
            "silence_01": {"status": "no_speech", "text": "", "language": None, "confidence": None, "error": None}
        },
    )

    result = _process(pipeline, metadata)

    assert result["status"] == "no_speech"
    _assert_schema_valid(result)


def test_scenario_invalid_metadata_never_becomes_an_asr_result() -> None:
    metadata = _load_valid_metadata()
    del metadata["sequence"]
    pipeline = _pipeline(resolver_fixtures={}, asr_fixtures={})

    with pytest.raises(ValueError) as excinfo:
        _process(pipeline, metadata)

    assert str(excinfo.value).startswith("missing_required_field:")


def test_scenario_expired_transport() -> None:
    metadata = copy.deepcopy(_load_valid_metadata())
    metadata["transport"]["expires_at"] = "2026-07-01T00:00:00Z"
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "normal_speech_01"},
        asr_fixtures={},
    )

    result = _process(pipeline, metadata)

    assert result["status"] == "media_unavailable"
    assert "expired" in result["error"]["message"]
    _assert_schema_valid(result)


def test_scenario_media_unavailable() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(resolver_fixtures={}, asr_fixtures={})

    result = _process(pipeline, metadata)

    assert result["status"] == "media_unavailable"
    _assert_schema_valid(result)


def test_scenario_unsupported_format() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "corrupt_format_01"},
        asr_fixtures={
            "corrupt_format_01": {
                "status": "unsupported_format",
                "text": "",
                "language": None,
                "confidence": None,
                "error": {"code": "unsupported_format", "message": "bad container", "retryable": False},
            }
        },
    )

    result = _process(pipeline, metadata)

    assert result["status"] == "unsupported_format"
    _assert_schema_valid(result)


def test_scenario_recognizer_unavailable() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "engine_down_01"},
        asr_fixtures={
            "engine_down_01": {
                "status": "recognizer_unavailable",
                "text": "",
                "language": None,
                "confidence": None,
                "error": {"code": "recognizer_unavailable", "message": "engine offline", "retryable": True},
            }
        },
    )

    result = _process(pipeline, metadata)

    assert result["status"] == "recognizer_unavailable"
    _assert_schema_valid(result)


def test_scenario_confidence_out_of_range_never_becomes_an_asr_result() -> None:
    metadata = _load_valid_metadata()
    pipeline = _pipeline(
        resolver_fixtures={metadata["sensor_id"]: "overconfident_01"},
        asr_fixtures={
            "overconfident_01": {
                "status": "succeeded",
                "text": "This should never reach a contract object.",
                "language": "en",
                "confidence": 1.5,
                "error": None,
            }
        },
    )

    with pytest.raises(ValueError) as excinfo:
        _process(pipeline, metadata)

    assert str(excinfo.value).startswith("invalid_field:")
