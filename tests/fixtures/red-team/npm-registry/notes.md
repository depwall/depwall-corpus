# Attack class: npm registry redirection via project `.npmrc`

npm, pnpm, and yarn-classic all honor a project-local `./.npmrc`. A committed
attacker `.npmrc` silently repoints **every** install off the public registry —
`npm install <anything>` then resolves from the attacker's host, with an
auth token attached.

| Fixture | Vector | Expected |
|---|---|---|
| `poisoned-npmrc` | `registry=` set to an attacker host + `_authToken` | ASK |

Ceiling is ASK: a non-default registry host alone is suspicious, not proof —
operators legitimately run private registries, which they allowlist via
`DEPWALL_REGISTRY_ALLOWLIST`. Config files are consulted only when the lockfile
does not already pin host-checkable resolved URLs.

Regression test: tests/hook/guard-npm-registry-redirect.test.ts
