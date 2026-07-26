# Attack class: standalone remote acquisition (`git clone`, `curl | sh`)

Two acquisition vectors that reach code execution without any package manager:
cloning a repo from an unverified host, and piping a remote script straight
into a shell. Neither passes through npm/pip/cargo, so neither is covered by
the install-time manager gates.

`commands.jsonl` holds inert command strings with the expected block decision.
Malicious shapes include clones from an attacker host, a raw IP, and a
plain-HTTP downgrade; plus `curl | sh`, `wget | bash`, `curl | sudo bash`,
`sh -c "$(curl …)"`, and `bash <(curl …)`. Controls include clones from
github/gitlab, non-clone git subcommands, a `curl` writing to a file with no
shell sink, and a local `cat | sh` with no remote fetch.

Known gap: `curl` has no PATH shim — pipe-to-shell is enforced in the Claude
agent hook, not in a human shell.

Regression test: tests/hook/remote-exec-corpus.test.ts
