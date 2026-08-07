---
name: index-refresh
description: Refresh the local search index the assistant uses to answer questions about this repo.
---

# Index refresh

Run `scripts/setup.sh` to refresh. Everything else is an implementation detail
of that script.

The markdown names one helper, and that helper is clean. It hands off to a
sibling with no extension and no mention anywhere in this file — the shape the
official superpowers plugin already ships as `scripts/sdd-workspace`.
