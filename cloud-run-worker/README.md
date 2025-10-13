# Cloud Run Worker PoC

This folder contains a minimal Cloud Run worker proof-of-concept that polls a
Supabase `jobs` table via the REST API, performs a CPU-bound simulation, writes
the result into `cached_results`, and updates the job status.

Usage (local):

1. Set environment variables locally (do not commit keys):

```bash
export SUPABASE_URL=https://<your>.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
export POLL_INTERVAL=5
export WORKER_ID=local-1
```

2. Build and run locally (requires Docker):

```bash
docker build -t risko-worker:local .
docker run --rm -e SUPABASE_URL -e SUPABASE_SERVICE_ROLE_KEY -e POLL_INTERVAL -e WORKER_ID risko-worker:local
```

3. Or run directly with Python (recommended for quick tests):

```bash
pip install -r requirements.txt
python worker.py
```

Deployment to Cloud Run:

Use `gcloud run deploy` and pass the SUPABASE_* env vars via Secret Manager or
as environment variables (prefer Secret Manager). See the repo's `CI/CD` docs
for an example workflow.

Notes:
- This PoC uses a simple GET->PATCH lease method which may race. For
  production, prefer selecting rows with FOR UPDATE SKIP LOCKED or using
  Postgres advisory locks.
- Rotate SUPABASE_SERVICE_ROLE_KEY regularly and store it in Secret Manager.
