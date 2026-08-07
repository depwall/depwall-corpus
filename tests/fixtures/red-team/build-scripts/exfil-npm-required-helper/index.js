// INERT FIXTURE — never executed.
//
// The entry point is a DECOY, and it stays asserted clean ON ITS OWN: the
// lifecycle script is `preinstall: node index.js`, the scan opens index.js as
// designed, and index.js does nothing hostile. It requires a sibling module and
// calls it — which is also how a large share of legitimate packages structure
// an install step, so no pattern applied to THIS file can separate them.
//
// The hostile code lives in `./lib/setup.js`, one file over. This was the
// pinned known gap (`gap-npm-required-helper/`) until the tarball walker
// learned to follow the relative require graph one hop out of the entry point
// and scan what it reaches. Its false-positive twin is
// `benign-npm-required-helper/`, identical in shape, which must stay clean.
const { configure } = require("./lib/setup");

configure({ quiet: process.env.npm_config_loglevel === "silent" });
