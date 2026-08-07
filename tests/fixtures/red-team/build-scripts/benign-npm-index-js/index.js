// Realistic benign npm install script: the node-gyp rebuild every native
// addon runs. Spawns a child process and reads npm's own config env vars —
// must NOT trip the deterministic signal. Spawning alone is never a finding;
// if it were, every native addon on the registry would ASK.
const { spawnSync } = require("child_process");

const jobs = process.env.npm_config_jobs || "max";
const python = process.env.npm_config_python || "python3";

const res = spawnSync("node-gyp", ["rebuild", `--jobs=${jobs}`, `--python=${python}`], {
  stdio: "inherit",
});

process.exit(res.status ?? 0);
