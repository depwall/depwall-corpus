# INERT FIXTURE — never executed.
#
# The legitimate half of the deferred-import pair, and it is deliberately not
# trivial: it reads the environment, inspects the platform and spawns a
# subprocess, which is most of what the AND-gates look at. Every one of them is
# ordinary packaging.
#
# The distinction `benign-platform-wheel-setup-py/` already pins, restated one
# import away: platform lookups choose an ARTIFACT, identity lookups choose a
# VICTIM. Nothing here is concealed, no whole-environment serialization, no
# secret-named read, and the only network-shaped thing is absent entirely.
import os
import sys
import platform
import subprocess
from pathlib import Path


def _cache_dir():
    # Honour the build system's own config, not the user's identity.
    root = os.environ.get("PIP_CACHE_DIR") or os.environ.get("XDG_CACHE_HOME")
    return Path(root) / "inert-fixture" if root else Path.home() / ".cache" / "inert-fixture"


def _target():
    return f"{platform.system().lower()}-{platform.machine()}"


def build_cache():
    out = _cache_dir()
    out.mkdir(parents=True, exist_ok=True)
    (out / "target").write_text(_target(), encoding="utf-8")

    # Compile the bundled extension the ordinary way. Plain argv, nothing
    # encoded, no shell.
    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", str(Path(__file__).parent)],
        check=False,
    )
    if result.returncode != 0:
        print("bytecode precompile skipped", file=sys.stderr)
    return out
