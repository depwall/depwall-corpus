#!/usr/bin/env bash
# INERT FIXTURE — never executed, contains no credential value. Copied in SHAPE
# from the real ~/.claude/skills/turnstile-spin helpers, a skill installed on
# this machine on purpose.
#
# THE false-positive trap for a helper-body rule. This short, single-purpose
# script reads a whole-segment secret-NAMED env var and immediately makes an
# authenticated request with it, because that is literally the script's job.
# Any rule shaped "secret-named env read AND network call" blocks it, and
# proximity bounding cannot save it: the read and the curl sit close together
# precisely BECAUSE they are related.
#
# This is the npm lesson (PR #84) inverted. Helper scripts are short and
# single-purpose, which does NOT restore co-occurrence as evidence — it removes
# the only defence, because a short helper's declared purpose is routinely
# "call a vendor API with the user's token".
set -uo pipefail

while [[ $# -gt 0 ]]; do
  case $1 in
    --account-id) ACCOUNT_ID="$2"; shift 2 ;;
    --sitekey)    SITEKEY="$2"; shift 2 ;;
    *) echo "fetch-widget got an unknown arg $1" >&2; exit 2 ;;
  esac
done

if [ -z "${VENDOR_API_TOKEN-}" ]; then
  echo "fetch-widget needs VENDOR_API_TOKEN in the environment" >&2
  exit 1
fi

RESPONSE=$(curl -sS \
  -H "Authorization: Bearer ${VENDOR_API_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.REDACTED.example/v4/accounts/${ACCOUNT_ID}/widgets/${SITEKEY}")

echo "$RESPONSE" | jq -r '.result.name'
