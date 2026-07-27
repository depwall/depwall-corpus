# DepWall — Red-Team Corpus

The public regression corpus behind [DepWall](https://depwall.com),
a dependency-provenance firewall for AI coding agents.

**[→ Read the detection evidence](docs/EVIDENCE.md)**

## What DepWall is

At install time — the moment an agent runs `npm install X` or `git clone` —
DepWall answers *"is this package safe to pull, or engineered to poison my
agent?"* It gates malicious dependencies, **slopsquats** (hallucinated package
names attackers pre-register), and **repos and packages crafted to manipulate
the LLM itself** into pulling attacker code.

Existing tools scan dependencies for known vulnerabilities; runtime agent guards
watch what an agent *does*. DepWall guards what an agent *installs*.

## What this repository is

Every attack shape DepWall claims to detect has a regression fixture. This
repository is that corpus, copied verbatim from the test suite, plus the
evidence page generated from it.

```
tests/fixtures/red-team/   the fixtures, one directory per attack class
docs/EVIDENCE.md           generated: every fixture, its verdict, its signals
docs/ANTI-HALLUCINATION.md why this project refuses to state unverified claims
docs/TESTING-SAFETY.md     why nothing here is executable
```

The directory depth matches the private repository so that every relative link
inside the fixtures resolves. These files are byte-identical to the ones the
test suite loads — that is a property you can check, not a promise.

## What this repository is not

**It is not the engine.** The signals engine, the LLM judge, the shell hook and
the verdict cache are not published. You can read what DepWall detects and what
it misses; you cannot yet recompute the verdicts yourself. `docs/EVIDENCE.md`
says so in its own words rather than leaving you to work it out.

**It is not a benchmark.** The fixtures are self-authored — each was written
alongside the detection it exercises. A recall percentage over them would
measure whether our tests agree with our own code. The evidence page publishes
no recall rate and no false-positive rate, and explains why.

**It is not runnable.** Every fixture is inert, redacted metadata. Nothing here
is installed or executed, and neither should you — see
[TESTING-SAFETY.md](docs/TESTING-SAFETY.md).

## Known gaps are published, not hidden

`docs/EVIDENCE.md` lists the attack shapes DepWall **does not** catch, including
one fixture that is a documented miss. A security tool that publishes only its
wins is asking for trust it has not earned. If you find a shape that evades
DepWall and is not on that list, that is a bug and we want the fixture — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Contributing

New attack shapes are the most valuable contribution. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the fixture format, and
[SECURITY.md](SECURITY.md) if the shape is unpublished or otherwise sensitive.

Questions and discussion: the **Discussions** tab.

## License

Apache-2.0. See [LICENSE](LICENSE).
