# Workstreams and Deliverables

- **DESIGN** - assignments are role-based. A participant may contribute to more than one workstream after interfaces and dependencies are agreed.

## Workstream A - Hardware and SDK evidence

- **DESIGN** - role: evidence and commissioning analyst.
- **DESIGN** - input: delivered hardware, public vendor sources, host-approved read-only inspection procedure.
- **DESIGN** - dependencies: host-approved access, safety documentation, and availability of the delivered configuration.
- **DESIGN** - deliverables: version matrix, capability evidence table, sensor/network inventory template, and open-question log.
- **OPEN** - no capability changes from `unverified` to `supported` without reproducible commissioning evidence.
- **DESIGN** - acceptance: another team member can reproduce the recorded read-only observations without motion.

## Workstream B - Perception metadata contracts

- **DESIGN** - role: perception-contract and privacy analyst.
- **DESIGN** - input: draft camera/audio metadata schemas and Workstream A evidence.
- **DESIGN** - dependencies: Workstream A sensor evidence plus host-approved privacy and transport requirements.
- **DESIGN** - deliverables: transport selection note, timestamp/calibration requirements, privacy checklist, and schema change proposals.
- **OPEN** - codec, resolution, sampling, channel count, depth, and acoustic processing remain unset until evidence exists.
- **DESIGN** - acceptance: example metadata validates without containing media payloads or private endpoints.

## Workstream C - Control and telemetry contracts

- **DESIGN** - role: control-contract and telemetry analyst.
- **DESIGN** - input: SkillCommand, RobotState, Capability, and Telemetry schemas.
- **DESIGN** - dependencies: Workstream A capability evidence and the safety/lease rules approved through Workstream D.
- **DESIGN** - deliverables: compatibility review, valid/invalid examples, idempotency state table, and versioning proposal.
- **DESIGN** - acceptance: motion without a lease and expired motion fail; lease-independent `stop` succeeds.

## Workstream D - Scheduler and safety design

- **DESIGN** - role: scheduler and safety-design analyst.
- **DESIGN** - input: side-effect-free interface protocols, safety rules, and host-approved policy requirements.
- **DESIGN** - dependencies: Workstream C contract semantics, Workstream A commissioning evidence, and host safety authority decisions.
- **DESIGN** - deliverables: state-transition table, rejection-reason catalog, lease lifecycle, failure-injection matrix, and review checklist.
- **DESIGN** - acceptance: the design gives the robot-side safety supervisor final authority and never maps physical E-Stop to an SDK command.

## Shared review cadence

- **DESIGN** - each update reports completed evidence, contract changes, new open questions, risks, and the next independently verifiable deliverable.
- **DESIGN** - interface changes are reviewed before implementation work begins in another repository or package.
