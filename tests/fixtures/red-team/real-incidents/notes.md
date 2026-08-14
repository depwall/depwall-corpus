# Red-team corpus: real historical incidents (inert metadata)

Proves DepWall's deterministic signals fire on the **shape** of real, publicly
documented supply-chain attacks — not just synthetic fixtures. Every file here
is **inert metadata only** (a `PackageRecord`-shaped JSON snapshot), REDACTED and
never executed, per [docs/TESTING-SAFETY.md](../../../../docs/TESTING-SAFETY.md).
No real package is installed or run; any exfil payload is replaced with an inert
`REDACTED.example` marker so only the detectable structure remains.

| Fixture | Incident | Signal exercised | Expected |
|---|---|---|---|
| `event-stream-flatmap-stream.json` | event-stream / flatmap-stream (2018) | `install-scripts` (network+pipe-to-sh) | BLOCK |
| `crossenv-typosquat.json` | crossenv typosquat wave (2017) | `slopsquat` (dist-1 from `express`) + `install-scripts` (env exfil) | BLOCK |
| `hallucinated-slopsquat.json` | AI package hallucination / slopsquatting (2024–25) | `provenance` (not found in registry) | BLOCK |
| `ua-parser-js-hijack.json` | ua-parser-js account compromise (Oct 2021, CISA) | `install-scripts` (cryptominer downloader, despite millions/week maturity) | BLOCK |
| `brandjack-newcomer.json` | dependency-confusion / brand-jack (Birsan 2021) | `maturity` only (new + low adoption) | ASK |
| `node-ipc-protestware.json` | node-ipc protestware (March 2022, 'peacenotwar') | **KNOWN GAP — zero signals** | ALLOW |
| `tarball-body-preinstall-loader.json` | `000webhost-admin@999.9.9` (Dec 2024, DataDog corpus) | `install-scripts` (presence only) + `maturity` | ASK — **KNOWN GAP: tarball body unread** |
| `mini-shai-hulud-optional-git-dep.json` | Mini Shai-Hulud (TeamPCP, May 2026) — npm delivery vector | `remote-dep` (optional dep → forge orphan commit, `prepare` runs at install) | ASK |
| `mini-shai-hulud-runner-token-theft.json` | Mini Shai-Hulud — CI OIDC token theft stage | `install-scripts` (`/proc/self/mem` + `ACTIONS_ID_TOKEN_REQUEST_*`) | BLOCK |
| `mini-shai-hulud-wiper.json` | Mini Shai-Hulud — dead-man switch + agent-config persistence | `install-scripts` (home-dir wipe, critical; `.claude/` write, warn) | BLOCK |
| `good-control-optional-platform-dep.json` | (control — per-platform `optionalDependencies` as semver) | none | ALLOW |
| `good-control-express.json` | (control — real popular package) | none | ALLOW |

Sources are cited in each fixture's `_disclosure` field.

Stage 2 of the slopsquatting attack — the hallucinated name **pre-registered**
so it resolves in-registry — is covered by
[`../hallucinated-names/`](../hallucinated-names/notes.md) (`hallucinated-name`
curated-feed signal).

**Known gap: `node-ipc-protestware.json`** documents a detection blind spot.
The real attack (malicious code injected directly into package source, running
at runtime via `index.js`, not via lifecycle scripts) escapes all current
signals — no install-script pattern, real registry entry, mature package,
no provenance drop (npm attestations didn't exist as ecosystem norm in 2022).
This mirrors the lockfile "uniform-total-poison" known limitation:
install-time gating is blind to package-source malice.
Mitigation roadmap: deeper pip/cargo/go analysis (setup.py/build-script
bodies), and runtime-phase defenses (not DepWall's scope).

**Fixture artifact, NOT a product gap: `tarball-body-preinstall-loader.json`
is ASK because the fixture has no tarball.** It is the dominant npm
malicious-intent shape in the public corpus: `preinstall: node index.js`, with
clean registry metadata and the payload inside the tarball.

This entry used to read *"npm does not fetch its tarball, so the verdict tops out
at ASK."* **That claim is obsolete, and leaving it standing was a defect in its
own right.** npm bodies have been fetched in the gray zone since PR #84, and the
scan now also follows the entry point's relative requires one hop (PR #99),
including through a required directory's own `package.json` `main`. Against a
real registry this shape reaches BLOCK on a malicious body.

The fixture still resolves to ASK, and that is a property of the FIXTURE: these
are inert metadata records with no archive attached, so the body-fetch path
cannot run here at all. The tier in the table is a floor from metadata alone, not
a statement about what the product does. End-to-end body coverage lives in
`tests/ecosystems/npm-tarball-body.test.ts` and `tests/ecosystems/pip-deep.test.ts`,
which drive the real fetch + extract path over real archive layouts.

Kept as a documented case rather than deleted, because the reason for the number
is the useful part. A security document that leaves a closed gap described as
open is the same class of error as claiming coverage it does not have — and this
one survived three releases.

**Known limitation: Mini Shai-Hulud carried VALID SLSA provenance.** The
malicious versions were signed by a real Sigstore certificate issued to the
victim's own CI identity, so the attestation-DROP detection is blind to this
class — there is no drop to see. `attestationSignal` stays `info` for a present
attestation for exactly this reason, and
`real-incidents.test.ts` pins that: provenance must never become credit that
offsets a finding.

**Residuals on the `remote-dep` signal.** It reads the dep blocks of the
*published package* (registry packument). Two neighbours are deliberately left
alone: (1) `prepare` is still not treated as a lifecycle install script for a
registry tarball — npm does not run it there, and flagging it would ASK on
`prepare: husky install` across half the ecosystem; (2) a forge-hosted git dep
in the *user's own* `package.json` remains suppressed as a pinned fork
(`directSourceFindings`). Fetching the git dep's own manifest at the pinned ref
is the precise fix and is deferred.

Regression test: tests/signals/real-incidents.test.ts

**Adding to this corpus:** if a real incident's shape is NOT caught, that is a
missing detection — add it fixture-first via the `adding-a-detection` skill
(new signal + GOOD/BAD fixtures), do not weaken the corpus to make it pass.
