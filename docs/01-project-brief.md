# Project Brief

## Objective

- **DESIGN** - build an R1-first edge-to-cloud contract that separates robot-local execution and safety from cloud-side perception and task reasoning.
- **DESIGN** - Phase 0 establishes a reproducible hardware and SDK baseline.
- **DESIGN** - Phase 1 uploads read-only perception and telemetry; it does not send motion commands.
- **DESIGN** - Phase 2 introduces a small, lease-controlled set of high-level action requests after laboratory approval.

## System boundary

- **DESIGN** - the target system boundary is:

```text
Cloud reasoning and services
        |
        | authenticated control/signaling and media sessions
        v
R1 edge gateway
  - contract validation
  - idempotency and lease checks
  - command scheduling
  - robot-side final safety gate
        |
        | vendor adapter boundary
        v
R1 controller and physical safety chain
```

- **DESIGN** - cloud components decide what action to request; they do not decide how motors or physical safety mechanisms operate.
- **DESIGN** - ABot-Claw may later consume the same capability and action contracts for multi-robot orchestration.
- **OPEN** - later integration with other robots is outside the Phase 0-2 deliverables.

## Phase deliverables

- **DESIGN** - the Phase 0-2 deliverables and exit criteria are:

| Phase | Deliverable | Exit condition |
| --- | --- | --- |
| 0 | Versioned hardware, firmware, SDK, network, sensor, and safety baseline | Read-only state works and the host team approves the baseline |
| 1 | Camera/audio metadata, telemetry, and authenticated upload contracts | Read-only data path passes stability and privacy review |
| 2 | Lease, idempotency, scheduler, and safety-supervisor contracts | Only approved high-level requests pass simulated and supervised tests |

## Non-goals

- **DESIGN** - no low-level joint, torque, motor, or continuous control is exposed remotely.
- **DESIGN** - no executable robot-control implementation is included in this package.
- **OPEN** - navigation, obstacle avoidance, depth sensing, ROS 2 integration, arm control, and `sit` remain outside the supported contract until separately validated.
