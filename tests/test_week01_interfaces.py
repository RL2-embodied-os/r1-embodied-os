"""Acceptance tests for the shared Week 1 interface surface."""

import ast
from pathlib import Path
from typing import get_type_hints

from interfaces.week01_interfaces import (
    ASRBackend,
    AudioResolver,
    DetectorBackend,
    MediaResolver,
    TelemetryNormalizer,
)
from interfaces.week01_models import (
    ASRBackendStatus,
    ASRResult,
    AudioHandle,
    AudioResolution,
    Detection2D,
    DetectionFrameResult,
    ImageHandle,
    ImageResolution,
    RawASRResult,
)
from week01_contracts import activate_contract_imports, require_contract_baseline


def test_week01_models_expose_required_contract_fields() -> None:
    assert {
        "schema_version",
        "source_frame",
        "detector",
        "image_width",
        "image_height",
        "processed_at",
        "detections",
    } == set(get_type_hints(DetectionFrameResult))
    assert {
        "detection_id",
        "class_id",
        "class_name",
        "confidence",
        "bbox_xyxy",
        "observed_at",
    } == set(get_type_hints(Detection2D))
    assert {
        "schema_version",
        "result_id",
        "source_audio",
        "recognizer",
        "status",
        "text",
        "language",
        "confidence",
        "processed_at",
        "error",
    } == set(get_type_hints(ASRResult))


def test_chain_protocols_are_shared_public_seams() -> None:
    for protocol in (
        TelemetryNormalizer,
        MediaResolver,
        DetectorBackend,
        AudioResolver,
        ASRBackend,
    ):
        assert getattr(protocol, "_is_protocol", False)


def test_runtime_contract_bootstrap_resolves_the_shared_baseline() -> None:
    assert activate_contract_imports() == require_contract_baseline()


def test_protocol_methods_have_complete_type_hints() -> None:
    methods = (
        TelemetryNormalizer.normalize,
        MediaResolver.resolve,
        DetectorBackend.detect,
        AudioResolver.resolve,
        ASRBackend.transcribe,
    )
    for method in methods:
        hints = get_type_hints(method)
        assert "return" in hints
        assert len(hints) >= 2


def test_visual_and_audio_protocols_preserve_media_kind() -> None:
    assert get_type_hints(MediaResolver.resolve)["return"] == ImageResolution
    assert get_type_hints(DetectorBackend.detect)["media"] == ImageHandle
    assert get_type_hints(AudioResolver.resolve)["return"] == AudioResolution
    assert get_type_hints(ASRBackend.transcribe)["audio_handle"] == AudioHandle
    assert get_type_hints(RawASRResult)["status"] == ASRBackendStatus


def test_week01_interfaces_have_no_forbidden_runtime_dependencies() -> None:
    interface_dir = Path(__file__).resolve().parents[1] / "interfaces"
    forbidden_imports = {
        "cyclonedds",
        "requests",
        "rospy",
        "socket",
        "subprocess",
        "threading",
        "unitree_sdk2py",
    }

    for path in (
        interface_dir / "week01_models.py",
        interface_dir / "week01_interfaces.py",
    ):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        assert imported_roots.isdisjoint(forbidden_imports)
