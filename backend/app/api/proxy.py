from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings
import httpx
from typing import Optional

router = APIRouter()


@router.get("/proxy/afad/events")
async def afad_events(limit: int = Query(50, ge=1, le=500)):
    """Server-side proxy to AFAD event filter to avoid CORS blocking from the browser."""
    base = settings.AFAD_API_URL
    if not base:
        raise HTTPException(status_code=503, detail="AFAD endpoint not configured")
    url = f"{base}/event/filter"
    payload = {"limit": limit}
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"AFAD request failed: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"AFAD error: {e.response.text}")


@router.get('/proxy/kandilli/recent')
async def kandilli_recent():
    # Kandilli may not have HTTPS by default; use configured HTTPS url if available
    url = settings.KANDILLI_HTTPS_URL or settings.KANDILLI_API_URL
    if not url:
        raise HTTPException(status_code=503, detail='Kandilli endpoint not configured')
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get('/proxy/weather')
async def weather(lat: float, lon: float):
    # Prefer OpenWeather if API key provided, else try Weatherbit
    if settings.OPENWEATHER_API_KEY:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'lat': lat, 'lon': lon, 'appid': settings.OPENWEATHER_API_KEY, 'units': 'metric', 'lang': 'tr'}
    elif settings.WEATHERBIT_API_KEY:
        url = 'https://api.weatherbit.io/v2.0/current'
        params = {'lat': lat, 'lon': lon, 'key': settings.WEATHERBIT_API_KEY, 'lang': 'tr'}
    else:
        raise HTTPException(status_code=503, detail='No weather API key configured')

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f'Weather request failed: {e}')
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f'Weather API error: {e.response.text}')
