# R1 Facts and Open Questions

## Verified public facts

- **VERIFIED** - Unitree publicly lists R1 AIR, R1, and R1 EDU. The published total joint counts are 20, 26, and 26-40 respectively. [Source](../SOURCES.md#unitree-r1)
- **VERIFIED** - the public product table marks secondary development for R1 EDU, not for the other two SKUs. [Source](../SOURCES.md#unitree-r1)
- **VERIFIED** - the public product table lists an eight-core base processor, a four-microphone array, a speaker, Wi-Fi 6, and Bluetooth 5.2. [Source](../SOURCES.md#unitree-r1)
- **VERIFIED** - pinned public SDK2 revision `21d0a3b` contains R1 examples for high-level locomotion, low-level development, upper-body control, and audio. [Source](../SOURCES.md#unitree-r1)
- **VERIFIED** - the R1 high-level header at pinned revision `21d0a3b` exposes a dedicated R1 `LocoClient`; `Sit` is not an exposed method in that header. [Source](../SOURCES.md#unitree-r1)
- **VERIFIED** - the R1 audio example at pinned revision `21d0a3b` treats the published audio message as an ASR text result and uses a separate mechanism for microphone PCM and playback. [Source](../SOURCES.md#unitree-r1)

## Design assumptions

- **DESIGN** - treat the delivered robot as unsupported until its SKU, firmware, SDK revision, and permissions are recorded.
- **DESIGN** - use a dedicated robot-side adapter boundary so public SDK details do not enter cloud contracts.
- **DESIGN** - use separate robot-local and cloud-facing network interfaces where practical, with forwarding disabled unless explicitly reviewed.
- **DESIGN** - keep media payloads outside JSON and exchange only metadata and transport references through these contracts.

## Open questions for commissioning

- **OPEN** - delivered SKU, joint layout, firmware version, SDK revision, and secondary-development entitlement.
- **OPEN** - available high-level actions and their behavior on the delivered firmware.
- **OPEN** - readable physical E-Stop, remote takeover, fall detection, and safety-state signals.
- **OPEN** - camera model, calibration, available streams, encoding, timestamps, and transport.
- **OPEN** - microphone transport, channel count, timing, acoustic echo cancellation, and privacy controls.
- **OPEN** - external compute, network ports, USB host behavior, power budget, cooling, and mounting.
- **OPEN** - ROS 2 compatibility, navigation, obstacle avoidance, depth sensing, arm control, head control, hand configuration, and `sit`.

## Evidence rule

- **DESIGN** - an SDK class, topic, or example proves only that public source exists. It does not prove that the delivered firmware enables the capability.
- **DESIGN** - a capability becomes `supported` only after a versioned commissioning test records its evidence.
