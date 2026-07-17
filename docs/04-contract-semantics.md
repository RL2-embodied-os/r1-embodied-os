# Contract Semantics

- **DESIGN** - SkillCommand, RobotState, Capability, and Telemetry are normative drafts for this project. Version `1.0` identifies their current wire shape; it does not claim product or standards-body finality.

## SkillCommand

- **DESIGN** - `command_id` is the globally unique idempotency key.
- **DESIGN** - `issued_at` and `expires_at` use RFC 3339 UTC timestamps. A command is rejected as `invalid_time_window` when `expires_at <= issued_at` or when `expires_at` is later than `issued_at + ttl_ms`.
- **DESIGN** - on first receipt, the edge rejects the command as `expired` when `expires_at <= receive_utc`; otherwise it computes `remaining_ms = min(ttl_ms, floor(expires_at - receive_utc))` and sets `local_deadline = monotonic_now + remaining_ms`. Clock rollback or retry cannot extend that deadline.
- **DESIGN** - an `issued_at` value beyond the locally configured clock-skew allowance is rejected as `clock_skew`; the allowance is robot-side policy and is not carried in the remote request.
- **DESIGN** - `invalid-expired-command.json` is intentionally schema-valid but semantically invalid because its `expires_at` is in the past.
- **DESIGN** - `priority` is a requested value and is not an authorization or safety limit.
- **DESIGN** - `preconditions` are independently recomputed by the robot-side safety supervisor.
- **DESIGN** - `on_timeout: "safe_stop"` requests a local state-machine outcome and never selects a hardware command.

### Initial skill set

| Skill | Lease | ARMED state | Contract behavior |
| --- | --- | --- | --- |
| `stand` | Required | Required | **DESIGN** - request an approved transition to standing |
| `move_velocity` | Required | Required | **DESIGN** - request a bounded velocity action; local hard limits remain authoritative |
| `stop` | Not required | Not required | **DESIGN** - request termination of active remote motion through local policy |

- **OPEN** - `sit` is excluded until the delivered firmware and supervised tests establish support.
- **DESIGN** - joint, torque, arm, head, navigation, and obstacle-avoidance commands are outside this contract version.

## Idempotency

- **DESIGN** - first receipt stores `command_id`, a canonical request digest, status, and eventual result.
- **DESIGN** - a repeated identifier with the same digest returns the stored status or result without another side effect.
- **DESIGN** - a repeated identifier with different content is rejected as `idempotency_conflict`.
- **DESIGN** - storage retention must be longer than the maximum accepted command lifetime and retry window.

## Capability

- **DESIGN** - capability status is one of `supported`, `unavailable`, `unverified`, or `degraded`.
- **DESIGN** - only `supported` capabilities with a passing current health check may be scheduled.
- **DESIGN** - evidence records the commissioning test or public source used for the status.
- **OPEN** - values in the example report illustrate the contract and are not a delivered-robot inventory.

## RobotState and telemetry

- **DESIGN** - `RobotState` is a current normalized snapshot; telemetry is a periodic or event-driven observation.
- **DESIGN** - unknown safety booleans use `null` rather than silently becoming `false`.
- **DESIGN** - monotonic time supports local ordering; UTC supports cross-system correlation.
- **DESIGN** - units are encoded in field names, including `_ns`, `_ms`, `_mps`, and `_ratio`.

## Media metadata

- **DESIGN** - media schemas are non-normative drafts pending commissioning.
- **DESIGN** - metadata references `webrtc`, `multipart_upload`, or `object_storage` transport.
- **DESIGN** - no media schema contains binary data, Base64, raw audio, or image bytes.
- **OPEN** - codec, sampling, resolution, calibration, and timing values remain unverified unless commissioning evidence is attached.
