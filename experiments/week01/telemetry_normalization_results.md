# Telemtry normalization results

**Author:** Matheus Ferreira
**Scope:** `TelemetryNormalizer`, `RobotStateProvider`

## Summary

`python -m pytest tests/telemetry/` - 13/13 passed
`python -m pytest tests/ -q` - 29/29 passed

All four required scenarios are demonstrated below with real input and output using jsonschema.Draft202012Validator

## Scenario 1 - normal input

**Input (Mock raw data)** 

```json
{
    "robot_id": "unit01",
    "timestamp_utc": "2026-07-17T08:00:00Z",
    "health": "ready",
    "mode": "idle",
    "battery_pct": 87.5,
    "network": {"rtt_ms": 12.0, "packet_loss_ratio": 0.0, "uplink_mbps": 50.0},
    "safety": {"armed": false, "estopped": false, "remote_override": false, "active_lease_id": null},
    "errors": []
}
```

**Output:** schema-valid `Telemetry` object, all fields populated as given.
**Validation:** PASS — no schema errors.

## Scenario 2 — Missing required fields


**Input A:** `{"timestamp_utc": "2026-07-17T08:00:00Z"}` (no robot_id)

**Output:** raises `ValueError: missing_required_field: robot_id` - no partial `Telemetry` object.

**Input B** `{"robot_id": "unit01"}` (no `timestamp_utc`)
**Output:** raises `ValueError: missing_required_field: timestamp_utc` — no partial `Telemetry` returned.

**Design note:** only robot_id and timestamp_utc are required from the raw input. health and mode default to the contract's \"unknown\" value when absent; network and safety fields default to null when absent.


## Scenario 3 - timestamp anomalies

**Input:** `{"robot_id": "unit01", "timestamp_utc": "not-a-timestamp"}`
**Output:** raises `ValueError: invalid_timestamp: timestamp_utc is not RFC3339 date-time: 'not-a-timestamp'`

out of range `battery_pct` and invalid `health` also raise `invalid_field` errors


## Scenario 4 - stale data

**Mechanism:** `RobotStateProvider.staleness_ns(now_mono_ns)` computes the gap between the current time and the timestamp recorded on the last `update()` call.

**Example** 
```python
provider.update("unit01", {...}) #monoclock = 1_000_000_000
provider.staleness_ns(now_mono_ns=6_000_000_000) # 5 seconds old
```

### OPEN - stale data policy proposal

- `staleness_ns()` stays a reporting method, not a rejectiong one, the provider itself should not silently drop or hide old data. there may be reasons for a consumer to know the data

- **Proproses threshold:** open question that needs real R1 tests to have an estimation
- Suggested follow-up: add `is_stale(now_mono_ns, threshold_ns)` method for convenience once the threshold above is confirmed by the team

