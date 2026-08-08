# DepWall Advisories

Real supply-chain incidents, and **what DepWall's engine actually returns for each one**.

Every verdict below is recomputed by running the incident's package record through `evaluate()` when this file is generated. None of them is a hand-written claim, which is why a row can say the engine **missed** something.

These are documents. DepWall's client does not read this feed, and no advisory here changes a verdict on your machine — a feed that fed the scanner would be a way to attack the scanner.

| ID | Disclosed | Severity | Class | Incident | DepWall |
|---|---|---|---|---|---|
| [DW-2026-0009](#dw-2026-0009) | 2026-08-04 | CRITICAL | Attested build, poisoned source | keyv/cacheable maintainer compromise (Aug 2026) — malicious release carrying valid npm provenance | **BLOCK** |
| [DW-2026-0005](#dw-2026-0005) | 2026-06-09 | CRITICAL | Worm | Mini Shai-Hulud (TeamPCP), 2026-05-11 — dead-man-switch / wiper stage | **BLOCK** |
| [DW-2026-0006](#dw-2026-0006) | 2026-06-09 | CRITICAL | Worm | Mini Shai-Hulud (TeamPCP), npm/PyPI worm, 2026-05-11 — CI credential-theft stage | **BLOCK** |
| [DW-2026-0007](#dw-2026-0007) | 2026-06-09 | CRITICAL | Worm | Mini Shai-Hulud (TeamPCP), npm/PyPI worm, 2026-05-11 | **ASK** |
| [DW-2026-0008](#dw-2026-0008) | 2026-06-02 | HIGH | Tarball substitution | npm preinstall loader whose payload lives in the tarball (000webhost-admin@999.9.9, discovered 2024-12-14) | **ASK** |
| [DW-2026-0003](#dw-2026-0003) | 2022-03-15 | HIGH | Protestware | node-ipc protestware (March 2022, 'peacenotwar') | ALLOW — **missed** |
| [DW-2026-0001](#dw-2026-0001) | 2021-10-22 | CRITICAL | Account takeover | ua-parser-js account compromise (Oct 2021, CISA alert) | **BLOCK** |
| [DW-2026-0002](#dw-2026-0002) | 2018-11-26 | CRITICAL | Dependency takeover | event-stream / flatmap-stream (Nov 2018) | **BLOCK** |
| [DW-2026-0004](#dw-2026-0004) | 2017-08-01 | HIGH | Typosquat | crossenv / cross-env typosquat wave (Aug 2017) | **BLOCK** |

## DW-2026-0009

**keyv/cacheable maintainer compromise (Aug 2026) — malicious release carrying valid npm provenance**

- **Disclosed:** 2026-08-04
- **Severity:** CRITICAL
- **Class:** Attested build, poisoned source
- **Reference:** https://osv.dev/vulnerability/MAL-2026-11524

DepWall returns **BLOCK** on `attestation`, `install-scripts`, `known-malicious`.

Regression fixture: `keyv-provenance-signed-compromise.json`

## DW-2026-0005

**Mini Shai-Hulud (TeamPCP), 2026-05-11 — dead-man-switch / wiper stage**

- **Disclosed:** 2026-06-09
- **Severity:** CRITICAL
- **Class:** Worm
- **Reference:** https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html

DepWall returns **BLOCK** on `install-scripts`.

Regression fixture: `mini-shai-hulud-wiper.json`

## DW-2026-0006

**Mini Shai-Hulud (TeamPCP), npm/PyPI worm, 2026-05-11 — CI credential-theft stage**

- **Disclosed:** 2026-06-09
- **Severity:** CRITICAL
- **Class:** Worm
- **Reference:** https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html

DepWall returns **BLOCK** on `install-scripts`, `maturity`.

Regression fixture: `mini-shai-hulud-runner-token-theft.json`

## DW-2026-0007

**Mini Shai-Hulud (TeamPCP), npm/PyPI worm, 2026-05-11**

- **Disclosed:** 2026-06-09
- **Severity:** CRITICAL
- **Class:** Worm
- **Reference:** https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html

DepWall returns **ASK** on `attestation`, `remote-dep`.

Regression fixture: `mini-shai-hulud-optional-git-dep.json`

## DW-2026-0008

**npm preinstall loader whose payload lives in the tarball (000webhost-admin@999.9.9, discovered 2024-12-14)**

- **Disclosed:** 2026-06-02
- **Severity:** HIGH
- **Class:** Tarball substitution
- **Reference:** https://github.com/DataDog/malicious-software-packages-dataset (samples/npm/malicious_intent/000webhost-admin/999.9.9)

DepWall returns **ASK** on `install-scripts`, `maturity`.

Regression fixture: `tarball-body-preinstall-loader.json`

## DW-2026-0003

**node-ipc protestware (March 2022, 'peacenotwar')**

- **Disclosed:** 2022-03-15
- **Severity:** HIGH
- **Class:** Protestware
- **Reference:** https://nvd.nist.gov/vuln/detail/CVE-2022-23812

**DepWall does NOT stop this.** The engine returns `ALLOW`. Published anyway — see [ANTI-HALLUCINATION.md](ANTI-HALLUCINATION.md).

Regression fixture: `node-ipc-protestware.json`

## DW-2026-0001

**ua-parser-js account compromise (Oct 2021, CISA alert)**

- **Disclosed:** 2021-10-22
- **Severity:** CRITICAL
- **Class:** Account takeover
- **Reference:** https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js

DepWall returns **BLOCK** on `install-scripts`.

Regression fixture: `ua-parser-js-hijack.json`

## DW-2026-0002

**event-stream / flatmap-stream (Nov 2018)**

- **Disclosed:** 2018-11-26
- **Severity:** CRITICAL
- **Class:** Dependency takeover
- **Reference:** https://github.com/dominictarr/event-stream/issues/116

DepWall returns **BLOCK** on `install-scripts`.

Regression fixture: `event-stream-flatmap-stream.json`

## DW-2026-0004

**crossenv / cross-env typosquat wave (Aug 2017)**

- **Disclosed:** 2017-08-01
- **Severity:** HIGH
- **Class:** Typosquat
- **Reference:** https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry

DepWall returns **BLOCK** on `install-scripts`, `maturity`, `slopsquat`.

Regression fixture: `crossenv-typosquat.json`

