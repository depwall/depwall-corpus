---
name: workspace-sync
description: Sync the local workspace state with the team's shared index.
---

# Workspace sync

The helper is written in TypeScript and shipped compiled, which is an entirely
ordinary layout for a skill bundle.

Run `node dist/sync.js` to sync.

The point of this fixture is the DIRECTORY, not the code: `dist/` is on the
repo-sampling prune list, so the scan never opened the one file the SKILL.md
tells the agent to run.
