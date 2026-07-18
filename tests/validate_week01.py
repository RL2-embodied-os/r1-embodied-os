#!/usr/bin/env python3
"""Validate the Week 01 capability report and evidence-policy invariants."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
    from jsonschema import FormatChecker
except ModuleNotFoundError:  # Keep the evidence pack runnable with the stdlib only.
    jsonschema = None
    FormatChecker = None


REQUIRED_NOTE_MARKERS = ("version:", "checked 2026-07-18", "by ")
PUBLIC_ONLY_HOSTS = ("unitree.com", "github.com/unitreerobotics")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def resolve_ref(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported external reference: {reference}")
    node: Any = root
    for part in reference[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def type_matches(value: Any, expected: str) -> bool:
    checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return checks[expected](value)


def validate_subset(value: Any, spec: dict[str, Any], root: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON Schema keywords used by capability.schema.json."""
    if "$ref" in spec:
        return validate_subset(value, resolve_ref(root, spec["$ref"]), root, path)

    errors: list[str] = []
    expected = spec.get("type")
    if expected is not None:
        expected_types = expected if isinstance(expected, list) else [expected]
        if not any(type_matches(value, kind) for kind in expected_types):
            return [f"{path}: expected type {expected_types}, got {type(value).__name__}"]
    if "const" in spec and value != spec["const"]:
        errors.append(f"{path}: expected constant {spec['const']!r}")
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{path}: {value!r} is not in {spec['enum']!r}")

    if isinstance(value, dict):
        required = spec.get("required", [])
        errors.extend(f"{path}: missing required property {name!r}" for name in required if name not in value)
        properties = spec.get("properties", {})
        if spec.get("additionalProperties") is False:
            errors.extend(f"{path}: unexpected property {name!r}" for name in value if name not in properties)
        for name, item in value.items():
            if name in properties:
                errors.extend(validate_subset(item, properties[name], root, f"{path}.{name}"))
    elif isinstance(value, list):
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        if len(value) > spec.get("maxItems", sys.maxsize):
            errors.append(f"{path}: more than maxItems")
        if "items" in spec:
            for index, item in enumerate(value):
                errors.extend(validate_subset(item, spec["items"], root, f"{path}[{index}]"))
    elif isinstance(value, str):
        if len(value) < spec.get("minLength", 0):
            errors.append(f"{path}: shorter than minLength")
        if len(value) > spec.get("maxLength", sys.maxsize):
            errors.append(f"{path}: longer than maxLength")
        if "pattern" in spec and re.search(spec["pattern"], value) is None:
            errors.append(f"{path}: does not match pattern {spec['pattern']!r}")
        if spec.get("format") == "date-time":
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    raise ValueError("timezone required")
            except ValueError:
                errors.append(f"{path}: invalid RFC 3339 date-time")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in spec and value < spec["minimum"]:
            errors.append(f"{path}: below minimum")
        if "maximum" in spec and value > spec["maximum"]:
            errors.append(f"{path}: above maximum")

    for condition in spec.get("allOf", []):
        if "if" in condition:
            if not validate_subset(value, condition["if"], root, path):
                errors.extend(validate_subset(value, condition.get("then", {}), root, path))
        else:
            errors.extend(validate_subset(value, condition, root, path))
    return errors


def main() -> None:
    args = parse_args()
    schema = load_json(args.schema)
    report = load_json(args.report)
    if jsonschema is not None:
        try:
            jsonschema.validate(report, schema, format_checker=FormatChecker())
        except jsonschema.ValidationError as exc:
            fail(f"schema validation: {exc.message}")
    else:
        errors = validate_subset(report, schema, schema)
        if errors:
            fail(f"schema validation: {errors[0]}")

    capabilities = report["capabilities"]
    for name, entry in capabilities.items():
        notes = entry["notes"].lower()
        missing = [marker for marker in REQUIRED_NOTE_MARKERS if marker not in notes]
        if missing:
            fail(f"{name}: notes missing evidence metadata {missing}")
        if entry["status"] == "supported":
            evidence = [item.lower() for item in entry["evidence"]]
            public_only = evidence and all(
                any(host in item for host in PUBLIC_ONLY_HOSTS) for item in evidence
            )
            if public_only:
                fail(f"{name}: supported is based only on public product/SDK evidence")
            if "delivered" not in notes or "commission" not in notes:
                fail(f"{name}: supported lacks delivered commissioning evidence")
        if entry["status"] == "unverified" and entry["verified_at"] is not None:
            fail(f"{name}: unverified entry must keep verified_at null")

    for item in iter_strings(report):
        if item.startswith(("http://", "https://")):
            continue
        if re.search(r"[A-Za-z]:\\Users\\|/home/|/Users/", item):
            fail("report contains a local absolute path")

    print("PASS: capability report conforms to schema and Week 01 evidence rules")
    print(f"PASS: {len(capabilities)}/{len(capabilities)} capability entries include version/date/method notes")
    print("PASS: no supported capability is based only on public product or SDK evidence")


if __name__ == "__main__":
    main()
