# Week 1 QA and Architecture Log

## 2026-07-17 — Initial baseline

Done:

- Defined the five Week 1 module boundaries and three Mock/read-only data flows.
- Added DetectionFrameResult/Detection2D and ASRResult Draft 2020-12 schemas and examples.
- Added shared TypedDicts and Protocols for telemetry normalization, media resolution, detection, audio resolution, ASR, and ASR normalization.
- Consolidated contracts, examples, interfaces, tests, and documentation into one self-contained Week 1 package.
- Added schema/metaschema validation with explicit `FormatChecker` and separate semantic checks.
- Ran `python -m pytest tests/`: 12 tests passed.

Next:

- Review data-adapter, visual-adapter, audio-adapter, and capability-evidence handoffs.
- Add their fixtures to the registered validation matrix without changing contract copies.
- Execute Saturday scenarios and record per-chain results.

Blocked:

- Real R1 camera, microphone, formats, timestamps, and transports remain unverified.
- Stale-data policy awaits the data-adapter proposal.

Need:

- Capability evidence and sanitized read-only mapping from the hardware workstream.
- Normalizer output from the data-adapter workstream.
- Deterministic visual and audio fixtures from the perception workstreams.
