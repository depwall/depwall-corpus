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

Added from the public corpus (DataDog/malicious-software-packages-dataset;
measurement recorded in the engine repo's corpus-eval report):

- `exfil-hidden-spawn-setup-py/` — hidden + base64-encoded interpreter spawn,
  no URL/secret/network anywhere in the source (esquelesquad wave, 2023)
  → critical → BLOCK
- `exfil-identity-recon-setup-py/` — login/host/cwd recon base64'd into a GET
  query; reads no env var at all (`pytabtrust`, 2023) → critical → BLOCK
- `benign-cmdclass-subprocess-setup-py/` — cmake build via a `build_ext`
  cmdclass override; spawns subprocesses with nothing concealed → NO finding
  (FP guard: concealment is the signal, not `subprocess`)
- `benign-platform-wheel-setup-py/` — inspects the platform, then downloads the
  matching prebuilt binary → NO finding (FP guard: platform lookups select an
  ARTIFACT, identity lookups identify a VICTIM)
- `gap-deferred-cmdclass-setup-py/` — install-command override that imports and
  calls a project module (`DeepSolid`, `HLLM`) → no finding, asserted clean

**Known gap: deferred install hook.** A `setup.py` whose `cmdclass` install
override imports a module from its own package and calls it moves the payload
one file away from the scanner, exactly as npm's `preinstall: node index.js`
does. Nothing in the `setup.py` is hostile, and legitimate packages run
post-install steps the same way, so no pattern here can separate them; closing
it means following the import. Pinned by `gap-deferred-cmdclass-setup-py/`.

Two rules were added, both AND-gated so neither fires alone:
concealed spawn (spawn + encoded command, or spawn + hidden-console flag + an
interpreter), and network + IDENTITY recon (login name / host name / nodename /
`getpwuid`). `os.getcwd()` and `expanduser("~")` are deliberately excluded from
the identity set, and `platform.system()/machine()`/`sys.platform` from both:
they are ubiquitous in real packaging.

Limitation of a text scanner: patterns match COMMENTS as well as code. A benign
`setup.py` that quotes `os.getlogin()` in a comment and also downloads something
would be flagged. `benign-platform-wheel-setup-py/` is written to avoid naming
those calls even in prose for exactly this reason.

Rule tightened: network + env combo now requires whole-environment HARVEST
(dict(os.environ), os.environ.items()/.copy(), json.dumps of os.environ) or a
SECRET-NAMED read (KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL) — not any env read.
An ordinary var like CFLAGS or OUT_DIR alongside a download stays clean.

Known gaps (documented, deliberate): PEP 517 backend hooks outside setup.py;
obfuscation beyond these patterns is the judge's job (it sees the full body);
deterministically-ALLOW packages (mature+popular) are never tarball-scanned.
