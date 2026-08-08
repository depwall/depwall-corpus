# Known-malicious tarball hashes

Packages whose exact tarball someone has already confirmed malicious, matched by
`dist.integrity` against a denylist baked into the release.

## Why this class exists

Every other npm signal infers from metadata: does it run an install script, is
the name close to a popular one, is it too new, does it have downloads. That is
all a gate can see before install, and it is blind to two shapes that dominate
live npm malware:

- **a prebuilt binary in the tarball** — the payload is the artifact, so there is
  no lifecycle script to notice;
- **a payload on `require()`** — it runs when the app imports the package, which
  is after install and after every metadata check has already passed.

Neither declares anything. A metadata read of them is indistinguishable from a
small, boring, legitimate package — and it should be, because from metadata they
are identical.

Measured, not assumed, by `scripts/osv-bench.mjs` — DepWall's real npm gate over
the packages OSV flags malicious **that are still installable from npm today**.
Only survivors count: ~97% of OSV's malicious corpus has been unpublished, and a
BLOCK on one of those says "not found in the registry", which measures npm's
takedown queue rather than any detection.

Before the signal existed (2026-08-08, 495 advisories sampled → 19 live packages
→ 36 installable versions):

| Verdict | Versions |
|---|---|
| BLOCK | 3 |
| ASK | 8 |
| ALLOW | 25 |

**69% walked straight through.**

After (2026-08-08, 355 advisories sampled → 10 live packages → 17 versions):
every package gated, and **6 of the 10 are gated by this signal alone** — strip
the hash finding and those six go back to ALLOW, because nothing else has
anything to say about them.

The two runs sample different advisories, so the tables are two independent
measurements rather than a before/after on one set. The claim that does not
depend on comparing them is the second one: on a package caught only by
`known-malicious`, removing the list removes the verdict.

## Why a hash and not a name

`dist.integrity` names one exact set of bytes, so a match is not a judgement —
the registry is serving the tarball the advisory is about, or it is not. That is
the only npm signal here with no false-positive rate to trade against, which is
why it is allowed to BLOCK on its own.

A name+version denylist would cover far more of OSV (only ~2% of its malicious
npm advisories carry a hash) at the cost of inheriting OSV's accuracy: one wrong
upstream entry would block a package nobody has confirmed is bad, on a tool whose
value is that it does not cry wolf. The narrower claim is the checkable one.

## Limits

**Known gap: coverage is small and version-exact.** The list holds ~4,000
tarballs out of the ~219,000 malicious npm advisories OSV carries, because most
advisories publish no hash. It also pins one version — OSV routinely names ten
malicious versions of a package and supplies a digest for one of them, and the
other nine are not covered here. Absence from this list is not evidence of
anything, which is why the signal is escalate-only and every other signal still
runs.

**Known gap: a freshly compromised tarball has no hash yet.** The list is baked
into the release and refreshed on a schedule, so a package poisoned after the
last sync is not on it, and neither is one nobody has reported. This signal is a
floor under the heuristics, never a replacement for them.

**Known gap: republishing evades it completely.** Change one byte, get a new
digest, and the list no longer matches. This is not a weakness to be fixed — it
is what "exact" means, and it is the same trade that buys the zero
false-positive rate. The heuristics are what have to catch the recompiled
version, which is why this signal is additive and nothing was relaxed to make
room for it.

**Known gap: it trusts the registry it is talking to.** `dist.integrity` comes
from whatever endpoint answered. A mirror under an attacker's control can omit
the field or report a digest for bytes it does not serve, and the signal goes
quiet. An attacker with that position has already won larger fights than this
one, so the response is to say so rather than to pretend otherwise.

## Adversarial review

Run before merge, per the repo rule. What it found:

| Attack | Result |
|---|---|
| `integrity: "constructor"` — inherited `Object` properties resolve truthy through `hashes[token]` | **Was a false BLOCK.** Five inherited names did it. Fixed with `Object.hasOwn`, pinned by a regression test |
| Space-separated SRI list hiding a known-bad digest in a non-first position | Caught — `multi-token-sri-evasion.json` |
| Cloud cache serving a pre-deploy `ALLOW` past the new signal | **Was a 24h bypass.** `VERDICT_LOGIC_VERSION` bumped to 6, which retires every key |
| Cloud `ALLOW` short-circuiting the local check (`cloud/client.ts`) | Closed by giving the Worker the same list — both read this one file, so they cannot disagree |
| Poisoned upstream entry naming a legitimate tarball's digest | Residual. The weekly sync opens a PR instead of pushing, CI runs the corpus against the new list, and a collapse in list size fails the job — but a single plausible-looking bad entry rests on human review of the diff |
| Malformed advisory id reaching a terminal or a URL | Validated in `scripts/osv-sync.mjs` and asserted over the shipped file in the tests |

## Fixtures

| File | What it is |
|---|---|
| `prebuilt-binary-no-install-script.json` | The real thing: a Mach-O Go agent with a hardcoded C2 broker, no lifecycle script, ALLOWed by every other signal |
| `multi-token-sri-evasion.json` | SRI permits space-separated digests; a whole-string equality test misses this |
| `good-mature-package.json` | Control — an ordinary tarball not on the list |
| `no-integrity-published.json` | Control — no `dist.integrity` at all; "nothing to compare" must not read as "clean" |

Fixture `integrity` values are digests, not code. Nothing in this directory is
executable and no payload is reproduced.
