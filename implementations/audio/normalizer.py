"""ASRNormalizer: shapes FakeASR (or a future real backend) output, or a
resolver-reported MediaUnavailable, into the frozen ASRResult v0.1 contract.

This is the last stop before schema validation, so it is also the boundary
that rejects a backend handing back a value the contract can never accept
(e.g. confidence outside [0, 1]) -- raising ValueError rather than letting a
malformed ASRResult escape.
"""

from __future__ import annotations

from typing import Optional

from interfaces.week01_models import (
    ASRError,
    ASRNormalizationInput,
    ASRResult,
    SourceMediaReference,
)


def _build(
    *,
    result_id: str,
    source_audio: SourceMediaReference,
    recognizer: str,
    processed_at: str,
    status: str,
    text: str,
    language: Optional[str],
    confidence: Optional[float],
    error: Optional[ASRError],
) -> ASRResult:
    return ASRResult(
        schema_version="0.1",
        result_id=result_id,
        source_audio=source_audio,
        recognizer=recognizer,
        status=status,
        text=text,
        language=language,
        confidence=confidence,
        processed_at=processed_at,
        error=error,
    )


class ASRNormalizer:
    """Normalizes ASRNormalizationInput (RawASRResult or MediaUnavailable)
    plus call context into a schema-shaped ASRResult."""

    def normalize(
        self,
        raw: ASRNormalizationInput,
        source_audio: SourceMediaReference,
        recognizer: str,
        result_id: str,
        processed_at: str,
    ) -> ASRResult:
        if raw["status"] == "media_unavailable":
            resolution_error = raw["error"]
            return _build(
                result_id=result_id,
                source_audio=source_audio,
                recognizer=recognizer,
                processed_at=processed_at,
                status="media_unavailable",
                text="",
                language=None,
                confidence=None,
                error=ASRError(
                    code="media_unavailable",
                    message=resolution_error["message"],
                    retryable=resolution_error["retryable"],
                ),
            )

        status = raw["status"]

        if status == "succeeded":
            confidence = raw["confidence"]
            if confidence is not None and not (0.0 <= confidence <= 1.0):
                raise ValueError(
                    f"invalid_field: confidence {confidence!r} is outside the [0, 1] range"
                )
            return _build(
                result_id=result_id,
                source_audio=source_audio,
                recognizer=recognizer,
                processed_at=processed_at,
                status="succeeded",
                text=raw["text"],
                language=raw["language"],
                confidence=confidence,
                error=None,
            )

        if status == "no_speech":
            return _build(
                result_id=result_id,
                source_audio=source_audio,
                recognizer=recognizer,
                processed_at=processed_at,
                status="no_speech",
                text="",
                language=None,
                confidence=None,
                error=None,
            )

        # unsupported_format, recognizer_unavailable, failed
        backend_error = raw["error"]
        return _build(
            result_id=result_id,
            source_audio=source_audio,
            recognizer=recognizer,
            processed_at=processed_at,
            status=status,
            text="",
            language=None,
            confidence=None,
            error=ASRError(
                code=backend_error["code"],
                message=backend_error["message"],
                retryable=backend_error["retryable"],
            ),
        )
