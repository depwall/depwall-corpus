# Attack class: agent lured into installing an attacker CLI via brew

An agent is manipulated (by malicious MCP tool output) into running
`brew install` for a CLI outside homebrew-core whose install scripts exfiltrate
SSH keys, AWS credentials, and `.env` contents.

| Fixture | Signals exercised | Expected |
|---|---|---|
| `attack.json` | `provenance` (not in homebrew-core, third-party tap) + `install-scripts` (curl-pipe-sh, credential exfil) | BLOCK |

The fixture is inert metadata and declares its own `expected_verdict` and
`must_never_regress_to: ALLOW`. Source: Nikita Benkovich public disclosure
(2026); full write-up in
docs/case-studies/2026-claude-code-brew-install-rce.md.

Regression test: tests/ecosystems/brew.test.ts
