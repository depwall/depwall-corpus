#!/usr/bin/env bash
# INERT FIXTURE — never executed. FALSE-POSITIVE CONTROL for the whole-directory
# credential arm, and NOT invented: this is the shape of the eight GitHub
# Actions deploy workflows that the directory arm flagged when it was first
# measured over 17,027 real files on a developer machine. Every one of them
# provisions ~/.ssh a few lines from an `unzip` and a `curl`, which is a
# credential directory, an archive verb and a network sink inside 400 chars.
#
# What makes it benign is structural: the directory is being CREATED and
# locked down, not read out. Same argument as the ssh-keygen suppressor.
#
# It also publishes the PUBLIC half of a key, which must stay allowed: `.pub` is
# meant to leave the machine.
set -uo pipefail

if ! command -v aws >/dev/null 2>&1; then
  curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "$TMPDIR/awscliv2.zip"
  unzip -q "$TMPDIR/awscliv2.zip" -d "$TMPDIR"
  "$TMPDIR/aws/install" --install-dir "$TMPDIR/awscli" --bin-dir "$TMPDIR/awsbin"
fi

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

cat >> "$HOME/.ssh/config" <<'EOF'
Host git.example.com
  User git
  IdentitiesOnly yes
EOF

curl -sS https://git.example.com/meta/host-keys >> "$HOME/.ssh/known_hosts"

if [ -f "$HOME/.ssh/id_ed25519.pub" ]; then
  cat "$HOME/.ssh/id_ed25519.pub" \
    | curl -sS -X POST --data-binary @- https://directory.example.com/machines
fi

echo "Provisioned."
