import { serve } from 'std/server'

serve(async (req) => {
  try {
    if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 })
    const body = await req.json()
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
    if (!serviceKey) return new Response(JSON.stringify({ error: 'Service key not configured' }), { status: 500 })

    // Basic payload validation
    const { user_id, input } = body
    if (!input) return new Response(JSON.stringify({ error: 'missing input' }), { status: 400 })

    // Insert a new job into Supabase Postgres via REST
    const insertResp = await fetch(`${Deno.env.get('SUPABASE_URL')}/rest/v1/jobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': serviceKey,
        'Authorization': `Bearer ${serviceKey}`
      },
      body: JSON.stringify([{ user_id: user_id || null, payload: input }])
    })

    const text = await insertResp.text()
    if (!insertResp.ok) {
      return new Response(text, { status: insertResp.status, headers: { 'Content-Type': 'application/json' } })
    }

    // Return inserted job (array) to caller
    return new Response(text, { status: 201, headers: { 'Content-Type': 'application/json' } })
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers: { 'Content-Type': 'application/json' } })
  }
})
