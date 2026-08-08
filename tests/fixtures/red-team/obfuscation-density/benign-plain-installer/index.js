// A prebuilt-binary installer in the ordinary shape: pick the platform package,
// fall back to building from source, fail loudly rather than silently.
// Written for this corpus rather than copied from a real package, so nothing
// third-party is republished here.
"use strict";

const { existsSync, chmodSync, mkdirSync, createWriteStream } = require("node:fs");
const { join, dirname } = require("node:path");
const { spawnSync } = require("node:child_process");
const os = require("node:os");

const PLATFORMS = {
  "darwin-arm64": "@example/tool-darwin-arm64",
  "darwin-x64": "@example/tool-darwin-x64",
  "linux-x64": "@example/tool-linux-x64",
  "linux-arm64": "@example/tool-linux-arm64",
  "win32-x64": "@example/tool-win32-x64",
};

function platformKey() {
  return `${os.platform()}-${os.arch()}`;
}

function resolvePrebuilt() {
  const pkg = PLATFORMS[platformKey()];
  if (!pkg) return null;
  try {
    return require.resolve(`${pkg}/bin/tool`);
  } catch {
    return null;
  }
}

function buildFromSource(destination) {
  mkdirSync(dirname(destination), { recursive: true });
  const result = spawnSync("node-gyp", ["rebuild"], { stdio: "inherit", shell: false });
  if (result.status !== 0) {
    throw new Error(
      `Could not build the native addon for ${platformKey()}. ` +
        `Install a toolchain, or file an issue with the output above.`,
    );
  }
  return destination;
}

function main() {
  const target = join(__dirname, "bin", "tool");
  if (existsSync(target)) {
    return;
  }
  const prebuilt = resolvePrebuilt();
  const binary = prebuilt ?? buildFromSource(target);
  chmodSync(binary, 0o755);
  console.log(`tool: using ${prebuilt ? "prebuilt binary" : "locally built addon"} for ${platformKey()}`);
}

try {
  main();
} catch (err) {
  console.error(`tool install failed: ${err.message}`);
  process.exit(1);
}
