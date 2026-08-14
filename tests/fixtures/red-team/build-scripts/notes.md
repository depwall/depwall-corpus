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
- `exfil-py-deferred-import/` — install-command override that imports and calls a
  project module (`DeepSolid`, `HLLM`); `setup.py` is asserted CLEAN on its own
  and the payload sits in `main.py`, reached by following the import one hop →
  critical → BLOCK
- `benign-py-deferred-import/` — identical shape with a real post-install helper
  behind it (reads build config, inspects the platform, spawns `compileall`) →
  NO finding (FP guard: deferring a post-install step to a module is ordinary
  packaging, not a tell)

**Closed: the deferred install hook.** A `setup.py` whose `cmdclass` install
override imports a module from its own package and calls it moved the payload
one file away from the scanner, exactly as npm's `preinstall: node index.js`
did. Nothing in the `setup.py` is hostile, and legitimate packages run
post-install steps the same way, so no pattern applied to it could separate
them — the fix was to read the module, not to widen a regex.

The sdist walk now resolves the modules its build scripts import — `import a.b`,
`import a, b`, `from a.b import c` — and reads them out of the same decompressed
archive: one hop, capped at 12 distinct modules. A dotted name resolves to a
PATH (`mypkg/installer.py`, plus the `__init__.py` a package directory would
use), which is why the sdist fetch moved from `basename` to `rootRelative`. An
sdist is rooted at one `<name>-<version>/` directory and setup.py runs with cwd
there, so a module names exactly one file; basename matching would have read
`vendor/main.py` in place of the `main.py` the install hook imports — the same
decoy the npm side already learned about.

There is deliberately NO stdlib denylist. `import os` resolves to candidates that
do not exist in the sdist, so the walker returns nothing for them, and a package
that really does ship its own `os.py` is one whose `os.py` should be read. A
denylist would be one more thing to drift. The cap is 12 rather than npm's 8 for
the same reason: a real setup.py spends its first few imports on setuptools and
stdlib before reaching anything interesting.

**What following the import broke, and the measurement that caught it.** The
Python gates tested co-occurrence anywhere in the body. That was sound while the
body was always a short single-purpose `setup.py` — and following the imports
destroyed the premise, because reading `__version__` out of a project module at
the top of setup.py is one of the most common patterns on PyPI (`dill`, `six`,
`lxml`, `grpcio-status`, `nodeenv`). The scanner now routinely gets a full
application file.

`nodeenv` — top-300 on PyPI, a pre-commit dependency — went to **BLOCK** on the
first version of this change. It calls `urlopen` because downloading a Node
tarball is its entire purpose, and calls `os.environ.copy()` ~40KB away to build
a child-process environment: two unrelated statements welded into an
"exfiltration" gate by file-scale matching. Precisely the `@scarf/scarf` lesson
that produced `JS_GATE_WINDOW`, restated in Python, and it was found by
measurement rather than by review — no fixture predicted it.

So the two-armed Python gates are proximity-bounded now (`PY_GATE_WINDOW`,
1200 — wider than the JS window because a setup.py is written with more vertical
space). `BODY_SEAM` takes the MAX of the two windows: it had been sized to the JS
window alone, and leaving it there would have silently re-opened cross-file
welding for sdists the moment pip started following imports. Pinned by
`benign-py-far-apart-module/`, whose padding between the two halves is
load-bearing — shrink it under the window and the fixture stops testing anything.

That fixture also re-taught an old lesson the hard way: its FIRST draft failed
because its own header comment named both calls 677 characters apart, and a text
scanner matches prose. `benign-platform-wheel-setup-py/` already avoids naming
what it does for exactly this reason.

*Measured, before and after.* Top 300 PyPI packages by download, real sdists,
each downloaded once and scanned both ways: 282 sdists, 123 with a `setup.py`,
the import hop engaged on **24** of them reading 33 module files (`setuptools`,
`six`, `lxml`, `pytz`, `versioneer`, `oauthlib`). Before the window: **1 flagged**
(`nodeenv`, a false positive). After: **0 flagged**, with the same 33 files still
read — the window removed the false positive without reducing coverage. 10 of 300
metadata fetches stayed unresolved and are counted rather than dropped.

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

## npm package entry points (2026-07-27)

Attack: the manifest's only tell is `preinstall: node index.js`. The registry
metadata is clean of exfil patterns because the payload lives in `index.js`
inside the tarball, which the npm path never opened. Measured cost of the gap:
391 of 400 npm samples in the public corpus topped out at ASK, while the
equivalent pip/cargo numbers moved, purely because those two read build-script
bodies and npm did not. Pinned end to end by the real-incident record
`tarball-body-preinstall-loader.json` (ASK on metadata, BLOCK once the body is
read).

- `exfil-npm-index-js/` — `JSON.stringify` of `process.env` + hostname/username
  POSTed over https → critical → BLOCK
- `exfil-npm-encoded-spawn/` — `spawn("powershell", ["-WindowStyle","Hidden",
  "-EncodedCommand", <b64>])`: no URL, no secret name, no network API visible.
  Concealment IS the signal → critical → BLOCK
- `benign-npm-index-js/` — the node-gyp rebuild every native addon runs.
  Spawns a child process and reads `npm_config_*` → must stay clean
- `benign-npm-network-index-js/` — platform-matched prebuilt download, the
  esbuild/sharp shape: network + env + `os.platform()/arch()` → must stay clean.
  Also carries the version-check + yarn-detection blocks that produced the
  `@depot/cli` false positive (below)
- `benign-npm-telemetry-index-js/` — reduced from `@scarf/scarf@1.4.0`: opt-out
  install telemetry that reads the username, its own `SCARF_API_TOKEN`, and
  makes an https request, as unrelated statements far apart → must stay clean
- `benign-npm-shell-hint-index-js/` — reduced from `@ottocode/install`: prints
  `curl … | sh` as a manual-install hint on its failure path → must stay clean
- `exfil-npm-required-helper/` — decoy entry point that requires a sibling and
  calls it; `index.js` is asserted CLEAN on its own and the payload sits in
  `lib/setup.js`, reached by following the require one hop → critical → BLOCK
- `benign-npm-required-helper/` — identical structure, with a real native-addon
  installer (platform-matched prebuilt download, plain `node-gyp` fallback) in
  the required file → NO finding (FP guard: deferring the install step to a
  module is ordinary packaging, not a tell)
- `exfil-npm-directory-main/` — the same decoy one level more indirect: the entry
  requires a DIRECTORY, there is no `lib/index.js`, and `lib/package.json` main
  redirects to the payload in `lib/run.js` → critical → BLOCK
- `benign-npm-directory-main/` — identical redirect with a legitimate installer
  behind it → NO finding (FP guard: a subdirectory carrying its own manifest is
  ordinary layout)

The AND-gate discipline is the Python side's, plus two npm-specific rules that
real packages forced. Spawning alone, network alone and identity recon alone are
all clean, because every native addon does the first two. `os.platform()` /
`os.arch()` answer WHAT-PLATFORM and stay out of the identity set, which is
`hostname()` / `userInfo()` / `networkInterfaces()` — WHO and WHERE.

**1. The halves of a gate must be NEAR each other (`JS_GATE_WINDOW`).** The
Python gates test co-occurrence anywhere in the body, which is sound for a short
single-purpose `setup.py`. An npm entry point is long and frequently a bundle,
so co-occurrence is close to vacuous: `@scarf/scarf`'s report.js reads
`os.userInfo()` on line 21, its token on 261 and calls `https.request` on 407 —
three unrelated statements that file-scale matching welds into two separate
"exfiltration" gates. Related to this, the network arm matches request CALL
SITES and not `require("https")`: imports sit at the top of a file next to
exactly the kind of setup code the other arms match, so the import alone
re-created the same false positive 123 characters away.

**2. A single secret-named env read is NOT harvest for npm** — unlike the
py/rs twins, which do count one. An npm installer reading its OWN namespaced
token to authenticate its OWN download is mainstream (`protolint` reads
`PROTOLINT_MIRROR_PASSWORD` beside its mirror `fetch`; `@scarf/scarf` signs its
telemetry with `SCARF_API_TOKEN`), and the read sits right next to the request
that consumes it, so proximity cannot separate it from exfiltration either.
Only whole-environment serialization counts. Accepted recall cost: a package
that reads exactly one secret and posts it elsewhere falls to the judge.

Shell-exfil patterns (`curl|sh`, `base64 -d`) are also treated differently
here. In a `setup.py`, shell text is shell about to run; in a JS file it is as
often a message — `@ottocode/install` prints the manual-install command from a
`console.error` on its failure path. For npm the command must sit inside a
spawn's argument list to count. Proximity alone was NOT enough: the recovery
hint is printed right next to the spawn that just failed.

Scope, deliberately narrow: the file a lifecycle script names with `node`, plus
`index.js`, capped at 4, and ONLY when the package declares a lifecycle script —
without one npm executes no package code at install time, so the entry point is
not install-time attack surface. Names are resolved the way node resolves them
(flags skipped, including value-taking ones like `-r`; extensionless targets get
`.js`) and matched as a path relative to the tarball's `package/` root, not as a
basename — npm runs the script with cwd at that root, so `node index.js` means
exactly one file. Following `main` still needs a reachability model the corpus
does not justify.

**Closed for a literal specifier: the required helper (one hop).** The residual
after the entry point started being read was that the payload moved one file
further out — `index.js` requires `./lib/setup.js` and calls it, and every
deterministic pattern stays silent on the file that was scanned, *correctly*,
because that is also how legitimate packages structure an install step. Widening
a regex could not fix that; reading the required file could. Read the
"What the hop does NOT close" list below before treating this as done — a
computed or aliased require still walks past it.

The scan now resolves the relative specifiers in the entry points it already
read — `require`, `import(...)`, `import "..."` and `from "..."` — and reads
what they name **out of the same decompressed tarball**, so there is no second
download. Resolution is node's: literal path when it carries a JS extension,
otherwise `.js`/`.cjs`/`.mjs`/`<dir>/index.js`, and always relative to the file
that required it rather than by basename (a basename match would re-open the
`dist/` decoy the rootRelative fix closed). Detection rules are UNCHANGED — they
are simply given the bytes that actually run.

Bounds, all of them because the entry point is attacker-controlled text: bare
specifiers ignored (a node_modules dependency is a different package, gated on
its own), specifiers that climb above the package root dropped entirely, **8**
distinct specifiers max per entry file, **require depth 1** — the helper's own
requires are not resolved. Two hops needs a cycle-safe reachability model, and
the corpus does not yet justify one. Pinned by `exfil-npm-required-helper/`
(caught) and `benign-npm-required-helper/` (the false-positive twin: identical
structure, real native-addon installer behind it, must stay clean).

**The directory redirect, and why there is a second round.** `require("./lib")`
is not necessarily `lib/index.js`. Node's LOAD_AS_DIRECTORY reads
`lib/package.json` and honours its `main` FIRST, so a package can ship
`lib/package.json` with `main: "./run.js"` and no `lib/index.js` at all: the
extension candidates reach nothing while `lib/run.js` is what executes at
install. Adversarial review found this, and it was reproduced under node 22
before anything was written — with both the manifest `main` and `lib/index.js`
present, `main` wins.

So the walker now takes an ARRAY of follow stages rather than a single callback.
Round one resolves requires and additionally asks for `<dir>/package.json`
whenever a specifier could name a directory; round two reads `main` out of those
manifests and resolves it. **The round count is a caller constant, never derived
from file contents** — that is what keeps "cannot cascade" true now that there is
more than one pass. Round two is manifest-only, so it cannot become a second
require hop, and it does not ask for further manifests, so there is no third
round.

`exports` is deliberately not consulted, and that is a measured decision rather
than an omission: node IGNORES `exports` for a relative directory require.
Verified — a `lib/package.json` carrying only `exports` fails to resolve at all,
and when both fields are present `main` is what runs. (The report that prompted
this work claimed `exports` applied here as well; it does not.) Consulting it
would mean guessing at conditions that cannot fire on this path.

The package ROOT's own manifest is skipped on purpose: resolving root `main`
here would open the `node .` gap sideways, without the entry-point-selection
analysis that gap actually needs. Pinned by `exfil-npm-directory-main/` (caught)
and `benign-npm-directory-main/` — a subdirectory carrying its own manifest is
ordinary layout, so the false-positive twin must stay clean.

**What the hop does NOT close.** It resolves *literal relative specifiers*.
Everything below is a shape where npm still runs code the scan never reads, all
of it found by adversarial review of this change and reproduced against the
code. None of it is a silent ALLOW — `installScriptSignal` emits its lifecycle
warn regardless, so an evaded package still floors at ASK. The loss is
BLOCK downgraded to ASK, not a clean pass.

- **A computed specifier.** `require("./lib/" + "setup")` captures `./lib/` and
  resolves to nothing; `require(\`./\${n}\`)` captures the literal `${n}`. Any
  concatenation, variable or interpolation defeats static resolution — this is
  the inherent ceiling of the technique, not a patchable miss.
- **A require that is not the token `require(`.** An alias (`const r = require;
  r("./x")`) or `module.createRequire`.
- **`#subpath` imports** resolved through the root package.json `imports` map.
  Confirmed to work under CJS `require`, literal (`#helper`) and wildcard
  (`#feat/*`) alike. Left open on cost/benefit rather than difficulty: it needs
  the root manifest in the wanted set, a re-scan of the entry bodies in round
  two to recover the specifier text, plus condition and pattern substitution —
  and it buys nothing while the computed and aliased specifiers above stay open,
  since both are strictly cheaper for an attacker and cannot be closed at all.
  Using it also means shipping an `imports` map in the published manifest, which
  is a visible, unusual artifact.
- **Depth 2.** The helper's own requires are not resolved, by construction. A
  manifest redirect does not extend this: round two resolves `main` and stops.
- **A padded require list.** Eight decoy specifiers ahead of the real one exhaust
  that file's budget. The cap is per file, so the blast radius stops there, but
  a static cap on attacker-controlled text is always gameable.
- **`node .` plus the root `main` field** — pre-existing, and a gap in entry
  point SELECTION rather than in the hop; see the `main`-field note above.

**The pip twin is now closed too** — see "Closed: the deferred install hook"
above. It needed the same two things: paths instead of basenames, and a follow
stage. What does NOT carry over is the npm residual list: Python has no
computed-specifier equivalent that matters here, because `__import__(name)` and
`importlib.import_module(name)` with a built-up string are already the
obfuscation shapes the deterministic rules look at directly, rather than a
resolution problem. A dotted literal import is the ordinary spelling, and that
is the one now followed.

**The join seam, and why the hop forced it.** `buildScriptFindings` concatenates
the bodies it is given before scanning, and the separator used to be a single
`\n`. That made every file boundary a proximity seam: an identity read on the
last line of one file and an `https.request` on the first line of the next sit
~20 characters apart, well inside `JS_GATE_WINDOW`, and weld into an
"exfiltration" gate spanning two unrelated files — the cross-file version of
precisely what that window exists to prevent within one. The defect predates the
hop; the hop made it urgent by turning a 1-4 body join into a 12-body one, one
new seam per helper. Bodies are now joined by a separator wider than the window.
A real multi-file exfil still fires: the half that builds the payload and the
half that sends it live in the same function.

`near()` became a two-pointer merge in the same pass. It was `O(n·m)` over match
positions, which is fine for one hand-written entry point and not fine once a
dozen files — any of them able to repeat a cheap half-gate token like
`process.env` tens of thousands of times — reach the same gate. Measured at
~18s of CPU for a single crafted package before the fix.

**False-positive cost, measured four times — the second corpus is the one that
mattered, the third covers the require hop, the fourth the manifest round.**

*First pass, name list.* All 5,973 names in `src/data/popular-names.json` run
through the production path. 55 declare a lifecycle script, 43 yielded a
scanned entry point, **1 flagged**: `@depot/cli`, whose installer does a
`JSON.stringify` version check four lines above an unrelated
`npm_config_user_agent` read. A real defect — the env-harvest arm used
`[\s\S]{0,120}?`, a span crossing `)` and newlines, where the Python twin has
always used `[^)\n]*`. Narrowed to `[^)]{0,200}`.

*What that pass could not see.* 43 bodies is too thin to support "0 false
positives", and the list is popularity-filtered names rather than the packages
developers actually install. Adversarial review found three real BLOCKs it had
missed — `@scarf/scarf` (millions of weekly installs), `protolint`,
`@ottocode/install` — and the arithmetic explains why: at the observed half-gate
rates, 43 samples has an expected count well under one, so 0/43 is
indistinguishable from a ~1.5% false-positive rate. **A zero on a corpus that
small was not evidence.**

*Second pass, real tarballs.* Every distinct npm tarball in the local npm cache
— 6,239 of them, real published artifacts — walked with the production gate and
production file selection. 6,108 declare no lifecycle script, **65 entry points
scanned, 0 flagged** after the fixes above. `@scarf/scarf` is in this corpus and
was flagged before them.

The gate is why the scanned counts stay small in both passes: the overwhelming
majority of packages declare no lifecycle script at all, so npm executes none of
their code at install time and no tarball is ever fetched for them.

*Third pass, the require hop.* When the scan learned to follow the entry
point's relative requires, the same 5,973-name sweep was re-run as a
before/after comparison over real tarballs, and then re-run AGAIN after
adversarial review changed what the hop reads (per-file cap, minified ESM
specifiers — both of which make it read *more*). Final numbers, from a sweep
with **0 unresolved packuments**: 58 declare a lifecycle script, 36 yielded a
scanned entry point, and the hop actually engaged in **14** of them, reading 25
helper files — `@sentry/cli`, `@swc/core`, `@pulumi/docker-build`,
`opencv-build`, prebuilt loaders, native-addon installers: exactly the
legitimate deferral shape `benign-npm-required-helper/` pins. **0 flagged
before, 0 flagged after**, in both sweeps. The hop added no finding to any real
package it touched.

*Fourth pass, the manifest round.* Re-run again when round two was added, for
the same reason: it makes the scan request `<dir>/package.json` for every
directory-ish specifier and then read whatever `main` names. Identical corpus,
0 unresolved: 58 lifecycle packages, 36 entry points, hop engaged in 14, and the
manifest round added exactly **one** file across all 5,973 names —
`@aws-amplify/cli`'s `lib/package.json`, a real directory require whose manifest
the scan previously could not see. **0 flagged before, 0 flagged after.**

Two process notes, because both are the kind of thing that quietly turns a
measurement into a rubber stamp. The first attempt at this sweep was silently
Cloudflare rate-limited into seeing 9 lifecycle packages instead of 58 — a
number the earlier passes existed to contradict, reported as a clean run.
Fetch failures are now retried with backoff and *counted*; the harness prints
the unresolved tally so a throttled sample can never read as a pass. And the
number was re-earned rather than assumed after the review fixes: changes that
widen what a detector reads invalidate the FP measurement taken before them.

**Do not read any of these numbers as a false-positive RATE.** 65 entry points
— or 25 helpers — cannot support one, and each corpus has its own bias. They
are floors, not measurements — the same reason `docs/EVIDENCE.md` refuses to
publish rates.
