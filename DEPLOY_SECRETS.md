Required secrets and their purpose
=================================

Add these repository secrets (Settings → Secrets and variables → Actions) before running deploy workflows.

- SUPABASE_URL: https://<project>.supabase.co
- SUPABASE_ANON_KEY: public anon key for client
- SUPABASE_SERVICE_ROLE_KEY: service role key (server-side only)
- SUPABASE_PROJECT_REF: project ref shown in Supabase dashboard
- API_BASE_URL: optional; the backend API base URL to inject into config.js

- GHCR_USERNAME: GitHub username or org name (do NOT include leading '@')
- GHCR_TOKEN: Personal access token with write:packages scope

- GCP_PROJECT_ID: Google Cloud project id
- GCP_REGION: region for Cloud Run (e.g. us-central1)
- GCP_SA_KEY: base64-encoded JSON service account key with Cloud Run deploy permissions
- CLOUD_RUN_SERVICE_NAME: desired Cloud Run service name (e.g. risko-worker)

Notes:
- If you stored GHCR_USERNAME as "@DevKursat", update it to "DevKursat" (without the @). The workflows expect the raw username/org string.
- For `GCP_SA_KEY` you can either store the JSON text directly as a secret or base64-encode it and decode it in the workflow.
