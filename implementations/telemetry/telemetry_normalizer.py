"""DESIGN: Telemetry_normalizer implementation.

It converts mock data into a normalized format for the telemetry system.
satisfying contracts/telemetry.schema.json.

Requirements from the contract: 
-no network, threads, devide, SDK or DDS access.
-unknown safety booleans must stay 'None'(JSON - null), never 'False'.
-failure convention: missing or invalid required fields raise ValueError with a reason attached to it
'missing_required_field' or 'invalid_field_value' or 'invalid_timestamp'. No partial Telemetry is returned.
"""

from datetime import datetime
from typing import Mapping, Optional
from interfaces.models import Telemetry, TelemetryNetwork, TelemetrySafety

_VALID_HEALTH = {"ready", "busy", "degraded", "offline", "estop", "unknown"}
_VALID_MODE = {"boot", "discovery", "idle", "armed", "executing", "safe_stop", "estop", "unknown"}

#only the following fields are required for a valid Telemetry object, as all other has default values "unknown"/"null"
_REQUIRED_RAW_FIELDS = {"robot_id", "timestamp_utc"}

def _require_string(raw: Mapping[str, object], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value: 
        raise ValueError(f"invalid_field: {key} must be a non-empty string")
    return value

def _parse_utc_timestamp(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("invalid_field: timestamp_utc must be a string, got {type(value).__name__}")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"invalid_timestamp: {value} is not RCF3339 date-time") from exc
    return value

def _optional_bool(raw: Mapping[str, object], key: str) -> Optional[bool]:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"invalid_field: {key} must be a bool or null, got {type(value).__name__}")
    return value

def _optional_number(raw: Mapping[str, object], key: str, minimum: Optional[float] = None, maximum: Optional[float] = None) -> Optional[float]:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"invalid_field: {key} must be a number or null, got {type(value).__name__}")
    if minimum is not None and value < minimum:
        raise ValueError(f"invalid_field: {key} must be >= {minimum}, got {value}")
    if maximum is not None and value > maximum:
        raise ValueError(f"invalid_field: {key} must be <= {maximum}, got {value}")
    return float(value)

class TelemetryNormalizer:

    def normalize(self, raw: Mapping[str, object]) -> Telemetry:
        for field in _REQUIRED_RAW_FIELDS:
            if field not in raw or raw[field] is None:
                raise ValueError(f"missing_required_field: {field}")
        robot_id = _require_string(raw, "robot_id")
        timestamp_utc = _parse_utc_timestamp(raw["timestamp_utc"])
        health = raw.get("health", "unknown")

        if health not in _VALID_HEALTH:
            raise ValueError(f"invalid_field: health {health!r} not in {sorted(_VALID_HEALTH)}")
        mode = raw.get("mode", "unknown")
        if mode not in _VALID_MODE:
            raise ValueError(f"invalid_field: mode {mode!r} not in {sorted(_VALID_MODE)}")
        
        battery_pct = _optional_number(raw, "battery_pct", minimum=0, maximum=100)
        network_raw = raw.get("network") or {}

        if not isinstance(network_raw, Mapping):
            raise ValueError(f"invalid_field: network must be an object or null")\
        
        network: TelemetryNetwork = {
            "rtt_ms" : _optional_number(network_raw, "rtt_ms", minimum=0),
            "packet_loss_ratio" : _optional_number(network_raw, "packet_loss_ratio", minimum=0, maximum=1),
            "uplink_mbps" : _optional_number(network_raw, "uplink_mbps", minimum=0),
        }

        safety_raw = raw.get("safety") or {}
        if not isinstance(safety_raw, Mapping):
            raise ValueError(f"invalid_field: safety must be an object or null")
        
        active_lease_id = safety_raw.get("active_lease_id")
        if active_lease_id is not None and not isinstance(active_lease_id, str):
            raise ValueError(f"invalid_field: safety.active_lease_id must be a string or null")
        
        safety: TelemetrySafety = {
            "armed": _optional_bool(safety_raw, "armed"),
            "estopped" : _optional_bool(safety_raw, "estopped"),
            "remote_override": _optional_bool(safety_raw, "remote_override"),
            "active_lease_id": active_lease_id,
        }

        errors_raw = raw.get("errors", [])
        if not isinstance(errors_raw, list) or not all(isinstance(item, str) for item in errors_raw):
            raise ValueError("invalid_field: errors must be a list of strings")

        return {
            "schema_version": "1.0",
            "robot_id": robot_id,
            "timestamp_utc": timestamp_utc,
            "health": health,
            "mode": mode,
            "battery_pct": battery_pct,
            "network": network,
            "safety": safety,
            "errors": list(errors_raw),
        }

