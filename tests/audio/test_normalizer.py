"""Behavioral tests for ASRNormalizer."""

import json

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from implementations.audio.normalizer import ASRNormalizer
from tests.contract_path import CONTRACTS_DIR


SOURCE_AUDIO = {"robot_id": "research-unit-01", "sensor_id": "audio-mock-01", "sequence": 3}
ASR_SCHEMA_PATH = CONTRACTS_DIR / "week01" / "asr-result.schema.json"


def _schema_validator() -> Draft202012Validator:
    with ASR_SCHEMA_PATH.open("r", encoding="utf-8") as stream:
        schema = json.load(stream)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _assert_schema_valid(result: dict) -> None:
    errors = list(_schema_validator().iter_errors(result))
    assert errors == [], [str(error) for error in errors]


def test_succeeded_raw_result_normalizes_and_is_schema_valid() -> None:
    normalizer = ASRNormalizer()
    raw = {
        "status": "succeeded",
        "text": "Please inspect the workbench.",
        "language": "en",
        "confidence": 0.95,
        "error": None,
    }

    result = normalizer.normalize(raw, SOURCE_AUDIO, "fake", "asr-result-0001", "2026-07-17T08:03:01Z")

    assert result["status"] == "succeeded"
    assert result["text"] == "Please inspect the workbench."
    assert result["error"] is None
    _assert_schema_valid(result)


def test_no_speech_raw_result_normalizes_and_is_schema_valid() -> None:
    normalizer = ASRNormalizer()
    raw = {"status": "no_speech", "text": "", "language": None, "confidence": None, "error": None}

    result = normalizer.normalize(raw, SOURCE_AUDIO, "fake", "asr-result-0002", "2026-07-17T08:04:01Z")

    assert result["status"] == "no_speech"
    assert result["text"] == ""
    assert result["language"] is None
    assert result["confidence"] is None
    _assert_schema_valid(result)


def test_unsupported_format_raw_result_normalizes_and_is_schema_valid() -> None:
    normalizer = ASRNormalizer()
    raw = {
        "status": "unsupported_format",
        "text": "",
        "language": None,
        "confidence": None,
        "error": {"code": "unsupported_format", "message": "bad container", "retryable": False},
    }

    result = normalizer.normalize(raw, SOURCE_AUDIO, "fake", "asr-result-0003", "2026-07-17T08:05:01Z")

    assert result["status"] == "unsupported_format"
    assert result["error"] == {"code": "unsupported_format", "message": "bad container", "retryable": False}
    _assert_schema_valid(result)


def test_recognizer_unavailable_raw_result_normalizes_and_is_schema_valid() -> None:
    normalizer = ASRNormalizer()
    raw = {
        "status": "recognizer_unavailable",
        "text": "",
        "language": None,
        "confidence": None,
        "error": {"code": "recognizer_unavailable", "message": "engine offline", "retryable": True},
    }

    result = normalizer.normalize(raw, SOURCE_AUDIO, "fake", "asr-result-0004", "2026-07-17T08:06:01Z")

    assert result["status"] == "recognizer_unavailable"
    assert result["error"]["retryable"] is True
    _assert_schema_valid(result)


def test_media_unavailable_input_normalizes_without_calling_asr() -> None:
    normalizer = ASRNormalizer()
    media_unavailable = {
        "status": "media_unavailable",
        "error": {"code": "media_unavailable", "message": "transport reference has expired", "retryable": False},
    }

    result = normalizer.normalize(media_unavailable, SOURCE_AUDIO, "fake", "asr-result-0005", "2026-07-17T08:07:01Z")

    assert result["status"] == "media_unavailable"
    assert result["error"]["code"] == "media_unavailable"
    assert result["text"] == ""
    _assert_schema_valid(result)


def test_confidence_out_of_range_is_rejected() -> None:
    normalizer = ASRNormalizer()
    raw = {
        "status": "succeeded",
        "text": "This should never reach a contract object.",
        "language": "en",
        "confidence": 1.5,
        "error": None,
    }

    with pytest.raises(ValueError) as excinfo:
        normalizer.normalize(raw, SOURCE_AUDIO, "fake", "asr-result-invalid-confidence", "2026-07-17T08:08:01Z")

    assert str(excinfo.value).startswith("invalid_field:")
