"""AudioChunkMetadata schema and format validation for the Week 1 Mock chain.

Schema-level checks only: structure, types, enums, and RFC 3339 timestamp
format (via jsonschema's FormatChecker). Transport reference expiry is a
resolver-owned semantic check, not validated here -- see
docs/week01/architecture_and_interfaces.md ("expired/unavailable reference
returns resolver error").
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from interfaces import AudioChunkMetadataDraft
from week01_contracts import CONTRACTS_DIR


_SCHEMA_PATH: Path = CONTRACTS_DIR / "audio-chunk-metadata.schema.json"


def _load_schema() -> Mapping[str, Any]:
    with _SCHEMA_PATH.open("r", encoding="utf-8") as stream:
        return json.load(stream)


_VALIDATOR = Draft202012Validator(_load_schema(), format_checker=FormatChecker())


def _reason(error: ValidationError) -> str:
    path = ".".join(str(part) for part in error.absolute_path) or "$"
    if error.validator == "required":
        return f"missing_required_field: {path}: {error.message}"
    if error.validator == "format":
        return f"invalid_timestamp: {path}: {error.message}"
    return f"invalid_field: {path}: {error.message}"


class AudioChunkMetadataValidator:
    """Validates raw AudioChunkMetadata against the audio-chunk-metadata contract."""

    def validate(self, document: Mapping[str, Any]) -> AudioChunkMetadataDraft:
        """Return the document typed as AudioChunkMetadataDraft, or raise ValueError.

        Raises ValueError with a stable reason-code prefix (missing_required_field,
        invalid_field, or invalid_timestamp) on the first schema violation found.
        No partial result is ever returned. Never reads or references binary audio.
        """

        errors = sorted(_VALIDATOR.iter_errors(document), key=str)
        if errors:
            raise ValueError(_reason(errors[0]))
        return cast(AudioChunkMetadataDraft, document)
