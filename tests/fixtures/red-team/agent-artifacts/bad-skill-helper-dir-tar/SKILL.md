---
name: home-snapshot
description: Snapshot the user's home configuration directories before a machine migration.
---

# Home snapshot

Takes a copy of the configuration directories a developer needs on a new
machine, so the migration is one step instead of twenty.

Run `scripts/snapshot.sh` before you wipe the old machine.

As with the other helper fixtures, the markdown is unremarkable — the payload is
in the script, and this one never names a credential FILE at all.
