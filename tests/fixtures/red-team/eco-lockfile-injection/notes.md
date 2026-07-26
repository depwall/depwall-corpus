# Attack class: lockfile provenance poisoning (Ruby / PHP)

Ruby `Gemfile.lock` and PHP `composer.lock` pin where each dependency is
fetched from. An attacker who edits the lock can keep benign `name@version`
entries while repointing the fetch at their own host, or downgrade the
transport to plain HTTP for a MITM.

| Fixture | Vector | Expected |
|---|---|---|
| `poisoned-Gemfile.lock` | `remote:` repointed to an attacker host | ASK |
| `poisoned-composer.lock.json` | `dist.url` repointed to an attacker host | ASK |
| `http-Gemfile.lock` | plain-HTTP transport downgrade | ASK |
| `http-composer.lock.json` | plain-HTTP transport downgrade | ASK |
| `private-mirror-Gemfile.lock` | legitimate uniform private mirror (control) | ALLOW |
| `private-satis-composer.lock.json` | legitimate Satis private repo (control) | ALLOW |

Regression test: tests/hook/ecoprovenance.test.ts
