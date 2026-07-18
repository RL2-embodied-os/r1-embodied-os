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

| Contract field | Proposed source | Classification | Rule before commissioning |
|---|---|---|---|
| `schema_version` | constant `1.0` | DESIGN | Populate exactly. |
| `robot_id` | deployment configuration | DESIGN | Use a non-secret logical ID; never copy serial number automatically. |
| `timestamp_utc` | adapter host clock correlated to receipt time | Candidate | Public `LowState.tick` exists, but its unit/epoch is not documented here; do not label host receipt time as device capture time. |
| `health` | normalizer over connection, diagnostics, safety state | Contract placeholder | Emit `unknown` until all inputs and precedence are defined. |
| `mode` | candidate `LocoClient.GetFsmId` / `GetFsmMode` result | Candidate from SDK source | Emit `unknown` until delivered values and the contract mapping table are verified; do not infer from the last command. |
| `battery_pct` | no field in inspected R1 `LowState_`; generic HG `AgvBmsState_` symbol is not an R1 publication guarantee | Contract placeholder | `null`; do not map a generic symbol or convert motor voltage without a verified R1 topic and battery model. |
| `network.rtt_ms` | adapter-to-robot measurement | Candidate | `null` until endpoint and method are approved. |
| `network.packet_loss_ratio` | transport counters over a defined window | Candidate | `null`; document window and denominator. |
| `network.uplink_mbps` | edge transport measurement | Candidate | `null`; this is not an SDK sensor field. |
| `safety.armed` | verified local safety-supervisor signal | Contract placeholder | `null`; locomotion mode is not automatically equivalent. |
| `safety.estopped` | vendor/lab-confirmed physical safety-state signal | Contract placeholder | `null`; never infer from a software stop call. |
| `safety.remote_override` | verified remote-takeover signal | Contract placeholder | `null`. |
| `safety.active_lease_id` | future shared Edge Gateway | DESIGN / later phase | `null` in Week 01; not an R1 SDK field. |
| `errors` | adapter validation/read failures and LocoClient/RPC return codes | Candidate | Preserve sanitized codes/messages without credentials, addresses, or personal data. |

## RobotState `1.0`

| Contract field | Proposed source | Classification | Rule before commissioning |
|---|---|---|---|
| `schema_version`, `robot_id` | constant and deployment config | DESIGN | Same identity rule as Telemetry. |
| `timestamp_mono_ns` | edge process monotonic clock at snapshot; future correlation candidate is `LowState.tick` | Candidate | Record host receipt/snapshot semantics until tick unit, wrap, reset, and clock domain are verified. |
| `timestamp_utc` | correlated edge UTC clock | Candidate | Verify NTP/PTP/source and reset behavior. |
| `mode`, `health` | same normalizer as Telemetry | Contract placeholder | `unknown`. |
| `battery_pct` | same verified BMS mapping as Telemetry | Contract placeholder | `null`. |
| `standing` | candidate verified FSM mapping plus posture criteria | Contract placeholder | `null`; `GetFsmId`/`GetFsmMode` numbers have no accepted delivered mapping yet. |
| `moving` | verified body/base velocity with threshold and time window | Contract placeholder | `null`; `motor_state[].dq` is joint velocity and must not be presented as body velocity. |
| `estopped` | verified physical safety-state signal | Contract placeholder | `null`. |
| `controlled_by_remote` | verified takeover/controller signal | Contract placeholder | `null`. |
| `errors` | sanitized current adapter/SDK errors | Candidate | Define active-versus-history semantics during interface freeze. |
| `capability_snapshot_version` | hash/version of accepted capability report | DESIGN | Use a reproducible report version after review; not firmware version. |

## CameraFrameMetadata `0.1 draft`

The R1 product-table row lists a binocular camera, but the pinned SDK R1 examples do
not contain a camera example. No raw camera stream or delivered device was inspected.

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
| `transport` | MediaResolver-issued opaque reference | DESIGN; not an SDK raw field and never a URL/media byte payload. |

Potential raw facts absent from the current contract: exposure, frame rate, pixel
format versus compression codec, intrinsics, distortion model, optical frame,
extrinsics, stream-session ID, clock uncertainty, and dropped-frame count. Record
them during commissioning and raise interface changes rather than overloading fields.

## AudioChunkMetadata `0.1 draft`

The public audio example distinguishes ASR text results, microphone PCM transport,
and playback services. Its code uses `int16_t` PCM storage, 16000 Hz, one channel,
and a receive buffer sized for 160 ms. These example constants do not verify the
delivered microphone settings.

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
| `transport` | AudioResolver-issued opaque reference | DESIGN; no raw audio or Base64 in JSON. |

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
  `mode_pr`, `mode_machine`, `tick`, `imu_state`, `motor_state[35]`,
  `wireless_remote[40]`, `reserve[4]`, `crc`.
- `IMUState_`: `quaternion[4]`, `gyroscope[3]`, `accelerometer[3]`, `rpy[3]`,
  `temperature`. Units and coordinate frame are not stated by the generated header.
- `MotorState_`: `mode`, `q`, `dq`, `ddq`, `tau_est`, temperatures, `vol`, sensor
  words, motor state, and reserve. Units, active joint count, and joint ordering for
  the delivered R1 remain unverified.
- R1 LocoClient read methods: `GetFsmId` and `GetFsmMode`. Numeric semantics on the
  delivered firmware remain unverified.

## Commissioning capture template

For each candidate mapping, preserve: delivered SKU, firmware, SDK commit, sanitized
interface/topic/API name, raw field name and type, unit, rate, sample value redacted
as needed, verification command, UTC date, operator/reviewer, and result. A symbol
inventory alone can move an item only to “candidate,” never to “supported.”
