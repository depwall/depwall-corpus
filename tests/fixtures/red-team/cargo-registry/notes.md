# Attack class: cargo registry / source redirection

A repo-shipped `.cargo/config.toml` can silently repoint crate resolution off
crates.io via `[source]` replace-with chains, `[registries]` entries, or
`[patch]` tables — dependency confusion against Rust builds. The parser must
survive TOML shape variants (quoted keys, dotted top-level keys, inline tables,
whitespace in dotted paths, case variants, and the legacy extensionless
`config`) rather than only the canonical layout.

Ceiling is **ASK**: a non-default registry host is suspicious, not proof —
operators legitimately run private registries, which they allowlist via
`DEPWALL_REGISTRY_ALLOWLIST`.

## Redirect fixtures → ASK

`poisoned-*` (source replace-with to an attacker host, plus the quoted-key,
inline-quoted-key, leaf-inline, whole-inline, top-level-dotted and
whitespace-dotted TOML shape variants, and the legacy extensionless
`poisoned-cargo-config`), `direct-registry-crates-io-*`,
`case-variant-crates-io-*`, `ssh-source-index-*`,
`patch-git-cargo-config.toml` (a `[patch]` repointing a crate at an attacker
git repo, whose `build.rs` runs at build time), and
`registry-default-cargo-config.toml` (a `[registry] default` selecting an
attacker-controlled `[registries.evil]` index) all redirect resolution off the
default registry and must reach ASK.

`unresolvable-chain-cargo-config.toml` names a `replace-with` target that is
never defined — the redirect destination is unknowable, so DepWall fails
**closed** (ASK) rather than silently allowing.

## Allowlist-gated fixtures → ASK by default, ALLOW when allowlisted

These are legitimate corporate setups that must not be nagged once the operator
declares the host, and must not be silently allowed before that.

| Fixture | Shape | Suppressed by |
|---|---|---|
| `corp-mirror-replace-with-registries-cargo-config.toml` | standard corporate sparse registry (Artifactory / CloudSmith / CodeArtifact) | `DEPWALL_REGISTRY_ALLOWLIST=mirror.corp` |
| `patch-git-corp-cargo-config.toml` | `[patch]` git source on a corp-mirror host | `DEPWALL_REGISTRY_ALLOWLIST=mirror.corp` |
| `registry-default-unresolvable-cargo-config.toml` | named default registry whose index lives in home config (split config) | `DEPWALL_REGISTRY_ALLOWLIST=corp` (bare-name hatch) |
| `replace-with-unresolvable-named-cargo-config.toml` | `replace-with` a named source defined in home config | `DEPWALL_REGISTRY_ALLOWLIST=corp` (bare-name hatch) |

## Control fixtures → ALLOW (zero false positives)

| Fixture | Why it is legitimate |
|---|---|
| `benign-cargo-config.toml` | proxy, transport, build tuning, alias, sparse opt-in — no redirect |
| `vendored-cargo-config.toml` | verbatim `cargo vendor` output; replace-with points at a local directory |
| `defined-unused-registry-cargo-config.toml` | a private registry defined but never selected |
| `patch-path-cargo-config.toml` | a `[patch]` pointing at a local path (dev checkout) |

Regression test: tests/hook/guard-cargo-registry-redirect.test.ts
