// INERT FIXTURE — never executed. Reduced from @scarf/scarf@1.4.0's report.js,
// a real package with millions of weekly installs that this rule BLOCKED
// before proximity bounding.
//
// FP trap: opt-out install telemetry legitimately does all three things the
// AND-gates look for — reads the user identity, reads its own vendor-namespaced
// API token, and makes an https request — but they are unrelated statements
// hundreds of lines apart. File-scale co-occurrence welds them into two
// separate "exfiltration" gates. Real exfil builds its payload and sends it in
// the same breath; that is the difference this fixture pins.
//
// The padding between the three markers is load-bearing: shrink it and the
// fixture stops testing what it exists to test.
const os = require("os");
const https = require("https");

function userInfo() {
  // identity read, for the "which developer opted out" record
  const username = os.userInfo().username;
  return username ? username.slice(0, 32) : "unknown";
}

function analyticsDisabled() {
  return (
    process.env.SCARF_ANALYTICS === "false" ||
    process.env.SCARF_NO_ANALYTICS === "true" ||
    process.env.DO_NOT_TRACK === "1"
  );
}

function rootPackageOf(dir) {
  // Walk upward looking for the consuming project's manifest, so the report can
  // name the direct dependent rather than this package. Deliberately verbose:
  // real installers carry hundreds of lines of this kind of bookkeeping between
  // the interesting calls.
  let current = dir;
  for (let depth = 0; depth < 32; depth++) {
    const parent = current.replace(/\/[^/]+$/, "");
    if (!parent || parent === current) return null;
    current = parent;
  }
  return current;
}

function dependencyChain(pkg) {
  const chain = [];
  let node = pkg;
  while (node && chain.length < 64) {
    chain.push({ name: node.name, version: node.version });
    node = node.parent;
  }
  return chain;
}

function shouldReport(pkg) {
  if (analyticsDisabled()) return false;
  if (!pkg || !pkg.name) return false;
  if (process.env.npm_config_global) return false;
  return true;
}

function buildPayload(pkg) {
  return {
    packageName: pkg.name,
    packageVersion: pkg.version,
    reportedUser: userInfo(),
    dependencyChain: dependencyChain(pkg),
    platform: `${os.platform()}-${os.arch()}`,
  };
}

// The vendor's own token, for authenticated reporting against their own
// endpoint. A whole-segment secret name — and entirely legitimate here.
function authHeaders() {
  const scarfApiToken = process.env.SCARF_API_TOKEN;
  return scarfApiToken ? { Authorization: `Bearer ${scarfApiToken}` } : {};
}

function send(pkg) {
  if (!shouldReport(pkg)) return;
  const data = JSON.stringify(buildPayload(pkg));
  const req = https.request(
    {
      hostname: "REDACTED.example",
      path: "/package-events",
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
    },
    () => {},
  );
  req.on("error", () => {});
  req.write(data);
  req.end();
}

module.exports = { send, rootPackageOf, shouldReport };
