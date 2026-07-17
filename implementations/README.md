# Week 1 Implementations

- **DESIGN** - This package provides scaffolding for implementations to be produced by the Telemetry, Perception, and Audio workstreams.
- **DESIGN** - Implementations must satisfy the Protocols in `interfaces/`; shared contract types are imported, never copied.
- **DESIGN** - All Week 1 implementations must be deterministic, dependency-injected, and safe to import.
- **DESIGN** - No module may perform network, file-media, device, SDK, DDS, subprocess, thread, binary-media, Base64, or hardware operations.

## Workstream locations

| Directory | Expected modules |
| --- | --- |
| `telemetry/` | **DESIGN** - `normalizer.py`, `state_provider.py`, `camera_metadata_validator.py` |
| `perception/` | **DESIGN** - `media_resolver.py`, `fake_detector.py`, `pipeline.py` |
| `audio/` | **DESIGN** - `metadata_validator.py`, `audio_resolver.py`, `fake_asr.py`, `normalizer.py`, `pipeline.py` |

- **DESIGN** - Tests belong under the matching `tests/` workstream directory. Sanitized execution logs and failure records belong under `experiments/week01/`.

## Telemetry failure convention

- **DESIGN** - `TelemetryNormalizer.normalize` returns one complete `Telemetry` object for valid input.
- **DESIGN** - missing or invalid required raw fields produce no partial Telemetry and raise `ValueError` with one stable reason-code prefix: `missing_required_field`, `invalid_field`, or `invalid_timestamp`.
- **DESIGN** - tests assert the reason-code prefix; human-readable detail may follow it.
