---
name: dev-machine-provision
description: Prepare a fresh dev machine — SSH client config, known hosts, and the team's git remotes.
---

# Dev machine provisioning

Run `scripts/provision.sh` on a new machine. It writes an SSH client config,
pins the git host keys, and registers the machine with the team directory.

This is a CONTROL fixture: it is the benign shape that sits closest to the
whole-directory credential rule.
