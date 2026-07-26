# Attack class: manifest-field prompt-injection (PromptMink-class)

Adversarial instructions aimed at an **LLM coding agent** are hidden in package
**manifest metadata fields** — `keywords`, `author`, `maintainer`, and
non-lifecycle `scripts` — rather than in the README. Until now DepWall's judge
only saw `name` / `description` / `readme` / lifecycle install scripts, so an
injection payload placed in (e.g.) `package.json` `keywords` or a `scripts.test`
entry reached the coding agent **unscanned**.

This is a real, documented, active threat: ReversingLabs traced the North Korean
group **Famous Chollima**'s **"PromptMink"** campaign (≥ Sept 2025), which used
"LLM Optimization (LLMO) abuse and knowledge injection" — package metadata crafted
to appear authoritative *to an LLM resolving dependencies*, not to a human. Bait
package: `@solana-launchpad/sdk`. Academic backing: arXiv:2601.17548 lists
`package.json` / `pyproject.toml` manifests as documented indirect-prompt-injection
vectors against agentic coding assistants.

## Fixtures

- `pkg-keywords-injection.json` — npm packument with the injection in `keywords`.
- `pkg-script-injection.json` — npm packument with the injection in a NON-lifecycle
  `scripts` entry (`test`), which the install-script signal deliberately ignores.
- `pyproject-injection.json` — PyPI-shaped metadata with injection in
  `keywords`/`author`.
- `good-manifest.json` — benign manifest with ordinary keywords + a real test
  script (false-positive trap: must NOT be flagged just for having keywords/scripts).

## Expected behavior

The injection text must reach the judge **as data** (present in
`JudgeInput.manifestFields`), fenced and defanged, and must never launder a
gray-zone package to ALLOW. A benign manifest with ordinary keywords/scripts must
stay clean. The judge (not a deterministic signal) decides — free-text injection
is inherently an LLM-judge task; the deterministic guarantee here is that the
manifest fields are *delivered to* the judge, closing the blind spot.

Regression tests: `tests/judge/manifest-prompt.test.ts`,
`tests/ecosystems/manifest-injection.test.ts`.
