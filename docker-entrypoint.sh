#!/bin/sh
set -e

CLOUDFLARE_TUNNEL_URL=${CLOUDFLARE_TUNNEL_URL:-http://127.0.0.1:8000}

if [ "${CLOUDFLARE_TUNNEL:-false}" = "true" ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000 &
  if [ -n "$CLOUDFLARE_TOKEN" ]; then
    exec cloudflared tunnel run --token "$CLOUDFLARE_TOKEN" --url "$CLOUDFLARE_TUNNEL_URL"
  fi
  exec cloudflared tunnel run --url "$CLOUDFLARE_TUNNEL_URL"
fi

exec "$@"
