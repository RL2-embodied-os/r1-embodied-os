# Week 1 — Perception Adapter Notes

Workstream: visual perception (Mock main line).
Chain: CameraFrameMetadata → MediaResolver → FakeDetector → DetectionFrameResult.
Code: `implementations/perception/` · Tests: `tests/perception/` · Branch: `DaniilPerception`.

## 1. What was implemented

- **VERIFIED** - `MockMediaResolver`: maps frame identity `(robot_id, sensor_id,
  sequence)` to an opaque fixture handle via an injected table; unknown frames
  return `media_unavailable`. No I/O, Base64, or file reads; metadata objects
  are never mutated or extended.
- **VERIFIED** - `FakeDetector`: implements `DetectorBackend`; consumes only
  `ImageHandle` + `DetectionContext` (never CameraFrameMetadata). Deterministic:
  detection ids derive from fixture id + index. Semantic self-checks reject
  invalid boxes (`invalid_bbox`, `image_size_mismatch`); unknown fixtures return
  `detector_unavailable` rather than a fabricated empty success.
- **VERIFIED** - `PerceptionPipeline`: enforces ordering — returns
  `media_unavailable` without invoking the detector (asserted by a
  counting-proxy test); returns `image_size_unavailable` when `width_px` /
  `height_px` are null; builds `DetectionContext` with an injected clock
  (no wall-clock reads).
- **VERIFIED** - Output conforms to `detection-frame-result.schema.json`
  (Draft 2020-12, FormatChecker) and passes the shared semantic validator.
  Full suite: 21 passed; perception scenarios: see `tests/perception/README.md`.

## 2. Fake ↔ YOLO switching seam

- **DESIGN** - Both backends implement the same async `DetectorBackend`
  Protocol: `detect(ImageHandle, DetectionContext) → DetectionBackendResult`.
  The handle is opaque (kind, fixture id, source triple — no path, URL, or
  bytes), so backends cannot bypass the resolver. A future `YoloV5Adapter`
  would resolve the handle to image bytes, call the YOLO HTTP service, map
  `x1, y1, x2, y2, confidence, class_id, class_name` onto `Detection2D`
  (`bbox_xyxy`), and wrap service errors into the shared error codes. No
  change is required in the resolver, pipeline, tests, or consumers. See the
  seam diagram in `docs/week01/detection2d_contract.md`.

## 3. Reference reading: existing YOLO service and SDK (read-only repo)

- **VERIFIED** - YOLO service (`service_layer/YOLO/SERVICE_AGENT.md`): HTTP
  single-image detection; request carries a base64 image plus optional
  `conf_thres` / `iou_thres`; response is a flat `detections` array
  (`x1..y2`, `confidence`, `class_id`, `class_name`) with no frame identity,
  image dimensions, or timestamps — those fields are the adapter's
  responsibility, which motivates `DetectionContext`.
- **VERIFIED** - `robot_sdk/yolo_sdk.py` couples ROS 1 (`rospy`, `tf2_ros`,
  `cv_bridge`), OpenCV, `requests`, threading, live camera topics, and 3D
  projection in one class; construction blocks waiting for a real camera
  frame. Per the task rules it was read only for field vocabulary and
  post-processing shape, and is not imported or executed anywhere.
- **VERIFIED** - Documented port discrepancy: the service manual states one
  default port while the SDK falls back to another; the deployed endpoint is
  supplied via the SDK's configuration file, which takes precedence over both
  defaults.
- **DESIGN** - Dependencies a real YOLO adapter would introduce (HTTP client,
  service availability, image byte access) are exactly what the Mock line
  excludes this week; none were added to `requirements-dev.txt`.

## 4. Open items

- **OPEN** - Transport-expiry checking is currently owned by the shared
  semantic validators (`camera_expired_transport`); the resolver does not
  duplicate it. Confirm ownership at the Day 3 interface freeze.
- **OPEN** - Async tests use `asyncio.run(...)` to keep dev dependencies
  unchanged; confirm whether a repo-wide pytest-asyncio convention is wanted.
- **OPEN** - Real CameraFrameMetadata handoff scenarios (one valid, one
  `media_unavailable`) are integrated from the telemetry workstream in
  Day 4–6; current test metadata mirrors `examples/`.
- **OPEN** - Camera remains `unverified` in the R1 capability matrix; no
  camera or YOLO availability is claimed. The YOLO adapter stays an optional,
  strictly timeboxed Day 4–6 bonus.
