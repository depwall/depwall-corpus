# Red-team corpus: pre-registered hallucinated names (slopsquatting stage 2)

The attack: LLMs hallucinate package names **systematically — the same names
recur across runs** (arXiv:2406.10279, USENIX Sec 2025), so an attacker can
predict and pre-register the *exact* name. Once registered, the name resolves
in-registry → the not-found `provenance` signal is silent; it is not an
edit-distance near miss → `slopsquat` is silent; age and downloads accumulate
(the hallucinating agents themselves generate downloads — `huggingface-cli`
drew 30k+ on an empty package) → `maturity` is silent. Every fixture here is
**inert metadata only** (PackageRecord-shaped JSON), never executed, per
[docs/TESTING-SAFETY.md](../../../../docs/TESTING-SAFETY.md).

Detection: curated feed `src/data/hallucinated-names.json`
of **documented** hallucination targets (exact-match, lowercase, per ecosystem,
citation required per entry) + `hallucinatedNameSignal`.
On-feed + registered + not established → **critical (BLOCK)**; on-feed +
established → **warn (ASK)** — never silent-ALLOW a documented hallucination
target, because adoption metrics are inflated by the very agents being fooled.
Wired into all four verdict paths: npm local (`runSignals`), npm cloud
(`computeNpm`), pip/cargo/go local (`deepProvenanceVerdict`), pip/cargo/go
cloud (`localProvenanceVerdict`).

| Fixture | Shape | Signal exercised | Expected |
|---|---|---|---|
| `preregistered-fresh.json` | `unused-imports` — live malware under a hallucinated name (Aikido, Feb 2026) | `hallucinated-name` (critical) | BLOCK |
| `preregistered-matured.json` | `react-codeshift` — aged + agent-inflated downloads; ALLOW without the feed | `hallucinated-name` (warn) | ASK |
| `good-real-eslint-plugin.json` | (control) the real package `unused-imports` imitates | none | ALLOW |
| `good-real-jscodeshift.json` | (control) real package `react-codeshift` conflates | none | ALLOW |

Sources are cited in each fixture's `_disclosure` field and in the feed's
`_sources` map.

Feed hygiene (enforced by tests): feed ∩ `popular-names.json` = ∅; entries
lowercase + non-empty. If a feed name ever becomes a legitimate package,
**remove it from the feed** — do not weaken the signal.

Regression test: tests/signals/hallucinated-name.test.ts
