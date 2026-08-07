# Attack class: poisoned agent-native artifacts (skills + MCP configs)

Agent skill files and MCP server configs are loaded into an agent's context or
spawned by its client. A malicious skill can carry prompt-injection in its
frontmatter or body; a malicious MCP config can point at an unverified remote
server or spawn a command that fetches remote code.

| Fixture | Vector | Expected |
|---|---|---|
| `bad-skill/SKILL.md` | injection in the skill `description` | BLOCK |
| `bad-skill-name/SKILL.md` | injection hidden in the frontmatter `name` (reaches the judge via `manifestFields`) | BLOCK |
| `good-skill/SKILL.md` | benign skill (control) | ALLOW |
| `bad-mcp/.mcp.json` | MCP server on an unverified remote host | ASK |
| `bad-mcp-command/.mcp.json` | server command fetches remote code (`bash -c "curl … \| sh"`) | ASK |
| `good-mcp/.mcp.json` | `npx` launcher, no remote fetch (control) | ALLOW |
| `bad-skill-bundled-payload/` | clean SKILL.md; payload in `scripts/sync.mjs` reads `~/.aws/credentials` + `~/.ssh/id_ed25519` and POSTs them | ASK |
| `bad-skill-helper-shell-tar/` | the SHELL twin: `tar` a private key + cloud creds, `base64`, pipe to `curl` | ASK |
| `bad-skill-helper-dir-tar/` | archives the credential DIRECTORIES (`.ssh` `.aws` `.gnupg`), naming no key file | ASK |
| `bad-skill-helper-dist/` | same payload, shipped compiled in `dist/` — a pruned directory | ASK |
| `bad-skill-helper-extensionless/` | dotless helper named in no markdown, reached only by its `#!` | ASK |
| `good-skill-vendor-token-helper/` | helper reads its OWN `VENDOR_API_TOKEN` and calls that vendor's API (control) | ALLOW |
| `good-skill-keygen-helper/` | helper CREATES a deploy key and registers the public half (control) | ALLOW |
| `good-skill-ssh-provision/` | CI-style provisioning: `unzip` + `mkdir -p ~/.ssh` + `curl` (control) | ALLOW |
| `good-skill-persistent-behavior/SKILL.md` | benign style skill that overrides agent behavior by design (control) | ALLOW |

Known gap: true MCP tool-poisoning lives in a live server's `tools/list`
metadata, reachable only by connecting to it — out of scope by design.

**Bundled helper files are now scanned — deterministically, and narrowly.**
`checkAgentArtifacts` used to collect `SKILL.md` and MCP configs only, so a
bundle whose markdown is unremarkable and whose `scripts/*.mjs` does the
stealing passed. Measured over the 204 malicious AI-skill bundles in
DataDog/malicious-software-packages-dataset: 66 ship executable helpers
(`.py`/`.js`/`.mjs`/`.ts`/`.sh`) and 33 of those reference the network, the
environment, or credential paths — while 138 are markdown-only, where the judge
is the right instrument.

`skillHelperFindings` fires on ONE shape: a credential STORE whose raw bytes are
both READ and SENT, with each pair proximity-bounded. Severity `warn`, so the
ceiling is ASK and never a deterministic BLOCK.

**Two granularities, because the attacker picks the granularity.** The first cut
matched credential FILES only, so `tar czf - -C "$HOME" .ssh .aws | curl` — one
argument's difference, and the shape that takes *everything* — scored zero
credential positions and reached ALLOW. The directory arm counts only ARCHIVE
verbs (`tar`/`zip`/`rsync`/`scp`/`cp -r`) as reading a directory, because you
cannot `cat` one, and it is suppressed by `mkdir`/`chmod` next to the path.
That suppressor is not a guess: without it the arm flagged eight real GitHub
Actions deploy workflows on one machine, every one of them provisioning `~/.ssh`
a few lines from the `unzip` of the AWS CLI and the `curl` that fetched it.
Pinned by `good-skill-ssh-provision/`.

**The selector gates the whole feature, so it has three arms.** Extension match,
OR a path *or bare filename* the SKILL.md names, OR a `#!` on the first line.
Adversarial review walked past the first cut three ways: put the payload in
`dist/` (pruned by the shared repo walker — right for sampling a repo, wrong for
vetting a shipped artifact, where the build output IS what runs); give it no
extension and let a named sibling `exec` it (the shape the official superpowers
plugin already ships as `scripts/sdd-workspace`); or bury it behind decoy
helpers, since the per-bundle cap used to `break` silently. The cap now escalates
and says what it skipped, the same contract the artifact cap already had.

Two arms that look obvious were measured against real installed skills and
REJECTED, which is the whole reason this rule is as narrow as it is:

- **secret-named env read + network.** Fires on `turnstile-spin`'s real helpers,
  where a token is read and used in the very next `curl` *because that is the
  script's job*. Proximity cannot separate them — they are close precisely
  because they are related. Identical conclusion to the npm side (PR #84), and
  it refutes the tempting "helpers are short like `setup.py`, so co-occurrence
  is sound again" hypothesis: shortness does not restore the evidence, it
  removes the only defence, because a short single-purpose helper's declared
  purpose is routinely "call a vendor API with the user's token". Pinned by
  `good-skill-vendor-token-helper/`.
- **identity recon + network.** Same class, same outcome.

A **credential-generation suppressor** discards a credential-path match sitting
within 200 chars of a creation verb (`ssh-keygen`, `aws configure`, `gpg
--gen-key`, `openssl genpkey`, …). Setting up a deploy key names the same paths,
reads them back, and calls an API in one breath. This is structural rather than
statistical — a path being CREATED cannot be a path being STOLEN — so it holds
at any corpus size, which matters because the denominator below does not.
Pinned by `good-skill-keygen-helper/`.

**False-positive cost, measured.** Every skill bundle installed on a real
developer machine plus a local dev tree, run through the production selector and
the production rule: **178 helper-bearing bundles, 920 distinct helper files, 0
flagged.** Separately, the rule alone over **17,027 real text files** across
`~/agentic-dev`, `~/.claude` and `~/.claude-work`: 12 hits, every one of them a
BAD fixture, a copy of one, or DepWall's own source quoting the pattern. The
rule fires on all five BAD fixtures.

**That zero is a floor, not a rate.** Rule of three puts the 95% upper bound on
the per-bundle false-positive rate at ~1.7%, and the corpus is one machine. The
first cut of the directory arm passed the bundle corpus and still flagged eight
real CI workflows — the wider sweep is what caught it, which is the whole
argument for measuring against something bigger than your own fixtures.
PR #84 shipped on "0 in 43" and blocked three real published packages, so the
number alone is not the argument — the corpus-size-INDEPENDENT controls are:
the read term is a positive requirement so the gate fails toward ALLOW, the
generation suppressor is structural, and the ceiling is ASK rather than BLOCK.

Deliberately NOT caught, each because the benign shape is indistinguishable:
env-var harvest with no credential file, single-token exfil, identity recon,
`curl … | sh` in a helper, a payload split across two files (the read in one,
the send in another — same class as `gap-npm-required-helper/`), and anything in
a file the selector does not open.

Cheap for an evasion-AWARE attacker, and accepted: any suppressor is a kill
switch if you write its verb next to your payload (`# ssh-keygen`, a stray
`chmod`), and any literal path list is defeated by a glob or a `path.join`.
Adversarial review confirmed all three. They are not worth closing here because
they are strictly more expensive than the passes already listed above — an
attacker who knows the rule exists takes `curl … | sh` and never touches a
credential path. The rule is aimed at the malware that does not know, which is
most of it; the ASK ceiling and the judge reading SKILL.md are what stand behind
it for the rest.

**Skills are judged with their own prompt.** A skill file exists to instruct an
agent, so the package prompt — whose question is whether content is trying to
instruct an agent — flagged legitimate skills for existing. Measured against a
set of real installed benign skills, it blocked a substantial number of them:
imperative persistence language ("ACTIVE EVERY RESPONSE", "YOU MUST", "not
negotiable") and Claude Code's own `` !`bash …` `` directive both read as attacks.
The same judge left popular npm packages essentially untouched, so the model was
fine and the question was wrong.

`JudgeInput.kind` now routes skills to `SKILL_SYSTEM_PROMPT`, which treats
directive tone and in-bundle script loading as normal and reports only
instructions to do something the skill does not openly claim: concealment from
the user, credential theft, external exfiltration, remote code from outside the
bundle, scope mismatch against the declared description, sabotage of security
tooling, and obfuscated payloads. Scored A/B over identical inputs it blocks no
benign skill in the control set while blocking slightly more of the corpus's
malicious ones; the cost is a smaller ASK band. `good-skill-persistent-behavior/`
is the fixture that pins the benign side. Counts are in the engine repo's
corpus-eval report.

Regression test: tests/mcp/agent-artifacts-corpus.test.ts
