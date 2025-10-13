import { serve } from 'std/server'

serve(async (req) => {
  try {
    const urlBase = 'https://api.openweathermap.org/data/2.5/weather'
    const url = new URL(req.url)
    const lat = url.searchParams.get('lat')
    const lon = url.searchParams.get('lon')
    const key = Deno.env.get('OPENWEATHER_API_KEY')
    if (!lat || !lon || !key) return new Response(JSON.stringify({ error: 'missing param or key' }), { status: 400 })

    const resp = await fetch(`${urlBase}?lat=${lat}&lon=${lon}&appid=${key}&units=metric&lang=tr`)
    const text = await resp.text()
    return new Response(text, { status: resp.status, headers: { 'Content-Type': 'application/json' } })
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 502, headers: { 'Content-Type': 'application/json' } })
  }
})
