"""Behavioral tests for FakeASR."""

import asyncio

from implementations.audio.fake_asr import FakeASR


def _handle(fixture_id: str) -> dict:
    return {
        "media_kind": "audio",
        "fixture_id": fixture_id,
        "source": {"robot_id": "research-unit-01", "sensor_id": "audio-mock-01", "sequence": 1},
    }


def _transcribe(asr: FakeASR, handle: dict):
    return asyncio.run(asr.transcribe(handle))


def _build_fixtures() -> dict:
    return {
        "normal_speech_01": {
            "status": "succeeded",
            "text": "Please inspect the workbench.",
            "language": "en",
            "confidence": 0.95,
            "error": None,
        },
        "silence_01": {
            "status": "no_speech",
            "text": "",
            "language": None,
            "confidence": None,
            "error": None,
        },
        "corrupt_format_01": {
            "status": "unsupported_format",
            "text": "",
            "language": None,
            "confidence": None,
            "error": {
                "code": "unsupported_format",
                "message": "fixture encodes an unsupported container",
                "retryable": False,
            },
        },
        "engine_down_01": {
            "status": "recognizer_unavailable",
            "text": "",
            "language": None,
            "confidence": None,
            "error": {
                "code": "recognizer_unavailable",
                "message": "fixture simulates the recognizer being offline",
                "retryable": True,
            },
        },
    }


def test_normal_speech_fixture_succeeds() -> None:
    asr = FakeASR(fixtures=_build_fixtures())

    result = _transcribe(asr, _handle("normal_speech_01"))

    assert result["status"] == "succeeded"
    assert result["text"] == "Please inspect the workbench."
    assert result["confidence"] == 0.95
    assert result["error"] is None


def test_silence_fixture_is_no_speech() -> None:
    asr = FakeASR(fixtures=_build_fixtures())

    result = _transcribe(asr, _handle("silence_01"))

    assert result["status"] == "no_speech"
    assert result["text"] == ""
    assert result["language"] is None
    assert result["confidence"] is None


def test_unsupported_format_fixture() -> None:
    asr = FakeASR(fixtures=_build_fixtures())

    result = _transcribe(asr, _handle("corrupt_format_01"))

    assert result["status"] == "unsupported_format"
    assert result["error"]["code"] == "unsupported_format"


def test_recognizer_unavailable_fixture() -> None:
    asr = FakeASR(fixtures=_build_fixtures())

    result = _transcribe(asr, _handle("engine_down_01"))

    assert result["status"] == "recognizer_unavailable"
    assert result["error"]["code"] == "recognizer_unavailable"


def test_same_fixture_always_returns_an_equal_result() -> None:
    asr = FakeASR(fixtures=_build_fixtures())
    handle = _handle("normal_speech_01")

    first = _transcribe(asr, handle)
    second = _transcribe(asr, handle)

    assert first == second


def test_returned_result_cannot_corrupt_future_calls() -> None:
    asr = FakeASR(fixtures=_build_fixtures())
    handle = _handle("normal_speech_01")

    first = _transcribe(asr, handle)
    first["text"] = "mutated by caller"

    second = _transcribe(asr, handle)

    assert second["text"] == "Please inspect the workbench."


def test_unregistered_fixture_id_yields_generic_failed_result() -> None:
    asr = FakeASR(fixtures=_build_fixtures())

    result = _transcribe(asr, _handle("does_not_exist"))

    assert result["status"] == "failed"
    assert result["error"]["code"] == "failed"
