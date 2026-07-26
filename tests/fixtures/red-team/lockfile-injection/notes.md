# Attack class: lockfile injection (resolved-URL / tarball poisoning)

A poisoned lockfile keeps a benign `name@version` — which passes every
name/version reputation check and looks clean in code review — but rewrites the
`resolved` (npm/yarn) or `resolution.tarball` (pnpm) URL so `npm ci` /
`npm|yarn|pnpm install` fetches attacker code instead. Lockfile diffs are
collapsed by default on GitHub, making this a classic malicious-PR vector
(publicly documented by Snyk as "lockfile injection", 2019).

Variants covered by fixtures here:

- `poisoned-package-lock-foreign-host.json` — one entry's `resolved` points at
  an attacker host while the rest of the tree resolves to registry.npmjs.org.
- `poisoned-package-lock-substitution.json` — `resolved` stays on
  registry.npmjs.org but points at a **different package's** tarball
  (same-host substitution; also covers version substitution).
- `poisoned-package-lock-http.json` — `resolved` downgraded to plain `http://`
  (MITM-able transport).
- `poisoned-yarn.lock` — foreign-host variant in yarn v1 format.
- `poisoned-pnpm-lock.yaml` — pnpm v9 `resolution.tarball` pointing at an
  attacker host for a registry-versioned package.

Expected verdicts: same-registry substitution → **BLOCK** (no legitimate
cause); foreign minority host / http downgrade / pnpm foreign tarball → **ASK**
(a lone entry on an unexpected host halts for human review; uniform private
registries and per-scope registry routing stay ALLOW — see the GOOD fixtures in
`tests/fixtures/lockfiles/`).

Regression test: tests/hook/lockfile-provenance.test.ts
