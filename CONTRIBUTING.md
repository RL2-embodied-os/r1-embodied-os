# Contributing

## Documentation rules

1. Write in English.
2. Prefix every technical claim with **VERIFIED**, **DESIGN**, or **OPEN**.
3. Add a public first-party citation for every new **VERIFIED** claim.
4. Do not convert an **OPEN** item into a **VERIFIED** item without reproducible evidence and a recorded firmware or source revision.
5. Do not include names, schools, private endpoints, passwords, internal paths, or unpublished hardware information.

## Contract rules

- **DESIGN** - all JSON Schemas use Draft 2020-12 and set `additionalProperties: false` on every object.
- **DESIGN** - changes to normative contracts require a `schema_version` change and updated examples.
- **DESIGN** - remote messages may narrow a requested action but may not define authoritative safety limits.
- **DESIGN** - media contracts contain metadata and transport references only; binary and Base64 payloads are prohibited.

## Interface-contract rules

- **DESIGN** - keep interface definitions in `.py` modules (TypedDict, Protocol with `...` bodies, type aliases, pure validators).
- **DESIGN** - do not add Unitree SDK, DDS, socket, subprocess, thread, device, or hardware-control imports.
- **DESIGN** - do not add method bodies, background tasks, connection setup, or example code that could move hardware.

## Week 1 implementation rules

- **DESIGN** - place reusable Week 1 code under `implementations/telemetry/`, `implementations/perception/`, or `implementations/audio/`; do not place production modules under `experiments/`.
- **DESIGN** - implement the Protocols exported by `interfaces/`; do not copy or redefine shared schemas, TypedDicts, enums, or Protocols.
- **DESIGN** - implementations must be deterministic and dependency-injected. They return structured results and have no import-time side effects.
- **DESIGN** - Week 1 code must not perform network, file-media, device, SDK, DDS, subprocess, thread, binary-media, Base64, or hardware operations.
- **DESIGN** - `experiments/week01/` contains sanitized reproduction logs and results only.

## Contract ownership

- **DESIGN** - the architecture/interface owner reviews and merges changes under `contracts/`, `examples/`, and `interfaces/`.
- **DESIGN** - workstream contributors may propose contract changes, but a shape change must update the JSON Schema, Python type, examples, documentation, and tests in one reviewed change.
- **DESIGN** - after the Day 3 v0.1 freeze, record the reason and compatibility impact of every contract change.

## Change checklist

- Validate every schema against the Draft 2020-12 metaschema.
- Validate expected-valid examples successfully.
- Confirm expected-invalid examples fail for their documented reason.
- Run `python -m compileall interfaces implementations` and confirm the public interface and implementation packages import with no side effects.
- Run `python -m pytest tests/` and `python -m tests.validate_all_contracts`.
- Check relative Markdown links from a standalone copy of this folder.
- Scan for credentials, private data, untranslated text, binary/Base64 media, and forbidden hardware behavior.
