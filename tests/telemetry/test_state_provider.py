"""Deterministic tests for RobotStateProvider
"""

import asyncio
import json
import pytest
from jsonschema import Draft202012Validator, FormatChecker
from implementations.telemetry.robot_state_provider import RobotStateProvider
from tests.contract_path import CONTRACTS_DIR

ROBOT_STATE_SCHEMA = json.loads((CONTRACTS_DIR / 'robot-state.schema.json').read_text())
_validator = Draft202012Validator(ROBOT_STATE_SCHEMA, format_checker=FormatChecker())

def assert_schema_valid(document: dict) -> None:
    errors = list(_validator.iter_errors(document))
    assert errors == [ ], [e.message for e in errors]

def _fixed_mono_clock(value : int):
    return lambda: value

def _fixed_utc_clock(value: str):
    return lambda: value

def test_update_get_state_is_schema_valid() -> None:
    provider = RobotStateProvider(
        capability_snapshot_version="1.0",
        mono_clock=_fixed_mono_clock(1_000_000_000), #1 second in nano seconds
        utc_clock = _fixed_utc_clock("2026-07-17T08:00:00Z")
    ) 
    provider.update('unit01', {'mode': 'idle', 'health': 'ready'})
    state = asyncio.run(provider.get_state('unit01'))
    assert_schema_valid(state)
    assert state['timestamp_mono_ns'] == 1_000_000_000
    assert state['capability_snapshot_version'] == "1.0"

def test_unknown_booleans_stay_null() -> None:
    provider = RobotStateProvider(
        capability_snapshot_version="1.0",
        mono_clock=_fixed_mono_clock(0), 
        utc_clock = _fixed_utc_clock("2026-07-17T08:00:00Z")
    )
    provider.update("unit01", {})
    state = asyncio.run(provider.get_state('unit01'))
    assert_schema_valid(state)
    assert state['standing'] is None
    assert state['moving'] is None
    assert state['estopped'] is None
    assert state['controlled_by_remote'] is None

def test_get_state_before_any_updates_gives_missing_required_field() -> None:
    provider = RobotStateProvider(capability_snapshot_version = '1.0')
    with pytest.raises(ValueError, match='^missing_required_field'):
        asyncio.run(provider.get_state('unit01'))

def test_staleness_ns_reflects_injected_clock_only() -> None:
    provider = RobotStateProvider(
        capability_snapshot_version = '1.0',
        mono_clock = _fixed_mono_clock(1_000_000_000),
        utc_clock= _fixed_utc_clock("2026-07-17T08:00:00Z"),
    )
    provider.update('unit01', {})
    # 5 seconds later
    assert provider.staleness_ns(now_mono_ns=6_000_000_000) == 5_000_000_000

def test_get_state_robot_id_mismatch_raises_invalid_field() ->None:
    provider = RobotStateProvider(
        capability_snapshot_version='1.0',
        mono_clock=_fixed_mono_clock(0),
        utc_clock=_fixed_utc_clock('2026-07-17T08:00:00Z')
    )
    provider.update('unit01',{})
    with pytest.raises(ValueError, match='^invalid_field'):
        asyncio.run(provider.get_state('other_robot'))
