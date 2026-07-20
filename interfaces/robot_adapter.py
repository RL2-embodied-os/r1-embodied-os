"""R1 robot adapter following ABot-Claw's /code/execute + env.xxx() pattern.

The LLM reads SDK docs describing these methods, then writes Python code
that calls them directly. Safety is provided by lease TTL, CodeValidator,
Critic feedback, and SDK2-level safety — not by an intermediate JSON layer.

Week 1 contracts (Telemetry, RobotState, CameraFrameMetadata, etc.) are
the data-definition side of the SDK docs that the LLM consults.
"""

from __future__ import annotations

from typing import Protocol

from .models import CapabilityReport, RobotState


class R1RobotAdapter(Protocol):
    # -- Capability & state ------------------------------------------------
    async def probe_capabilities(self) -> CapabilityReport:
        """Probe the connected R1 for currently available services."""
        ...

    async def get_state(self) -> RobotState:
        """Return an aggregated snapshot from rt/lowstate + rt/sportmodestate."""
        ...

    # -- Motion ------------------------------------------------------------
    async def stand(self) -> dict:
        """Stand up. Returns {"success": bool}."""
        ...

    async def move_velocity(
        self,
        vx: float,
        vy: float,
        yaw_rate: float,
        duration_ms: int,
    ) -> dict:
        """Velocity-controlled move.

        Args:
            vx: Forward velocity (m/s). R1 range approximately -2.5 to 3.8.
            vy: Lateral velocity (m/s). R1 range approximately -1.0 to 1.0.
            yaw_rate: Yaw rate (rad/s). R1 range approximately -4.0 to 4.0.
            duration_ms: How long to sustain the velocity before auto-stop.

        Returns:
            {"success": bool}
        """
        ...

    async def stop(self) -> dict:
        """Stop all motion (StopMove). Returns {"success": bool}."""
        ...

    async def damp(self) -> dict:
        """Emergency soft-stop (Damp). Highest priority, non-preemptable."""
        ...

    # -- Perception --------------------------------------------------------
    async def read_cameras(self) -> tuple[dict, dict]:
        """Capture current camera frames.

        Returns:
            (images, timestamps) where images is {sensor_id: np.ndarray}
            and timestamps is {sensor_id: float}.
        """
        ...
