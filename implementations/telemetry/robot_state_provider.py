"""
DESIGN: Robot_state_provider implementation

Keeps a current Robot_state snapshot in memory. 

Cotract Requirements:
- clock sources are injectable so tests are deterministic and do not depend on wall-clock time.
- 'timestamp_mono_ns' supports local ordering, 'timestamp_utc' supports global ordering.
"""

from datetime import datetime
from typing import Optional, Mapping, Callable
from interfaces.models import RobotState

ClockMono = Callable[[], int]
ClockUtc = Callable[[], str]

def default_mono_clock() -> int:
    import time
    return time.monotonic_ns()

def default_utc_clock() -> str:
    return datetime.utcnow().isoformat().replace("+00:00", "Z")

class RobotStateProvider: 
    def __init__(self, capability_snapshot_version: str, mono_clock: ClockMono = default_mono_clock, utc_clock: ClockUtc = default_utc_clock) -> None:
        self._capability_snapshot_version = capability_snapshot_version
        self._mono_clock = mono_clock
        self._utc_clock = utc_clock
        self._snapshot: Optional[RobotState] = None

    def update(self, robot_id: str, fields: Mapping[str, object]) -> RobotState:
        """
        records a new snapshot from mock or confirmed read-only fields.

        unknown booleans are registered as None
        """

        if not isinstance(robot_id, str) or not robot_id: 
            raise ValueError(f"invalid_field: robot_id must be a non-empty string, got {type(robot_id).__name__}")
        state: RobotState = {
            "schema_version": "1.0",
            "robot_id": robot_id,
            "timestamp_mono_ns": self._mono_clock(),
            "timestamp_utc": self._utc_clock(),
            "mode": fields.get("mode", "unknown"),
            "health": fields.get("health", "unknown"),
            "battery_pct": fields.get("battery_pct"),
            "standing": fields.get("standing"),
            "moving": fields.get("moving"),
            "estopped": fields.get("estopped"),
            "controlled_by_remote": fields.get("controlled_by_remote"),
            "errors": list(fields.get("errors", [])),
            "capability_snapshot_version": self._capability_snapshot_version,
        }
        self._snapshot = state
        return state

    async def get_state(self, robot_id: str) -> Optional[RobotState]:
        if self._snapshot is None:
            raise ValueError(f"missing_required_field: no snapshot recorded yet for robot_id {robot_id!r}")
        if self._snapshot["robot_id"] != robot_id:
            raise ValueError(f"invalid_field: robot_id {robot_id!r} does not match snapshot robot_id {self._snapshot['robot_id']!r}")
        return self._snapshot

    def staleness_ns(self, now_mono_ns: str) -> RobotState:
        """
        Returns how many nanoseconds old the current snapshot is, None if empty
        """
        if self._snapshot is None:
            return None
        return now_mono_ns - self._snapshot["timestamp_mono_ns"]