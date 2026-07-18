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
| `stand` | `unverified` | Live guide documents `StandUp` and FSM ID `4=locked standing`; R1 LocoClient header, SDK `21d0a3b` | Official-guide/pinned-source inspection, 2026-07-18 | High-level service is unavailable in debug mode; firmware compatibility, transition result, posture, permissions, and safe commissioning were not tested. |
| `move_velocity` | `unverified` | Live guide documents `Move`/`SetVelocity` and FSM ID `811`; R1 LocoClient header, SDK `21d0a3b` | Official-guide/pinned-source inspection, 2026-07-18 | No motion test permitted; units, clipping bounds, delivered support, controller state, and behavior remain unknown. |
| `stop` | `unverified` | Live guide documents `StopMove` as setting velocity to zero; R1 LocoClient source, SDK `21d0a3b` | Official-guide/source inspection, 2026-07-18 | `StopMove` is not physical E-Stop; stopping distance, failure behavior, balance and safety chain are unverified. |
| `camera` | `unverified` | R1 product-table row; live R1 guide documents WebRTC as the main App video path and says current software does not support GST video streaming | Operator-transcribed official page plus source inspection, 2026-07-18 | Exact software version, delivered WebRTC developer access, encoding, calibration, and timestamps unknown. |
| `audio_input` | `unverified` | Live guide names audio in the App WebRTC path; R1 audio example, SDK `21d0a3b` | Official-page/local-source inspection, 2026-07-18 | Direction and developer access are unclear; example uses 16 kHz mono signed 16-bit PCM, but delivered format, timing, permission, and privacy procedure are unknown. |
| `audio_output` | `unverified` | R1 product page; R1 audio example, SDK `21d0a3b` | Product/local-source inspection, 2026-07-18 | Delivered speaker/playback availability and approval unknown; no output was run. |
| `depth_camera` | `unverified` | R1 row lists a binocular camera; guide mentions lidar point clouds over WebRTC, not a depth-camera API | Product/source inspection, 2026-07-18 | Neither binocular hardware nor lidar point clouds prove a depth-camera stream; no depth units/calibration/API evidence. |
| `navigation` | `unverified` | Live guide lists a `unitree_slam` service name; pinned RobotStateClient can inventory services | Official-guide/pinned-source inspection, 2026-07-18 | A service label or running state is not functional navigation evidence; delivered service list, API, sensor, behavior, and safety tests are absent. |
| `obstacle_avoidance` | `unverified` | No R1-specific supporting evidence in the pinned baseline | Baseline/source inventory, 2026-07-18 | Requires sensor, algorithm, behavior, and safety verification. |
| `ros2` | `unverified` | Live R1 guide says DDS IDL is ROS 2-compatible with a suitable RMW and EDU can invoke interfaces through ROS 2 | Operator-transcribed official page, 2026-07-18 | Delivered unit has not been confirmed as EDU; RMW, ROS 2 distribution, PC1 permission, and delivered test are absent. |
| `sit` | `unverified` | `Sit` is commented out in pinned R1 LocoClient header/example | Local header inventory, 2026-07-18 | Commented source is not support evidence or proof of permanent unavailability. |

## Sensor fact matrix

| Sensor / signal | Public product fact | Delivered status | Required commissioning evidence |
|---|---|---|---|
| Camera | Product table lists a binocular camera; guide documents App video over WebRTC and reports GST unsupported by the current software version. | `unverified` | Identify exact software version and WebRTC developer interface; verify delivered stream, encoding, timestamps, calibration, and frame name. |
| Depth | Guide mentions lidar point clouds over WebRTC, not a depth-camera stream. | `unverified` | Vendor-supported depth-camera API/topic, units, range, calibration, timestamp, accuracy test. |
| Microphone | Product table lists a four-microphone array; guide names audio in the App WebRTC path. | `unverified` | Confirm input direction and developer access; privacy approval; encoding, sample rate, channels, chunking, timestamp source. |
| Speaker | Product table lists a speaker. | `unverified` | Delivered SKU/configuration, permission, safe volume procedure; no playback in Week 01. |
| Battery | Official R1 topic list names `rt/lf/bmsstate`; pinned `BmsState_` contains `soc`, `soh`, voltages, current, temperatures, cycle, and status fields. | `unverified` | Receive the delivered topic and confirm `soc` scale/range before mapping it to `battery_pct`. |
| Mainboard diagnostics | Official list names `rt/lf/mainboardstate`; pinned type contains fan, temperature, value, and state arrays. | `unverified` | Obtain array-index semantics, units, thresholds, and delivered samples before deriving `health`. |
| Robot state / telemetry | Official topic list names normal/low-frequency LowState, secondary IMU, odometry, BMS, and mainboard feedback; low-level guide defines `mode_pr`, R1 DoF codes in `mode_machine`, and 1 ms `tick`; pinned source exposes `GetFsmId`/`GetFsmMode`. | `unverified` | Read-only capture showing delivered availability, raw version/modes, active joint slots, exact values, rates, reset/wrap behavior, errors, and firmware. |
| Service/version inventory | Reused B2 RobotStateClient exposes read-only `ServiceList`, `LowPowerStatus`, and `GetPkgVersion`; pinned client API version is `1.0.0.2`. | `unverified` | Capture delivered names/status/protection and package/module versions; do not equate them with capability, safety state, or whole-robot firmware. |
| Timestamp correlation | Subscriber API documents receipt time as host-uptime microseconds; low-level guide says device `tick` increments every 1 ms. | `unverified` | Correlate both clock domains to UTC; verify whether `tick` denotes capture time plus its epoch, drift, reboot reset and wrap behavior. |
| Joint/IMU state | Guide defines quaternion order `Qw,Qx,Qy,Qz` and motor `q/dq/ddq` units as rad/rad/s/rad/s^2. | `unverified` | Determine IMU units/axes/frame, joint-slot ordering and active count, torque/temperature/voltage units, state bits, rates and calibration. |
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
- R1 developer guide: <https://support.unitree.com/home/zh/R1_developer/about_R1>;
  version: live/unversioned; official text transcribed by the operator on 2026-07-18.
  Establishes DDS interaction patterns, the C++ SDK, and the current-version GST
  limitation; documents WebRTC, MQTT/HTTP/STUN/TURN roles, conditional EDU ROS 2
  access, PC1-only secondary development, Channel/Client API semantics, RPC errors,
  the R1 Topic inventory, and RobotState service names. Exact software version and
  sensitive PC1 connection details are not included.
- RobotStateClient source: <https://github.com/unitreerobotics/unitree_sdk2/tree/21d0a3b/include/unitree/robot/b2/robot_state>;
  version `21d0a3b`; checked 2026-07-18 by local source inspection. Read-only and
  state-changing methods were separated; no call was made to a robot.
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
