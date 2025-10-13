import json
import time
from typing import Optional

import requests
from jose import jwt
from jose.utils import base64url_decode

from app.core.config import settings


_JWKS_CACHE = {
    "keys": None,
    "fetched_at": 0,
}


def _get_jwks_url() -> Optional[str]:
    if settings.SUPABASE_JWKS_URL:
        return settings.SUPABASE_JWKS_URL
    if settings.SUPABASE_URL:
        # Standard JWKS endpoint for GoTrue (Supabase Auth)
        return f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
    return None


def _fetch_jwks():
    now = time.time()
    if _JWKS_CACHE["keys"] and now - _JWKS_CACHE["fetched_at"] < 3600:
        return _JWKS_CACHE["keys"]
    url = _get_jwks_url()
    if not url:
        raise RuntimeError("Supabase JWKS URL not configured")
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    _JWKS_CACHE["keys"] = data
    _JWKS_CACHE["fetched_at"] = now
    return data


def verify_supabase_jwt(token: str) -> dict:
    """Verify Supabase JWT (RS256) via JWKS and return claims.

    Raises Exception if invalid.
    """
    jwks = _fetch_jwks()
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise ValueError("No matching JWKS key")
    claims = jwt.decode(
        token,
        key,
        algorithms=[settings.SUPABASE_JWT_ALG],
        audience=None,  # Supabase does not require audience for client JWT
        options={"verify_aud": False},
    )
    return claims
