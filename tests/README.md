# Test Layout

| Location | Scope |
| --- | --- |
| `test_contract_validation.py` | **DESIGN** - shared JSON Schema and semantic-validation baseline |
| `test_week01_interfaces.py` | **DESIGN** - shared type and Protocol seam checks |
| `telemetry/` | **DESIGN** - Telemetry, RobotState, clock, missing-field, and stale-data tests |
| `perception/` | **DESIGN** - MediaResolver, Fake Detector, result, and error-path tests |
| `audio/` | **DESIGN** - metadata, resolver, Fake ASR, normalizer, and error-path tests |
| `integration/` | **DESIGN** - cross-workstream scenarios |

- **DESIGN** - Tests exercise the same public interfaces used by callers. They must not import ABot-Claw, connect to services or devices, or read binary media.
