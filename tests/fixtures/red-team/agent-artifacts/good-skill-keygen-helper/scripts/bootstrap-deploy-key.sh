#!/usr/bin/env bash
# INERT FIXTURE — never executed, contains no credential value.
#
# The second false-positive trap: a helper that legitimately NAMES credential
# store paths, reads one back, and makes a network call in the same breath —
# because it is CREATING the credential and registering it, not stealing it.
# Setting up a deploy key is an ordinary devops-skill job.
#
# A rule that only asks "does a credential path appear near a read near a
# request?" halts this. The discriminator is structural rather than statistical:
# a path being CREATED cannot be a path being STOLEN, so a creation verb next to
# the path suppresses the match at any corpus size.
set -uo pipefail

KEY_PATH="$HOME/.ssh/id_ed25519_deploy"

if [ ! -f "$KEY_PATH" ]; then
  ssh-keygen -t ed25519 -N "" -C "deploy@example" -f "$KEY_PATH"
fi

# Register the PUBLIC half with the forge so CI can pull.
PUBKEY=$(cat "$KEY_PATH.pub")

curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data "{\"key\":\"$PUBKEY\",\"title\":\"deploy\"}" \
  "https://api.REDACTED.example/repos/acme/app/keys"

echo "deploy key registered"
