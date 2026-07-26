# Security policy

## Reporting a missed detection

DepWall is a security tool, so "it failed to catch X" is a security report, not
a feature request.

Use **GitHub private vulnerability reporting** on this repository
(Security → Report a vulnerability), or email **security@depwall.com** if you
would rather not use GitHub, for anything that should not be public yet:

- an attack shape that evades DepWall and is **not** already listed under
  *Known gaps* in [docs/EVIDENCE.md](docs/EVIDENCE.md);
- a way to bypass a gate DepWall claims to enforce;
- a live malicious package or repository in the wild.

Shapes already published as known gaps can be discussed openly — they are
documented precisely so they do not need to be secret.

## What to include

- The shape: what an attacker constructs, and why it slips through.
- What you expected DepWall to do, and what it did.
- An inert fixture if you can produce one — metadata and text only, exfiltration
  targets replaced with `REDACTED.example`.

**Do not attach live malware, real credentials, or working payloads.** DepWall's
own corpus is inert by policy ([TESTING-SAFETY.md](docs/TESTING-SAFETY.md)) and
this repository will not accept anything that is not.

## What to expect

An acknowledgement, and a fixture added to the corpus once the shape is
confirmed. If it turns out DepWall cannot detect it, it is published as a
documented gap rather than quietly dropped.

## Scope

This repository contains no executable code — it is fixtures and documentation.
Reports about the engine, the CLI, or the verdict cache are still welcome here;
they will be routed to the private repository where that code lives.
