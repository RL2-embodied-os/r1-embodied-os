# Week 1 Integration Report — Initial Draft

## Scope

- **DESIGN** — This draft covers contract and interface readiness only. It does not claim that teammate chains or real R1 sensors have passed integration.
- **OPEN** — Final results will be completed during the Day 6 review.

## Baseline result

| Area | Result | Evidence |
| --- | --- | --- |
| Development dependencies | PASS | `requirements-dev.txt` contains pytest and jsonschema format support only |
| Shared contract path | PASS | Tests resolve the in-package contract directories as a single source |
| Contract metaschemas | PASS | Draft 2020-12 `check_schema` runs for every registered schema |
| Valid/invalid examples | PASS | Expectations are asserted by automated tests |
| Schema/semantic separation | PASS | Missing lease, expiry, bbox ordering, image bounds, dimensions, and transport expiry are distinguished |
| Interface imports | PASS | Week 1 interface modules import without robot/service dependencies |
| Full teammate chains | PENDING | Awaiting role handoffs |

## Automated test result

```text
python -m pytest tests/ -q
12 passed
```

## Pending review

| Workstream | Required handoff | Status |
| --- | --- | --- |
| Hardware evidence | Capability matrix and sanitized mappings | Pending |
| Read-only data | Telemetry/RobotState outputs and anomaly fixtures | Pending |
| Visual perception | Mock resolver, Fake detector, and five anomaly scenarios | Pending |
| Audio perception | Mock resolver, Fake ASR/normalizer, and eight scenario categories | Pending |

## Teacher confirmation list

- **OPEN** — Delivered R1 sensor inventory and usable read-only fields.
- **OPEN** — Camera/audio formats, timestamps, and transport availability.
- **OPEN** — Whether an optional real-camera or YOLO attempt is appropriate after the Mock chain passes.
