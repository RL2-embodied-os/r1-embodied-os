# Week 1 Read-only Architecture and Interface Baseline

## Status and scope

- **DESIGN** — This document defines the Week 1 Mock/read-only integration seams. It is not evidence of delivered R1 capabilities.
- **DESIGN** — The only executable scope is contract validation and deterministic Mock data processing.
- **OPEN** — R1 sensor availability, firmware fields, timestamps, formats, and transport behavior require evidence from the hardware workstream.
- **DESIGN** — R1 follows ABot-Claw's `/code/execute + env.xxx()` pattern. The Week 1 data contracts
  serve as the data-definition side of R1's SDK docs for LLM code generation.
- **DESIGN** — Robot motion, audio output, vendor SDK calls, DDS, ROS, sockets, subprocesses, and
  device access are outside Week 1.

## Module boundaries

| Module | Responsibility | Input | Output | Explicit exclusions |
| --- | --- | --- | --- | --- |
| R1 Source / Robot Adapter seam | **DESIGN** — Isolate version-specific, read-only observations from shared models. | Mock observations or fields backed by hardware evidence | Raw observation mapping, capability evidence, media metadata | Motion, actuation, guessed fields, safety decisions |
| Edge Data Adapter | **DESIGN** — Normalize observations without inventing unavailable values. | Raw observation mapping and injected clock | `Telemetry` or `RobotState` | Capability status injection, network access, implicit `null` to `false` conversion |
| Perception Adapter | **DESIGN** — Resolve opaque Mock media handles and call replaceable perception backends. | Camera/audio metadata and test-owned fixture identifiers | `DetectionFrameResult` or `ASRResult`, or an explicit pipeline error | Binary media in JSON, Base64, local paths, real sensor I/O |
| Contract Validation | **DESIGN** — Validate Draft 2020-12 structure and separate semantic invariants. | Schema plus JSON document and an injected current time | Schema status, semantic status, reproducible errors | Robot authorization and physical safety policy |
| Mock Data Source | **DESIGN** — Supply deterministic, clearly labeled fixtures for tests. | Test case identifier | Mock observation or opaque fixture identifier | Claims about real R1 hardware |

## Read-only data flows

```text
Mock/verified read-only observation
  -> TelemetryNormalizer
  -> Telemetry / RobotState
  -> schema + semantic QA

CameraFrameMetadata
  -> MediaResolver (Mock; no I/O)
  -> ImageHandle
  -> DetectorBackend (Fake required; YOLO optional)
  -> DetectionFrameResult
  -> schema + bbox semantic QA

AudioChunkMetadata
  -> AudioResolver (Mock; no I/O)
  -> AudioHandle
  -> ASRBackend (Fake)
  -> RawASRResult
  -> ASRNormalizer
  -> ASRResult
  -> schema + semantic QA
```

## Shared interface ownership

| Contract/interface | Producer | Consumer | Failure behavior | Unknown handling |
| --- | --- | --- | --- | --- |
| `Telemetry` | Edge Data Adapter | QA and monitoring | **DESIGN** — Valid input returns a complete object; missing/invalid raw fields raise `ValueError` with `missing_required_field`, `invalid_field`, or `invalid_timestamp`; no partial object is returned | Safety booleans remain `null`; capability state is not inserted |
| `RobotState` | RobotState provider | QA and later agent/edge consumers | Schema rejection; invalid clock data is reported | Unverified physical state remains `null` or `unknown` as allowed |
| `CapabilityReport` | Hardware evidence workstream | QA and feature gating | Unsupported/unverified capability keeps dependent chains Mock-only | Missing evidence remains `unverified`, never inferred from an SDK symbol |
| Camera/Audio metadata | Read-only metadata adapter or Mock source | Resolver | Invalid schema is rejected before resolution; expired/unavailable reference returns resolver error | Unverified format fields remain `null` |
| `DetectionFrameResult` | Detector backend adapter | QA and downstream perception consumers | Invalid bbox/result is rejected; no verified detection is emitted | Missing image size returns `image_size_unavailable` |
| `ASRResult` | ASR normalizer | QA and later language consumers | Status distinguishes no speech from media/backend/format/system failures | Language and confidence may be `null` where the contract permits |

## Contract source and development setup

- **DESIGN** — This `week01/` directory is self-contained and does not require files from sibling project directories.
- **DESIGN** — `week01_contracts.py` resolves the single in-package `contracts/`, `examples/`, and `interfaces/` sources.
- **DESIGN** — Standalone demos call `week01_contracts.activate_contract_imports()` before importing `interfaces.week01_models` or `interfaces.week01_interfaces`; pytest performs the same activation in `conftest.py`.
- **OPEN** — A future repository integration may replace this bootstrap with an installable package.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/
python -m tests.validate_all_contracts
python -c "import week01_contracts; week01_contracts.activate_contract_imports(); import interfaces.week01_models"
```

## Internal handoff objects

| Object | Producer -> consumer | Constraints | Error and unknown behavior |
| --- | --- | --- | --- |
| `SourceMediaReference` | **DESIGN** — Metadata adapter -> resolver/backend context | `robot_id`, `sensor_id`, non-negative `sequence` | Identity only; never interpreted as ROS/TF |
| `ImageHandle` | **DESIGN** — `MediaResolver` -> `DetectorBackend` | `media_kind: image`, opaque fixture ID, source identity | No bytes, URL, or local path |
| `AudioHandle` | **DESIGN** — `AudioResolver` -> `ASRBackend` | `media_kind: audio`, opaque fixture ID, source identity | No bytes, URL, or local path |
| `ImageResolution` / `AudioResolution` | **DESIGN** — Resolver -> pipeline coordinator | Kind-specific success handle or `media_unavailable` | Unavailable result prevents backend invocation |
| `DetectionContext` | **DESIGN** — Pipeline coordinator -> detector | Positive known dimensions plus source/clock context | Missing size is handled before detector invocation |
| `DetectionBackendResult` | **DESIGN** — Detector -> coordinator | Success result or explicit detection error | Backend failure must not become an empty success |
| `RawASRResult` | **DESIGN** — ASR backend -> normalizer | Backend statuses exclude resolver-owned `media_unavailable` | Unknown confidence/language remain `null` |
| `ASRNormalizationInput` | **DESIGN** — Backend or resolver -> normalizer | Raw backend result or resolver failure | Allows normalized `media_unavailable` without calling ASR |

## Safety and replacement rules

- **DESIGN** — `MediaHandle.fixture_id` is opaque and must not contain media bytes, URLs, local paths, credentials, or private endpoints.
- **DESIGN** — Fake and future real backends implement the same Protocol; replacing a backend does not change the normalized result contract.
- **DESIGN** — Resolver errors are returned outside strict metadata objects; `additionalProperties: false` remains intact.
- **DESIGN** — Capability gating is evaluated from `CapabilityReport`, not from `Telemetry` or `RobotState` fields.
- **OPEN** — No real camera, microphone, depth stream, YOLO service, or ASR service is considered available until evidence and supervised integration establish it.
