# Safety and Laboratory Rules

## Authority boundaries

- **DESIGN** - the physical E-Stop and vendor safety chain have authority over every software component.
- **DESIGN** - remote clients cannot arm the robot, clear a physical E-Stop, choose a physical stop mechanism, or enlarge local hard limits.
- **DESIGN** - the robot-side safety supervisor owns authorization, hard limits, lease enforcement, final precondition checks, and safe-state selection.
- **DESIGN** - `stop` bypasses lease and ARMED requirements so loss of remote authority cannot block a stop request.

## Prohibited work

- **DESIGN** - do not implement or expose low-level motor, torque, joint, or continuous movement control.
- **DESIGN** - do not connect these importable interface contracts to a robot, simulator, device, network, or vendor SDK inside this package.
- **DESIGN** - do not treat an SDK method as physical E-Stop.
- **DESIGN** - do not test motion without written host-team approval, an approved support arrangement, an identified physical E-Stop operator, and an agreed test procedure.
- **DESIGN** - do not publish credentials, network addresses, serial numbers, raw recordings, or personally identifying sensor data.

## Required motion-test gate

The following gate applies to a future implementation outside this package:

1. **OPEN** - record the delivered SKU, firmware, SDK revision, and safety manual.
2. **OPEN** - demonstrate the physical E-Stop and remote takeover procedure without cloud dependencies.
3. **DESIGN** - validate schema, expiry, idempotency, lease, and capability rejection with no hardware action.
4. **OPEN** - obtain host-team approval for the exact posture, support equipment, speed, duration, workspace, and personnel.
5. **OPEN** - measure detection-to-command and command-to-physical-state timing; do not assume a response-time guarantee.

## Stop terminology

- **DESIGN** - `controlled_stop` means a locally selected deceleration or motion-termination behavior.
- **DESIGN** - `safe_stop` means a safety-supervisor state, not a particular SDK call.
- **OPEN** - damping, zero-torque behavior, and other vendor modes require posture-specific validation.
- **DESIGN** - public SDK symbol names alone are insufficient evidence of safety certification or physical E-Stop behavior.

## Incident rule

- **DESIGN** - unexpected motion, stale state, clock uncertainty, invalid safety signals, or loss of local control authority ends the test and preserves logs for host-team review.
