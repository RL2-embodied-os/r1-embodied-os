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

## Workstream C - Adapter design and data contracts

- **DESIGN** - role: adapter-contract and data-format analyst.
- **DESIGN** - input: `R1RobotAdapter` Protocol, RobotState, Capability, and Telemetry schemas.
- **DESIGN** - dependencies: Workstream A capability evidence and ABot-Claw's existing lease/CodeValidator patterns.
- **DESIGN** - deliverables: per-method data contracts (input/output TypedDicts), valid/invalid examples, and adapter-ABot-Claw integration notes.
- **DESIGN** - acceptance: adapter method signatures match their TypedDict documentation; LLM-facing SDK docs are internally consistent.

## Workstream D - Lease and safety integration

- **DESIGN** - role: lease and safety-integration analyst.
- **DESIGN** - input: ABot-Claw's existing lease manager, CodeValidator, and `/code/execute` infrastructure.
- **DESIGN** - dependencies: Workstream C adapter contracts, Workstream A commissioning evidence, and host safety authority decisions.
- **DESIGN** - deliverables: lease-lifecycle mapping to R1 modes, safe-stop behavior specification, failure-injection matrix, and R1 safety review checklist.
- **DESIGN** - acceptance: lease TTL expiry triggers local safe-stop; CodeValidator blocks dangerous Python patterns; physical E-Stop is never mapped to an SDK call.

## Shared review cadence

- **DESIGN** - each update reports completed evidence, contract changes, new open questions, risks, and the next independently verifiable deliverable.
- **DESIGN** - interface changes are reviewed before implementation work begins in another repository or package.
