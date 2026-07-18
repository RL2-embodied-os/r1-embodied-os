# R1 read-only candidate mapping

**Contract versions:** `Telemetry 1.0`, `RobotState 1.0`,
`CameraFrameMetadata 0.1 draft`, `AudioChunkMetadata 0.1 draft`
**SDK reference:** `unitree_sdk2@21d0a3b`
**Verification date:** 2026-07-18

## Mapping labels

- **Verified public:** a public source or project contract contains the item; this is
  not delivered-data verification.
- **Contract placeholder:** required by the shared contract but no R1 raw mapping is
  verified. Emit `null`, `unknown`, or an explicit error where the schema permits.
- **Candidate:** a future adapter input or derivation to test; never ship it as a
  verified mapping without a versioned capture.
- **Absent from contract:** evidence should be recorded during commissioning even
  though the current contract has no field for it.

## Telemetry `1.0`

The official R1 developer guide establishes DDS publish/subscribe as the intended
pattern for sustained or medium/high-frequency data. `rt/lowstate` is therefore a
source-backed candidate for the adapter's subscriber path, but delivered publication
and field semantics still require capture. Low-frequency FSM reads fit the documented
request/response pattern through function-style SDK calls. The guide also documents
motion state over the App's WebRTC path, but the Week 01 local adapter remains DDS
first until a delivered WebRTC metadata/status interface is verified.

| Contract field | Proposed source | Classification | Rule before commissioning |
|---|---|---|---|
| `schema_version` | constant `1.0` | DESIGN | Populate exactly. |
| `robot_id` | deployment configuration | DESIGN | Use a non-secret logical ID; never copy serial number automatically. |
| `timestamp_utc` | adapter host UTC correlated to DDS receipt time and `LowState.tick` | Candidate | Official guide says `tick` increments every 1 ms. Its epoch/reset/wrap behavior and relation to capture time remain unverified; do not label receipt UTC as device capture UTC. |
| `health` | normalizer over connection, RPC errors, and candidate `rt/lf/mainboardstate` diagnostics | Candidate / contract placeholder | Emit `unknown` until mainboard array semantics and error precedence are verified. |
| `mode` | `LocoClient.GetFsmId` plus separately captured `GetFsmMode` | Publicly documented candidate | Public FSM IDs are `0=zero torque`, `1=damping`, `4=locked standing`, and `811=walk/run controller`. Preserve unknown IDs and raw `GetFsmMode`; emit contract `unknown` until the delivered value and mapping policy are accepted. Never infer from the last command. |
| `battery_pct` | `rt/lf/bmsstate` → `BmsState_.soc` | Publicly documented candidate | Keep `null` until the delivered topic is received and `soc` range/unit is confirmed as percentage. Do not convert voltage. |
| `network.rtt_ms` | adapter-to-robot measurement | Candidate | `null` until endpoint and method are approved. |
| `network.packet_loss_ratio` | transport counters over a defined window | Candidate | `null`; document window and denominator. |
| `network.uplink_mbps` | edge transport measurement | Candidate | `null`; this is not an SDK sensor field. |
| `safety.armed` | verified local safety-supervisor signal | Contract placeholder | `null`; locomotion mode is not automatically equivalent. |
| `safety.estopped` | vendor/lab-confirmed physical safety-state signal | Contract placeholder | `null`; never infer from a software stop call. |
| `safety.remote_override` | verified remote-takeover signal | Contract placeholder | `null`. |
| `safety.active_lease_id` | future shared Edge Gateway | DESIGN / later phase | `null` in Week 01; not an R1 SDK field. |
| `errors` | adapter validation/read failures and documented RPC codes `3001`, `3102`–`3107`, `3201`–`3207` | Candidate | Preserve numeric code and sanitized context; do not map lease/rejection errors to physical E-Stop. |

## RobotState `1.0`

| Contract field | Proposed source | Classification | Rule before commissioning |
|---|---|---|---|
| `schema_version`, `robot_id` | constant and deployment config | DESIGN | Same identity rule as Telemetry. |
| `timestamp_mono_ns` | Prefer validated device `LowState.tick × 1,000,000`; retain `GetLastDataAvailableTime() × 1000` separately as receipt time | Public unit semantics / delivered behavior unverified | `tick` increments every 1 ms, but epoch, reset and wrap are unknown. Subscriber time is host-uptime receipt time, not device capture time; never merge the two clock domains silently. |
| `timestamp_utc` | correlated edge UTC clock | Candidate | Verify NTP/PTP/source and reset behavior. |
| `mode`, `health` | same normalizer as Telemetry | Contract placeholder | `unknown`. |
| `battery_pct` | same verified BMS mapping as Telemetry | Contract placeholder | `null`. |
| `standing` | delivered `GetFsmId()==4` plus independent posture criteria | Contract placeholder | `null`; official ID 4 means locked-standing mode, but a mode response alone does not prove posture, balance, or successful transition. |
| `moving` | verified body/base velocity with threshold and time window | Contract placeholder | `null`; `motor_state[].dq` is joint velocity and must not be presented as body velocity. |
| `estopped` | verified physical safety-state signal | Contract placeholder | `null`. |
| `controlled_by_remote` | verified takeover/controller signal | Contract placeholder | `null`. |
| `errors` | sanitized current adapter/SDK errors | Candidate | Define active-versus-history semantics during interface freeze. |
| `capability_snapshot_version` | hash/version of accepted capability report | DESIGN | Use a reproducible report version after review; not firmware version. |

## CameraFrameMetadata `0.1 draft`

The R1 product-table row lists a binocular camera, but the pinned SDK R1 examples do
not contain a camera example. The live R1 developer guide states that the current
software version does not support GST video-stream transport; it does not name the
software version. It separately identifies WebRTC as the main App path for video, so
WebRTC is now the preferred candidate transport rather than GST. No raw camera stream
or delivered device was inspected.

| Contract field | Candidate mapping | Current value/status |
|---|---|---|
| `schema_version`, `contract_status` | constants `0.1`, `draft` | DESIGN |
| `robot_id` | deployment config | DESIGN |
| `sensor_id` | sanitized adapter sensor registry ID | UNVERIFIED; never expose device serial. |
| `captured_at` | device timestamp correlated to UTC, otherwise receipt UTC | UNVERIFIED; semantics must be declared. |
| `sequence` | source counter, otherwise adapter counter scoped to stream session | UNVERIFIED; reset/wrap behavior required. |
| `timestamp_source` | selected only after clock investigation | `unknown` |
| `content_type` | derived from verified stream/container negotiation | UNVERIFIED; contract requires a value. Mock-only until verified. |
| `encoding` | verified camera pixel/codec encoding | `null` |
| `width_px`, `height_px` | verified stream configuration | `null`, `null` |
| `calibration_version` | immutable calibration artifact version | `null` |
| `verification_status` | commissioning outcome | `unverified` |
| `transport` | MediaResolver-issued opaque WebRTC reference | DESIGN/CANDIDATE; official architecture names WebRTC, while GST is unavailable on the current unversioned software. Keep the Mock resolver until delivered WebRTC negotiation is verified. |

Potential raw facts absent from the current contract: exposure, frame rate, pixel
format versus compression codec, intrinsics, distortion model, optical frame,
extrinsics, stream-session ID, clock uncertainty, and dropped-frame count. Record
them during commissioning and raise interface changes rather than overloading fields.

## AudioChunkMetadata `0.1 draft`

The public audio example distinguishes ASR text results, microphone PCM transport,
and playback services. Its code uses `int16_t` PCM storage, 16000 Hz, one channel,
and a receive buffer sized for 160 ms. These example constants do not verify the
delivered microphone settings. The official architecture also names audio as part of
the App WebRTC data path, making WebRTC a transport candidate without establishing
direction, encoding, channels, timing, or developer access.

| Contract field | Candidate mapping | Current value/status |
|---|---|---|
| `schema_version`, `contract_status` | constants `0.1`, `draft` | DESIGN |
| `robot_id` | deployment config | DESIGN |
| `sensor_id` | sanitized adapter microphone-stream ID | UNVERIFIED |
| `captured_at` | first-sample device time correlated to UTC, else receipt UTC | UNVERIFIED |
| `sequence` | stream chunk counter | UNVERIFIED; define session/reset/wrap. |
| `timestamp_source` | device/UTC/correlated choice after timing test | `unknown` |
| `content_type` | verified MIME type for resolver payload | UNVERIFIED; Mock-only until verified. |
| `encoding` | example stores signed 16-bit PCM; byte order and delivered representation unknown | `null`; public-example candidate only. |
| `sample_rate_hz` | public example constant `16000` | `null`; verify delivered datagrams before emitting 16000. |
| `channels` | public example writes one-channel WAV | `null`; neither the example nor a four-mic product claim proves the delivered PCM channel layout. |
| `chunk_duration_ms` | example receive buffer is sized for `160` ms at its assumed format | `null`; actual datagram length/timing must be measured. |
| `verification_status` | commissioning outcome | `unverified` |
| `transport` | AudioResolver-issued opaque WebRTC reference | DESIGN/CANDIDATE; official App architecture names WebRTC, but delivered developer access is unverified. No raw audio or Base64 in JSON. |

Potential raw facts absent from the current contract: sample width, endianness,
interleaving, channel order/geometry, gain, AEC/AGC/noise suppression, chunk byte
length, dropped samples, stream-session ID, and timestamp uncertainty.

## Timestamp and coordinate-frame verification plan

1. Record every device timestamp field, unit, epoch, clock domain, wrap width, and
   reset behavior from a read-only capture.
2. Pair device time with host monotonic and UTC receipt times; measure drift and
   latency distribution without claiming capture-time UTC prematurely.
3. Record every frame name and transform with axes, handedness, origin, units,
   parent, calibration version, and validity interval.
4. Treat missing time/frame data as `unknown`/`null`; do not silently substitute a
   host timestamp or assume ROS conventions.

## Pinned public raw-field inventory

The following symbols are **verified in source only**, not on the delivered robot:

- `rt/lowstate` candidate `unitree_hg::msg::dds_::LowState_`: `version[2]`,
  `mode_pr`, `mode_machine`, millisecond `tick`, `imu_state`, `motor_state[35]`,
  `wireless_remote[40]`, `reserve[4]`, `crc`. The guide defines `mode_pr` as
  `0=PR`, `1=AB`, and `mode_machine` as `4=23-DoF`, `5=29-DoF`,
  `6=27-DoF (29-DoF with waist locked)`.
- `IMUState_`: quaternion order is `Qw,Qx,Qy,Qz`; other fields are
  `gyroscope[3]`, `accelerometer[3]`, `rpy[3]`, and `temperature`. The supplied
  excerpt does not state angular-rate, acceleration, RPY, or temperature units,
  coordinate frame, handedness, or axes convention.
- `MotorState_`: `q` is rad, `dq` is rad/s, and `ddq` is rad/s^2. Other fields are
  `mode`, `tau_est`, two temperatures (surface and winding), `vol`, sensor words,
  motor state, and reserve. Torque/temperature/voltage units, active slot count,
  joint ordering, and state-bit semantics remain unverified.
- R1 LocoClient read methods: `GetFsmId` and `GetFsmMode`. The live guide defines
  FSM IDs `0=zero torque`, `1=damping`, `4=locked standing`, and `811=walk/run
  controller`; `GetFsmMode` numeric semantics and delivered behavior remain
  unverified. The high-level service depends on the built-in controller and is
  unavailable when debug mode has made that controller exit.
- R1 BMS candidate: `rt/lf/bmsstate` with `BmsState_` fields `version_high`,
  `version_low`, `fn`, `cell_vol[40]`, `bmsvoltage[3]`, `current`, `soc`, `soh`,
  `temperature[12]`, `cycle`, `manufacturer_date`, `bmsstate[5]`, and reserve.
  Field names are source-verified; units/scales remain unverified.
- Mainboard candidate: `rt/lf/mainboardstate` with fan, temperature, value, and state
  arrays. Array-index semantics remain absent.

## Read-only probe rules

1. Prefer low-frequency topics initially: `rt/lf/lowstate`, `rt/lf/bmsstate`,
   `rt/lf/mainboardstate`, `rt/lf/secondary_imu`, and, if approved,
   `rt/lf/odommodestate`.
2. Use `ChannelSubscriber`/`CreateRecvChannel` only, with a short callback and queue
   length `1`. The live page's `CreateSendChannel` subscriber note conflicts with the
   pinned source and must not be implemented.
3. Record `GetLastDataAvailableTime()` after each received sample. Treat `-1` as
   uninitialized; convert microseconds to nanoseconds only after validating the value.
   Also record raw `LowState.tick`; test monotonicity, reboot reset and wrap before
   using `tick × 1,000,000` as device monotonic nanoseconds. A 32-bit millisecond
   counter would wrap after about 49.7 days, which must be verified on the wire.
4. After client `Init()`, record `GetApiVersion()` and `GetServerApiVersion()`.
   A mismatch is evidence to stop and review, not permission to call setters.
5. For `RobotStateClient`, allow only `ServiceList`, `LowPowerStatus`, and
   `GetPkgVersion`. Preserve `ServiceState.name/status/protect` and package/module
   versions as inventory evidence; do not infer motion, navigation, audio, health,
   armed, E-Stop, or firmware state from them.
6. Never call `ServiceSwitch`, `SetReportFreq`, or `LowPowerSwitch`. Do not run the
   Go2 robot-state example because it changes report frequency and service state.
7. Do not call `WaitLeaseApplied()` in this read-only task and never create publishers
   for `rt/lowcmd` or dexterous-hand command topics.
8. Do not persist `wireless_remote[40]` during the initial probe. It is raw controller
   input and is unnecessary for the contract baseline; record only that the field is
   present unless a separate safety/privacy review approves its capture.
9. For `LocoClient`, call only `GetFsmId` and optionally raw `GetFsmMode`. Never call
   `Damp`, `Start`, `StandUp`, `ZeroTorque`, `Move`, `StopMove`, `SetFsmId`, or
   `SetVelocity` during read-only commissioning. `StopMove` only sends zero velocity;
   it is not a physical E-Stop or verified safe-stop mechanism.

## Commissioning capture template

For each candidate mapping, preserve: delivered SKU, firmware, SDK commit, sanitized
interface/topic/API name, raw field name and type, unit, rate, sample value redacted
as needed, verification command, UTC date, operator/reviewer, and result. A symbol
inventory alone can move an item only to “candidate,” never to “supported.”
