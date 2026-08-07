---
name: deploy-key-bootstrap
description: Create a dedicated deploy key for a repository and register its public half with the forge.
---

# Deploy key bootstrap

Creates a repo-scoped deploy key so CI can pull without a personal credential,
then registers the public half with the forge.

Run `scripts/bootstrap-deploy-key.sh`. It is idempotent — if the key already
exists it re-registers the existing public half rather than rotating it.

Only the public half ever leaves the machine.
