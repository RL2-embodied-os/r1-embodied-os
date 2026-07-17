# Saturday Integration Acceptance Scenarios

## Execution rules

- **DESIGN** — Run only Mock or verified read-only inputs. No robot motion, sound output, device access, SDK/DDS initialization, networking, subprocesses, or binary media.
- **DESIGN** — Every run records the input fixture, normalized output, schema status, semantic status, failure reason, and reproduction command.
- **OPEN** — Scenarios depending on R1 evidence remain Mock-only until the capability report supplies supported status, evidence, and verification time.

## Baseline commands

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/
python -m tests.validate_all_contracts
```

## Contract and state scenarios

| ID | Input | Expected result | Initial readiness |
| --- | --- | --- | --- |
| CT-01 | Existing valid examples | Schema valid; semantic valid where applicable | Ready |
| CT-02 | Motion command without lease | `schema_invalid`; no semantic execution | Ready |
| CT-03 | Structurally valid expired command | `schema_valid` then `semantic_invalid: expired` | Ready |
| ST-01 | Normal Mock observation | Telemetry and RobotState validate | Pending data-adapter handoff |
| ST-02 | Unknown safety observation | Safety booleans remain `null`, never silently `false` | Fixture ready; normalizer pending |
| ST-03 | Invalid RFC 3339 timestamp | `schema_invalid` through explicit `FormatChecker` | Ready |
| ST-04 | Stale observation with injected clock | Normalizer reports stale according to documented policy | Pending data-adapter policy |
| ST-05 | Camera capability `unverified` | Visual chain remains Mock-only; no capability field is injected into state JSON | Gating assertion ready |

## Visual scenarios

| ID | Input | Expected result | Initial readiness |
| --- | --- | --- | --- |
| VI-01 | Valid metadata + normal fixture | Deterministic result with one valid Detection2D | Contract fixture ready; adapter pending |
| VI-02 | Valid metadata + empty fixture | Successful `detections: []` | Adapter fixture pending |
| VI-03 | Reversed bbox coordinates | Schema valid; semantic `invalid_bbox` | Ready |
| VI-04 | Bbox exceeds image dimensions | Schema valid; semantic `image_size_mismatch` | Ready |
| VI-05 | Metadata dimensions are `null` | `image_size_unavailable`; detector not called | Ready |
| VI-06 | Expired/unavailable media reference | `media_unavailable`; detector not called | Expired fixture ready; adapter pending |
| VI-07 | Detector backend unavailable | `detector_unavailable`; no empty-success fabrication | Adapter scenario pending |

## Audio scenarios

| ID | Input | Expected result | Initial readiness |
| --- | --- | --- | --- |
| AU-01 | Normal speech fixture | Deterministic `succeeded` ASRResult | Contract fixture ready; adapter pending |
| AU-02 | No-speech fixture | `no_speech`, empty text, null confidence/error | Contract fixture ready; adapter pending |
| AU-03 | Invalid AudioChunkMetadata | Rejected before resolution | Adapter fixture pending |
| AU-04 | Expired transport | Resolver returns `media_unavailable` | Adapter fixture pending |
| AU-05 | Missing Mock fixture | Resolver returns `media_unavailable` | Adapter fixture pending |
| AU-06 | Unsupported format | `unsupported_format` with matching error | Adapter fixture pending |
| AU-07 | ASR backend unavailable | `recognizer_unavailable` with matching error | Adapter fixture pending |
| AU-08 | Confidence outside `[0, 1]` | `schema_invalid` | Ready |

## Review record

For each teammate handoff, record:

```text
Role:
Revision/path:
Reviewed inputs and outputs:
Commands run:
Passed:
Failed:
Unverified assumptions:
Follow-up owner and deadline:
```
