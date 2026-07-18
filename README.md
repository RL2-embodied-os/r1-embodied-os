# R1 Embodied OS

## Week 01: R1 fact baseline

The `ChronoIvan` branch contains the read-only R1 SDK, sensor, capability, mapping,
and safety evidence baseline. No robot motion, sound output, playback, or hardware
actuation is implemented or authorized by these artifacts.

- [SDK and environment baseline](docs/week01/r1_sdk_baseline.md)
- [Sensor capability matrix](docs/week01/r1_sensor_capability_matrix.md)
- [Read-only contract mapping](docs/week01/r1_readonly_mapping.md)
- [Hardware and investigation log](experiments/week01/r1_hardware_log.md)
- [Capability report](experiments/week01/r1_capability_report.json)
- [Validation results](experiments/week01/test_results.md)

With `r1-summer-research-starter-pack/` next to this repository, reproduce the
capability validation from this repository root:

```bash
python3 tests/validate_week01.py \
  --schema ../r1-summer-research-starter-pack/contracts/capability.schema.json \
  --report experiments/week01/r1_capability_report.json
```

The public repository uses logical ID `research-r1-01`. Keep the physical unit's
unique identifier in the lab's private asset/commissioning record, not Git history.
