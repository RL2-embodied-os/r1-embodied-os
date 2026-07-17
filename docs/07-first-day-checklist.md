# First-Day Checklist

## Before technical work

- [ ] **DESIGN** - read the package [README](../README.md).
- [ ] **DESIGN** - read [R1 facts and open questions](02-r1-facts-and-open-questions.md).
- [ ] **DESIGN** - read [Safety and laboratory rules](05-safety-and-lab-rules.md).
- [ ] **DESIGN** - confirm your assigned role and expected deliverable from [Workstreams](06-workstreams-and-deliverables.md).
- [ ] **DESIGN** - confirm that this package contains contracts only and is not a robot-control application.

## Contract orientation

- [ ] **DESIGN** - identify the normative core schemas and draft media schemas.
- [ ] **DESIGN** - explain why `command_id` is the idempotency key.
- [ ] **DESIGN** - explain why remote `priority`, arguments, and preconditions are not authoritative safety policy.
- [ ] **DESIGN** - confirm that motion requires a lease and valid expiry.
- [ ] **DESIGN** - confirm that `stop` does not require a lease or ARMED state.
- [ ] **OPEN** - confirm that `sit` is excluded from the initial skill contract pending delivered-firmware validation.

## Evidence discipline

- [ ] **DESIGN** - use **VERIFIED**, **DESIGN**, or **OPEN** for each technical claim.
- [ ] **DESIGN** - cite a public first-party source for every new **VERIFIED** claim.
- [ ] **OPEN** - record delivered-firmware evidence before changing a capability from `unverified`.
- [ ] **DESIGN** - keep credentials, personal data, private endpoints, and internal paths out of all artifacts.

## First deliverable

- **DESIGN** - submit one small, independently reviewable artifact: an evidence-table update, schema review, example case, state transition, or test matrix.
- **DESIGN** - include assumptions, open questions, acceptance criteria, and evidence links.
