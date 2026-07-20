"""Edge-side interfaces aligned with ABot-Claw's /code/execute + env.xxx() pattern.

No separate CommandScheduler, SafetySupervisor, or typed SkillCommand.
Scheduling and safety are handled by ABot-Claw's lease manager and
code executor; the robot adapter is the only typed execution seam.
"""

from typing import Protocol

from .models import RobotState


class RobotStateProvider(Protocol):
    """Provides the current RobotState snapshot to the LLM context."""
    async def get_state(self, robot_id: str) -> RobotState: ...
