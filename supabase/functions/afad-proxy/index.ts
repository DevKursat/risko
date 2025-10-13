import { serve } from 'std/server'

serve(async (req) => {
  try {
    const url = 'https://deprem.afad.gov.tr/apiv2/event/filter'
    // Expect JSON body with filters from client (or use defaults)
    const body = await req.json().catch(() => ({
      limit: 100
    }))

    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    const text = await resp.text()
    return new Response(text, { status: resp.status, headers: { 'Content-Type': 'application/json' } })
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 502, headers: { 'Content-Type': 'application/json' } })
  }
})
