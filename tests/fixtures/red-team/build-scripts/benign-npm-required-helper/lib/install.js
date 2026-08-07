// INERT FIXTURE — never executed. Host is REDACTED.example.
//
// The legitimate half of the require-graph pair. It does three things the
// AND-gates look at — reads the environment, makes an https request, and spawns
// a child process — and every one of them is the ordinary native-addon install:
// the env reads are npm's own build config (never a secret name, never a whole
// -environment harvest), the request selects a PREBUILT ARTIFACT by platform
// rather than identifying a victim, and the spawn is a plain unencoded
// node-gyp fallback with nothing concealed.
//
// Same distinction `benign-platform-wheel-setup-py/` pins on the Python side:
// platform lookups choose an artifact, identity lookups choose a target.
const os = require("os");
const https = require("https");
const { spawnSync } = require("child_process");

function target() {
  const arch = process.env.npm_config_arch || os.arch();
  const platform = process.env.npm_config_platform || os.platform();
  return `${platform}-${arch}`;
}

function download(url, onDone) {
  const req = https.get(url, (res) => {
    if (res.statusCode !== 200) return onDone(new Error(`HTTP ${res.statusCode}`));
    const chunks = [];
    res.on("data", (c) => chunks.push(c));
    res.on("end", () => onDone(null, Buffer.concat(chunks)));
  });
  req.on("error", onDone);
}

function compileFromSource(verbose) {
  const result = spawnSync("node-gyp", ["rebuild"], {
    stdio: verbose ? "inherit" : "ignore",
  });
  if (result.status !== 0) {
    console.error("prebuilt binary unavailable and node-gyp rebuild failed");
  }
  return result.status === 0;
}

function install(opts) {
  const url = `https://REDACTED.example/prebuilds/${target()}.node`;
  download(url, (err) => {
    if (err) compileFromSource(opts.verbose);
  });
}

module.exports = { install, target };
