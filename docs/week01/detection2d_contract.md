# DetectionFrameResult and Detection2D Contract v0.1

## Contract status

- **DESIGN** — This is the internal Week 1 normalized 2D detection contract.
- **DESIGN** — It is independent of media transport and contains no image bytes, Base64, URLs, or local paths.
- **OPEN** — Camera availability, image dimensions, encoding, calibration, and a usable R1-to-YOLO path remain unverified.

The authoritative schema is `contracts/week01/detection-frame-result.schema.json`. The matching Python types are in `interfaces/week01_models.py`.

## Producer and consumer

| Object | Producer | Consumer |
| --- | --- | --- |
| `DetectionFrameResult` | **DESIGN** — A `DetectorBackend` adapter after successful media resolution | **DESIGN** — Contract QA and downstream perception/task components |
| `Detection2D` | **DESIGN** — A Fake detector or normalized YOLO backend | **DESIGN** — Consumers of the enclosing frame result |

`MediaResolver` consumes `CameraFrameMetadata`. `DetectorBackend` consumes only an opaque `ImageHandle` plus a `DetectionContext`; it must not consume metadata directly or resolve media itself.

## Fields and constraints

| Field | Constraint and meaning |
| --- | --- |
| `schema_version` | **DESIGN** — Constant `0.1`. |
| `source_frame` | **DESIGN** — Object containing `robot_id`, `sensor_id`, and `sequence`; it is media identity, not a ROS/TF coordinate frame. |
| `detector` | **DESIGN** — `fake` or `yolo_v5` for this version; it identifies implementation source, not verified R1 capability. |
| `image_width`, `image_height` | **DESIGN** — Positive pixel dimensions copied from validated processing context. Missing dimensions prevent result generation. |
| `processed_at` | **DESIGN** — RFC 3339 time at which normalized processing completed. |
| `detections` | **DESIGN** — Array of zero or more detections. An empty array means processing succeeded and found no targets. |
| `detection_id` | **DESIGN** — Identifier unique within the producing pipeline's result scope. |
| `class_id`, `class_name` | **DESIGN** — Backend class identifier and label after normalization. They do not assert a permanent ontology. |
| `confidence` | **DESIGN** — Number in `[0, 1]`. |
| `bbox_xyxy` | **DESIGN** — Pixel coordinates `[x1, y1, x2, y2]`; all values are non-negative. |
| `observed_at` | **DESIGN** — RFC 3339 observation time supplied by the processing context. |

## Schema and semantic validation

- **DESIGN** — JSON Schema validates required fields, types, confidence range, non-negative bbox values, timestamp format, and `additionalProperties: false`.
- **DESIGN** — Semantic validation separately enforces `x1 < x2`, `y1 < y2`, `x2 <= image_width`, and `y2 <= image_height`.
- **DESIGN** — A schema-valid document can therefore be `semantic_invalid`; validators must report both categories.

| Condition | Return behavior | Detection result |
| --- | --- | --- |
| Width or height is `null` | `image_size_unavailable` | Do not emit a result claiming verified boxes |
| `x1 >= x2` or `y1 >= y2` | `invalid_bbox` | Reject result |
| Box exceeds image dimensions | `image_size_mismatch` | Reject result |
| Resolver cannot provide a handle | `media_unavailable` | Do not call detector |
| Detector backend cannot run | `detector_unavailable` | Return pipeline error; do not fabricate an empty success |
| Detector succeeds with no targets | Success | Emit `detections: []` |

## Existing YOLO response mapping

The existing service is a legacy backend candidate. It is read for field mapping only; its Base64/URL/path request boundary is excluded from this contract.

| Existing YOLO field | v0.1 destination | Rule |
| --- | --- | --- |
| `detections[]` | `detections[]` | **DESIGN** — Normalize each entry after media resolution and inference. |
| `x1`, `y1`, `x2`, `y2` | `bbox_xyxy[0..3]` | **DESIGN** — Preserve pixel coordinate order, then run semantic checks. |
| `confidence` | `confidence` | **DESIGN** — Reject values outside `[0, 1]`. |
| `class_id` | `class_id` | **DESIGN** — Convert to a non-negative integer. |
| `class_name` | `class_name` | **DESIGN** — Preserve a non-empty normalized label. |
| `count` | Not carried | **DESIGN** — Derive with `len(detections)` to avoid contradictory fields. |
| Request `image` | Not carried | **DESIGN** — Replaced by `MediaResolver -> MediaHandle`; no Base64 crosses the new contract. |
| No legacy frame identity | `source_frame` | **DESIGN** — Supplied from validated CameraFrameMetadata identity. |
| No legacy timestamps | `observed_at`, `processed_at` | **DESIGN** — Supplied by the processing context and injected clock. |

## Fake/YOLO replacement seam

```text
CameraFrameMetadata -> MediaResolver -> ImageHandle
                                      -> FakeDetector  --+
                                      -> YoloV5Adapter --+-> DetectionFrameResult
```

- **DESIGN** — Fake detector is mandatory for Week 1 and must be deterministic for the same fixture.
- **DESIGN** — A YOLO adapter is optional and must not be imported by baseline tests.
- **OPEN** — Selecting the YOLO adapter for real R1 media requires verified sensor and transport evidence.
