"""Deterministic Fake ASR backend for the Week 1 audio perception chain.

Same fixture_id in -> same RawASRResult out, always. No model, no network,
no audio bytes -- just a caller-injected lookup table, so each test/scenario
controls its own canned recognizer outcomes (normal speech, no speech,
unsupported format, recognizer unavailable, ...).

A future real recognizer implements the same ASRBackend Protocol and replaces
only this module; AudioResolver, ASRNormalizer, and ASRResult stay stable.
"""

from __future__ import annotations

import copy
from typing import Mapping

from interfaces.week01_models import AudioHandle, ASRError, RawASRResult


def _unrecognized_fixture(fixture_id: str) -> RawASRResult:
    return RawASRResult(
        status="failed",
        text="",
        language=None,
        confidence=None,
        error=ASRError(
            code="failed",
            message=f"no fixture registered for fixture_id {fixture_id!r}",
            retryable=False,
        ),
    )


class FakeASR:
    """Deterministic ASRBackend: fixture_id -> canned RawASRResult.

    `fixtures` maps fixture_id -> the exact RawASRResult to return for it,
    injected by the caller. An AudioHandle whose fixture_id is not in the
    table yields a generic `failed` RawASRResult rather than raising, so the
    normalizer always has a well-formed status to work from.
    """

    def __init__(self, fixtures: Mapping[str, RawASRResult]) -> None:
        self._fixtures = dict(fixtures)

    async def transcribe(self, audio_handle: AudioHandle) -> RawASRResult:
        fixture_id = audio_handle["fixture_id"]
        result = self._fixtures.get(fixture_id)
        if result is None:
            return _unrecognized_fixture(fixture_id)
        return copy.deepcopy(result)
