# R1 SDK baseline

**Status:** source and reported-hardware baseline complete; delivered-system commissioning is blocked
**Verification date:** 2026-07-18
**Safety scope:** read-only inspection only; no robot connection or actuation

## 1. Evidence labels

- **VERIFIED-PUBLIC**: directly supported by a cited Unitree product page or official
  repository at the stated revision. This does not verify delivered hardware.
- **VERIFIED-LOCAL**: observed on the research workstation during this investigation.
- **REPORTED-LAB**: supplied by the operator but not independently read from the
  robot; suitable for inventory planning, not capability verification.
- **DESIGN**: a project contract or proposed adapter behavior.
- **UNVERIFIED**: requires the delivered robot, its records, or lab approval.
- **BLOCKED**: attempted but could not be completed; the failure is recorded.

## 2. Delivered system inventory

| Item | Recorded value | Status | Blocking reason / required evidence |
|---|---|---|---|
| Hardware model / SKU | Unitree R1 / `R1` | REPORTED-LAB | Operator report received 2026-07-18. The unique device identifier is intentionally withheld from this public repository. |
| Firmware version | `null` | UNVERIFIED | Requires a read-only vendor-supported version query or commissioning screen. |
| SDK revision used by delivered robot | `null` | UNVERIFIED | Requires the lab's approved SDK checkout and compatibility record. |
| Public reference revision | `21d0a3b2c46ee48c8fdf2783becb6be3beb0a59b` | VERIFIED-LOCAL | Successfully checked out from Unitree's official repository on 2026-07-18; not a delivered-system claim. |
| Robot OS | `null` | UNVERIFIED | Requires a permitted read-only query; do not assume Ubuntu from SDK build docs. |
| Joint layout | `null` | UNVERIFIED | Product variants differ; requires SKU and delivered configuration. |
| SDK entitlement / permissions | `null` | UNVERIFIED | Requires lab/vendor confirmation for the delivered SKU. |
| Network / device permissions | `null` | UNVERIFIED | No approved robot network interface or device access was provided. |

The operator identifies the unit as the R1 SKU, so the R1 product-table row is the
correct public comparison row. Product-table entries still do not prove the
delivered configuration, firmware enablement, or API permissions.

## 3. Repository revisions

| Repository | Branch / revision | Role |
|---|---|---|
| `RL2-embodied-os/r1-embodied-os` | `ChronoIvan`, base `afb7e750820622a90b03ec72f5d7c35899c3d693` | Target repository for these artifacts. |
| `amap-cvlab/ABot-Claw` | `main`, `39c9ffc94a84f2e6baac431a9bff9771111f8539` | Architecture reference inspected read-only. |
| `unitreerobotics/unitree_sdk2` | `21d0a3b2c46ee48c8fdf2783becb6be3beb0a59b` | Pinned first-party SDK source inventory. |

## 4. Local build workstation

| Item | Observation | Status |
|---|---|---|
| Host OS | Microsoft Windows NT `10.0.26200.0`, x64 process environment | VERIFIED-LOCAL |
| Git | `2.55.0.windows.2` on PATH | VERIFIED-LOCAL |
| CMake | not found on PATH | VERIFIED-LOCAL |
| C/C++ compiler | `gcc`, `g++`, and `cl` not found on PATH | VERIFIED-LOCAL |
| Make / Ninja | not found on PATH | VERIFIED-LOCAL |
| Python | not found on PATH; an isolated validation runtime was available | VERIFIED-LOCAL |
| WSL Linux distribution | none installed | VERIFIED-LOCAL |
| Docker | not found on PATH | VERIFIED-LOCAL |

This workstation does not match the official SDK prebuild environment. The official
repository README specifies Ubuntu 20.04 LTS, aarch64 or x86_64, GCC 9.4.0, CMake
3.10+, Make, and the listed development libraries.

## 5. First-party setup and build recipe

The following is a reproducible transcription of the official SDK README, pinned to
the project reference revision. Run it only in an approved Ubuntu 20.04 development
environment. Building does not authorize running examples against a robot.

```bash
sudo apt-get update
sudo apt-get install -y cmake g++ build-essential libyaml-cpp-dev \
  libeigen3-dev libboost-all-dev libspdlog-dev libfmt-dev

git clone https://github.com/unitreerobotics/unitree_sdk2.git
cd unitree_sdk2
git checkout 21d0a3b
git rev-parse HEAD
mkdir build
cd build
cmake ..
make -j"$(nproc)"
```

Expected revision output begins with `21d0a3b`. Expected build acceptance is a zero
exit status from both CMake configure and compilation. No build-pass claim is made
in this report.

## 6. Attempt result

After three recorded local HTTPS failures on 2026-07-17, an approved network path
successfully checked out the official repository on 2026-07-18 and verified the full
SHA `21d0a3b2c46ee48c8fdf2783becb6be3beb0a59b`. Configure and compilation remain
blocked because this host has no Ubuntu distribution, CMake, Make, or C/C++ compiler
and therefore does not match Unitree's published build environment. Full commands,
errors, resolution, assessment, needed help, and next steps are in the hardware log.

## 7. Safe interface/header inventory

The following inventory records source presence, not delivered capability:

| Public source at `21d0a3b` | What it establishes | What it does not establish |
|---|---|---|
| `example/r1/` | R1 example categories exist in public SDK2. | Compatibility, permissions, or safe behavior on the delivered robot. |
| `include/unitree/robot/r1/loco/r1_loco_client.hpp` | A published high-level R1 client header exists; the baseline found no `Sit` method there. | That any method is enabled by delivered firmware. |
| `example/r1/low_level/r1_ankle_swing_example.cpp` | A low-level R1 example exists. | Safety approval; it must not be run in this task. |
| `example/r1/high_level/r1_arm_sdk_dds_example.cpp` | A public upper-body example exists. | Delivered joint layout or arm-control authorization. |
| `example/r1/audio/r1_audio_client_example.cpp` | Public code distinguishes ASR result, microphone PCM transport, and playback services. | Delivered audio format, permissions, or microphone/speaker availability. |
| `include/unitree/idl/hg/LowState_.hpp` plus the R1 low-level example | Public `rt/lowstate` candidate contains `version`, `mode_pr`, `mode_machine`, `tick`, IMU, 35 motor-state slots, wireless bytes, reserve, and CRC. | That this exact topic/layout is enabled or semantically documented on the delivered R1. |

The public audio example uses signed 16-bit PCM storage, `16000` Hz, one channel,
and a receive buffer sized for `160` ms. These are **example constants**, not verified
delivered stream properties; the contract fields remain `null` pending capture.

No motion, arm, low-level, audio playback, or other actuation example was run.

## 8. Read-only execution allowlist for commissioning

Nothing should be executed until the lab confirms the exact SDK revision, network
interface, delivered SKU, and which examples are side-effect-free. Candidate checks:

1. Print firmware/SDK/robot identity through a vendor-documented read-only path.
2. Use a purpose-built probe limited to `GetFsmId`, `GetFsmMode`, and approved topic
   subscriptions. Do not run the full public examples: several combine getters with
   setters, playback, LED, or motion behavior.
3. Capture field names, types, units, timestamps, and coordinate-frame identifiers;
   redact serial numbers and network addresses.
4. Confirm camera and microphone enumeration without recording or transmitting raw
   media unless separately approved.
5. Stop immediately if a program initializes a publisher, playback client, motion
   client, or device actuator.

## 9. Sources

All were checked by documentation/source inspection on 2026-07-18.

- [Unitree R1 product page](https://www.unitree.com/R1/) — live public product page;
  no immutable revision.
- [SDK2 repository README at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/README.md)
- [R1 examples at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/tree/21d0a3b/example/r1)
- [R1 LocoClient header at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/include/unitree/robot/r1/loco/r1_loco_client.hpp)
- [R1 low-level example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/low_level/r1_ankle_swing_example.cpp)
- [R1 arm example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/high_level/r1_arm_sdk_dds_example.cpp)
- [R1 audio example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/audio/r1_audio_client_example.cpp)
