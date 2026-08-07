// INERT FIXTURE — never executed. Reduced from @ottocode/install's start.js,
// a real package this rule BLOCKED before shell text was required to sit
// inside a spawn.
//
// FP trap: a JS installer that FAILS prints the manual-install command so the
// developer can recover. That string contains `curl https://... | sh`, which
// the shell-exfil patterns match on sight. Those patterns were written for
// setup.py/build.rs, where shell text in the file IS shell about to run; in a
// JS file it is just as often a message. The distinction that matters is
// whether the command is executed or printed.
const { spawnSync } = require("child_process");

function installBinary() {
  const res = spawnSync("node-gyp", ["rebuild"], { stdio: "inherit" });
  if (res.status === 0) return true;

  console.error("Failed to install the otto CLI:", res.error && res.error.message);
  console.error("\nPlease try installing manually:");
  console.error("  curl -fsSL https://REDACTED.example/install | sh");
  console.error("\nOr, if you use a private registry, set NPM_TOKEN first.");
  return false;
}

if (!installBinary()) process.exit(1);
