# DepWall — Detection Evidence

*Generated from DepWall's red-team corpus and published here by `npm run sync-public`.*
*Do not edit by hand — it is regenerated from the corpus in the same directory.*

## What this page does not claim

DepWall does **not** publish a detection-recall percentage or a false-positive rate here, and neither should be inferred from this page.

- **No recall percentage.** This repository's red-team fixtures are self-authored: each was written alongside the detection it exercises. A recall figure over them would measure whether our tests agree with our own code — not whether DepWall catches real attacks.
- **No false-positive rate.** A defensible false-positive rate needs a large, representative population of benign packages. This corpus carries only a handful of benign controls.

Publishing either number from this corpus would be the failure mode [ANTI-HALLUCINATION.md](ANTI-HALLUCINATION.md) exists to prevent. Real percentages require an independent malicious corpus plus a benign control set — separate, unfinished work, and constrained by [TESTING-SAFETY.md](TESTING-SAFETY.md): such datasets carry live malware and must be handled as metadata only, never detonated.

An attack shape the engine does not catch is listed below as a **documented gap**, never omitted.

## Real-incident replay

Each fixture below is inert, redacted metadata. Most are modelled on a publicly documented supply-chain incident; the set also includes a generic attack pattern and a benign control, both labelled as such in the table. When this page is generated, every fixture is loaded, its documentation fields stripped, and run through the **real signals engine** — the verdicts here are recomputed, not transcribed.

**5 of 6** documented malicious incident shapes are gated — 4 BLOCK, 1 ASK — and 1 is a documented miss. **1 of 1** benign control correctly allowed.

*Gated* means the install was stopped or held for a human (BLOCK or ASK), not silently allowed. An ASK is not a clean detection — it is DepWall refusing to decide on its own, and on a small set like this it can be driven by a single broad signal such as package immaturity.

| Incident | Fixture | Verdict | Signals | Result | Source |
|---|---|---|---|---|---|
| brand-jacking newcomer (generic pattern; cf. 2021-2024 dependency-confusion & impostor waves) | `brandjack-newcomer.json` | ASK | `maturity` | detected | [source](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610) Birsan 2021 |
| crossenv / cross-env typosquat wave (Aug 2017) | `crossenv-typosquat.json` | BLOCK | `install-scripts`, `maturity`, `slopsquat` | detected | [source](https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry) |
| event-stream / flatmap-stream (Nov 2018) | `event-stream-flatmap-stream.json` | BLOCK | `install-scripts` | detected | [source](https://github.com/dominictarr/event-stream/issues/116) |
| GOOD control — a real, popular, mature package | `good-control-express.json` | ALLOW | none | control allowed | — |
| AI slopsquatting — hallucinated package name (2024-2025 research) | `hallucinated-slopsquat.json` | BLOCK | `maturity`, `provenance`, `slopsquat` | detected | [source](https://arxiv.org/abs/2406.10279) package hallucination in code-gen LLMs; Socket/Lasso 'slopsquatting' coverage |
| node-ipc protestware (March 2022, 'peacenotwar') | `node-ipc-protestware.json` | ALLOW | none | **MISS (documented gap)** | [source](https://nvd.nist.gov/vuln/detail/CVE-2022-23812) |
| ua-parser-js account compromise (Oct 2021, CISA alert) | `ua-parser-js-hijack.json` | BLOCK | `install-scripts` | detected | [source](https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js) |

This is a small, hand-curated set — it demonstrates that the deterministic signals fire on the *shape* of real attacks. It is not a benchmark, and no rate should be extrapolated from it.

## Known gaps

- Runtime-payload injection — malicious code placed directly in package source that runs at import time (not via a lifecycle script) is not detectable at install time. *(documented in `tests/fixtures/red-team/real-incidents/notes.md`)*
- Uniform-total-poison lockfile — a lockfile rewritten wholesale onto a single unlisted host is only caught when DEPWALL_REGISTRY_ALLOWLIST is configured.
- MCP runtime tool-poisoning — tool descriptions served by a live MCP server (tools/list) are reachable only by connecting to it, which DepWall will not do.
- curl has no PATH shim — pipe-to-shell is enforced in the Claude agent hook, not in a human shell.
- A poisoned repository on a known forge passes the git-clone host gate; scan it explicitly with `depwall scan <url>`.
- The command scanner is lightweight tokenization, not a shell parser — eval, variable indirection, and xargs can evade it. It is defense-in-depth, not a sandbox.

Marked in the corpus itself:

- `agent-artifacts`: Known gap: true MCP tool-poisoning lives in a live server's `tools/list` metadata, reachable only by connecting to it — out of scope by design.
- `build-scripts`: Known gaps (documented, deliberate): PEP 517 backend hooks outside setup.py; obfuscation beyond these patterns is the judge's job (it sees the full body); deterministically-ALLOW packages (mature+popular) are never tarball-scanned.
- `real-incidents`: Known gap: `node-ipc-protestware.json` documents a detection blind spot. The real attack (malicious code injected directly into package source, running at runtime via `index.js`, not via lifecycle scripts) escapes all current signals — no install-script pattern, real registry entry, mature package, no provenance drop (npm attestations didn't exist as ecosystem norm in 2022). This mirrors the lockfile "uniform-total-poison" known limitation: install-time gating is blind to package-source malice. Mitigation roadmap: deeper pip/cargo/go analysis (setup.py/build-script bodies), and runtime-phase defenses (not DepWall's scope).
- `remote-exec`: Known gap: `curl` has no PATH shim — pipe-to-shell is enforced in the Claude agent hook, not in a human shell.

## Corpus census

Every attack class with a regression fixture in this repository.

| Attack class | Fixtures | Notes |
|---|---|---|
| `agent-artifacts` | 6 | [notes](../tests/fixtures/red-team/agent-artifacts/notes.md) |
| `brew-bundled-cli` | 1 | [notes](../tests/fixtures/red-team/brew-bundled-cli/notes.md) |
| `build-scripts` | 8 | [notes](../tests/fixtures/red-team/build-scripts/notes.md) |
| `cargo-registry` | 22 | [notes](../tests/fixtures/red-team/cargo-registry/notes.md) |
| `eco-lockfile-injection` | 6 | [notes](../tests/fixtures/red-team/eco-lockfile-injection/notes.md) |
| `env-redirect` | 1 | [notes](../tests/fixtures/red-team/env-redirect/notes.md) |
| `hallucinated-names` | 4 | [notes](../tests/fixtures/red-team/hallucinated-names/notes.md) |
| `index-redirect` | 1 | [notes](../tests/fixtures/red-team/index-redirect/notes.md) |
| `lockfile-injection` | 5 | [notes](../tests/fixtures/red-team/lockfile-injection/notes.md) |
| `manifest-injection` | 4 | [notes](../tests/fixtures/red-team/manifest-injection/notes.md) |
| `npm-registry` | 1 | [notes](../tests/fixtures/red-team/npm-registry/notes.md) |
| `provenance-drop` | 3 | [notes](../tests/fixtures/red-team/provenance-drop/notes.md) |
| `readme-injection` | 1 | [notes](../tests/fixtures/red-team/readme-injection/notes.md) |
| `real-incidents` | 7 | [notes](../tests/fixtures/red-team/real-incidents/notes.md) |
| `remote-exec` | 1 | [notes](../tests/fixtures/red-team/remote-exec/notes.md) |
| `url-confusion` | 1 | [notes](../tests/fixtures/red-team/url-confusion/notes.md) |

## How to verify

The verdicts above are **recomputed by the real signals engine every time this page is generated** — they are not transcribed by hand, and a fixture that stopped being detected would change this page rather than be quietly omitted.

The engine itself is **not public**, so today you are trusting that generation step. `npx depwall verify-corpus` will recompute this table on your own machine, against these fixtures, once the CLI is published — at which point this page becomes independently reproducible.

Every fixture here is inert metadata. Nothing in this repository is executable, and nothing should be installed — see [TESTING-SAFETY.md](TESTING-SAFETY.md).
