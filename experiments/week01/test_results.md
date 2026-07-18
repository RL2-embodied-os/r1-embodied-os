# Week 01 validation results

**Run date:** 2026-07-18
**Scope:** capability report schema and evidence-policy checks

## Command

```bash
python3 tests/validate_week01.py \
  --schema ../r1-summer-research-starter-pack/contracts/capability.schema.json \
  --report experiments/week01/r1_capability_report.json
```

## Expected output

```text
PASS: capability report conforms to schema and Week 01 evidence rules
PASS: 11/11 capability entries include version/date/method notes
PASS: no supported capability is based only on public product or SDK evidence
```

## Result

Executed successfully with an isolated Python 3 runtime against the unchanged
starter-pack `capability.schema.json`:

```text
PASS: capability report conforms to schema and Week 01 evidence rules
PASS: 11/11 capability entries include version/date/method notes
PASS: no supported capability is based only on public product or SDK evidence
```

The validator used its standard-library schema subset because the isolated runtime
did not include the optional `jsonschema` package. The subset implements every JSON
Schema keyword used by this capability schema, including local `$ref`, conditional
`if`/`then`, required and additional properties, types, enums, constants, bounds,
patterns, array limits, and RFC 3339 date-time checks.
