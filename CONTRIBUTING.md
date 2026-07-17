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

## Interface-stub rules

- **DESIGN** - keep interface definitions in `.py` modules (TypedDict, Protocol with `...` bodies, type aliases, pure validators).
- **DESIGN** - do not add Unitree SDK, DDS, socket, subprocess, thread, device, or hardware-control imports.
- **DESIGN** - do not add method bodies, background tasks, connection setup, or example code that could move hardware.

## Change checklist

- Validate every schema against the Draft 2020-12 metaschema.
- Validate expected-valid examples successfully.
- Confirm expected-invalid examples fail for their documented reason.
- Run `python -m compileall interfaces` and confirm `interfaces.models`, `interfaces.robot_adapter`, `interfaces.edge_interfaces`, `interfaces.week01_models`, and `interfaces.week01_interfaces` import with no side effects.
- Check relative Markdown links from a standalone copy of this folder.
- Scan for credentials, private data, untranslated text, binary/Base64 media, and forbidden hardware behavior.
