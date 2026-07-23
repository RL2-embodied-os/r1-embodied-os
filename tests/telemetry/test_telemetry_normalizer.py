"""
Deterministic tests for TelemetryNormalizer
"""

import pytest 
from implementations.telemetry.telemetry_normalizer import TelemetryNormalizer
from tests.contract_path import CONTRACTS_DIR
import json
from jsonschema import Draft202012Validator, FormatChecker

TELEMETRY_SCHEMA =  json.loads((CONTRACTS_DIR / "telemetry.schema.json").read_text())
_validator = Draft202012Validator(TELEMETRY_SCHEMA, format_checker=FormatChecker())

def assert_schema_valid(document: dict) -> None:
    errors = list(_validator.iter_errors(document))
    assert errors == [], [e.message for e in errors]

def test_normal_input_produces_schema_valid_telemetry() -> None:
    raw = {
        "robot_id": "unit01",
        "timestamp_utc": "2026-07-17T08:00:00Z",
        "health": "ready",
        "mode": "idle",
        "battery_pct": 87.5,
        "network": {"rtt_ms": 12.0, "packet_loss_ratio": 0.0, "uplink_mbps": 50.0},
        "safety": {"armed": False, "estopped": False, "remote_override": False, "active_lease_id": None},
        "errors": [],
    }
    telemetry = TelemetryNormalizer().normalize(raw)
    assert_schema_valid(telemetry)
    assert telemetry["health"] == "ready"
    assert telemetry["battery_pct"] == 87.5

def test_missing_robot_id() -> None:
    raw = {"timestamp_utc": "2026-07-17T08:00:00Z"}
    with pytest.raises(ValueError, match="^missing_required_field"):
        TelemetryNormalizer().normalize(raw)

def test_missing_timestamp() -> None:
    raw = {"robot_id": "unit01"}
    with pytest.raises(ValueError, match="^missing_required_field"):
        TelemetryNormalizer().normalize(raw)

def test_invalid_timestamp_format() -> None:
    raw = {'robot_id': 'unit01', 'timestamp_utc': 'not_a_timestamp'}
    with pytest.raises(ValueError, match="^invalid_timestamp"):
        TelemetryNormalizer().normalize(raw)

def test_unknown_safety_state_stays_null():
    raw = {'robot_id': 'unit01', 'timestamp_utc': '2026-07-17T08:00:00Z', 'safety': {}}
    telemetry = TelemetryNormalizer().normalize(raw)
    assert_schema_valid(telemetry)
    assert telemetry["safety"]["armed"] is None
    assert telemetry["safety"]["estopped"] is None
    assert telemetry["safety"]["remote_override"] is None

def test_capability_is_not_in_telemetry():
    raw= {'robot_id': 'unit01',
          'timestamp_utc': '2026-07-17T08:00:00Z'}
    telemetry = TelemetryNormalizer().normalize(raw)
    assert "capability" not in telemetry
    assert "capability_status" not in telemetry

def test_invalid_health_value() -> None:
    raw = {'robot_id': 'unit01', 'timestamp_utc': '2026-07-17T08:00:00Z', 'health': 'invalid_health'}
    with pytest.raises(ValueError, match="^invalid_field"):
        TelemetryNormalizer().normalize(raw)

def test_invalid_battery_pct_value() -> None:
    raw = {'robot_id': 'unit01', 'timestamp_utc': '2026-07-17T08:00:00Z', 'battery_pct': 150}
    with pytest.raises(ValueError, match="^invalid_field"):
        TelemetryNormalizer().normalize(raw)