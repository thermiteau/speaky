#!/usr/bin/env bash
set -euo pipefail

# Fallback text can be passed as arg 1 or defaults to this string
FALLBACK="${1:-I need your input to proceed.}"

# Read stdin (the hook payload)
payload="$(cat || true)"

# Extract .message if present; empty string if not
msg="$(printf '%s' "$payload" | jq -r 'try .message // empty' 2>/dev/null || true)"

# Fallback if missing/null/empty
if [[ -z "$msg" || "$msg" == "null" ]]; then
  msg="$FALLBACK"
fi

# Call your TTS
speaky "$msg"
