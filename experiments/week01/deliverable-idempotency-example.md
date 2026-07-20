# First Deliverable: Idempotency Conflict Example

**DESIGN** - This artifact serves as the first deliverable, creating an example case for an `idempotency_conflict` to demonstrate understanding of the project's contract semantics and evidence discipline.

## Assumptions

- It is assumed that the `command_id` "cmd-stand-001" from `valid-stand-command.json` has already been processed by the system.
- It is assumed that the system stores a digest of the original request alongside the `command_id`.

## Open Questions

- What is the precise retention period for the idempotency store? The documentation states it must be "longer than the maximum accepted command lifetime and retry window," but a specific duration is not defined.

## Acceptance Criteria

1. The new file `invalid-idempotency-conflict.json` must be a valid `SkillCommand` according to the JSON Schema.
2. A semantic validator should identify this file as invalid, specifically because its `command_id` is identical to `valid-stand-command.json` but its content (the `skill` has changed from `stand` to `stop`) is different.

## Evidence Links

- **DESIGN** - The idempotency conflict rule is defined in Contract Semantics (docs/04-contract-semantics.md).