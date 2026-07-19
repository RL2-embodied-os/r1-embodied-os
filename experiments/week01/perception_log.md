# Week 1 — Perception Run Log

Sanitized record of implementation runs. Commands are executed from the
repository root on branch `DaniilPerception`.

## Environment

- **VERIFIED** - Python 3.11 (conda base); dependencies from
  `requirements-dev.txt` only (`pytest`, `jsonschema[format]`).

## Baseline verification (before implementation)

    $ python -m pytest tests/ -q
    12 passed

    $ python -m tests.validate_all_contracts
    20/20 PASS (schema and semantic categories as expected)

## After implementation (Day 3 state)

    $ python -m pytest tests/ -q
    21 passed

    $ python -m pytest tests/perception/ -v
    9 passed  (scenario mapping: tests/perception/README.md)

    $ python -m tests.validate_all_contracts
    20/20 PASS — unchanged, including detection and camera semantic cases

    $ python -m compileall interfaces implementations
    OK — all modules import without networking, threads, or device access

## Failure records

- **VERIFIED** - Schema validation initially failed on the in-memory result:
  `bbox_xyxy` tuples are not JSON arrays until serialized
  (`jsonschema.ValidationError` on `instance['detections'][n]['bbox_xyxy']`).
  Resolution: tests validate the JSON-serialized document
  (`json.loads(json.dumps(result))`), i.e. the wire format.
- **VERIFIED** - Running a test file directly
  (`python tests/perception/test_perception_chain.py`) fails with
  `ModuleNotFoundError: interfaces`: `tests/conftest.py` activates the shared
  contract import path only under pytest. Resolution: always run via
  `python -m pytest` from the repository root.

## Reproduction

    python -m pytest tests/ -q
    python -m pytest tests/perception/ -v
    python -m tests.validate_all_contracts
