"""Side-effect-free data contracts for the Week 1 read-only chains."""

from typing import List, Literal, Optional, Tuple, TypedDict, Union


ASRStatus = Literal[
    "succeeded",
    "no_speech",
    "media_unavailable",
    "unsupported_format",
    "recognizer_unavailable",
    "failed",
]
ASRBackendStatus = Literal[
    "succeeded",
    "no_speech",
    "unsupported_format",
    "recognizer_unavailable",
    "failed",
]
DetectionErrorCode = Literal[
    "image_size_unavailable",
    "invalid_bbox",
    "image_size_mismatch",
    "detector_unavailable",
    "failed",
]
ASRErrorCode = Literal[
    "media_unavailable",
    "unsupported_format",
    "recognizer_unavailable",
    "failed",
]


class SourceMediaReference(TypedDict):
    """Stable media identity; this is not a ROS/TF frame identifier."""

    robot_id: str
    sensor_id: str
    sequence: int


class DetectionError(TypedDict):
    code: DetectionErrorCode
    message: str
    retryable: bool


class ASRError(TypedDict):
    code: ASRErrorCode
    message: str
    retryable: bool


class ImageHandle(TypedDict):
    """Opaque image fixture handle with no bytes, URLs, or local paths."""

    media_kind: Literal["image"]
    fixture_id: str
    source: SourceMediaReference


class AudioHandle(TypedDict):
    """Opaque audio fixture handle with no bytes, URLs, or local paths."""

    media_kind: Literal["audio"]
    fixture_id: str
    source: SourceMediaReference


MediaHandle = Union[ImageHandle, AudioHandle]


class ResolutionError(TypedDict):
    code: Literal["media_unavailable"]
    message: str
    retryable: bool


class ImageAvailable(TypedDict):
    status: Literal["media_available"]
    handle: ImageHandle


class AudioAvailable(TypedDict):
    status: Literal["media_available"]
    handle: AudioHandle


class MediaUnavailable(TypedDict):
    status: Literal["media_unavailable"]
    error: ResolutionError


ImageResolution = Union[ImageAvailable, MediaUnavailable]
AudioResolution = Union[AudioAvailable, MediaUnavailable]
MediaResolution = Union[ImageAvailable, AudioAvailable, MediaUnavailable]


class Detection2D(TypedDict):
    detection_id: str
    class_id: int
    class_name: str
    confidence: float
    bbox_xyxy: Tuple[float, float, float, float]
    observed_at: str


class DetectionFrameResult(TypedDict):
    schema_version: Literal["0.1"]
    source_frame: SourceMediaReference
    detector: Literal["fake", "yolo_v5"]
    image_width: int
    image_height: int
    processed_at: str
    detections: List[Detection2D]


class DetectionContext(TypedDict):
    source_frame: SourceMediaReference
    image_width: int
    image_height: int
    observed_at: str
    processed_at: str


class DetectionBackendSuccess(TypedDict):
    status: Literal["succeeded"]
    result: DetectionFrameResult


class DetectionBackendFailure(TypedDict):
    status: Literal["failed"]
    error: DetectionError


DetectionBackendResult = Union[DetectionBackendSuccess, DetectionBackendFailure]


class ASRResult(TypedDict):
    schema_version: Literal["0.1"]
    result_id: str
    source_audio: SourceMediaReference
    recognizer: str
    status: ASRStatus
    text: str
    language: Optional[str]
    confidence: Optional[float]
    processed_at: str
    error: Optional[ASRError]


class RawASRResult(TypedDict):
    status: ASRBackendStatus
    text: str
    language: Optional[str]
    confidence: Optional[float]
    error: Optional[ASRError]


ASRNormalizationInput = Union[RawASRResult, MediaUnavailable]
