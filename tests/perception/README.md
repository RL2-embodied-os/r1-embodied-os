# Perception Tests

- **DESIGN** - Add deterministic tests for normal detection, empty detection, invalid bounding boxes, image-size mismatch, unavailable media, and unavailable detector behavior.

- **VERIFIED** - All behaviors below are implemented in `test_perception_chain.py`
  and pass on the shared baseline: `python -m pytest tests/perception/ -v`
  (9 tests; full suite: 21 passed).

## Scenario coverage

| Required behavior | Test |
| --- | --- |
| Normal detection | `test_normal_detection_succeeds_and_conforms` |
| Determinism (same input, identical output) | `test_normal_detection_is_deterministic` |
| Empty detection (success, no targets) | `test_empty_detection_is_success_with_empty_array` |
| Invalid bounding box | `test_invalid_bbox_is_rejected_not_emitted`, `test_shared_validator_flags_invalid_bbox_example` |
| Image-size mismatch | `test_out_of_bounds_bbox_is_image_size_mismatch` |
| Missing image size | `test_null_dimensions_yield_image_size_unavailable` |
| Unavailable media | `test_unknown_frame_is_media_unavailable_and_detector_not_called` |
| Unavailable detector | `test_unknown_fixture_is_detector_unavailable_not_fake_success` |

## Conventions

- **DESIGN** - Interfaces are async; tests wrap calls in `asyncio.run(...)` to
  keep `requirements-dev.txt` unchanged (no pytest-asyncio dependency).
- **DESIGN** - Schema validation runs on the JSON-serialized document
  (`json.loads(json.dumps(result))`), i.e. the wire format: Python tuples are
  not JSON arrays until serialized.
- **DESIGN** - Fixture tables (frame identity → fixture id; fixture id →
  scripted detections) and the clock are injected by the tests; no I/O,
  wall-clock time, or network anywhere in the suite.
- **DESIGN** - `media_unavailable` short-circuits the chain: a counting proxy
  asserts the detector is never invoked.
- **VERIFIED** - Invalid examples are loaded from `examples/week01/` and checked
  through the shared semantic validator rather than duplicated here.

## Deliberately out of scope

- **DESIGN** - Transport-expiry checking is owned by the shared contract
  validators (`camera_expired_transport` in `validate_all_contracts`); it is
  referenced, not re-tested here. **OPEN** - confirm this ownership at the
  Day 3 interface freeze.
- **OPEN** - Real CameraFrameMetadata handoff scenarios from the telemetry
  workstream are integrated in Day 4–6; current metadata mirrors the shapes
  in `examples/`.

## How to run

    python -m pytest tests/perception/ -v

Run from the repository root; `tests/conftest.py` activates the shared
contract import path, so tests are not runnable as standalone scripts.
