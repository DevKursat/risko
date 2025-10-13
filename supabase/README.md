# Supabase Edge Functions proxy examples

This folder contains example Supabase Edge Functions you can deploy to Supabase to act as server-side proxies for external APIs (AFAD, weather).

Why use Supabase Edge Functions?
- Server-side proxy avoids CORS and mixed-content errors when frontend is hosted on GitHub Pages.
- Serverless, low-latency, and managed by Supabase (no separate server required).

Files:
- `functions/afad-proxy/index.ts` - a simple POST proxy to AFAD event filter
- `functions/weather-proxy/index.ts` - a GET proxy to OpenWeather (uses `OPENWEATHER_API_KEY` secret)

Deploy:
1. Install supabase CLI and login: `npm i -g supabase` then `supabase login`
2. Initialize functions folder in your Supabase project and deploy the functions:

```bash
cd supabase
supabase functions deploy afad-proxy --project-ref <PROJECT_REF>
supabase functions deploy weather-proxy --project-ref <PROJECT_REF>
```

3. Set environment secrets in Supabase (Project Settings > Environment Variables) e.g. `OPENWEATHER_API_KEY`.
4. Use the function URL in frontend by setting `API_BASE_URL` to your Supabase project's functions domain, for example: `https://<project>.functions.supabase.co`.

Security notes:
- Do not store service role keys in client code.
- Protect functions with rate limiting or API key verification if needed.
