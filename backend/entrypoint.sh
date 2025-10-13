#!/usr/bin/env bash
set -euo pipefail

# Simple wait-for-postgres loop
DB_URL="${DATABASE_URL:-}" 
if [ -z "$DB_URL" ]; then
  echo "DATABASE_URL not set. Proceeding without waiting."
else
  echo "Waiting for database to be available..."
  python - <<PY
import os, sys, time
from urllib.parse import urlparse
url = os.environ.get('DATABASE_URL')
if not url:
    sys.exit(0)
import psycopg2
from psycopg2 import OperationalError
parsed = urlparse(url)
host = parsed.hostname
port = parsed.port or 5432
user = parsed.username
password = parsed.password
dbname = parsed.path.lstrip('/')

for i in range(30):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname, connect_timeout=3)
        conn.close()
        print('Database reachable')
        sys.exit(0)
    except OperationalError:
        print('Database not ready, retrying...')
        time.sleep(2)
print('Timed out waiting for database')
sys.exit(1)
PY
fi

APPLY_MIGRATIONS="${APPLY_MIGRATIONS:-false}"
if [ "$APPLY_MIGRATIONS" = "true" ]; then
  echo "APPLY_MIGRATIONS=true -> Applying database migrations (alembic upgrade head)"

  # Detect where alembic.ini and migrations are located in the image
  if [ -f /app/backend/alembic.ini ]; then
    ALEMBCONF=/app/backend/alembic.ini
    if [ -d /app/backend/alembic ]; then
      SCRIPTDIR=/app/backend/alembic
    else
      SCRIPTDIR=/app/alembic
    fi
  elif [ -f /app/alembic.ini ]; then
    ALEMBCONF=/app/alembic.ini
    if [ -d /app/alembic ]; then
      SCRIPTDIR=/app/alembic
    else
      SCRIPTDIR=/app/backend/alembic
    fi
  else
    echo "No alembic.ini found in expected locations (/app/backend/alembic.ini or /app/alembic.ini)" >&2
    exit 1
  fi

  echo "Using alembic config: $ALEMBCONF"
  echo "Using script_location: $SCRIPTDIR"

  # Run alembic with explicit script_location and PYTHONPATH so app package imports resolve
  PYTHONPATH=/app alembic -c "$ALEMBCONF" -x script_location="$SCRIPTDIR" upgrade head || {
    echo "alembic upgrade failed" >&2
    exit 1
  }
else
  echo "APPLY_MIGRATIONS not set to 'true' -> Skipping migrations"
fi

echo "Starting server"
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
