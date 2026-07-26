# Red-team corpus: provenance-attestation drop (account-takeover shape)

npm provenance (SLSA/Sigstore, `npm publish --provenance`) verifies build
**origin**, not behavior — so DepWall consumes it as a *complementary* signal,
never a rival verdict source. Every fixture here is **inert metadata only**
(PackageRecord-shaped JSON), never executed, per
[docs/TESTING-SAFETY.md](../../../../docs/TESTING-SAFETY.md).

The detection is the **drop**: a maintainer who publishes through an attesting
CI pipeline cannot be impersonated with a stolen npm token alone — the
attacker's publish lacks `dist.attestations` while recent prior versions carry
them. This is the modern signature of the ua-parser-js (CISA 2021) /
event-stream (2018) account-takeover class, applied to a mature popular
package where `maturity`, `slopsquat`, and name-`provenance` are all silent.

Signal: `attestationSignal`, history
extracted purely from the packument in
`normalizeMetadata`: up to the **5** most
recently published prior **stable** versions, preferring the requested
version's **own major line** (so an unattested backport/hotfix on an old major
never inherits attested history from a newer line — the perpetual-FP trap),
falling back to all lines when the requested major has no priors (a takeover
published as a fresh major stays covered). Prerelease requests get no history
(canary/nightly lanes are routinely unattested). Dist-tags (`latest`, `next`,
…) are resolved inside the normalizer so the cloud path — which has no other
resolver — never evaluates a phantom version. Live shape verified against
`registry.npmjs.org/sigstore`. Tiering:

- current attested → **info** (mild positive, never tier-changing)
- current NOT attested, immediately-prior attested OR ≥2 of window attested →
  **warn (ASK)** — covers the direct drop and 1–2 junk smokescreen versions
- never attested → **no finding** (absence is the registry norm; flagging it
  would ASK effectively the whole ecosystem — see ANTI-HALLUCINATION rule 7)

**Known limitations (accepted for v1, documented on purpose):**

1. **Window flush** — ≥4 unattested junk publishes before the payload push all
   attested history out of the 5-window → silent. Cost to the attacker: a
   noisy registry trail of extra publishes with the stolen token.
2. **History erasure** — an attacker who *unpublishes* the recent attested
   versions removes them from `versions` (npm unpublish policy limits this on
   popular packages) and the window slides back to older versions.
3. **Identity continuity not checked** — a stolen token CAN mint a *valid*
   attestation from the attacker's own repo/workflow; we only normalize
   presence, not the attesting identity. Comparing the attesting repo/workflow
   across versions is the robust tell → backlog (needs the attestation
   endpoint, not just the packument).
4. **Semver ranges** (`^1.x`) are not resolved (dist-tags are) → empty history,
   detection silently off for range requests.

| Fixture | Shape | Signal exercised | Expected |
|---|---|---|---|
| `takeover-drop.json` | mature+popular, previous `[true,true,true]`, current unattested | `attestation` (warn) | ASK |
| `good-never-attested.json` | (control) mature package, never attested | none | ALLOW |
| `good-attested-current.json` | (control) attested current version | `attestation` (info only) | ALLOW |

Regression test: tests/signals/attestation.test.ts
