// INERT FIXTURE — never executed. Host is REDACTED.example.
//
// The legitimate half of the manifest-redirect pair. Reached the same way as
// the payload in `exfil-npm-directory-main/` — entry requires a directory, the
// directory's package.json main names this file — and it does the ordinary
// native-addon install: npm's own build config (never a secret name, never a
// whole-environment harvest), a request that selects a PREBUILT ARTIFACT by
// platform rather than identifying a victim, and a plain unconcealed
// node-gyp fallback.
const os = require("os");
const https = require("https");
const { spawnSync } = require("child_process");

function target() {
  const arch = process.env.npm_config_arch || os.arch();
  const platform = process.env.npm_config_platform || os.platform();
  return `${platform}-${arch}`;
}

function fetchPrebuilt(url, onDone) {
  const req = https.get(url, (res) => {
    if (res.statusCode !== 200) return onDone(new Error(`HTTP ${res.statusCode}`));
    const chunks = [];
    res.on("data", (c) => chunks.push(c));
    res.on("end", () => onDone(null, Buffer.concat(chunks)));
  });
  req.on("error", onDone);
}

function buildFromSource(verbose) {
  const result = spawnSync("node-gyp", ["rebuild"], { stdio: verbose ? "inherit" : "ignore" });
  if (result.status !== 0) {
    console.error("prebuilt binary unavailable and node-gyp rebuild failed");
  }
  return result.status === 0;
}

function install(opts) {
  fetchPrebuilt(`https://REDACTED.example/prebuilds/${target()}.node`, (err) => {
    if (err) buildFromSource(opts.verbose);
  });
}

module.exports = { install, target };
