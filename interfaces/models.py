from enum import Enum
from typing import List, Literal, Optional, TypedDict, Union

SkillName = Literal["stand", "move_velocity", "stop"]
TimeoutBehavior = Literal["safe_stop"]
CapabilityStatus = Literal["supported", "unavailable", "unverified", "degraded"]
RobotMode = Literal["boot", "discovery", "idle", "armed", "executing", "safe_stop", "estop", "unknown"]
RobotHealth = Literal["ready", "busy", "degraded", "offline", "estop", "unknown"]
Precondition = Literal["capability_available", "not_estopped", "armed", "lease_valid"]
TransportType = Literal["webrtc", "multipart_upload", "object_storage"]
TimestampSource = Literal["monotonic_correlated", "utc", "device", "unknown"]

class CommandDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IDEMPOTENT_REPLAY = "idempotent_replay"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"

class CommandStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"

class StandArgs(TypedDict):
    pass

class MoveVelocityArgs(TypedDict):
    vx_mps: float
    vy_mps: float
    yaw_rate_rps: float
    duration_ms: int

class StopArgs(TypedDict):
    pass

class _SkillCommandBase(TypedDict):
    schema_version: Literal["1.0"]
    command_id: str
    robot_id: str
    issued_at: str
    expires_at: str
    ttl_ms: int
    priority: int
    preconditions: List[Precondition]
    on_timeout: TimeoutBehavior

class StandCommand(_SkillCommandBase):
    lease_id: str
    skill: Literal["stand"]
    args: StandArgs

class MoveVelocityCommand(_SkillCommandBase):
    lease_id: str
    skill: Literal["move_velocity"]
    args: MoveVelocityArgs

class _StopCommandRequired(_SkillCommandBase):
    skill: Literal["stop"]
    args: StopArgs

class StopCommand(_StopCommandRequired, total=False):
    lease_id: str

SkillCommand = Union[StandCommand, MoveVelocityCommand, StopCommand]

class RobotState(TypedDict):
    schema_version: Literal["1.0"]
    robot_id: str
    timestamp_mono_ns: int
    timestamp_utc: str
    mode: RobotMode
    health: RobotHealth
    battery_pct: Optional[float]
    standing: Optional[bool]
    moving: Optional[bool]
    estopped: Optional[bool]
    controlled_by_remote: Optional[bool]
    errors: List[str]
    capability_snapshot_version: str

class CapabilityEvidence(TypedDict):
    status: CapabilityStatus
    evidence: List[str]
    verified_at: Optional[str]
    notes: str

class CapabilitySet(TypedDict):
    stand: CapabilityEvidence
    move_velocity: CapabilityEvidence
    stop: CapabilityEvidence
    camera: CapabilityEvidence
    audio_input: CapabilityEvidence
    audio_output: CapabilityEvidence
    depth_camera: CapabilityEvidence
    navigation: CapabilityEvidence
    obstacle_avoidance: CapabilityEvidence
    ros2: CapabilityEvidence
    sit: CapabilityEvidence

class CapabilityReport(TypedDict):
    schema_version: Literal["1.0"]
    robot_id: str
    robot_type: Literal["unitree_r1"]
    sku: Optional[str]
    firmware_version: Optional[str]
    sdk_revision: Optional[str]
    joint_layout_version: Optional[str]
    generated_at: str
    capabilities: CapabilitySet

class TelemetryNetwork(TypedDict):
    rtt_ms: Optional[float]
    packet_loss_ratio: Optional[float]
    uplink_mbps: Optional[float]

class TelemetrySafety(TypedDict):
    armed: Optional[bool]
    estopped: Optional[bool]
    remote_override: Optional[bool]
    active_lease_id: Optional[str]

class Telemetry(TypedDict):
    schema_version: Literal["1.0"]
    robot_id: str
    timestamp_utc: str
    health: RobotHealth
    mode: RobotMode
    battery_pct: Optional[float]
    network: TelemetryNetwork
    safety: TelemetrySafety
    errors: List[str]

class MediaTransportReference(TypedDict):
    type: TransportType
    reference: str
    expires_at: Optional[str]

class CameraFrameMetadataDraft(TypedDict):
    schema_version: Literal["0.1"]
    contract_status: Literal["draft"]
    robot_id: str
    sensor_id: str
    captured_at: str
    sequence: int
    timestamp_source: TimestampSource
    content_type: str
    encoding: Optional[str]
    width_px: Optional[int]
    height_px: Optional[int]
    calibration_version: Optional[str]
    verification_status: Literal["unverified", "verified", "degraded"]
    transport: MediaTransportReference

class AudioChunkMetadataDraft(TypedDict):
    schema_version: Literal["0.1"]
    contract_status: Literal["draft"]
    robot_id: str
    sensor_id: str
    captured_at: str
    sequence: int
    timestamp_source: TimestampSource
    content_type: str
    encoding: Optional[str]
    sample_rate_hz: Optional[int]
    channels: Optional[int]
    chunk_duration_ms: Optional[int]
    verification_status: Literal["unverified", "verified", "degraded"]
    transport: MediaTransportReference

class ActionReceipt(TypedDict):
    command_id: str
    decision: CommandDecision
    status: CommandStatus
    reason: Optional[str]

class ValidationResult(TypedDict):
    accepted: bool
    reason: Optional[str]
    local_deadline_mono_ns: Optional[int]
