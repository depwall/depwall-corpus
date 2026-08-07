// INERT FIXTURE — never executed.
//
// The decoy entry point, one level more indirect than
// `exfil-npm-required-helper/`. The lifecycle script is
// `preinstall: node index.js`; this file requires a DIRECTORY and calls it.
//
// There is no `lib/index.js`. Node's LOAD_AS_DIRECTORY reads `lib/package.json`
// and honours its `main` first, so `lib/run.js` is what actually executes at
// install — a file the entry point never names and the extension candidates
// (`lib.js`, `lib.cjs`, `lib.mjs`, `lib/index.js`) never reach.
//
// Verified against node 22, not assumed: with both `lib/package.json` main and
// `lib/index.js` present, main wins.
const { run } = require("./lib");

run({ quiet: process.env.npm_config_loglevel === "silent" });
