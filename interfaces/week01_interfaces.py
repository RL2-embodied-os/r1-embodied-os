"""Protocol seams for the Week 1 read-only Mock pipelines."""

from typing import Mapping, Protocol

from .models import AudioChunkMetadataDraft, CameraFrameMetadataDraft, Telemetry
from .week01_models import (
    AudioHandle,
    AudioResolution,
    ASRNormalizationInput,
    ASRResult,
    DetectionBackendResult,
    DetectionContext,
    ImageHandle,
    ImageResolution,
    RawASRResult,
    SourceMediaReference,
)


class TelemetryNormalizer(Protocol):
    def normalize(self, raw: Mapping[str, object]) -> Telemetry: ...


class MediaResolver(Protocol):
    async def resolve(self, metadata: CameraFrameMetadataDraft) -> ImageResolution: ...


class DetectorBackend(Protocol):
    async def detect(
        self, media: ImageHandle, context: DetectionContext
    ) -> DetectionBackendResult: ...


class AudioResolver(Protocol):
    async def resolve(self, metadata: AudioChunkMetadataDraft) -> AudioResolution: ...


class ASRBackend(Protocol):
    async def transcribe(self, audio_handle: AudioHandle) -> RawASRResult: ...


class ASRNormalizer(Protocol):
    def normalize(
        self,
        raw: ASRNormalizationInput,
        source_audio: SourceMediaReference,
        recognizer: str,
        result_id: str,
        processed_at: str,
    ) -> ASRResult: ...
