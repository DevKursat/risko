# Deployment and Real Data Proxy Setup

This document explains how to deploy the backend so the frontend (GitHub Pages) can fetch real-time external APIs via server-side proxy endpoints to avoid CORS and mixed-content issues.

1. Environment variables

- Create a `.env` (do NOT commit) with the following values:

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
FRONTEND_BASE_URL=https://devkursat.github.io
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=["https://devkursat.github.io"]

# External APIs
AFAD_API_URL=https://deprem.afad.gov.tr/apiv2
KANDILLI_API_URL=https://api.orhanaydogdu.com.tr/deprem/kandilli/live
KANDILLI_HTTPS_URL=https://api.orhanaydogdu.com.tr/deprem/kandilli/live
OPENWEATHER_API_KEY=your_openweather_key
WEATHERBIT_API_KEY=your_weatherbit_key

# Supabase (if used)
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

2. Deploying

- You can deploy the backend to services like Render, Fly, Heroku, or Cloud Run.
- Ensure the `FRONTEND_BASE_URL` and `CORS_ORIGINS` include your GitHub Pages origin so browser requests to the backend are allowed.
- After deploying, set the `API_BASE_URL` in the frontend runtime config (via GitHub Actions secret `API_BASE_URL`) to the backend's public URL (e.g., `https://api.example.com`).

3. Verify

- Visit `https://<frontend>/app.html` and open developer console.
- The app should call backend proxy endpoints (e.g. `/api/v1/proxy/afad/events`) and receive JSON without CORS errors.

4. Security notes

- Keep service role keys out of GitHub repository and use repository secrets or deployment environment variables.
- Rate-limit and cache proxy responses to avoid excessive external API usage.

