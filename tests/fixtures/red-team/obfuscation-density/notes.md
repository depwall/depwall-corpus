# Machine-obfuscated install-time code

An npm install-script entry point that has been run through a JavaScript
obfuscator: escaped string tables, `_0x`-prefixed identifiers, member names
assembled at runtime. No `eval`, no network call, no environment read anywhere
in the source.

## Why this class exists

`build-scripts` matches SHAPES — `eval(atob(`, `new Function(Buffer.from(`,
a network call sitting near a secret read. Every commercial JS obfuscator emits
none of them, because **avoiding a recognisable shape is the entire point of
running one**. The fixtures here contain no dangerous API at all, and the test
asserts that before asserting the detection, so this class cannot quietly become
a duplicate of the one next door.

So this signal measures density instead of presence: how much of the body is
concealment machinery.

## Minified is not obfuscated

This is the whole design problem, and it is why the signal takes **two**
independent indicators rather than one.

A minifier shortens identifiers and strips whitespace. It does not escape string
literals, does not name variables `_0x4f2a`, and does not rewrite `a.b` into
`a['b']`. Measured:

| | escapes/KB | hex identifiers | bracket-access ratio |
|---|---|---|---|
| Obfuscated fixtures | 70–106 | 4–7 | up to 1.00 |
| Plain installer | 0 | 0 | 0.00 |
| The same installer, really minified | 0 | 0 | 0.00 |
| 24 real install-script entry points | **0** | **0** | ≤ 0.20 |

`benign-minified-installer/index.js` is `benign-plain-installer/index.js` put
through a real minifier, not an impression of one.

## False-positive cost, measured

Searched npm for packages that run install scripts, read the entry point out of
each tarball, ran the signal:

- **2,395** candidate packages
- **270** actually declare an install script with a readable entry point
- **1** flagged — `np-audit-test-obfuscated`, whose own description reads
  *"Test fixture for np-audit — simulates a supply chain attack with obfuscated
  postinstall."* A true positive, and someone else's detection test at that.
- **0 false positives**

Reproduce the corpus half of that with the tests; the live sweep is a one-off
because it depends on registry search results that move.

## Why critical rather than warn

`deepEvaluate` fetches tarball bodies **only when the deterministic tier is
already ASK**. A `warn` here would therefore move no verdict anywhere — the
signal either decides or it is decoration. That is the reason for the two-
indicator rule and for the measurement above, not a preference for strictness.

## KNOWN GAP — a body under 200 bytes is not measured

Density on a 60-byte one-liner is arithmetic, not evidence: three escapes in it
reads as 48 escapes/KB. `MIN_BODY_BYTES` is the floor and a payload small enough
to fit under it is not covered here — the other signals have to catch it. The
floor is not free, and it is stated rather than tuned away.

## KNOWN GAP — an obfuscator that avoids all four indicators

The indicators are escapes, `_0x` identifiers, bracketed-string member access,
and runtime name assembly. An obfuscator that renames to plain short identifiers
and leaves strings readable produces something that looks like minified output,
and this will not fire on it. That is the honest cost of not firing on real
minified installers, which is the trade this class exists to make.

## Fixtures

| File | What it is |
|---|---|
| `obfuscated-hex-string-array/` | The javascript-obfuscator signature: rotated `\x`-escaped string array, `_0x` identifiers, bracketed dispatch |
| `obfuscated-unicode-escape/` | Every string `\u`-escaped; no array, no rotation |
| `obfuscated-charcode-build/` | Member names built from character codes at runtime — no escapes at all, caught by the other arms |
| `benign-plain-installer/` | Control — an ordinary prebuilt-binary installer |
| `benign-minified-installer/` | Control — that same file through a real minifier |
| `benign-inline-asset/` | Control — a long legitimate base64 blob, which a naive "encoded bytes" check would flag |

Payloads are `console.log` of an inert marker. Only the shape is real; nothing
here is executable malware and no live sample is reproduced.

The 24 real install-script entry points used as the false-positive baseline live
in `tests/fixtures/installer-corpus/`, deliberately **outside** this tree: they
are other projects' files, kept locally rather than republished in the public
corpus.

## Adversarial pass

Run before merge, per the repo rule. What it found:

| Attack | Result |
|---|---|
| Split the payload across four 150-byte files, each under the measurement floor | **Was a complete bypass.** Sub-floor bodies are now judged together; a body at or over the floor is still judged alone, so dilution stays closed |
| Pad an obfuscated body with 6 KB of clean comment to sink the ratio | Caught — hex-identifier and bracket counts are counts, not ratios |
| A file that is nothing but 120 legitimate `\u` escapes (emoji table) | Silent. One indicator is a style; the two-indicator rule is what makes this a non-event |
| Catastrophic backtracking on 100k brackets / 200k escapes | No blow-up — 0.4 ms and 27 ms. Bodies are attacker-controlled bytes, so a hang here would be a denial of verdict |
| Rename away from the `_0x` prefix | Residual, and documented above as a known gap: escapes and bracket dispatch still have to carry it alone |
