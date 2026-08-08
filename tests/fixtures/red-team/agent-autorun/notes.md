# Agent auto-run configs

Files an IDE or coding agent executes **just because a repository was opened** —
no install, no explicit run, no user action beyond `code .` or pointing an agent
at a checkout.

## Why this class exists

The Keyv / Cacheable npm compromise (Aug 2026, 779 packages) used exactly this.
From Snyk's write-up:

> Unlike more common npm supply chain attacks that rely only on preinstall or
> postinstall scripts, this activity also executes through IDE auto-run hooks
> (`.claude/settings.json`, `.vscode/tasks.json`) — triggering code execution
> simply when an affected repository is opened in an IDE or coding agent.

DepWall already vetted `.mcp.json`, `mcp.json`, `claude_desktop_config.json` and
`SKILL.md`. It did **not** look at `.claude/settings.json` or `.vscode/tasks.json`
— measured, not assumed, before this class was added.

This is the sharpest possible version of DepWall's own thesis. The gate stops a
package before its code runs; an auto-run config is code that runs without any
package being installed at all, so the install gate never sees it. The Write/Edit
hook is the only surface that can catch it, and it was not looking.

## Payload discipline

Every payload here is **inert**. Real ones fetched a Bun runtime and ran an
obfuscated loader; these use `echo` and a `REDACTED.example` host, so the SHAPE
is preserved and nothing here can do anything if it were ever executed by
accident. See ../../../../docs/TESTING-SAFETY.md.

## Fixtures

| file | shape |
|---|---|
| `claude-settings-hook-curl.json` | `.claude/settings.json` PreToolUse hook piping a remote script to a shell |
| `claude-settings-hook-benign.json` | a real DepWall hook — must NOT fire, this is the false-positive control |
| `vscode-tasks-folder-open.json` | `.vscode/tasks.json` with `runOptions.runOn: folderOpen` |
| `vscode-tasks-benign.json` | an ordinary build task — must NOT fire |
