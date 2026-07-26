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
| `bad-skill-bundled-payload/` | clean SKILL.md; payload in `scripts/sync.mjs` | **ALLOW — KNOWN GAP** |
| `good-skill-persistent-behavior/SKILL.md` | benign style skill that overrides agent behavior by design (control) | ALLOW |

Known gap: true MCP tool-poisoning lives in a live server's `tools/list`
metadata, reachable only by connecting to it — out of scope by design.

**Known gap: bundled helper files.** `checkAgentArtifacts` collects `SKILL.md`
and MCP configs; nothing else in a skill directory is opened. A bundle whose
markdown is unremarkable and whose `scripts/*.mjs` does the stealing passes.
Measured over the 204 malicious AI-skill bundles in
DataDog/malicious-software-packages-dataset: 66 ship executable helpers
(`.py`/`.js`/`.mjs`/`.ts`/`.sh`) and 33 of those helpers reference the network,
the environment, or credential paths — while 138 are markdown-only, where the
judge is the right instrument. `bad-skill-bundled-payload/` pins the gap; the
full measurement is recorded in the engine repo's corpus-eval report.

**Known gap: the judge prompt is written for PACKAGES, and a skill is not a
package.** Scored against the public corpus's malicious skills it carries the
class — most were flagged, and injection was the dominant reason. Scored against
a set of real installed *benign* skills it also flagged a large share of them,
because the thing it looks for — content instructing an agent to change its
behavior — is what a legitimate style or process skill *is*. Two recurring
causes: imperative persistence language ("ACTIVE EVERY RESPONSE", "YOU MUST",
"not negotiable"), and Claude Code's own `` !`bash …` `` directive, read as
command injection. The same judge on the same model left popular npm packages
essentially untouched, so this is the package prompt applied to an artifact type
it was not written for, not a miscalibrated model. Closing it needs a
skill-specific prompt that separates declared in-scope behavior from covert
redirection (exfil endpoints, credential paths, "do not tell the user",
instructions unrelated to the stated purpose).
`good-skill-persistent-behavior/` is the target fixture; counts are in the
engine repo's corpus-eval report.

Regression test: tests/mcp/agent-artifacts-corpus.test.ts
