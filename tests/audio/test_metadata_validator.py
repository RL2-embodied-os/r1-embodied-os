"""Behavioral tests for AudioChunkMetadataValidator."""

import copy
import json

import pytest

from implementations.audio.metadata_validator import AudioChunkMetadataValidator
from tests.contract_path import EXAMPLES_DIR


def _load_valid_metadata() -> dict:
    with (EXAMPLES_DIR / "audio-chunk-metadata.json").open("r", encoding="utf-8") as stream:
        return json.load(stream)


def test_valid_metadata_is_accepted() -> None:
    validator = AudioChunkMetadataValidator()
    document = _load_valid_metadata()

    result = validator.validate(document)

    assert result == document


def test_missing_required_field_is_rejected() -> None:
    validator = AudioChunkMetadataValidator()
    document = _load_valid_metadata()
    del document["sequence"]

    with pytest.raises(ValueError) as excinfo:
        validator.validate(document)

    assert str(excinfo.value).startswith("missing_required_field:")


def test_invalid_enum_value_is_rejected() -> None:
    validator = AudioChunkMetadataValidator()
    document = _load_valid_metadata()
    document["timestamp_source"] = "not_a_real_source"

    with pytest.raises(ValueError) as excinfo:
        validator.validate(document)

    assert str(excinfo.value).startswith("invalid_field:")


def test_malformed_timestamp_is_rejected() -> None:
    validator = AudioChunkMetadataValidator()
    document = _load_valid_metadata()
    document["captured_at"] = "not-a-timestamp"

    with pytest.raises(ValueError) as excinfo:
        validator.validate(document)

    assert str(excinfo.value).startswith("invalid_timestamp:")


def test_expired_transport_reference_is_not_the_validators_job() -> None:
    """Transport expiry is a resolver-owned semantic check, not a validator check.

    A metadata document with an already-expired transport reference is still
    schema-valid: the validator only confirms the timestamp is well-formed,
    not that it is in the future. See docs/week01/architecture_and_interfaces.md.
    """

    validator = AudioChunkMetadataValidator()
    document = copy.deepcopy(_load_valid_metadata())
    document["transport"]["expires_at"] = "2000-01-01T00:00:00Z"

    result = validator.validate(document)

    assert result["transport"]["expires_at"] == "2000-01-01T00:00:00Z"
