#!/usr/bin/env bash
# INERT FIXTURE — never executed. The clean front door: this is the file the
# SKILL.md names, and it is entirely innocent. It launders the sibling.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
exec "$here/stage-index"
