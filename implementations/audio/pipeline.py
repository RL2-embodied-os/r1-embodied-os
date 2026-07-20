"""Wires the Week 1 Mock audio chain together:

AudioChunkMetadata -> Validator -> Resolver -> FakeASR -> Normalizer -> ASRResult

This is the single entry point used for the Day 3 interface-freeze demo: feed
it raw metadata and get back a schema-shaped ASRResult (or a ValueError for
invalid metadata, which never becomes an ASRResult).
"""

from __future__ import annotations

from typing import Any, Mapping

from interfaces.week01_models import ASRResult

from .audio_resolver import MockAudioResolver
from .fake_asr import FakeASR
from .metadata_validator import AudioChunkMetadataValidator
from .normalizer import ASRNormalizer


class AudioPipeline:
    """Coordinates the Mock audio chain without owning any of its I/O.

    The resolver and ASR backend are injected so callers control the fixture
    catalogue for each scenario; this class only sequences the four steps.
    """

    def __init__(
        self,
        resolver: MockAudioResolver,
        asr: FakeASR,
        recognizer: str = "fake",
    ) -> None:
        self._validator = AudioChunkMetadataValidator()
        self._resolver = resolver
        self._asr = asr
        self._normalizer = ASRNormalizer()
        self._recognizer = recognizer

    async def process(
        self,
        raw_metadata: Mapping[str, Any],
        result_id: str,
        processed_at: str,
    ) -> ASRResult:
        metadata = self._validator.validate(raw_metadata)
        source_audio = {
            "robot_id": metadata["robot_id"],
            "sensor_id": metadata["sensor_id"],
            "sequence": metadata["sequence"],
        }

        resolution = await self._resolver.resolve(metadata)
        if resolution["status"] == "media_unavailable":
            raw = resolution
        else:
            raw = await self._asr.transcribe(resolution["handle"])

        return self._normalizer.normalize(
            raw, source_audio, self._recognizer, result_id, processed_at
        )
