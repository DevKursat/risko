SECURITY NOTICE
===============

This repository previously contained Supabase keys and possibly other secrets in
`config.js` and `.env`. Those values have been removed from tracked files and
replaced with placeholders. Follow the steps below to finalize secret hygiene.

1) Rotate keys immediately
   - In the Supabase dashboard, revoke the old service role key and generate a
     new one. Also rotate the anon key if you believe it was exposed.

2) Move secrets to a secure store
   - For GitHub Actions: add the following as repository secrets (Settings →
     Secrets and variables → Actions):
       - SUPABASE_URL
       - SUPABASE_ANON_KEY
       - SUPABASE_SERVICE_ROLE_KEY
       - SUPABASE_PROJECT_REF
   - For Cloud Run / GCP: add secrets to Secret Manager and reference them in
     your Cloud Run service configuration.

3) Remove secrets from Git history (optional but recommended)
   - Use the `bfg-repo-cleaner` or `git filter-repo` to remove secrets from
     history. Example with bfg:

     ```bash
     # Install BFG and run (example)
     bfg --delete-files .env
     git reflog expire --expire=now --all && git gc --prune=now --aggressive
     git push --force
     ```

   - Note: Rewriting git history is disruptive for collaborators. Coordinate
     before doing a force-push.

4) Verify CI and deploy workflows
   - Make sure `.github/workflows/*` use the secret names you added. The
     `deploy_github_pages.yml` will inject `config.js` at deploy time using the
     `SUPABASE_URL` and `SUPABASE_ANON_KEY` secrets.

5) Do not paste or share service-role keys in chat or code comments.

If you want, I can prepare a `git filter-repo` recipe to scrub history and a
GitHub Actions workflow for Cloud Run deploy that references the secrets you
added. Say the word and I'll add those files.
