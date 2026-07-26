# Build-script exfil / injection fixtures

Attack: malicious code in the install-time build script — `setup.py` inside a
PyPI sdist (runs on `pip install` of an sdist), `build.rs` inside a crate
(runs on first `cargo build`). npm's analog (lifecycle install scripts) has
been covered since Slice 1; these close the same hole for pip/cargo.

All fixtures are INERT TEXT (hosts REDACTED, never executed/compiled) fed to
the pure `buildScriptFindings` signal and, in adapter tests, packed into
in-memory tar.gz bytes. See docs/TESTING-SAFETY.md.

- `exfil-setup-py/` — env-harvest + urlopen POST (crossenv/ctx shape) → critical → BLOCK
- `exfil-build-rs/` — registry-token read + TcpStream (build-time exfil crate shape) → critical → BLOCK
- `injection-setup-py/` — prompt-injection against the judge; no exfil pattern
  → NO deterministic finding; judge must treat it as data (must NOT launder to clean)
- `benign-setup-py/` — C-extension build (env CFLAGS + subprocess toolchain) → NO finding (FP guard)
- `benign-build-rs/` — cc-crate build.rs (Command/env OUT_DIR) → NO finding (FP guard)
- `benign-setup-py-network/` — downloads test data + reads CFLAGS (FP guard: network + ordinary env var must stay clean)
- `benign-build-rs-network/` — downloads a prebuilt artifact + reads OUT_DIR (FP guard: network + ordinary env var must stay clean)

Rule tightened: network + env combo now requires whole-environment HARVEST
(dict(os.environ), os.environ.items()/.copy(), json.dumps of os.environ) or a
SECRET-NAMED read (KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL) — not any env read.
An ordinary var like CFLAGS or OUT_DIR alongside a download stays clean.

Known gaps (documented, deliberate): PEP 517 backend hooks outside setup.py;
obfuscation beyond these patterns is the judge's job (it sees the full body);
deterministically-ALLOW packages (mature+popular) are never tarball-scanned.
