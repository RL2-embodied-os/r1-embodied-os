# R1 sensor and capability matrix

**Report version:** Week 01 / contract `1.0`
**Public SDK reference:** `unitree_sdk2@21d0a3b`
**Verification date:** 2026-07-18
**Method:** public first-party product/source inspection plus local environment audit
**Delivered robot:** Unitree R1, operator-reported 2026-07-18; not connected or queried

## Decision rule

A public product-table entry, SDK header, topic name, or example proves only that
public material exists. It cannot make a delivered capability `supported`. Because
the delivered SKU is reported as R1, but firmware, permissions, and lab procedure
were not available, so every delivered capability remains `unverified`. `unavailable` is also not used:
absence from one public header is not proof of absence from the delivered system.

## Contract capability matrix

| Capability | Status | Public evidence / source version | Verification method and date | Delivered-system gap |
|---|---|---|---|---|
| `stand` | `unverified` | R1 LocoClient header, SDK `21d0a3b` | Local pinned-source inspection, 2026-07-18 | Firmware compatibility, permissions, and safe commissioning not tested. |
| `move_velocity` | `unverified` | R1 LocoClient header, SDK `21d0a3b` | Local pinned-source inspection, 2026-07-18 | No motion test permitted; method presence is not support evidence. |
| `stop` | `unverified` | Project contract plus R1 LocoClient source, SDK `21d0a3b` | Contract/source inspection, 2026-07-18 | Physical stop behavior and safety chain are unknown; software stop is not E-Stop. |
| `camera` | `unverified` | R1 product-table row; no R1 camera example at pinned SDK revision | Product/source inspection, 2026-07-18 | Delivered camera device, access, format, calibration, and transport unknown. |
| `audio_input` | `unverified` | R1 product page; R1 audio example, SDK `21d0a3b` | Product/local-source inspection, 2026-07-18 | Example uses 16 kHz mono signed 16-bit PCM, but delivered format, timing, permission, and privacy procedure are unknown. |
| `audio_output` | `unverified` | R1 product page; R1 audio example, SDK `21d0a3b` | Product/local-source inspection, 2026-07-18 | Delivered speaker/playback availability and approval unknown; no output was run. |
| `depth_camera` | `unverified` | R1 row lists a binocular camera, not a verified depth API | Product/source inspection, 2026-07-18 | Binocular hardware must not be equated with a depth stream; no calibration/API evidence. |
| `navigation` | `unverified` | No R1-specific supporting evidence in the pinned baseline | Baseline/source inventory, 2026-07-18 | Requires vendor documentation and delivered-firmware test. |
| `obstacle_avoidance` | `unverified` | No R1-specific supporting evidence in the pinned baseline | Baseline/source inventory, 2026-07-18 | Requires sensor, algorithm, behavior, and safety verification. |
| `ros2` | `unverified` | SDK2 uses DDS, but that is not R1 ROS 2 compatibility evidence | Source-boundary review, 2026-07-18 | Requires an R1-specific supported matrix and delivered-system test. |
| `sit` | `unverified` | `Sit` is commented out in pinned R1 LocoClient header/example | Local header inventory, 2026-07-18 | Commented source is not support evidence or proof of permanent unavailability. |

## Sensor fact matrix

| Sensor / signal | Public product fact | Delivered status | Required commissioning evidence |
|---|---|---|---|
| Camera | Product table lists a binocular camera in the R1 row. | `unverified` | Delivered device enumeration; read permission; stream, encoding, dimensions, timestamps, calibration, frame name. |
| Depth | No verified depth stream follows from the product table alone. | `unverified` | Vendor-supported depth API/topic, units, range, calibration, timestamp, accuracy test. |
| Microphone | Product table lists a four-microphone array. | `unverified` | Device enumeration; privacy approval; encoding, sample rate, channels, chunking, timestamp source. |
| Speaker | Product table lists a speaker. | `unverified` | Delivered SKU/configuration, permission, safe volume procedure; no playback in Week 01. |
| Robot state / telemetry | Pinned R1 source exposes `GetFsmId`, `GetFsmMode`, and a candidate `rt/lowstate` layout. | `unverified` | Read-only capture showing delivered availability, exact values, semantics, units, rates, errors, and firmware. |
| Timestamp correlation | No delivered evidence. | `unverified` | Device/host clock source, monotonic-to-UTC correlation, drift and reset behavior. |
| Coordinate frames | No delivered frame inventory. | `unverified` | Frame names, handedness, axes, units, origin, transforms, and calibration version. |

## Safety procedure baseline

| Procedure | Status | Rule for the next session |
|---|---|---|
| Physical E-Stop identification and test | `unverified` | Obtain vendor/lab procedure; identify the physical device and operator before any actuation. |
| Power-on / support arrangement | `unverified` | Obtain written checklist for posture, support, exclusion zone, and personnel. |
| Remote takeover | `unverified` | Demonstrate locally without cloud dependency and record controller/mode indications. |
| Read-only test approval | `unverified` | Obtain approver, scope, date, permitted binaries/topics, data handling, and stop conditions. |

No SDK method, process kill, network disconnect, `controlled_stop`, or `safe_stop`
label is described here as a physical E-Stop.

## Source register

- Product page: <https://www.unitree.com/R1/>; version: live/unversioned; checked
  2026-07-18 by visual product-table inspection.
- SDK R1 examples: <https://github.com/unitreerobotics/unitree_sdk2/tree/21d0a3b/example/r1>;
  version `21d0a3b`; checked 2026-07-18 by local pinned-source inspection.
- R1 LocoClient header: <https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/include/unitree/robot/r1/loco/r1_loco_client.hpp>;
  version `21d0a3b`; checked 2026-07-18 by local source inventory.
- R1 audio example: <https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/audio/r1_audio_client_example.cpp>;
  version `21d0a3b`; checked 2026-07-18 by local source inventory.
- Contract baseline `SOURCES.md`; version observed 2026-07-15; reused as the
  project's pinned evidence register and rechecked 2026-07-18.
- Operator report; version: message received 2026-07-18; method: direct operator
  statement that the delivered hardware is Unitree R1. The unique identifier is
  intentionally excluded from this public evidence pack.
