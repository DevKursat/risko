#!/usr/bin/env bash
set -euo pipefail

if [ -z "${SUPABASE_URL:-}" ] || [ -z "${SUPABASE_SERVICE_ROLE_KEY:-}" ]; then
  echo "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment"
  exit 1
fi

python worker.py
