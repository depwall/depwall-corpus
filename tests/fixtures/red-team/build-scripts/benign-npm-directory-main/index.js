// INERT FIXTURE — never executed.
//
// FALSE-POSITIVE TRAP for the manifest-redirect round. Structurally identical
// to `exfil-npm-directory-main/`: entry point requires a DIRECTORY whose
// `package.json` main points at the file that really runs.
//
// A subdirectory carrying its own manifest is ordinary layout, not a tell —
// it is how packages keep an install helper's dependencies and `type` field
// separate from the published root. Following the redirect must therefore judge
// the target on what the target DOES, and this one must produce zero findings.
const { install } = require("./scripts");

install({ verbose: process.env.npm_config_loglevel === "verbose" });
