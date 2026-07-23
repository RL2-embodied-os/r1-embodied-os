"""
DESIGN: CameraFrameMetadata semantic validator

Handles metadata and transport references only. Schema-level checks (types, enums, patterns) already live in contracts/camera-frame-metadata.scheman.json and are enforced bt jsonschema
this module adds the semantic check that JSON schema cannot exprees
"""

from datetime import datetime, timezone
from typing import Optional
from interfaces.models import CameraFrameMetadataDraft

class CameraMetadataValidationError(ValueError):
    """raising errors with a stable reason-code prefix, same used in the telemetry convetion"""

def _parse_dt(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    return datetime.fromisoformat(normalized)

def validate_camera_frame_metadata(metadata: CameraFrameMetadataDraft, now: Optional[datetime] = None) -> None:
    """
    Raise CameraMetadataValidation error on semantic violations.
    'now' is injectable for deterministic tests, it defaults to real UTC time
    """

    current_time = now if now is not None else datetime.now(timezone.utc)
    width = metadata.get("width_px")
    height = metadata.get("height_px")

    if (width is None) != (height is None):
        raise CameraMetadataValidationError("invalid_field: width_px and heigh_px must both be present or be both null")
    transport = metadata["transport"]
    expires_at = transport.get('expires_at')

    if expires_at is not None:
        expiry = _parse_dt(expires_at)
        if expiry <= current_time:
            raise CameraMetadataValidationError(f"expired_transport: transport reference expired at {expires_at} ")

def image_size_status(metadata: CameraFrameMetadataDraft) -> str:
    """
    Return 'image_size_unavailable if the dimension is missing, otherwise returns 'ok'

    this status tells if wether the image should be feed to the Detection2D (when valid) or the perception chain when the dimensions are missing
    """
    if metadata.get('width_px') is None or metadata.get('height_px') is None:
        return 'image_size_unavailable'
    return 'ok'

