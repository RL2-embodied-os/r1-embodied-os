# R1 Week 1 Read-only Starter Package

- **DESIGN** - this package is the team-internal contract baseline for R1 integration into ABot-Claw. It contains documentation, strict data contracts, examples, and side-effect-free Python interface definitions. The contracts defined here apply to all robots (R1, Go2, G1, Piper) — the R1-specific work is the Robot Adapter layer beneath them.
- **DESIGN** - this directory also contains the Week 1 architecture, QA tests, integration scenarios, and initial reports. It can be copied and tested independently of the source project directories.

## Run the Week 1 baseline

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/
python -m tests.validate_all_contracts
```

## Evidence labels

- **VERIFIED** - supported by a cited public first-party source.
- **DESIGN** - an architectural choice for this project, not a product fact.
- **OPEN** - requires validation against the delivered robot, firmware, or laboratory setup.

## Start here

1. Read [Project brief](docs/01-project-brief.md).
2. Review [R1 facts and open questions](docs/02-r1-facts-and-open-questions.md).
3. Study [Architecture and data flow](docs/03-architecture-and-data-flow.md) and [Contract semantics](docs/04-contract-semantics.md).
4. Read [Safety and lab rules](docs/05-safety-and-lab-rules.md) before any robot-facing work.
5. Select a role from [Workstreams and deliverables](docs/06-workstreams-and-deliverables.md).
6. Complete the [First-day checklist](docs/07-first-day-checklist.md).
7. Use the [Phase 0-2 team guide](docs/08-phase-0-2-team-guide.md) to align on what is ready now, what still needs validation, and what belongs to later work.

## Week 1 read-only additions

- **DESIGN** - `contracts/week01/` defines DetectionFrameResult and ASRResult v0.1.
- **DESIGN** - `examples/week01/` contains expected-valid, schema-invalid, and semantic-invalid fixtures.
- **DESIGN** - `interfaces/week01_models.py` and `interfaces/week01_interfaces.py` define the shared data types and Protocol seams for telemetry, visual, and audio Mock chains.
- **OPEN** - these additions do not verify any delivered R1 sensor or perception capability.

## Package boundary

- **DESIGN** - RTDL/SkillCommand messages are remote action requests, not motor, joint, DDS, or physical-safety commands.
- **DESIGN** - local authorization, hard limits, arbitration, expiry enforcement, and final safety decisions belong to the robot-side safety supervisor.
- **DESIGN** - the files under `interfaces/` are importable `.py` contracts with no import-time side effects or hardware implementation. They cannot connect to or control a robot.
- **DESIGN** - SkillCommand, RobotState, Capability, and Telemetry are normative draft contracts for this project; camera and audio metadata contracts are non-normative drafts pending commissioning.
- **OPEN** - no R1 capability is considered usable merely because a public SDK symbol exists. Delivered-firmware validation is required.

- **DESIGN** - this package intentionally contains no robot SDK imports, DDS initialization, sockets, subprocesses, device access, credentials, private endpoints, or binary media.

## Two-layer architecture: shared Edge Gateway vs per-robot Adapter

- **DESIGN** - The target architecture separates shared Edge Gateway responsibilities from per-robot Adapter responsibilities:

```
ABot-Claw Cloud (perception, reasoning, task planning)
        │
        │  SkillCommand / RobotState / Telemetry / Capability
        │
┌─ Edge Gateway (SHARED — one implementation for all robots) ─┐
│  command_validator    schema + expiry + clock skew          │
│  idempotency_store    command_id dedup                      │
│  lease_manager        grant / validate / revoke             │
│  safety_supervisor    final software gate before adapter    │
└─────────────────────────────────────────────────────────────┘
        │
        │  R1RobotAdapter Protocol  (per-robot)
        │
┌─ Robot Adapter (PER-ROBOT — R1-specific) ─┐      Go2   G1   Piper
│  telemetry_normalizer   raw→Telemetry      │      ...   ...   ...
│  robot_state_provider   snapshot           │
│  capability discovery   SDK→Capability     │
│  motion adapter         SkillCommand→SDK   │
└────────────────────────────────────────────┘
        │
   R1 SDK / Hardware
```

- **DESIGN** - the Edge Gateway layer is robot-agnostic. A future shared implementation should reuse an audited lease pattern rather than duplicate robot-specific lease logic.
- **DESIGN** - the Robot Adapter layer is per-robot. R1 needs its own adapter because the SDK, sensor layout, and physical behavior differ from Piper. This is the layer where Phase 0-2 R1 work happens.
- **DESIGN** - Phase 0-1 (this week): read-only Robot Adapter work only (telemetry, state, capability). No Edge Gateway implementation needed yet.
- **DESIGN** - Phase 2 (later): Edge Gateway implementation — at that point the team should extract from Piper rather than build from scratch.

## Directory guide

- **DESIGN** - `docs/` contains English onboarding, architecture, safety, and role descriptions.
- **DESIGN** - `contracts/` contains JSON Schema Draft 2020-12 contracts.
- **DESIGN** - `interfaces/` contains importable Python interface contracts for models, edge services, and the robot-adapter boundary.
- **DESIGN** - `examples/` contains expected-valid and expected-invalid contract examples.
- **VERIFIED** - [SOURCES.md](SOURCES.md) records the public first-party evidence used by this package.
