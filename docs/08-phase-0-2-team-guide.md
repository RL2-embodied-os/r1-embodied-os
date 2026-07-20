# Phase 0-2 Team Guide and Phase 3 Outlook

## Why this document exists

- **DESIGN** - this page gives our team a shared view of what we can use now, what still needs validation during Phase 0-2, and what we are intentionally leaving for Phase 3.
- **DESIGN** - for now, we only need to work with the Phase 0-2 material. The Phase 3 section is future context, not current work.
- **DESIGN** - the package contains architecture notes, contract drafts, examples, and side-effect-free Python interfaces. It is not an operational robot stack.
- **OPEN** - claims about the delivered robot remain open until we have evidence from its exact hardware, firmware, SDK, and laboratory setup.

## How we describe status

- **DESIGN** - `AVAILABLE NOW` means that teammates can review or reuse the artifact as a project draft. It does not prove that the corresponding robot capability works.
- **DESIGN** - `TO VALIDATE` means that we still need implementation evidence, delivered-hardware evidence, a test result, or the applicable safety approval during Phase 0-2.
- **DESIGN** - `LATER: PHASE 3` means that the item is useful future work but is outside our current Phase 0-2 scope.

## What the team can use now

| Area | Status | Where to start | How we can use it |
| --- | --- | --- | --- |
| Package orientation | **DESIGN** - `AVAILABLE NOW` | [README](../README.md), [project brief](01-project-brief.md), and [first-day checklist](07-first-day-checklist.md) | **DESIGN** - a self-contained English orientation package is available for Phase 0-2 review. |
| Public R1 evidence | **DESIGN** - `AVAILABLE NOW` as an evidence register | [Public sources](../SOURCES.md) and [R1 facts and open questions](02-r1-facts-and-open-questions.md) | **DESIGN** - cited public facts are separated from delivered-robot claims. **OPEN** - delivered SKU and firmware capabilities remain unverified. |
| Phase 0-2 architecture | **DESIGN** - `AVAILABLE NOW` for design review | [Architecture and data flow](03-architecture-and-data-flow.md) | **DESIGN** - cloud requests, edge validation, local safety authority, and the robot-adapter seam are defined. Agent internals and simulation are not defined. |
| Core contracts | **DESIGN** - `AVAILABLE NOW` as normative project drafts | [SkillCommand](../contracts/skill-command.schema.json), [RobotState](../contracts/robot-state.schema.json), [CapabilityReport](../contracts/capability.schema.json), and [Telemetry](../contracts/telemetry.schema.json) | **DESIGN** - Phase 0-2 wire shapes and invariants can be reviewed and tested independently of hardware. |
| Media metadata | **DESIGN** - `AVAILABLE NOW` as non-normative drafts | [Camera metadata](../contracts/camera-frame-metadata.schema.json) and [audio metadata](../contracts/audio-chunk-metadata.schema.json) | **DESIGN** - metadata and opaque transport references are defined without media bytes. **OPEN** - actual sensor formats remain unverified. |
| Python interfaces | **DESIGN** - `AVAILABLE NOW` | [Models](../interfaces/models.py), [edge interfaces](../interfaces/edge_interfaces.py), and [robot adapter](../interfaces/robot_adapter.py) | **DESIGN** - importable, side-effect-free contracts are available. No robot, network, simulator, or vendor implementation is included. |
| Examples | **DESIGN** - `AVAILABLE NOW` | [Examples directory](../examples/) | **DESIGN** - valid and intentionally invalid contract cases are available for schema and semantic review. |
| Safety policy | **DESIGN** - `AVAILABLE NOW` as a project policy draft | [Safety and laboratory rules](05-safety-and-lab-rules.md) | **DESIGN** - authority and prohibited-work rules are explicit. **OPEN** - physical procedures and responses require host and delivered-hardware validation. |

## Phase 0 - Baseline and evidence

### Available to us now

- **DESIGN** - the package defines the evidence labels, source policy, hardware questions, capability status vocabulary, and role-based evidence workstream.
- **DESIGN** - `CapabilityReport` can record `supported`, `unavailable`, `unverified`, or `degraded` with version and evidence metadata.
- **DESIGN** - the example capability report leaves delivered capabilities `unverified` rather than inferring support from public source symbols.
- **DESIGN** - we can use the Phase 0 material as an evidence and commissioning framework, not as a completed robot inventory.

### What we still need to validate in this phase

- **OPEN** - record the delivered SKU, firmware version, SDK revision, joint layout, permissions, and secondary-development entitlement.
- **OPEN** - complete the host-approved read-only inspection procedure without motion.
- **OPEN** - attach reproducible evidence before changing any delivered capability to `supported`, `unavailable`, or `degraded`.
- **OPEN** - record the applicable safety manual, physical E-Stop procedure, remote takeover process, and laboratory approval process.

### Shared Phase 0 conclusion

- **DESIGN** - the Phase 0 design and evidence material is ready for team use.
- **OPEN** - robot commissioning remains incomplete until the delivered-hardware questions above have recorded answers.

## Phase 1 - Read-only data contracts

### Available to us now

- **DESIGN** - normalized telemetry, robot-state, camera-metadata, and audio-metadata schemas are available with validating examples.
- **DESIGN** - camera and audio JSON contain metadata and opaque transport references only; binary and Base64 media are excluded.
- **DESIGN** - the architecture defines a read-only robot-to-cloud path and keeps remote motion outside Phase 1.
- **DESIGN** - privacy, endpoint, credential, and personal-data exclusions are documented.

### What we still need to validate in this phase

- **OPEN** - validate actual camera and audio availability, format, timestamp source, calibration, encoding, and privacy controls on the delivered configuration.
- **OPEN** - select and review the actual WebRTC, multipart-upload, or object-storage integration outside this package.
- **OPEN** - demonstrate authenticated read-only transport, stability, clock correlation, retention policy, and privacy review with no motion path.
- **OPEN** - record degraded and unavailable sensor behavior rather than substituting guessed formats.

### Shared Phase 1 conclusion

- **DESIGN** - the Phase 1 data contracts are ready for team review and integration planning.
- **OPEN** - a working sensor or cloud-upload pipeline is not part of this package.

## Phase 2 - R1RobotAdapter and ABot-Claw integration

### Available to us now

- **DESIGN** - R1 follows ABot-Claw's `/code/execute + env.xxx()` pattern. Safety is provided
  by lease TTL, CodeValidator, Critic feedback, and SDK2-level safety — no intermediate
  JSON command layer.
- **DESIGN** - `R1RobotAdapter` exposes a clean Python API (`stand()`, `move_velocity()`,
  `stop()`, `damp()`, `read_cameras()`, `get_state()`) modeled on ABot-Claw's `PiperRobotEnv`.
- **DESIGN** - `contracts/skill-command.schema.json` is kept as reference documentation of
  valid parameter ranges for the LLM — not as an execution interface.
- **DESIGN** - lease management and code execution reuse ABot-Claw's existing implementations.
- **DESIGN** - local authorization, hard limits, and final safety decisions remain robot-side
  responsibilities.

### Phase 2 acceptance checks

| ID | Status | Requirement | Current evidence |
| --- | --- | --- | --- |
| P2-A1 | **DESIGN** - `AVAILABLE NOW` | `R1RobotAdapter` method signatures and TypedDict docs are internally consistent. | [robot_adapter.py](../interfaces/robot_adapter.py), [models.py](../interfaces/models.py) |
| P2-A2 | **DESIGN** - `AVAILABLE NOW` | Lease TTL expiry triggers local safe-stop. | ABot-Claw `lease.py` pattern; R1 integration pending |
| P2-A3 | **DESIGN** - `AVAILABLE NOW` | CodeValidator blocks dangerous Python (shell, network, file delete). | ABot-Claw `code_executor.py` pattern; R1 adaptation pending |
| P2-A4 | **DESIGN** - `AVAILABLE NOW` | Adapter methods return documented shapes. | Per-method docstrings on `R1RobotAdapter` |
| P2-A5 | **DESIGN** - `AVAILABLE NOW` | `stop` always works regardless of lease state. | Adapter exposes `stop()` and `damp()` unconditionally |
| P2-A6 | **OPEN** - `TO VALIDATE` | LLM-generated code calling the adapter executes correctly on R1. | Requires supervised hardware test |
| P2-A7 | **DESIGN** - `AVAILABLE NOW` | No SDK method is equated with physical E-Stop. | [Safety rules](05-safety-and-lab-rules.md) |

### What we still need to validate in this phase

- **OPEN** - integrate ABot-Claw's existing lease manager and CodeValidator with R1's Agent Server.
- **OPEN** - implement `R1RobotAdapter` methods against the delivered R1 SDK2/DDS interface.
- **OPEN** - demonstrate that lease TTL expiry and cloud-session loss enter a locally configured safe state.
- **OPEN** - obtain explicit approval before any supervised motion test.

### Shared Phase 2 conclusion

- **DESIGN** - the Phase 2 adapter contracts and ABot-Claw integration plan are ready for team review.
- **OPEN** - a working R1 Adapter implementation, lease integration, or supervised motion test is not part of this package.

## Boundaries we should keep clear in Phase 0-2

- **OPEN** - no delivered R1 skill or sensor is claimed operational without commissioning evidence.
- **DESIGN** - no SDK method is equated with physical E-Stop.
- **DESIGN** - `sit`, `head_control`, and low-level motor/joint/torque/arm commands are excluded pending hardware evidence.
- **DESIGN** - no working cloud service, scheduler implementation, safety implementation, simulation, robot connection, or hardware-control path is included.
- **DESIGN** - no visual memory, multimodal memory, critic feedback, manipulation recovery, VLA, or autonomous replanning capability is included.

## Looking ahead: Phase 3, not required now

| Backlog item | Status | Why deferred | Expected future artifact |
| --- | --- | --- | --- |
| Agent Layer interface | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - Phase 0-2 requires high-level requests, not a complete agent loop. | **DESIGN** - responsibility map for context assembly, registered-skill selection, tool execution, result handling, and session state. |
| Full action lifecycle | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - the current package covers admission and basic status, not preemptive multi-skill execution. | **DESIGN** - `ActionStatus`, transition table, error catalog, timestamps, `FAILED`, `EXPIRED`, and `PREEMPTED` semantics. |
| Skill registry enforcement | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - schema-level skill rejection is sufficient for the current contract handoff. | **DESIGN** - end-to-end proof that an agent cannot submit a skill absent from the active capability-backed registry. |
| Simulation conformance | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - no simulator or executable adapter belongs in the current shared package. | **DESIGN** - Mock, MuJoCo, and real-adapter conformance matrix against a shared robot interface, with no claim of physical equivalence. |
| Memory query | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - Phase 1 first establishes read-only observations without visual-memory policy. | **DESIGN** - draft `MemoryQuery`, retention, provenance, privacy, invalidation, and evaluation contracts. |
| Critic feedback | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - the minimal Phase 0-2 loop does not require critic-driven correction. | **DESIGN** - draft `CriticResult`, confidence, evidence, retry recommendation, and escalation contracts. |
| Complex skill recovery | **DESIGN** - `LATER: PHASE 3` | **OPEN** - manipulation capabilities such as `grasp` are not validated or registered. | **DESIGN** - capability-gated recovery flow for re-observation, local correction, retry budget, and replanning. |
| Formal decision records | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - current decisions are documented inline and are sufficient for the Phase 0-2 starter handoff. | **DESIGN** - ADRs for SkillCommand versus generated Python, the agent-to-edge seam, local safety authority, delayed visual memory, and adapter conformance. |
| Research traceability | **DESIGN** - `LATER: PHASE 3` | **DESIGN** - Phase 0-2 establishes contracts before broader research comparison. | **DESIGN** - traceability from paper claim to interface invariant, implementation test, experiment, and result. |

## When we can start Phase 3

- **OPEN** - the delivered configuration and Phase 0 capability evidence are recorded.
- **OPEN** - the Phase 1 read-only path has passed stability and privacy review.
- **OPEN** - the Phase 2 admission, expiry, lease, idempotency, capability, and local-safety invariants have implementation evidence.
- **OPEN** - the host safety authority has approved the proposed scope extension.
- **DESIGN** - Phase 3 backlog items should be started one vertical slice at a time rather than as simultaneous memory, critic, simulation, manipulation, and VLA efforts.

## How the team uses this material

- [ ] **DESIGN** - the complete folder is tracked in the ABot-Claw repository so all relative links remain intact for every team member.
- [ ] **DESIGN** - treat this package as a Phase 0-2 design and contract handoff, not an operational robot stack.
- [ ] **DESIGN** - each teammate starts from the open validation questions relevant to their role (see Week 1 task breakdown).
- [ ] **DESIGN** - internal experiment logs, device details, and lab-specific information stay in `experiments/week01/`, not in this package.
- [ ] **DESIGN** - keep the Phase 3 backlog as planning context only; do not include it in Phase 0-2 completion claims.
- [ ] **DESIGN** - ABot-Claw's lease manager, CodeValidator, and code executor are shared across all robots. R1 reuses them via the `/code/execute` pattern rather than reimplementing scheduling or safety logic.

## What we can say as a team

- **DESIGN** - the current folder is the team's contract baseline for R1 integration — architecture, contracts, safety rules, evidence framework, and onboarding are in one place.
- **OPEN** - the folder does not by itself close hardware commissioning, read-only integration, scheduler implementation, simulation, or supervised robot testing.
- **DESIGN** - we can revisit Phase 3 together after the Phase 0-2 evidence and validation criteria are satisfied.
