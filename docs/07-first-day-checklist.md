# First-Day Checklist

## Before technical work

- [x] **DESIGN** - read the package [README](../README.md).
- [x] **DESIGN** - read [R1 facts and open questions](02-r1-facts-and-open-questions.md).
- [x] **DESIGN** - read [Safety and laboratory rules](05-safety-and-lab-rules.md).
- [x] **DESIGN** - confirm your assigned role and expected deliverable from [Workstreams](06-workstreams-and-deliverables.md).
- [x] **DESIGN** - confirm that this package contains contracts only and is not a robot-control application.

## Contract orientation

- [x] **DESIGN** - identify the normative core schemas and draft media schemas.
- [x] **DESIGN** - explain why `command_id` is the idempotency key.
- [x] **DESIGN** - explain why remote `priority`, arguments, and preconditions are not authoritative safety policy.
- [x] **DESIGN** - confirm that motion requires a lease and valid expiry.
- [x] **DESIGN** - confirm that `stop` does not require a lease or ARMED state.
- [x] **OPEN** - confirm that `sit` is excluded from the initial skill contract pending delivered-firmware validation.

## Evidence discipline

- [x] **DESIGN** - use **VERIFIED**, **DESIGN**, or **OPEN** for each technical claim.
- [x] **DESIGN** - cite a public first-party source for every new **VERIFIED** claim.
- [x] **OPEN** - record delivered-firmware evidence before changing a capability from `unverified`.
- [x] **DESIGN** - keep credentials, personal data, private endpoints, and internal paths out of all artifacts.

## First deliverable

- **DESIGN** - submit one small, independently reviewable artifact: an evidence-table update, schema review, example case, state transition, or test matrix.
- **DESIGN** - include assumptions, open questions, acceptance criteria, and evidence links.
