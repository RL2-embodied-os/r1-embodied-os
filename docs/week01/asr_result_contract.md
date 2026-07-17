# ASRResult Contract v0.1

## Contract status

- **DESIGN** — This is a normalized result contract for the Week 1 Mock audio chain.
- **DESIGN** — It contains text and result metadata only; audio bytes, Base64, local paths, transport URLs, and credentials are prohibited.
- **OPEN** — R1 microphone availability, audio format, sample rate, channels, transport, and real recognizer compatibility remain unverified.

The authoritative schema is `contracts/week01/asr-result.schema.json`. The Python types and Protocols are in `interfaces/week01_models.py` and `interfaces/week01_interfaces.py`.

## Ownership and flow

```text
AudioChunkMetadata
  -> AudioResolver
  -> AudioHandle / ResolutionError
  -> ASRBackend
  -> RawASRResult
  -> ASRNormalizer
  -> ASRResult
```

| Object | Producer | Consumer | Failure handling |
| --- | --- | --- | --- |
| `AudioHandle` | **DESIGN** — Mock `AudioResolver` | **DESIGN** — `ASRBackend` | Resolver returns `media_unavailable`; no backend call occurs |
| `RawASRResult` | **DESIGN** — Fake ASR or future adapter | **DESIGN** — `ASRNormalizer` | Backend/format failures remain explicit statuses |
| `ASRResult` | **DESIGN** — `ASRNormalizer` | **DESIGN** — QA and later language consumers | Invalid combinations are rejected by Schema |

## Fields

| Field | Constraint and unknown handling |
| --- | --- |
| `schema_version` | **DESIGN** — Constant `0.1`. |
| `result_id` | **DESIGN** — Non-empty result identifier. |
| `source_audio` | **DESIGN** — `robot_id`, `sensor_id`, and `sequence`; identity only, never a media payload. |
| `recognizer` | **DESIGN** — Implementation label such as `fake`; it does not assert a real service is available. |
| `status` | **DESIGN** — One of the six states below. |
| `text` | **DESIGN** — Non-empty only for `succeeded`; empty for no-speech and failures. |
| `language` | **DESIGN** — BCP-47-like tag or `null` when unavailable. |
| `confidence` | **DESIGN** — Number in `[0, 1]` or `null`; no value may be invented. |
| `processed_at` | **DESIGN** — RFC 3339 normalization completion time. |
| `error` | **DESIGN** — `null` for success/no-speech; otherwise a strict object containing `code`, `message`, and `retryable`. |

## Status semantics

| Status | Required result shape |
| --- | --- |
| `succeeded` | Non-empty `text`; `error: null`; language/confidence may be unavailable if not fabricated |
| `no_speech` | Empty `text`; `language: null`; `confidence: null`; `error: null` |
| `media_unavailable` | Empty result fields; error code matches status; recognizer is not called |
| `unsupported_format` | Empty result fields; error code matches status |
| `recognizer_unavailable` | Empty result fields; error code matches status |
| `failed` | Empty result fields; generic normalized failure with matching error code |

- **DESIGN** — `no_speech` is a successful recognition outcome with no detected speech, not a system failure.
- **DESIGN** — Schema validation rejects confidence outside `[0, 1]`, invalid timestamps, status/error mismatches, unknown fields, and missing required fields.
- **DESIGN** — Transport expiry is checked before ASR and is reported by `AudioResolver`, not inserted into AudioChunkMetadata.

## Backend replacement

- **DESIGN** — Week 1 implements a deterministic Fake ASR through `ASRBackend.transcribe(AudioHandle)`.
- **DESIGN** — A future real recognizer replaces only the `ASRBackend`; `AudioResolver`, `ASRNormalizer`, and `ASRResult` remain stable unless the contract is versioned.
- **DESIGN** — Baseline tests must not import a cloud SDK, open sockets, read audio files, access devices, or start subprocesses.
- **OPEN** — No real ASR provider is selected in Week 1.
