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
| SDK entitlement / permissions | `null` | UNVERIFIED | Public guide documents PC1-only secondary development for R1 EDU; delivered EDU status and PC1 permission require lab/vendor confirmation. |
| Network / device permissions | `null` | UNVERIFIED | No approved robot network interface or device access was provided. |

The operator identifies the unit as the R1 SKU, so the R1 product-table row is the
correct public comparison row. Product-table entries still do not prove the
delivered configuration, firmware enablement, or API permissions.

The live R1 developer guide, transcribed by the operator on 2026-07-18, states that
R1 uses DDS as its message middleware, with publish/subscribe for sustained or
medium/high-frequency exchange and request/response for low-frequency queries or
function switching. It describes direct API calls and function-style wrappers, and
identifies `unitree_sdk2` as the C++ development library. This is verified public
architecture evidence, not proof that a particular topic or API is enabled on the
delivered firmware.

The same guide documents the following public architecture facts: MQTT carries
fault/OTA telemetry and WebRTC signalling; HTTP binds App/Web users to robots;
STUN/TURN assists WebRTC connectivity; and WebRTC is the main App data path for
audio/video, lidar point clouds, motion state, and control. It states that functional
modules primarily exchange DDS data, the DDS IDL is ROS 2-compatible with a suitable
RMW, and the EDU variant can invoke interfaces through DDS or ROS 2. It also limits
secondary development on R1 EDU to PC1. The documented PC1 address and credential
acquisition details are deliberately excluded from this public repository.

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
| Live R1 developer guide | R1 uses DDS; publish/subscribe and request/response are documented interaction patterns; `unitree_sdk2` is the C++ development kit. | Delivered topic availability, field semantics, service permissions, or firmware compatibility. |
| Live R1 cloud/development architecture | WebRTC is the main App media/state/control path; DDS supports C++/Python; ROS 2 use is documented for EDU with a suitable RMW; sensor data is forwarded to DDS. | That the delivered unit is EDU, that PC1 access is authorized, or that any stream/topic is enabled. |
| `include/unitree/robot/b2/robot_state/` | The reused B2 `RobotStateClient` has read-only service/version queries as well as state-changing calls; pinned client API version is `1.0.0.2`. | That any named service or associated capability is present, enabled, safe, or functional on the delivered R1. |

The public audio example uses signed 16-bit PCM storage, `16000` Hz, one channel,
and a receive buffer sized for `160` ms. These are **example constants**, not verified
delivered stream properties; the contract fields remain `null` pending capture.

### High-level motion service boundary

The live R1 guide documents RPC whole-body control and a DDS upper-body path. The
high-level service depends on the built-in motion controller; after entering debug
mode, the built-in controller exits and this service is unavailable.

The only high-level RPC admitted to this read-only baseline is `GetFsmId` (and the
pinned-source `GetFsmMode`, retained as an undocumented raw value). The public FSM
table defines `0=zero torque`, `1=damping`, `4=locked standing`, and
`811=walk/run controller`.

The following calls change robot state and are prohibited during Week 01 read-only
commissioning: `Damp`, `Start`, `StandUp`, `ZeroTorque`, `Move`, `StopMove`,
`SetFsmId`, and `SetVelocity`. `Move` defaults to a one-second command, while
`SetVelocity` accepts a duration and clips to an allowed range; the supplied excerpt
does not state velocity units or clipping bounds. `StopMove` sets commanded velocity
to zero and must not be represented as physical E-Stop or verified safe-stop.

### Live documentation versus pinned source

The operator-transcribed live guide and `unitree_sdk2@21d0a3b` are not API-identical:

- Live documentation shows `ChannelFactory::Init(domainId, networkInterface,
  enableSharedMemory)` and requires external R1 applications to set shared memory to
  `false`. The pinned public header exposes only the two-argument
  `Init(domainId, networkInterface)` overload.
- A live-documentation note says `ChannelSubscriber` uses `CreateSendChannel`, while
  the pinned source constructor creates no channel and `InitChannel()` correctly
  calls `CreateRecvChannel`.
- The live table repeats the name `GetApiVersion` for the server-version row, while
  both its prototype and the pinned header use `GetServerApiVersion()`.
- The live RobotStateClient excerpt lists errors `5201` and `5202`; the pinned
  `robot_state_error.hpp` additionally defines `5203` and `5204` for low-power
  switch/status failures.

These are documentation/version discrepancies, not delivered-firmware findings.
Do not add the third `Init` argument to the pinned source or implement a subscriber
with a send channel. First record the delivered SDK revision and compile against its
actual headers.

### Official R1 read-only topic inventory

| Topic | Message type | Public description | Week 01 rule |
|---|---|---|---|
| `rt/lf/mainboardstate` | `unitree_hg::msg::dds_::MainBoardState_` | Low-frequency mainboard feedback | Subscribe only; array semantics require documentation. |
| `rt/lowstate`, `rt/lf/lowstate` | `unitree_hg::msg::dds_::LowState_` | IMU and motor feedback, normal/low-frequency | Prefer `rt/lf/lowstate` for initial commissioning. |
| `rt/lf/bmsstate` | `unitree_hg::msg::dds_::BmsState_` | Battery feedback | Candidate source for `battery_pct`; verify `soc` scale. |
| `rt/odommodestate`, `rt/lf/odommodestate` | `unitree_go::msg::dds_::IMUState_` | Odometry feedback, normal/low-frequency | Name/description do not establish pose fields, units, or frame. |
| `rt/secondary_imu`, `rt/lf/secondary_imu` | `unitree_hg::msg::dds_::IMUState_` | Torso IMU, normal/low-frequency | Prefer low-frequency; verify units and frame. |
| `rt/dex3/*/state`, `rt/lf/dex3/*/state` | `unitree_hg::msg::dds_::HandState_` | Optional left/right dexterous-hand feedback | Use only if delivered hand configuration is confirmed. |

The official low-level message excerpt further defines:

- `LowState.mode_pr`: `0=PR`, `1=AB` for parallel ankle/waist mechanism mode.
- `LowState.mode_machine`: `4=23-DoF`, `5=29-DoF`,
  `6=27-DoF (29-DoF with waist locked)`.
- `LowState.tick`: an unsigned counter incrementing every `1 ms`.
- `IMUState.quaternion`: order `Qw,Qx,Qy,Qz`.
- `MotorState.q`, `dq`, `ddq`: `rad`, `rad/s`, `rad/s^2` respectively; its two
  temperature elements represent surface and winding temperature.

The excerpt does not provide IMU physical units/axes/frame, torque and temperature
units, joint-slot ordering, `motorstate` bit meanings, CRC algorithm, or counter
reset/wrap behavior. `version[2]` must be captured raw until its encoding is defined.
The 35 slots are storage capacity, not proof that all 35 motors are active.

The following documented topics are excluded from the read-only probe:
`rt/lowcmd`, `rt/dex3/left/cmd`, and `rt/dex3/right/cmd`.

The documented RPC error inventory includes client errors `3001`, `3102`–`3107`
and service errors `3201`–`3207`. Preserve numeric codes and sanitized context;
do not reinterpret lease or rejection errors as physical safety state.

### RobotStateClient boundary

R1 documentation reuses the B2 device-state client. At pinned SDK `21d0a3b`, the
following calls are acceptable candidates for an approved read-only probe:

| Method | Read-only use | Interpretation limit |
|---|---|---|
| `ServiceList(std::vector<ServiceState>&)` | Inventory `name`, `status`, and `protect`. | A service name or running state does not prove its associated robot capability. |
| `LowPowerStatus(int32_t&)` | Record the reported low-power service state. | It is not physical E-Stop, armed state, or motion-safe state. |
| `GetPkgVersion(...)` | Record package version and module-version map. | Package/module versions must not be relabelled as whole-robot firmware. |
| `GetApiVersion()` / `GetServerApiVersion()` | Record client/server API compatibility after `Init()`. | A match does not prove delivered feature availability. |

Do **not** call `ServiceSwitch`, `SetReportFreq`, or `LowPowerSwitch`: each changes
service or device state. The SDK's Go2 robot-state example is not an approved
read-only test because it changes report frequency and switches services off/on.

The documented service names `ai_sport`, `basic_service`, `r1_arm_example`,
`vui_service`, and `unitree_slam` are inventory labels only. They do not by
themselves establish stand/motion, low-level health, arm, audio/light, or navigation
support on this delivered robot.

No motion, mode-switch, arm, low-level, audio playback, service-switch, or other
actuation example was run.

## 8. Read-only execution allowlist for commissioning

Nothing should be executed until the lab confirms the exact SDK revision, network
interface, delivered SKU, and which examples are side-effect-free. Candidate checks:

1. Print firmware/SDK/robot identity through a vendor-documented read-only path.
2. Use a purpose-built probe limited to `GetFsmId`, `GetFsmMode`, approved
   RobotStateClient read-only calls, and approved topic subscriptions. Do not run
   the full public examples: several combine getters with setters, service switches,
   playback, LED, or motion behavior.
3. Initialize the actual delivered SDK according to its installed header. For an
   external R1 application, follow the live guide's shared-memory-disabled rule; do
   not assume the pinned two-argument header implements the live three-argument API.
4. Capture field names, types, units, timestamps, and coordinate-frame identifiers;
   redact serial numbers and network addresses.
5. Confirm camera and microphone enumeration without recording or transmitting raw
   media unless separately approved.
6. Stop immediately if a program initializes a publisher, playback client, motion
   client, or device actuator.

## 9. Sources

All were checked by documentation/source inspection on 2026-07-18.

- [Unitree R1 product page](https://www.unitree.com/R1/) — live public product page;
  no immutable revision.
- [Unitree R1 developer guide](https://support.unitree.com/home/zh/R1_developer/about_R1)
  — live/unversioned page; official text transcribed by the operator on 2026-07-18.
- [SDK2 repository README at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/README.md)
- [R1 examples at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/tree/21d0a3b/example/r1)
- [R1 LocoClient header at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/include/unitree/robot/r1/loco/r1_loco_client.hpp)
- [R1 low-level example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/low_level/r1_ankle_swing_example.cpp)
- [R1 arm example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/high_level/r1_arm_sdk_dds_example.cpp)
- [R1 audio example at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/example/r1/audio/r1_audio_client_example.cpp)
- [RobotStateClient header at `21d0a3b`](https://github.com/unitreerobotics/unitree_sdk2/blob/21d0a3b/include/unitree/robot/b2/robot_state/robot_state_client.hpp)
