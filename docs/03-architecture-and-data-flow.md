# Architecture and Data Flow

## Layers

| Layer | Responsibility |
| --- | --- |
| Cloud / OpenClaw | **DESIGN** - perception, language processing, task reasoning. Generates Python code that calls the Adapter's methods directly. |
| Agent Server | **DESIGN** - lease management, code validation (`CodeValidator`), code execution (`/code/execute`), state polling. Reused from ABot-Claw. |
| Adapter (`R1RobotAdapter`) | **DESIGN** - stable Python API (`stand()`, `move_velocity()`, `read_cameras()`, etc.) over version-specific robot SDKs. The only typed execution seam. |
| Robot | **DESIGN** - vendor control (SDK2/DDS), physical state, and the physical safety chain. |

## Control flow

Following ABot-Claw's `/code/execute + env.xxx()` pattern:

```text
OpenClaw / LLM
  -> reads SDK docs (Adapter methods + Week 1 data contracts)
  -> generates Python code: env.stand(); env.move_velocity(0.15, 0, 0, 800)
  -> POST /code/execute  (with lease)
  -> CodeValidator (AST-level safety: no shell, no network, no file deletion)
  -> subprocess executes
  -> R1RobotAdapter calls SDK2 / DDS
  -> hardware executes
  -> Critic monitors progress, replans on failure

Safety: lease TTL + CodeValidator + Critic feedback + SDK2 internal safety.
No intermediate JSON command translation layer.
```

## Week 1 contracts role

The contracts (Telemetry, RobotState, CapabilityReport, CameraFrameMetadata,
AudioChunkMetadata) serve as the **data-definition side of R1's SDK docs**.
The LLM reads them alongside the Adapter's Python method signatures to know
what `env.get_state()` returns and what `env.read_cameras()` produces.
