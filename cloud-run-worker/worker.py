#!/usr/bin/env python3
"""
Simple Cloud Run worker PoC that polls a Supabase 'jobs' table via the REST API
using the service role key, marks jobs as running, performs a CPU-bound dummy
computation (simulating heavy analysis), writes a row into `cached_results`, and
updates the job status to 'done'.

This is intentionally minimal and meant as a PoC. It requires the following
environment variables to be set at runtime:
  - SUPABASE_URL (e.g. https://xxxx.supabase.co)
  - SUPABASE_SERVICE_ROLE_KEY (service role key, keep secret)
  - POLL_INTERVAL (optional, seconds, default 5)
  - WORKER_ID (optional, for logging)

Do NOT commit secrets into the repo. Use Cloud Run environment variables or
Secret Manager to pass the service role key.
"""
import os
import time
import uuid
import json
import math
import logging
from typing import Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("cloud-run-worker")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "5"))
WORKER_ID = os.getenv("WORKER_ID", str(uuid.uuid4())[:8])

if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    logger.error("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    raise SystemExit(1)


HEADERS = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
}


def lease_job() -> Optional[dict]:
    """Attempt to find one queued job and atomically mark it as 'running'.
    We use the Supabase REST API: GET jobs where status=queued, then PATCH the
    same row to set status=running and worker_id. This is a simple lease and
    may race; for production use prefer Postgres advisory locks or
    SELECT...FOR UPDATE via a dedicated worker DB connection.
    """
    url = f"{SUPABASE_URL}/rest/v1/jobs"
    params = {
        "status": "eq.queued",
        "limit": 1,
        "order": "created_at.asc",
        "select": "*",
    }
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json()
        if not items:
            return None
        job = items[0]

        # Try to claim the job
        job_id = job.get("id")
        claim_url = f"{url}?id=eq.{job_id}"
        patch = {"status": "running", "worker_id": WORKER_ID, "started_at": "now()"}
        p = requests.patch(claim_url, headers=HEADERS, data=json.dumps(patch), timeout=10)
        if p.status_code in (200, 204):
            logger.info("Leased job %s", job_id)
            # Re-fetch to get latest row
            r2 = requests.get(f"{url}?id=eq.{job_id}&select=*", headers=HEADERS, timeout=10)
            r2.raise_for_status()
            refreshed = r2.json()[0]
            return refreshed
        else:
            logger.info("Failed to claim job %s (status %s)", job_id, p.status_code)
            return None
    except Exception as e:
        logger.exception("Error leasing job: %s", e)
        return None


def heavy_compute(seed: int) -> dict:
    """Simulate heavy CPU work. We'll compute a moderately expensive value
    deterministically from the seed (e.g., sum of fibonacci numbers or
    repeated prime testing). Returns a dict with metadata and numeric result.
    """
    # Simple CPU-bound task: compute the sum of first N fibonacci numbers mod big prime
    n = max(30, min(1000, seed % 500 + 30))
    a, b = 0, 1
    total = 0
    for i in range(n):
        a, b = b, a + b
        total += a
        # Introduce some non-trivial work
        if i % 50 == 0:
            _ = math.isqrt(total)
    result = total % 1000000007
    return {"n": n, "result": result}


def write_cached_result(job: dict, result: dict) -> Optional[int]:
    url = f"{SUPABASE_URL}/rest/v1/cached_results"
    payload = {
        "job_id": job.get("id"),
        "result": result,
        "created_at": "now()",
    }
    try:
        r = requests.post(url, headers=HEADERS, data=json.dumps(payload), timeout=10)
        r.raise_for_status()
        # Supabase returns the created row(s)
        created = r.json()
        if created and isinstance(created, list):
            return created[0].get("id")
        return None
    except Exception:
        logger.exception("Failed to write cached_result")
        return None


def update_job_completion(job_id: int, status: str, result_id: Optional[int] = None, error: Optional[str] = None):
    url = f"{SUPABASE_URL}/rest/v1/jobs?id=eq.{job_id}"
    payload = {"status": status}
    if result_id is not None:
        payload["cached_result_id"] = result_id
    if error:
        payload["error"] = error
    payload["completed_at"] = "now()"
    try:
        r = requests.patch(url, headers=HEADERS, data=json.dumps(payload), timeout=10)
        r.raise_for_status()
        logger.info("Updated job %s to %s", job_id, status)
    except Exception:
        logger.exception("Failed updating job status for %s", job_id)


def main_loop():
    logger.info("Starting worker %s, polling %ss", WORKER_ID, POLL_INTERVAL)
    while True:
        job = lease_job()
        if not job:
            time.sleep(POLL_INTERVAL)
            continue

        job_id = job.get("id")
        try:
            seed = job.get("seed", int(time.time())) if job else int(time.time())
            logger.info("Processing job %s (seed=%s)", job_id, seed)
            result = heavy_compute(int(seed))
            result_id = write_cached_result(job, result)
            update_job_completion(job_id, "done", result_id=result_id)
        except Exception as e:
            logger.exception("Error processing job %s: %s", job_id, e)
            update_job_completion(job_id, "errored", error=str(e))


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logger.info("Worker interrupted, exiting")
