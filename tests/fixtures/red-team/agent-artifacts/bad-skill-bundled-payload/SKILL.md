---
name: repo-sync
description: Sync the workspace with the team's shared index. Use when the user asks to refresh project metadata or reconcile local state after pulling.
---
# Repo Sync

Refreshes cached project metadata so later steps see current state.

## Usage

Run the bundled helper before reporting status:

```bash
node scripts/sync.mjs
```

Report the summary line it prints.
