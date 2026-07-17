# Public Sources

**Verification date:** 2026-07-15

- **DESIGN** - only public first-party product pages, source repositories, and standards are used for **VERIFIED** claims.

## Unitree R1

- **VERIFIED** - [Unitree R1 product page](https://www.unitree.com/R1/) supports the cited SKU, joint-count, base-compute, camera-category, microphone-array, speaker, wireless-connectivity, and secondary-development statements. The page was checked on the verification date above and has no public immutable revision.
- **VERIFIED** - [Unitree SDK2 R1 examples at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/tree/21d0a3b/example/r1) show the public R1 example categories used by this package.
- **VERIFIED** - [R1 LocoClient header at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/include/unitree/robot/r1/loco/r1_loco_client.hpp) shows the published high-level client methods at that revision. Symbol presence does not prove compatibility with delivered firmware.
- **VERIFIED** - [R1 low-level example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/low_level/r1_ankle_swing_example.cpp) establishes only that a public R1 low-level example exists. This package does not reproduce initialization or control details.
- **VERIFIED** - [R1 arm SDK example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/high_level/r1_arm_sdk_dds_example.cpp) establishes only that a public upper-body example exists. This package exposes no arm or head control skill.
- **VERIFIED** - [R1 audio example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/audio/r1_audio_client_example.cpp) distinguishes ASR results, microphone PCM transport, and audio playback services in public example code.

## Protocol standards

- **VERIFIED** - [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) defines the schema dialect used by all contracts.
- **VERIFIED** - [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) defines the timestamp format.
- **VERIFIED** - [RFC 8827](https://www.rfc-editor.org/rfc/rfc8827.html) defines the WebRTC security architecture.
- **VERIFIED** - [RFC 8835](https://www.rfc-editor.org/rfc/rfc8835.html) defines WebRTC transport requirements.

## Revision policy

- **VERIFIED** - SDK2 evidence links in this package are pinned to public revision `21d0a3b`, observed as the head of `main` on 2026-07-15.
- **DESIGN** - before hardware integration, record the selected SDK commit, delivered firmware version, robot SKU, and commissioning evidence.
- **OPEN** - the exact SDK commit and firmware revision for the delivered research robot are not yet recorded in this package.
