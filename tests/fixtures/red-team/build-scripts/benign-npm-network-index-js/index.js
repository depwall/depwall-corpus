// Realistic benign npm install script: fetch the prebuilt binary matching this
// platform, the esbuild/sharp/playwright shape. Network + env reads + platform
// detection together, and all three must stay clean.
//
// This is the false-positive trap for the npm body scan: os.platform()/arch()
// answer WHAT-PLATFORM (pick an artifact), not WHO-AND-WHERE (identify a
// victim), and npm_config_* / https_proxy are not secrets. A rule that cannot
// tell these apart would ASK on every native package with a download step.
// The version-check and yarn-detection blocks below are not decoration. They
// are the shape that produced the ONE false positive when this rule was
// measured over 5,973 popular npm packages (@depot/cli): a `JSON.stringify`
// used for an error message, and an unrelated `process.env` read a few lines
// later. A span-matching env-harvest pattern joins those two into
// "stringify of the environment" and BLOCKs a legitimate CLI installer.
const os = require("os");
const https = require("https");
const fs = require("fs");

const target = `${os.platform()}-${os.arch()}`;
const proxy = process.env.npm_config_https_proxy || process.env.HTTPS_PROXY;
const url = `https://registry.example/prebuilds/${target}.tar.gz`;

function checkVersion(fromPackageJSON, fromStdout) {
  if (fromStdout !== fromPackageJSON) {
    throw new Error(
      `Expected ${JSON.stringify(fromPackageJSON)} but got ${JSON.stringify(fromStdout)}`,
    );
  }
}

function isYarn() {
  const { npm_config_user_agent } = process.env;
  return npm_config_user_agent ? /\byarn\//.test(npm_config_user_agent) : false;
}

https.get(url, { agent: proxy ? undefined : false }, (res) => {
  res.pipe(fs.createWriteStream(`prebuild-${target}.tar.gz`));
});

module.exports = { checkVersion, isYarn };
