#!/usr/bin/env bash
set -euo pipefail

exec /opt/homebrew/bin/tailscale \
  --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock \
  "$@"
