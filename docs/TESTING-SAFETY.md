# Testing Safety — Never Detonate Live Malware on a Real Machine

DepWall is a security tool. Validating it will, over time, mean handling **real
malicious packages** (live slopsquats, poisoned deps, exfiltration payloads). Doing
that wrong compromises the tester's machine — the exact outcome DepWall exists to
prevent.

## Hard rules

1. **Never install, execute, or `postinstall` a real suspect package on your own
   device.** No `npm install <suspect>`, no `brew install`, no running its scripts —
   not "just to see." Install/postinstall is code execution.
2. **Detonate only in a disposable sandbox** — a throwaway VM or container with:
   - no SSH keys, no `~/.aws`, no `.env`, no cloud creds, no password manager
   - no network access to internal systems (egress-restricted or offline)
   - snapshot-and-revert, treated as burned after each run
3. **DepWall's own tests are inert by design.** Signals and the judge operate on
   **fetched metadata and text** (registry JSON, README, declared script *bodies as
   strings*) — they never execute package code. The red-team fixtures
   (`tests/fixtures/red-team/`) are static JSON/text describing an attack, not runnable
   payloads. Keep it that way: a fixture is data, never an executable.
4. **If a test ever needs to actually run a package** (dynamic analysis), it goes in
   the sandbox, gated behind an explicit opt-in flag, and is never part of the default
   `npm test`.

## Why this matters for contributors and agents

An AI agent helping build DepWall must **not** install or run a suspect package on the
maintainer's machine to "verify" a detection. Verify against fetched metadata/fixtures.
If dynamic execution is genuinely required, stop and hand it to a sandboxed environment.
