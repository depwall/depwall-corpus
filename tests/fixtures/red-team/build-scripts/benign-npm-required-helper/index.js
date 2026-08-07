// INERT FIXTURE — never executed.
//
// FALSE-POSITIVE TRAP for require-graph following, and the whole reason that
// feature is bounded rather than greedy. Structurally identical to
// `exfil-npm-required-helper/`: `preinstall: node index.js`, an entry point that
// does nothing but require a sibling and call it. Deferring the install step to
// a module is ordinary packaging, not a tell — prebuild-install, node-gyp
// wrappers and every native addon are shaped exactly like this.
//
// Following the require must therefore judge the helper on what the helper
// DOES. This one selects a build artifact for the current platform and falls
// back to compiling; it must produce zero findings.
const { install } = require("./lib/install");

install({ verbose: process.env.npm_config_loglevel === "verbose" });
