# Architecture and Data Flow

## Layers

| Layer | Responsibility |
| --- | --- |
| Cloud | **DESIGN** - perception, language processing, task reasoning, policy checks, and remote action requests |
| Edge gateway | **DESIGN** - authentication, schema validation, idempotency, leases, scheduling, final safety validation, telemetry, and media transport |
| Adapter boundary | **DESIGN** - stable contract over version-specific robot services and state sources |
| Robot | **DESIGN** - vendor control, physical state, and the physical safety chain |

## Control flow

- **DESIGN** - the target contract-level control flow is:

```text
Cloud policy
  -> SkillCommand request
  -> authenticated edge ingress
  -> schema and expiry validation
  -> idempotency lookup
  -> lease and scheduler checks
  -> robot-side safety supervisor
  -> adapter contract
  -> robot-local implementation outside this package
```

- **DESIGN** - the safety supervisor is the final software gate before a robot-local implementation receives an action request.
- **DESIGN** - the cloud-provided `priority` is requested priority only; local policy maps or caps it.
- **DESIGN** - preconditions are claims to re-evaluate, never trusted sensor facts.
- **DESIGN** - retransmission does not extend command validity.

## Read-only data flow

- **DESIGN** - the target read-only data flow is:

```text
Robot-local state and sensors
  -> adapter or media backend outside this package
  -> normalized metadata and telemetry
  -> authenticated cloud session
  -> storage, monitoring, or perception services
```

- **DESIGN** - Phase 1 contains no remote motion path.
- **DESIGN** - camera and audio payloads travel through negotiated media or upload transports, not JSON contracts.
- **DESIGN** - control/signaling may use mutually authenticated TLS or an equivalent device identity mechanism.
- **VERIFIED** - WebRTC media security uses its own transport security model; mutually authenticated HTTPS does not replace DTLS-SRTP. [Source](../SOURCES.md#protocol-standards)

## Failure boundaries

- **DESIGN** - invalid schema, expired command, idempotency conflict, missing motion lease, unsupported capability, or failed precondition results in rejection before execution.
- **DESIGN** - loss of the cloud session revokes remote authority and invokes a locally configured safe-state transition.
- **DESIGN** - `safe_stop` names a state-machine outcome, not a vendor SDK method.
- **OPEN** - the correct physical response for each R1 posture and failure mode requires host-team and vendor validation.
