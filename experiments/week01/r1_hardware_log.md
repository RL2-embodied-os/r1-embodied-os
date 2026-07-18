# R1 hardware and SDK investigation log

**Date:** 2026-07-17 to 2026-07-18
**Operator:** Codex-assisted local investigation
**Scope:** local environment and public read-only evidence only

## Safety declaration

No physical robot, robot network, SDK runtime, camera, microphone, speaker, motor,
or remote controller was accessed. No motion, playback, sound output, or actuation
example was run. Physical E-Stop, power-on, remote takeover, and approval procedures
remain unverified.

## Inputs present

- Contract baseline directory was available and read without modification.
- Target repository `RL2-embodied-os/r1-embodied-os`, branch `ChronoIvan`, was
  confirmed at base revision `afb7e750820622a90b03ec72f5d7c35899c3d693`.
- Reference repository `amap-cvlab/ABot-Claw`, branch `main`, was inspected at
  `39c9ffc94a84f2e6baac431a9bff9771111f8539`.
- The operator reported the delivered model/SKU as Unitree R1 on 2026-07-18. The
  unique device identifier was not copied into this public repository.
- No firmware record, delivered-SDK compatibility record, safety manual, lab
  approval, or permitted robot network interface was supplied.

## Local environment audit

```text
Host: Microsoft Windows NT 10.0.26200.0
Architecture: x64 process environment
Git: 2.55.0.windows.2
CMake: NOT_FOUND
gcc/g++/cl: NOT_FOUND
make/ninja: NOT_FOUND
Python on PATH: NOT_FOUND
WSL distribution: none installed
Docker: NOT_FOUND
```

The host does not satisfy the official Ubuntu/GCC/CMake/Make recipe. An isolated
Python runtime was used only for JSON validation.

## Attempt 1 — official SDK checkout with system Git

Command:

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2.git unitree_sdk2
git -C unitree_sdk2 checkout 21d0a3b
git -C unitree_sdk2 rev-parse HEAD
```

Full relevant error:

```text
Cloning into 'unitree_sdk2'...
fatal: unable to access 'https://github.com/unitreerobotics/unitree_sdk2.git/':
schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS (0x8009030e)
fatal: cannot change to 'unitree_sdk2': No such file or directory
```

Assessment: download failed before a source checkout existed. This is a local HTTPS
credential/TLS backend problem, not evidence of an SDK source or build defect.

## Attempt 2 — isolated Git runtime

Command: same clone URL using the isolated Git executable.

Full error:

```text
Cloning into 'unitree_sdk2'...
git: 'remote-https' is not a git command. See 'git --help'.
fatal: remote helper 'https' aborted session
```

Assessment: that runtime is intentionally incomplete for remote HTTPS operations.

## Attempt 3 — direct fixed-source retrieval

A read-only HTTPS request for the pinned header was attempted using an isolated
runtime.

Full relevant error:

```text
TypeError: fetch failed
ConnectTimeoutError: Connect Timeout Error
code: UND_ERR_CONNECT_TIMEOUT
```

Assessment: direct raw-source retrieval was unavailable from the local shell. Public
first-party pages remained inspectable through the approved documentation-search
path. No local source tree was synthesized from search snippets.

## Attempt 4 — approved official SDK checkout

Command:

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2.git unitree_sdk2
git -C unitree_sdk2 checkout 21d0a3b
git -C unitree_sdk2 rev-parse HEAD
```

Result:

```text
HEAD is now at 21d0a3b add r1_arm_sdk_dds_example
21d0a3b2c46ee48c8fdf2783becb6be3beb0a59b
```

Assessment: **PASS** for source acquisition and revision pinning. The prior failures
were environment/network-path failures, not repository failures.

## Build result

**BLOCKED — not run.** The exact SDK source tree is now available, but configure and
compile were not attempted because the host lacks Ubuntu, CMake, a C/C++ compiler,
and Make. The SDK's checked-in libraries target its published Linux environments;
substituting an unapproved Windows toolchain would not reproduce the first-party
recipe. Reporting a build pass would be false. The official installation and build
commands are recorded in `docs/week01/r1_sdk_baseline.md` for an approved Ubuntu host.

## Interface/header inventory result

The local pinned source confirms R1 high-level, low-level, upper-body, and audio
sources. `r1_loco_client.hpp` exposes read calls `GetFsmId` and `GetFsmMode`, while
the same client also contains setters and motion helpers. The R1 low-level example
names `rt/lowstate`; its `LowState_` type contains version/mode/tick, IMU, motor,
wireless, reserve, and CRC fields. The audio example contains 16 kHz, mono, signed
16-bit PCM example constants. None confirms delivered firmware support.

## Blockers and requests

| Blocker | Attempted | Need | Owner / deadline |
|---|---|---|---|
| Delivered robot facts partial | R1 SKU supplied by operator; baseline and first-party source reviewed | Firmware, joint layout, SDK entitlement/compatibility, and sanitized commissioning record | Lab owner before capability approval |
| Linux build toolchain absent | Audited PATH, WSL, and Docker | Approved Ubuntu 20.04 x86_64/aarch64 environment with GCC 9.4 and CMake 3.10+ | Build-environment owner before build rerun |
| Safety procedures absent | Reviewed project safety baseline | Written physical E-Stop, power-on, support, remote takeover, read-only test approval, and data-handling procedures | Lab safety owner before robot connection |

Resolved items: target/reference repository revisions, reported R1 SKU, and pinned
SDK source checkout. Remaining delivered robot facts are firmware, joint layout,
SDK compatibility/permissions, sensors, timestamps, coordinate frames, and safety
procedures.

## Next-step verification plan

1. Review and push these artifacts on target branch `ChronoIvan`; do not modify
   starter-pack examples or include the unique device identifier.
2. On an approved Ubuntu environment, reuse the verified SDK SHA, record dependency
   versions, configure output, build output, and all failures.
3. Before robot connection, lab owner signs the read-only binary/topic allowlist and
   demonstrates the physical E-Stop and remote takeover procedure.
4. Query only identity/version and approved read-only state; capture sanitized field
   names, types, units, rates, timestamp domains, and coordinate frames.
5. Update each capability individually. Use `supported` only with a delivered-system
   evidence record and RFC 3339 verification time; otherwise retain `unverified`.
6. Run the capability validator and preserve its output in `test_results.md`.

## Daily async update

```text
Done: confirmed target/reference repositories and R1 SKU; checked out pinned SDK;
      completed environment audit, source inventory, capability matrix, read-only
      mapping, hardware/failure log, capability JSON, and validator.
Next: rerun pinned SDK build and read-only commissioning after inputs and approval arrive.
Blocked: delivered firmware/joint layout, approved Linux toolchain, SDK compatibility,
         robot permissions, and lab safety procedures are unavailable.
Need: build owner supplies approved Ubuntu environment; lab owner supplies firmware,
      permission record, and written read-only/safety approval before testing.
```
